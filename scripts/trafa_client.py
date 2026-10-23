"""Small JSON client: save full responses, show only relevant metadata.

The OpenAPI contract controls HTTP requests and response validation.
No trafapy dependency. Query semantics remain product-specific.
"""
import argparse
import codecs
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from api_contract import APIContract
from reference_metadata import validate_reference_selection
from structure_routing import StructureSizeLimit, plan_metadata


class APIResponseError(ValueError):
    """The server returned a JSON response with an explicit API error."""


def require_no_api_errors(payload):
    if payload.get('Errors'):
        raise APIResponseError('API Errors: ' + repr(payload['Errors']))


def _reject_json_constant(value):
    raise ValueError('Non-finite value is not valid JSON: ' + value)


def is_year_dimension(name, label=''):
    return str(name).casefold() in {'ar', 'ar_t'} or str(label).casefold() in {'år', 'ar'}


def chronological_year_values(values, code_key='code'):
    """Sort concrete year codes without modifying source records or special filters."""
    years, special = [], []
    for value in values:
        code = value.get(code_key)
        if isinstance(code, str) and len(code) == 4 and code.isascii() and code.isdigit():
            years.append(value)
        else:
            special.append(value)
    return sorted(years, key=lambda x: int(x[code_key])) + special


def year_bounds(values, code_key='code'):
    years = [x[code_key] for x in chronological_year_values(values, code_key)
             if isinstance(x.get(code_key), str) and len(x[code_key]) == 4
             and x[code_key].isascii() and x[code_key].isdigit()]
    return {'earliest_year_code': years[0] if years else None,
            'latest_year_code': years[-1] if years else None}


def walk(items):
    for x in items:
        if not isinstance(x, dict): raise ValueError('StructureItem must be an object')
        yield x
        yield from walk(x.get('StructureItems') or [])


def save(path, value):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def _contract_record(contract):
    return {'version': contract.version, 'sha256': contract.sha256,
            'file': str(contract.path)}


def _read_body(response, max_chars=None):
    if max_chars is None:
        return response.read()
    decoder = codecs.getincrementaldecoder('utf-8-sig')()
    chunks, characters = [], 0
    while True:
        chunk = response.read(16384)
        if not chunk:
            characters += len(decoder.decode(b'', final=True))
            break
        chunks.append(chunk)
        characters += len(decoder.decode(chunk))
        if characters > max_chars:
            raise StructureSizeLimit(max_chars, characters)
    if characters > max_chars:
        raise StructureSizeLimit(max_chars, characters, complete=True)
    return b''.join(chunks)


