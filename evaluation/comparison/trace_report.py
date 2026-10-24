"""Summarize normalized observations. Missing coverage is unknown, never zero."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

KINDS = {'metadata', 'http', 'tool', 'web_search', 'web_open', 'calculation', 'render'}

def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def summarize(run):
    if run.get('schema_version') != 1: raise ValueError('Unsupported schema_version')
    if run.get('total_ms') is not None and not number(run['total_ms']):
        raise ValueError('Invalid total_ms')
    events = run['events']
    ids = set()
    for event in events:
        if event['id'] in ids: raise ValueError('Duplicate event id')
        ids.add(event['id'])
        if event['kind'] not in KINDS: raise ValueError('Unknown event kind')
        if not number(event['start_ms']) or not number(event['duration_ms']):
            raise ValueError('Invalid timing')
        if event.get('outcome') not in {'success', 'error', 'cancelled', 'unknown'}:
            raise ValueError('Invalid outcome')
        if event['kind'] == 'http' and not all(event.get(k) for k in ('endpoint','query','lang')):
            raise ValueError('HTTP identity incomplete')
    for event in events:
        parent = event.get('parent_id')
        if parent is not None:
            if parent not in ids: raise ValueError('Unknown parent')
            ancestors = {event['id']}
            current = parent
            by_id = {e['id']: e for e in events}
            while current is not None:
                if current in ancestors: raise ValueError('Parent cycle')
                ancestors.add(current)
                current = by_id[current].get('parent_id')
    coverage = run.get('coverage', {})
    if any(v not in {'complete','partial','unavailable'} for v in coverage.values()):
        raise ValueError('Invalid coverage')
    counts = Counter(e['kind'] for e in events)
    # Nested tool and HTTP spans overlap: union avoids double counting.
    end = 0; busy = 0
    for start, stop in sorted((e['start_ms'], e['start_ms']+e['duration_ms']) for e in events):
        busy += max(0, stop-max(start,end)); end = max(end,stop)
    successes = Counter((e['endpoint'], e['query'], e['lang'], e.get('format','json'))
                        for e in events if e['kind']=='http' and e['outcome']=='success')
    duplicates = [dict(endpoint=k[0], query=k[1], lang=k[2], format=k[3], count=n)
                  for k,n in successes.items() if n>1]
    warnings = []
    for e in events:
        if e['kind'] in {'web_search','web_open'} and not e.get('reason'):
            warnings.append('Web action lacks documented information gap: '+e['id'])
    grade = run.get('statistical_grade', 'unassessed')
    if grade not in {'pass','fail','unassessed'}: raise ValueError('Invalid statistical grade')
    return dict(observed_counts=dict(counts), web_actions=(counts['web_search']+counts['web_open'])
                if coverage.get('host')=='complete' else None,
                upstream_http=counts['http'] if coverage.get('upstream')=='complete' else None,
                observed_busy_ms=busy, total_ms=run.get('total_ms'),
                repeated_successful_requests=duplicates, warnings=warnings, statistical_grade=grade,
                note='Repeated requests require review; revisions, retries and distinct scopes can justify them.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('trace',type=Path)
    args=parser.parse_args()
    print(json.dumps(summarize(json.loads(args.trace.read_text())),ensure_ascii=False,indent=2))
