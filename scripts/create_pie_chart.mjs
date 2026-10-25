#!/usr/bin/env node
import {readFile,writeFile} from 'node:fs/promises';
import {renderPie} from './charts/pie.mjs';
const [input,output]=process.argv.slice(2);
if(!input||!output||!output.endsWith('.png')){console.error('Användning: node scripts/create_pie_chart.mjs validerad-tabell.json diagram.png');process.exit(2);}
try{
 const result=await renderPie(JSON.parse(await readFile(input,'utf8')));
 await writeFile(output,result.png);
 await writeFile(output+'.table.json',JSON.stringify(result.table,null,2)+'\n');
 await writeFile(output+'.table.md',result.markdown);
 console.log(JSON.stringify({png:output,bytes:result.png.length,total:result.table.total}));
}catch(e){console.error(e.message);process.exitCode=1;}
