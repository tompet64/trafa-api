"""Compare deterministic transports, never assistant behavior or live latency."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
import trafa_client as client

CASES = [('B01', 'ev'), ('B01', 'registrations_total'), ('B02', 'malmo'),
         ('B04', 'licences'), ('B06', 'finland')]

class Response:
    status = 200
    headers = {'Content-Type': 'application/json'}
    def __init__(self, raw): self.body = io.BytesIO(raw)
    def read(self, size=-1): return self.body.read(size)
    def __enter__(self): return self
    def __exit__(self, *_): self.body.close()


def direct(name):
    fixtures = ROOT / 'evaluation/fixtures/live'
    query = json.loads((fixtures / (name + '.json.request.json')).read_text())['query']
    events = []
    def transport(request, **_):
        started = time.perf_counter()
        url = urlsplit(request.full_url)
        params = parse_qs(url.query)
        if url.netloc != 'api.trafa.se' or params != {'query': [query], 'lang': ['sv']}:
            raise AssertionError('Unrecorded request')
        endpoint = url.path.rsplit('/', 1)[-1]
        if endpoint not in {'structure', 'data'}: raise AssertionError('Unknown endpoint')
        raw = (fixtures / (name + ('.structure' if endpoint == 'structure' else '') + '.json')).read_bytes()
        events.append(dict(kind='http', endpoint=endpoint, query=query, lang='sv',
                           start_ms=started*1000, duration_ms=(time.perf_counter()-started)*1000,
                           outcome='success', bytes=len(raw)))
        return Response(raw)
    started = time.perf_counter()
    with tempfile.TemporaryDirectory() as temp, patch.object(client, 'urlopen', side_effect=transport):
        result = client.extract(query, Path(temp)/'data.json', sample_rows=100)
    return dict(status='success', elapsed_ms=(time.perf_counter()-started)*1000,
                events=events, result=result)


def run(worker=None, preflight=False):
    rows = []
    for case, name in CASES:
        skill = direct(name)
        record = dict(case_id=case, fixture=name, skill=skill)
        if worker:
            proc = subprocess.run(['node', str(Path(__file__).with_name('replay_mcp.mjs')),
                                   str(worker), str(ROOT/'evaluation/fixtures/live'), name] + (['--preflight'] if preflight else []),
                                  text=True, capture_output=True, check=True, timeout=30)
            mcp = json.loads(proc.stdout)
            record['mcp'] = mcp
            # Compare all raw headers/cells, not just a row count or assistant prose.
            expected = json.loads((ROOT/'evaluation/fixtures/live'/(name+'.json')).read_text(encoding='utf-8-sig'))
            record['raw_data_equal'] = None if mcp['status'] == 'unsupported' else (mcp['status'] == 'success' and
                all(mcp['result'].get(key) == expected[key] for key in ('Header', 'Rows')))
        rows.append(record)
    return dict(mode='fixture_replay', skill_commit_note='Record Git SHA with the output',
                worker_sha256=hashlib.sha256(worker.read_bytes()).hexdigest() if worker else None,
                limitation='No model routing, ChatGPT search, live network latency or statistical prose grading.',
                runs=rows)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', type=Path, help='Exact Worker index.js; requires Node 20+')
    parser.add_argument('--preflight', action='store_true', help='Diagnostic: deliberately request the identical structure before get_statistics')
    args = parser.parse_args()
    result = run(args.worker.resolve() if args.worker else None, args.preflight)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.worker and any(r['mcp']['status'] == 'error' or r['raw_data_equal'] is False for r in result['runs']):
        raise SystemExit(1)
