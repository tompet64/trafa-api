/** Offline PNG generator. No network, dependencies or statistics retrieval. */
import glyphs from './font.mjs';
const W=1200,H=950;
const colors=['#176b87','#e69f00','#009e73','#cc79a7','#0072b2','#d55e00','#756bb1','#6b705c','#a55194','#4d9221','#8c510a','#666666'];
const bad=m=>{throw new Error(m);};
const text=(x,n,max=200)=>typeof x==='string'&&x.trim()&&x.length<=max&&!/[\x00-\x1f]/.test(x)?x:bad(`Ogiltig ${n}`);
export function preparePie(input){
 if(!input||typeof input!=='object'||Array.isArray(input))bad('Tabell krävs');
 const allowed=new Set(['title','period','unit','source','query','retrieved_at','rows','complete','disjoint','additive','value_kind','legend_source']);
 if(Object.keys(input).some(k=>!allowed.has(k)))bad('Okänt tabellfält');
 const {title,period,unit,source,query,retrieved_at,rows}=input;
 for(const [n,v] of Object.entries({title,period,unit,source,query,retrieved_at}))text(v,n,n==='query'?500:({title:120,period:60,unit:40,source:160,retrieved_at:40}[n]));
 const valueKind=input.value_kind??'numeric';if(!['count','numeric'].includes(valueKind))bad('Ogiltig value_kind');
 if(input.legend_source!==undefined)text(input.legend_source,'legend_source',180);
 if(input.complete!==true||input.disjoint!==true||input.additive!==true)bad('Kräver bekräftad fullständighet, disjunkta kategorier och additivt mått');
 if(!Array.isArray(rows)||rows.length<1||rows.length>13)bad('Ange 1–12 kategorier och högst en total');
 const seen=new Set(),labels=new Set();let published=null;
 const categories=[];
 for(const r of rows){
  if(!r||typeof r!=='object')bad('Ogiltig rad');
  if(Object.keys(r).some(k=>!['code','label','value','is_total'].includes(k)))bad('Okänt radfält');
  text(r.code,'kategorikod',80);text(r.label,'etikett',60);
  if(seen.has(r.code)||labels.has(r.label))bad('Duplicerad kategori');seen.add(r.code);labels.add(r.label);
  if(typeof r.is_total!=='boolean')bad('Explicit totalmarkering krävs');
  let value=r.value,sourceSymbol;
  if(value==='-'||value==='–'){
   if(valueKind!=='count'||!input.legend_source)bad('Streck kräver uppräkningsbart antal och dokumenterad teckenförklaring: '+r.label);
   sourceSymbol=value;value=0;
  }
  // Other textual/unknown markers and numeric strings are never coerced.
  if(typeof value!=='number'||!Number.isFinite(value)||value<0||value>1e12)bad('Saknat eller ogiltigt värde: '+r.label);
  if(valueKind==='count'&&!Number.isSafeInteger(value))bad('Uppräkningsbart antal kräver heltal');
  if(r.is_total){if(published!==null)bad('Flera totaler');published=value;}
  else categories.push({...r,value,...(sourceSymbol?{source_symbol:sourceSymbol}:{})});
 }
 if(!categories.length||categories.length>12)bad('Ange 1–12 kategorier');
 const total=categories.reduce((a,r)=>a+r.value,0);
 if(!Number.isFinite(total)||total<=0)bad('Summan måste vara positiv');
 if(published!==null&&Math.abs(published-total)>Math.max(1e-9,Math.abs(total)*1e-12))bad('Kategorisumman avviker från publicerad total');
 return {title,period,unit,source,query,retrieved_at,value_kind:valueKind,legend_source:input.legend_source??null,total,total_basis:published===null?'sum_of_validated_categories':'published_total',rows:categories.map(r=>({...r,share:100*r.value/total}))};
}
const num=x=>new Intl.NumberFormat('sv-SE',{maximumFractionDigits:Number.isInteger(x)?0:1}).format(x).replace(/\u00a0/g,' ');
const shareText=x=>x>0&&x<0.1?'<0,1':num(x);
export function tableMarkdown(table){
 const esc=s=>String(s).replace(/\|/g,'\\|').replace(/[\r\n]/g,' ');
 return `**${esc(table.title)} — ${esc(table.period)}**\n\n| Kategori | ${esc(table.unit)} | Andel |\n|---|---:|---:|\n`+table.rows.map(r=>`| ${esc(r.label)} | ${num(r.value)}${r.source_symbol?' ('+r.source_symbol+')':''} | ${shareText(r.share)} % |`).join('\n')+`\n| Summa | ${num(table.total)} | 100 % |\n\nKälla: ${esc(table.source)}. Query: ${esc(table.query)}. Hämtat: ${esc(table.retrieved_at)}.${table.rows.some(r=>r.source_symbol)?' Streck har tolkats som exakt noll för antal; originaltecknet visas i parentes. Teckenförklaring: '+esc(table.legend_source)+'.':''} Andelar är egna beräkningar; avrundning kan ge annan summa än 100 %.\n`;
}
const rgb=s=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16));
function raster(t){
 const data=new Uint8Array(W*H*3).fill(255);
 const pixel=(x,y,c,a=255)=>{if(x<0||x>=W||y<0||y>=H)return;const k=(y*W+x)*3;for(let j=0;j<3;j++)data[k+j]=Math.round((c[j]*a+data[k+j]*(255-a))/255);};
 const rect=(x,y,w,h,color)=>{const c=rgb(color);for(let yy=y;yy<y+h;yy++)for(let xx=x;xx<x+w;xx++)pixel(xx,yy,c);};
 const draw=(s,x,y,color='#263746')=>{const c=rgb(color);for(const ch of s){const g=glyphs[ch];if(!g)bad('Tecken saknar glyph: '+ch);const [w,h,dy,advance,b]=g;const bytes=Uint8Array.from(atob(b),c=>c.charCodeAt(0));for(let yy=0;yy<h;yy++)for(let xx=0;xx<w;xx++)pixel(x+xx,y+dy+yy,c,bytes[yy*w+xx]);x+=advance;}};
 const wrap=(s,max)=>{const width=max*10,lines=[''];let used=0;
  for(const ch of s){const g=glyphs[ch];if(!g)bad('Tecken saknar glyph: '+ch);if(used+g[3]>width){lines.push('');used=0;}lines[lines.length-1]+=ch;used+=g[3];}
  return lines;
 };
 if(wrap(t.title,110).length>2||wrap(`${t.period} · ${t.unit}`,110).length>1||wrap(`Källa: ${t.source}`,110).length>3||t.rows.some(r=>wrap(r.label,32).length>2))bad('Texten är för lång för diagrammets layout; behåll tabellen eller välj kortare verifierade benämningar');
 wrap(t.title,110).forEach((l,i)=>draw(l,45,25+i*27));
 draw(`${t.period} · ${t.unit}`,45,88,'#516573');
 const cx=295,cy=366,radius=222;let edges=[],sum=0;
 for(const row of t.rows){sum+=row.value/t.total;edges.push(sum*Math.PI*2);}
 for(let y=cy-radius;y<=cy+radius;y++)for(let x=cx-radius;x<=cx+radius;x++){
  const distance=Math.hypot(x-cx,y-cy);if(distance>radius+.5)continue;
  let angle=(Math.atan2(y-cy,x-cx)+Math.PI/2+Math.PI*2)%(Math.PI*2);
  let i=edges.findIndex(e=>angle<e);if(i<0)i=edges.length-1;
  pixel(x,y,rgb(colors[i]),Math.round(Math.min(1,Math.max(0,radius+.5-distance))*255));
 }
 draw('Kategori',565,127);draw('Värde / andel',965,127);
 t.rows.forEach((row,i)=>{const y=168+i*44;rect(565,y+5,16,16,colors[i]);
  // Full labels are preserved. A long label gets a second line and more vertical space.
  const labelLines=wrap(row.label,32);labelLines.forEach((l,j)=>draw(l,595,y+j*20));
  draw(num(row.value)+(row.source_symbol?' ('+row.source_symbol+')':''),965,y);draw(`${shareText(row.share)} %`,965,y+20,'#516573');
 });
 draw(`Summa: ${num(t.total)} ${t.unit}`,45,734);
 draw(t.rows.some(r=>r.source_symbol)?'Streck (-/–) betyder exakt noll för antal. Andelar: egna beräkningar.':'Andelar av kategorisumman; egna beräkningar. Avrundning kan påverka summan.',45,771);
 wrap(`Källa: ${t.source}`,110).forEach((l,i)=>draw(l,45,808+i*25));
 draw(`Hämtat: ${t.retrieved_at}`,45,889,'#516573');
 return data;
}
const crcTable=Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
const crc=bytes=>{let c=0xffffffff;for(const b of bytes)c=crcTable[(c^b)&255]^(c>>>8);return (c^0xffffffff)>>>0;};
const u32=n=>new Uint8Array([n>>>24,n>>>16&255,n>>>8&255,n&255]);
const concat=parts=>{let b=new Uint8Array(parts.reduce((n,p)=>n+p.length,0)),i=0;for(const p of parts){b.set(p,i);i+=p.length;}return b;};
const chunk=(name,bytes)=>{const c=concat([new TextEncoder().encode(name),bytes]);return concat([u32(bytes.length),c,u32(crc(c))]);};
export async function renderPie(input){
 const table=preparePie(input),pixels=raster(table),scan=new Uint8Array(H*(W*3+1));
 for(let y=0;y<H;y++)scan.set(pixels.subarray(y*W*3,(y+1)*W*3),y*(W*3+1)+1);
 const zipped=new Uint8Array(await new Response(new Blob([scan]).stream().pipeThrough(new CompressionStream('deflate'))).arrayBuffer());
 const ihdr=concat([u32(W),u32(H),new Uint8Array([8,2,0,0,0])]);
 return {png:concat([new Uint8Array([137,80,78,71,13,10,26,10]),chunk('IHDR',ihdr),chunk('IDAT',zipped),chunk('IEND',new Uint8Array())]),table,markdown:tableMarkdown(table)};
}
export const pngBase64=bytes=>{let s='';for(let i=0;i<bytes.length;i+=8192)s+=String.fromCharCode(...bytes.subarray(i,i+8192));return btoa(s);};