def fetch(endpoint, query, path, lang='sv', *, max_chars=None, contract=None):
    """Save full JSON and provenance; a configured structure budget is optional."""
    contract = contract or APIContract()
    request = contract.request(endpoint, query, lang)
    if max_chars is not None and (endpoint != 'structure' or type(max_chars) is not int or max_chars < 1):
        raise ValueError('A positive response budget is supported for structure requests only')
    started = time.perf_counter()
    url = request['url']
    path = Path(path)
    record = {'endpoint': endpoint, 'query': query, 'lang': lang, 'url': url,
              'contract': _contract_record(contract), 'response_limit_characters': max_chars}
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=request['headers'], method=request['method']), timeout=35) as r:
                record.update(http_status=r.status, content_type=r.headers.get('Content-Type'))
                mime = (record['content_type'] or '').split(';', 1)[0].strip().lower()
                if max_chars is not None and mime != 'application/json':
                    raise ValueError('Expected declared application/json before bounded structure reading; got ' + repr(mime))
                raw = _read_body(r, max_chars)
            break
        except HTTPError as exc:
            record.update(http_status=exc.code, content_type=exc.headers.get('Content-Type') if exc.headers else None)
            if exc.code not in {429,502,503,504} or attempt==2:
                record.update(outcome='http_error', error=str(exc), attempts=attempt+1,
                              checked_at_utc=datetime.now(timezone.utc).isoformat())
                save(str(path)+'.request.json', record)
                raise
            wait = exc.headers.get('Retry-After') if exc.headers else None
            if wait and wait.isdigit() and int(wait)>30:
                record.update(outcome='http_error', error=str(exc), attempts=attempt+1,
                              checked_at_utc=datetime.now(timezone.utc).isoformat())
                save(str(path)+'.request.json', record)
                raise
            time.sleep(int(wait) if wait and wait.isdigit() else 2**attempt)
        except StructureSizeLimit as exc:
            record.update(outcome='structure_size_limit', attempts=attempt+1,
                          checked_at_utc=datetime.now(timezone.utc).isoformat(),
                          response_characters_lower_bound=exc.characters, complete=False)
            save(str(path)+'.request.json', record)
            measurement = {'endpoint': endpoint, 'query': query, 'lang': lang,
                           'scope': 'exact_query', 'requested_format': 'json',
                           'checked_at_utc': record['checked_at_utc'], 'complete': False,
                           'failure': 'structure_size_limit',
                           'response_characters_lower_bound': exc.characters,
                           'declared_content_type': record['content_type'],
                           'request_log': str(path)+'.request.json'}
            inventory_path = str(path)+'.size.json'
            save(inventory_path, {'schema_version': 1, 'measurements': [measurement]})
            exc.evidence = {'measurement': measurement, 'inventory_path': inventory_path,
                            'response_body_saved': False}
            raise
        except Exception as exc:
            record.update(outcome='transport_or_format_error', error=str(exc), attempts=attempt+1,
                          checked_at_utc=datetime.now(timezone.utc).isoformat())
            save(str(path)+'.request.json', record)
            raise
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    record.update(checked_at_utc=datetime.now(timezone.utc).isoformat(),
                  response_utf8_bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                  elapsed_seconds=round(time.perf_counter()-started,3), attempts=attempt+1)
    try:
        text = raw.decode('utf-8-sig')
        record['response_characters'] = len(text)
        payload = json.loads(text, parse_constant=_reject_json_constant)
        contract.validate_response(endpoint, payload)
    except (ValueError, UnicodeError) as exc:
        record.update(outcome='invalid_response', error=str(exc))
        save(str(path)+'.request.json', record)
        raise
    record['schema_validated'] = True
    try:
        require_no_api_errors(payload)
    except APIResponseError as exc:
        record.update(outcome='api_error', error=str(exc))
        save(str(path)+'.request.json', record)
        raise
    record.update(outcome='success')
    save(str(path)+'.request.json', record)
    return payload


def validate_selection(payload, query):
    require_no_api_errors(payload)
    parts = query.split('|')
    if not parts[0] or any(not x for x in parts): raise ValueError('Empty query segment')
    flat = list(walk(payload.get('StructureItems') or []))
    products = [x for x in flat if x.get('Type')=='P' and x.get('Selected') is True]
    if len(products)!=1 or products[0].get('Name')!=parts[0]:
        raise ValueError('Exact query product is not selected in structure')
    measures, seen = [], set()
    for token in parts[1:]:
        name, sep, codes = token.partition(':')
        if not name or name in seen: raise ValueError('Empty or repeated entity: '+name)
        seen.add(name)
        nodes = [x for x in flat if x.get('Name')==name and x.get('Type') in {'D','H','M'}]
        if len(nodes)!=1: raise ValueError('Missing or ambiguous entity: '+name)
        node = nodes[0]
        if node.get('Selected') is not True: raise ValueError('Entity not selected: '+name)
        if node.get('Option') is not True: raise ValueError('Entity availability is not confirmed: '+name)
        parent, ancestors = node.get('ParentName'), set()
        while parent != parts[0]:
            if not parent or parent in ancestors:
                raise ValueError('Entity has no unambiguous parent path to the selected product: '+name)
            ancestors.add(parent)
            parents = [x for x in flat if x.get('Name')==parent and x.get('Type') in {'D','H'}]
            if len(parents)!=1: raise ValueError('Missing or ambiguous parent: '+str(parent))
            parent = parents[0].get('ParentName')
        if node.get('Type')=='M':
            measures.append(name)
            if sep: raise ValueError('A measure cannot have dimension filters')
        if sep:
            selected_codes = codes.split(',')
            if not all(selected_codes) or len(set(selected_codes)) != len(selected_codes):
                raise ValueError('Empty or repeated filter value: '+token)
            for code in selected_codes:
                values = [x for x in flat if x.get('Name')==code and x.get('ParentName')==name
                          and x.get('Type') in {'DV','F'}]
                if len(values)!=1 or values[0].get('Selected') is not True:
                    raise ValueError('Value not selected under dimension: '+token)
                if values[0].get('Option') is not True:
                    raise ValueError('Value availability is not confirmed: '+token)
    if not measures: raise ValueError('No selected measure in query')
    unavailable = [x['Name'] for x in flat if x.get('Type') in {'D','H','M'}
                   and x.get('Selected') is True and x.get('Option') is False]
    if unavailable: raise ValueError('Selected entities not available: '+repr(unavailable))
    return {'product':products[0]['Name'],'measures':measures,'DataCount':payload.get('DataCount'),
            'validation_source':'structure'}


