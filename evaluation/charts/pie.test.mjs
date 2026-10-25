import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {inflateSync} from 'node:zlib';
import {preparePie,renderPie,tableMarkdown} from '../../scripts/charts/pie.mjs';
const fixture=name=>JSON.parse(fs.readFileSync(new URL(name+'.json',import.meta.url)));
const base=()=>fixture('vehicles-2025');
test('2025 source rows, labels and denominator; published total is excluded',()=>{
 const a=base(),t=preparePie(a);assert.equal(t.total,402098);assert.equal(t.rows.length,8);
 assert.deepEqual(t.rows.map(r=>r.label),a.rows.map(r=>r.label));assert.ok(Math.abs(t.rows.reduce((a,r)=>a+r.share,0)-100)<1e-10);
 a.rows.push({code:'total',label:'Totalt',value:t.total,is_total:true});
 assert.equal(preparePie(a).total,t.total);assert.equal(preparePie(a).rows.length,8);
 a.rows.at(-1).value++;assert.throws(()=>preparePie(a),/avviker/);
});
test('September Gas dash is exactly zero with preserved symbol and authorized count legend',async()=>{
 const a=fixture('fuel-2026-09'),snapshot=structuredClone(a);assert.equal(a.rows.find(r=>r.label==='Gas').value,'-');
 const result=await renderPie(a),t=result.table,gas=t.rows.find(r=>r.label==='Gas');
 assert.equal(gas.value,0);assert.equal(gas.source_symbol,'-');assert.equal(gas.share,0);
 assert.equal(t.total,29850);assert.equal(t.rows.length,8);assert.deepEqual(a,snapshot);
 assert.ok(result.markdown.includes('| Gas | 0 (-) | 0 % |'));
 assert.ok(result.markdown.includes('| Övriga | 4 | <0,1 % |'));
 assert.ok(Math.abs(t.rows.find(r=>r.label==='El').share-100*14096/29850)<1e-12);
});
for(const symbol of ['-','–'])test('dash requires count and cited legend: '+symbol,()=>{
 const a=base();a.rows[0].value=symbol;
 assert.throws(()=>preparePie(a));a.value_kind='count';assert.throws(()=>preparePie(a));
 a.legend_source='Trafikanalys teckenförklaring, Tom 2026-10-25';assert.equal(preparePie(a).rows[0].value,0);
 a.value_kind='numeric';assert.throws(()=>preparePie(a));
});
for(const symbol of ['..','.','...','*','U','p','0,0','—','xxx','k','r','0',''])test('count legend does not turn other markers into zero: '+symbol,()=>{
 const a=fixture('fuel-2026-09');a.rows[0].value=symbol;assert.throws(()=>preparePie(a));
});
test('count requires integers; explicit numeric zero remains zero',()=>{
 const a=fixture('fuel-2026-09');a.rows[0].value=0;assert.equal(preparePie(a).rows[0].value,0);
 a.rows[0].value=0.2;assert.throws(()=>preparePie(a),/heltal/);
});

for(const value of [null,'-',NaN,Infinity,-1,'123',true])test(`reject invalid numeric ${value}`,()=>{
 const a=base();a.rows[0].value=value;assert.throws(()=>preparePie(a));
});
for(const field of ['complete','disjoint','additive'])test(`requires ${field}`,()=>{
 const a=base();a[field]=false;assert.throws(()=>preparePie(a));
});
test('reject duplicate codes/labels, zero total, too many rows, missing metadata',()=>{
 for(const edit of [a=>a.rows.push(a.rows[0]),a=>a.rows[1].label=a.rows[0].label,a=>a.rows.forEach(r=>r.value=0),a=>delete a.period,a=>a.rows[0].is_total=undefined]){
  const a=base();edit(a);assert.throws(()=>preparePie(a));
 }
});
test('one nonzero category and zero category are valid; no invented other category',async()=>{
 const a=base();a.rows=a.rows.slice(0,2);a.rows[1].value=0;const t=preparePie(a);assert.equal(t.rows[0].share,100);assert.equal(t.rows[1].share,0);
 assert.ok((await renderPie(a)).png.length>1000);
});
test('PNG has valid chunks, CRC, decompressed scanlines and independent table',async()=>{
 const r=await renderPie(base());assert.deepEqual([...r.png.slice(0,8)],[137,80,78,71,13,10,26,10]);
 let pos=8,idat=[],width,height;
 while(pos<r.png.length){const v=new DataView(r.png.buffer,r.png.byteOffset+pos);const n=v.getUint32(0);const type=new TextDecoder().decode(r.png.slice(pos+4,pos+8));const bytes=r.png.slice(pos+8,pos+8+n);
  let crc=0xffffffff;for(const byte of r.png.slice(pos+4,pos+8+n)){crc^=byte;for(let k=0;k<8;k++)crc=crc&1?0xedb88320^(crc>>>1):crc>>>1;}
  assert.equal((crc^0xffffffff)>>>0,v.getUint32(8+n));
  if(type==='IHDR'){width=new DataView(bytes.buffer).getUint32(0);height=new DataView(bytes.buffer).getUint32(4);}
  if(type==='IDAT')idat.push(bytes);pos+=12+n;
 }
 assert.equal(pos,r.png.length);assert.equal(width,1200);assert.equal(height,950);
 assert.equal(inflateSync(Buffer.concat(idat)).length,height*(width*3+1));
 assert.ok(r.markdown.includes('402 098'));assert.ok(r.markdown.includes('Terrängskoter'));
});
test('no network even when fetch throws',async()=>{
 const old=globalThis.fetch;globalThis.fetch=()=>assert.fail('network');
 try{await renderPie(base());}finally{globalThis.fetch=old;}
});

test('fixture tables are faithful projections of captured MCP rows',()=>{
 for(const [name,dimension] of [['vehicles-2025','fslag'],['fuel-2026-09','drivm']]){
  const a=fixture(name),raw=fixture(name+'.raw');assert.equal(raw.ok,true);assert.equal(raw.metadata_source,'current_structure');assert.equal(raw.row_count,raw.Rows.length);
  assert.equal(a.query,raw.query);assert.equal(a.retrieved_at,raw.source.retrieved_at);
  assert.deepEqual(a.rows,raw.Rows.map(r=>{
   const c=Object.fromEntries(r.Cell.map(c=>[c.Column,c]));const v=c.nyreg.Value;
   return {code:c[dimension].Name,label:c[dimension].Value,value:/^\d+$/.test(v)?Number(v):v,is_total:r.IsTotal};
  }));
 }
});
test('long labels, all twelve categories, unsupported glyph and unknown fields',async()=>{
 const a=base();a.rows=Array.from({length:12},(_,i)=>({code:String(i),label:'Lång benämning för en kategori '+String(i),value:i+1,is_total:false}));
 assert.ok((await renderPie(a)).png.length>1000);
 const long=base();long.rows[0].label='W'.repeat(60);await assert.rejects(()=>renderPie(long),/layout/);
 a.title='🚗';await assert.rejects(()=>renderPie(a),/glyph/);
 const b=base();b.extra=true;assert.throws(()=>preparePie(b),/Okänt/);
});

test('observed lone comma and historical missing marker are not numeric zero',()=>{
 const raw=fixture('symbols-api-regional');
 const observed=raw.Rows.flatMap(r=>r.Cell).find(c=>c.IsMeasure&&c.Value===',');
 assert.ok(observed);assert.equal(observed.FormattedValue,',');assert.equal(observed.Versions[0].Value,'..');
 const a=fixture('fuel-2026-09');a.rows[0].value=observed.Value;
 assert.throws(()=>preparePie(a));
});
