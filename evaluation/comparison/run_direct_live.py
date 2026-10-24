"""Explicit opt-in live direct-client probe. Never invoked by routine CI."""
import argparse
import json
from pathlib import Path
import sys
import tempfile
import time
from datetime import datetime, timezone
from unittest.mock import patch
from urllib.parse import urlsplit, parse_qs
from urllib.request import urlopen

from run_replay import ROOT, CASES, Response, client


def run():
    observations=[]
    for case,name in CASES:
        events=[]
        def transport(request, **kwargs):
            start=time.perf_counter()
            url=urlsplit(request.full_url);params=parse_qs(url.query)
            event=dict(endpoint=url.path.rsplit('/',1)[-1],query=params['query'][0],lang=params['lang'][0])
            try:
                with urlopen(request,**kwargs) as response:
                    raw=response.read();status=response.status;headers=dict(response.headers)
                event.update(outcome='success',bytes=len(raw),http_status=status)
                replay=Response(raw);replay.status=status;replay.headers=headers
                return replay
            except Exception as exc:
                event.update(outcome='error',error_type=type(exc).__name__)
                raise
            finally:
                event['duration_ms']=(time.perf_counter()-start)*1000;events.append(event)
        query=json.loads((ROOT/'evaluation/fixtures/live'/(name+'.json.request.json')).read_text())['query']
        started=time.perf_counter()
        record=dict(case_id=case,fixture=name,query=query,measured_at_utc=datetime.now(timezone.utc).isoformat())
        with tempfile.TemporaryDirectory() as temp, patch.object(client,'urlopen',side_effect=transport):
            try:
                result=client.extract(query,Path(temp)/'data.json',sample_rows=100)
                raw=json.loads((Path(temp)/'data.json').read_text(encoding='utf-8-sig'))
                reference=json.loads((ROOT/'evaluation/fixtures/live'/(name+'.json')).read_text(encoding='utf-8-sig'))
                record.update(status='success',raw_data_equal=all(raw[k]==reference[k] for k in ('Header','Rows')),
                              result=result)
            except Exception as exc:
                record.update(status='error',error_type=type(exc).__name__,error=str(exc))
        record.update(elapsed_ms=(time.perf_counter()-started)*1000,events=events)
        observations.append(record)
    return dict(mode='live_direct_smoke',limitation='Single sequential run. Not randomized, not assistant behavior, not evidence of a route speed advantage.',observations=observations)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--allow-network',action='store_true',required=True)
    p.parse_args()
    print(json.dumps(run(),ensure_ascii=False,indent=2))
