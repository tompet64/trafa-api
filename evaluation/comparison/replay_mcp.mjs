// Replay a supplied Worker source. No network, deployment or source rewriting.
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const [workerPath, root, name, preflight] = process.argv.slice(2);
const query = JSON.parse(fs.readFileSync(`${root}/${name}.json.request.json`)).query;
const events = [], serverLogs = [];
// Workers emit structured logs. Keep stdout as exactly one JSON report.
const writeReport = console.log.bind(console);
for (const level of ['log','info','warn','error','debug']) {
  console[level] = (...values) => serverLogs.push({level,message:values.map(String).join(' ')});
}
globalThis.fetch = async input => {
  const start = performance.now(), url = new URL(input);
  if (url.origin !== 'https://api.trafa.se' || url.searchParams.get('query') !== query || url.searchParams.get('lang') !== 'sv') throw Error('Unrecorded request');
  const endpoint = url.pathname.split('/').pop();
  if (!['data','structure'].includes(endpoint)) throw Error('Unrecorded endpoint');
  const file = `${root}/${name}${endpoint === 'structure' ? '.structure' : ''}.json`;
  const bytes = fs.readFileSync(file);
  events.push({kind:'http',endpoint,query,lang:'sv',start_ms:start,duration_ms:performance.now()-start,outcome:'success',bytes:bytes.length});
  return new Response(bytes,{headers:{'content-type':'application/json'}});
};
const worker = (await import(pathToFileURL(workerPath))).default;
const structure = JSON.parse(fs.readFileSync(`${root}/${name}.structure.json`));
const flat = [];
function walk(nodes) { for (const node of nodes ?? []) { flat.push(node); walk(node.StructureItems); } }
walk(structure.StructureItems);
const [product,...tokens] = query.split('|'), measures=[], filters={}, dimensions=[];
for (const t of tokens) {
  const [key,values] = t.split(':');
  if (values !== undefined) filters[key] = values.split(',');
  else if (flat.some(n => n.Name === t && ['D','H'].includes(n.Type))) dimensions.push(t);
  else if (flat.some(n => n.Name === t && n.Type === 'M')) measures.push(t);
  else throw Error(`Unknown fixture entity: ${t}`);
}
if (dimensions.length) {
  writeReport(JSON.stringify({status:'unsupported',reason:'Unfiltered reporting dimension cannot be expressed by current MCP input schema',dimensions,events,server_logs:serverLogs}));
  process.exit(0);
}
const started = performance.now();
if (preflight === '--preflight') {
  await worker.fetch(new Request('https://replay.invalid/mcp',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:0,method:'tools/call',params:{name:'get_structure',arguments:{product,measures,filters}}})}));
}
const response = await worker.fetch(new Request('https://replay.invalid/mcp',{method:'POST',body:JSON.stringify({jsonrpc:'2.0',id:1,method:'tools/call',params:{name:'get_statistics',arguments:{product,measures,filters,time_dimension:'ar',max_rows:100}}})}));
const rpc = await response.json(), result = rpc.result;
writeReport(JSON.stringify({status:result?.isError ? 'error':'success',elapsed_ms:performance.now()-started,events,server_logs:serverLogs,result:result?.structuredContent ?? rpc.error}));