def structure_summary(payload, names=None, with_values=False):
    require_no_api_errors(payload)
    flat = list(walk(payload.get('StructureItems') or []))
    selected = [x for x in flat if x.get('Type')=='P' and x.get('Selected') is True]
    keep = ['Name','Label','ParentName','Type','DataType','Selected','Option','Description']
    if not selected:
        return {'DataCount':payload.get('DataCount'),'products':[
            {k:x.get(k) for k in ['Name','Label','UniqueId']} for x in flat if x.get('Type')=='P']}
    if len(selected)!=1: raise ValueError('More than one selected product')
    reached = {selected[0]['Name']}; candidates = [x for x in flat if x.get('Type') in {'D','H','M'}]
    chosen = []
    while candidates:
        layer = [x for x in candidates if x.get('ParentName') in reached]
        if not layer: break
        chosen.extend(layer); reached.update(x['Name'] for x in layer)
        candidates = [x for x in candidates if x not in layer]
    variables = []
    for x in chosen:
        if names and x['Name'] not in names: continue
        v = {k:x.get(k) for k in keep}
        children = x.get('StructureItems') or []
        v['value_count'] = sum(q.get('Type')=='DV' for q in children)
        v['filters'] = [{k:q.get(k) for k in keep} for q in children if q.get('Type')=='F']
        values = [{k:q.get(k) for k in keep} for q in children if q.get('Type')=='DV']
        if x.get('Type') == 'D' and is_year_dimension(x['Name'], x.get('Label')):
            values = chronological_year_values(values, 'Name')
            v.update(year_bounds(values, 'Name'))
        if with_values: v['values'] = values
        variables.append(v)
    return {'DataCount':payload.get('DataCount'),'product':{k:selected[0].get(k) for k in keep},
            'variables':variables,'values_included':with_values,
            'warning':'Snapshot only: validate the full current query before data retrieval.'}


def data_summary(payload, sample_rows=0):
    require_no_api_errors(payload)
    rows = payload.get('Rows')
    result = {'Name':payload.get('Name'),'OriginalName':payload.get('OriginalName'),
            'row_count':len(rows) if isinstance(rows,list) else None,
            'empty_result':not rows,'Header':payload.get('Header'),'Notes':payload.get('Notes'),
            'warning':'Empty rows do not establish that statistics are unavailable.' if not rows else None}
    if sample_rows:
        result['row_sample']=[{
            'dimensions':{c.get('Column'):{'code':c.get('Name'),'label':c.get('Value')}
                          for c in (row.get('Cell') or []) if not c.get('IsMeasure')},
            'measures':{c.get('Column'):c.get('Value') for c in (row.get('Cell') or []) if c.get('IsMeasure')},
            'is_total':row.get('IsTotal'),
            'note_ids':list(dict.fromkeys(n for c in (row.get('Cell') or []) for n in (c.get('NoteIds') or [])))
        } for row in (rows or [])[:sample_rows]]
        result['sample_complete']=len(rows or [])<=sample_rows
    return result


def extract(query, path, lang='sv', sample_rows=0, *, metadata_source='auto',
            structure_max_chars=None, metadata_root=None, structure_inventory=None):
    """Validate one exact selection and retrieve it; never search or switch sources."""
    path = Path(path)
    structure_path = path.with_name(path.stem+'.structure.json')
    contract = APIContract()
    contract.request('data', query, lang)
    plan = plan_metadata(query, mode=metadata_source, max_chars=structure_max_chars,
                         lang=lang, inventory_path=structure_inventory)
    if plan['metadata_source'] == 'structure':
        try:
            structure = fetch('structure', query, structure_path, lang,
                              max_chars=structure_max_chars, contract=contract)
        except StructureSizeLimit as exc:
            if metadata_source != 'auto':
                raise
            plan.update(metadata_source='references', reason='observed_structure_exceeds_budget',
                        size_evidence=exc.evidence)
        else:
            validation = validate_selection(structure, query)
            evidence = json.loads(Path(str(structure_path)+'.request.json').read_text())
            validation.update(query=query, lang=lang, structure_path=str(structure_path),
                              structure_sha256=evidence['sha256'],
                              structure_checked_at_utc=evidence['checked_at_utc'])
    if plan['metadata_source'] == 'references':
        validation = validate_reference_selection(query, metadata_root, lang)
        structure_path = None
    validation.update(contract=_contract_record(contract), metadata_plan=plan)
    validation_path = path.with_name(path.stem+'.validation.json')
    save(validation_path, validation)
    if validation.get('DataCount') == 0:
        return {'selection':validation,'data_requested':False,
                'empty_selection':True,'structure_path':str(structure_path) if structure_path else None,
                'validation_path':str(validation_path),
                'warning':'This exact selection has DataCount 0. Check a documented alternative; do not infer product-wide absence.'}
    payload = fetch('data', query, path, lang, contract=contract)
    result = data_summary(payload, sample_rows)
    result.update(selection=validation,data_requested=True,
                  structure_path=str(structure_path) if structure_path else None,
                  validation_path=str(validation_path), raw_path=str(path))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('endpoint', choices=['structure','data','extract','plan'])
    ap.add_argument('--query'); ap.add_argument('--lang', choices=['sv','en'], default='sv')
    ap.add_argument('--raw', type=Path)
    ap.add_argument('--input', type=Path, help='Read saved response instead of HTTP')
    ap.add_argument('--summary', type=Path); ap.add_argument('--names', nargs='*')
    ap.add_argument('--values', action='store_true')
    ap.add_argument('--rows', type=int, default=0, help='Show at most N data rows with exact dimension codes and measure values (0–100)')
    ap.add_argument('--structure', type=Path, help='Saved validated structure for exactly this data query')
    ap.add_argument('--metadata-source', choices=['auto','structure','references'], default='auto',
                    help='Use current structure or explicit dated reference validation; auto falls back only for size limits')
    ap.add_argument('--metadata-root', type=Path, help='Reference metadata directory; defaults to the bundled catalogs')
    ap.add_argument('--structure-max-chars', type=int,
                    help='Optional structure response budget; no Action limit is imposed on direct Python by default')
    ap.add_argument('--structure-inventory', type=Path, help='Saved size inventory; an observed .size.json can be reused')
    a = ap.parse_args()
    if not 0<=a.rows<=100:ap.error('--rows must be between 0 and 100')
    if a.structure_max_chars is not None and a.structure_max_chars < 1:
        ap.error('--structure-max-chars must be positive')
    if a.endpoint != 'plan' and not a.raw: ap.error('--raw is required for response files')
    contract = APIContract()
    if a.endpoint == 'plan':
        if not a.query or a.input or a.structure:
            ap.error('plan needs --query and does not read response files')
        contract.request('data', a.query, a.lang)
        summary = {'contract': _contract_record(contract), 'query': a.query, 'lang': a.lang,
                   'metadata_plan': plan_metadata(a.query, mode=a.metadata_source,
                       max_chars=a.structure_max_chars, lang=a.lang, inventory_path=a.structure_inventory),
                   'network_requested': False}
        if summary['metadata_plan']['metadata_source'] == 'references':
            summary['reference_validation'] = validate_reference_selection(a.query, a.metadata_root, a.lang)
        if a.summary: save(a.summary, summary)
        if a.raw: save(a.raw, summary)
        print(json.dumps(summary,ensure_ascii=False,indent=2));return
    if a.endpoint=='extract':
        if not a.query or a.input or a.structure:ap.error('extract needs --query; no --input or --structure')
        summary=extract(a.query,a.raw,a.lang,a.rows,metadata_source=a.metadata_source,
                        structure_max_chars=a.structure_max_chars,metadata_root=a.metadata_root,
                        structure_inventory=a.structure_inventory)
        if a.summary:save(a.summary,summary)
        print(json.dumps(summary,ensure_ascii=False,indent=2));return
    if a.endpoint=='data':
        if not a.query: ap.error('data needs --query')
        contract.request('data', a.query, a.lang)
        if a.metadata_source == 'references':
            if a.structure: ap.error('Choose reference validation or --structure, not both')
            validation = validate_reference_selection(a.query, a.metadata_root, a.lang)
        else:
            if not a.structure: ap.error('data needs --structure or --metadata-source references; use extract for automatic routing')
        # Offline inspection does not assert freshness. Live data requires traceable matching request.
        if a.metadata_source != 'references' and not a.input:
            evidence = json.loads(Path(str(a.structure)+'.request.json').read_text())
            if evidence.get('endpoint')!='structure' or evidence.get('query')!=a.query or evidence.get('lang')!=a.lang:
                raise ValueError('Structure request does not match data request')
            if hashlib.sha256(a.structure.read_bytes()).hexdigest()!=evidence.get('sha256'):
                raise ValueError('Structure file differs from its request record')
            if evidence.get('outcome') not in {None, 'success'}:
                raise ValueError('Structure request did not complete successfully')
        if a.metadata_source != 'references':
            structure = json.loads(a.structure.read_text())
            contract.validate_response('structure', structure)
            validation = validate_selection(structure, a.query)
            validation.update(query=a.query, lang=a.lang, structure_path=str(a.structure),
                              structure_sha256=hashlib.sha256(a.structure.read_bytes()).hexdigest(),
                              offline_inspection=bool(a.input))
            if not a.input: validation['structure_checked_at_utc'] = evidence.get('checked_at_utc')
        validation.update(contract=_contract_record(contract))
        save(a.raw.with_name(a.raw.stem+'.validation.json'), validation)
    elif a.metadata_source == 'references':
        ap.error('Use metadata_lookup.py --validate-reference for references; structure returns actual API structure only')
    if a.input:
        payload = json.loads(a.input.read_text(), parse_constant=_reject_json_constant)
        contract.validate_response(a.endpoint, payload)
    else:
        if a.endpoint == 'structure' and a.query and a.structure_max_chars is not None:
            plan_metadata(a.query, mode='structure', max_chars=a.structure_max_chars,
                          lang=a.lang, inventory_path=a.structure_inventory)
        payload = fetch(a.endpoint,a.query,a.raw,a.lang,
                        max_chars=a.structure_max_chars if a.endpoint=='structure' else None,contract=contract)
    summary = structure_summary(payload,a.names,a.values) if a.endpoint=='structure' else data_summary(payload,a.rows)
    if a.endpoint == 'data': summary.update(selection=validation,raw_path=str(a.input or a.raw))
    if a.summary: save(a.summary,summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
