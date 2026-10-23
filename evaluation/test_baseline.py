"""Offline contract/selection tests. These do not grade assistant prose.

Set TRAFA_SKILL_ROOT to test an unchanged checkout. Transport replay maps exact
requests to recorded bytes; it is a fixture lookup, not a mandated workflow.
"""
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

EVALUATION = Path(__file__).resolve().parent
SKILL = Path(os.environ.get('TRAFA_SKILL_ROOT', EVALUATION.parent))
sys.path.insert(0, str(SKILL / 'scripts'))
import trafa_client as client
from api_contract import APIContract
from reference_metadata import validate_reference_selection

LIVE = EVALUATION / 'fixtures/live'
SYNTHETIC = EVALUATION / 'fixtures/synthetic'

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

class Response:
    def __init__(self, body):
        self.stream = io.BytesIO(body)
        self.status = 200
        self.headers = {'Content-Type':'application/json; charset=utf-8'}
    def read(self, size=-1): return self.stream.read(size)
    def __enter__(self): return self
    def __exit__(self, *_): self.stream.close()

class BaselineRegressionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name)/'result.json'
        for target in ['socket.create_connection','socket.getaddrinfo']:
            p = patch(target, side_effect=AssertionError('Network forbidden in ordinary tests'))
            p.start(); self.addCleanup(p.stop)

    def replay(self, name, data_override=None):
        log = read(LIVE/(name+'.structure.json.request.json'))
        query = log['query']
        calls=[]
        def respond(request, **kwargs):
            url=urlsplit(request.full_url)
            self.assertEqual(url.netloc, 'api.trafa.se')
            self.assertEqual(parse_qs(url.query)['query'], [query])
            self.assertEqual(parse_qs(url.query)['lang'], ['sv'])
            endpoint=url.path.rsplit('/',1)[-1]; calls.append(endpoint)
            path = LIVE/(name+('.structure.json' if endpoint=='structure' else '.json'))
            if endpoint=='data' and data_override: path=data_override
            return Response(path.read_bytes())
        with patch.object(client, 'urlopen', side_effect=respond):
            result=client.extract(query,self.output,sample_rows=10)
        return result,calls

    def test_live_small_selections_are_parsed_without_losing_values_or_codes(self):
        expected={'ev':('nyreg',['14096']), 'registrations_total':('nyreg',['29850']),
                  'malmo':('itrfslut',['120967','125388']),
                  'ore_loaded':('godsm',['123754']),
                  'licences':('andelbefolk',['78,4','24']), 'finland':('pax',['3021'])}
        for name,(measure,values) in expected.items():
            with self.subTest(name=name):
                result,calls=self.replay(name)
                self.assertEqual(calls,['structure','data'])
                self.assertEqual([r['measures'][measure] for r in result['row_sample']], values)
                self.assertTrue(result['sample_complete'])
                self.assertEqual(result['selection']['query'],read(LIVE/(name+'.json.request.json'))['query'])
        # This exercises transport/parser behavior only, not statistical interpretation.

    def test_observed_empty_selection_does_not_make_data_request(self):
        for name in ['finland_empty','ore_broad']:
            with self.subTest(name=name):
                result,calls=self.replay(name)
                self.assertEqual(calls,['structure'])
                self.assertFalse(result['data_requested'])
                self.assertTrue(result['empty_selection'])
                self.assertEqual(result['selection']['DataCount'],0)
                self.assertIn('do not infer product-wide absence',result['warning'])

    def test_empty_data_after_positive_structure_is_not_a_zero_observation(self):
        result,calls=self.replay('ev',SYNTHETIC/'empty-data.json')
        self.assertEqual(calls,['structure','data'])
        self.assertTrue(result['empty_result'])
        self.assertEqual(result['row_count'],0)
        self.assertEqual(result['row_sample'],[])
        self.assertEqual(result['selection']['DataCount'],1)
        self.assertIn('do not establish',result['warning'])

    def test_http200_with_errors_is_rejected_and_logged(self):
        body=(SYNTHETIC/'http200-errors.json').read_bytes()
        with patch.object(client,'urlopen',return_value=Response(body)):
            with self.assertRaises(client.APIResponseError):
                client.fetch('data','t10036|nyreg|ar:2026|drivm:103|manad:09',self.output)
        record=read(str(self.output)+'.request.json')
        self.assertEqual(record['http_status'],200)
        self.assertEqual(record['outcome'],'api_error')

    def test_unknown_filter_value_stops_before_data_request(self):
        query='t10036|nyreg|ar:2026|drivm:NOT_A_CODE|manad:09'
        with patch.object(client,'urlopen') as http:
            with self.assertRaises(ValueError):
                client.extract(query,self.output,metadata_source='references')
            http.assert_not_called()
        with self.assertRaises(ValueError):
            client.validate_selection(read(LIVE/'ev.structure.json'),query)

    def test_unsorted_year_domain_uses_numeric_extrema_and_keeps_special_filter(self):
        values=read(SYNTHETIC/'years.json');before=copy.deepcopy(values)
        self.assertEqual(client.year_bounds(values),{'earliest_year_code':'2019','latest_year_code':'2026'})
        self.assertEqual([v['code'] for v in client.chronological_year_values(values)],['2019','2021','2023','2026','senaste'])
        self.assertEqual(values,before)
        self.assertEqual(client.year_bounds([values[2]]),{'earliest_year_code':None,'latest_year_code':None})

    def test_reversed_observation_rows_preserve_year_identity(self):
        payload=read(LIVE/'malmo.json');payload['Rows'].reverse()
        rows=client.data_summary(payload,10)['row_sample']
        mapped={r['dimensions']['ar']['code']:r['measures']['itrfslut'] for r in rows}
        self.assertEqual(mapped,{'2019':'120967','2023':'125388'})
        # Sorting presentation is an assistant responsibility, tested in T04.

    def test_missing_combination_support_fails_closed_before_data_request(self):
        refs=Path(self.temp.name)/'metadata'
        shutil.copytree(SKILL/'references/metadata',refs)
        path=refs/'kombinationer.json';combinations=read(path)
        del combinations['T10036']
        path.write_text(json.dumps(combinations),encoding='utf-8')
        with patch.object(client,'urlopen') as http:
            with self.assertRaises(ValueError):
                client.extract('t10036|nyreg|ar:2026|drivm:103|manad:09',self.output,
                               metadata_source='references',metadata_root=refs)
            http.assert_not_called()

    def test_recorded_sources_hashes_and_request_identity(self):
        for record in read(EVALUATION/'sources.json')['captured']:
            with self.subTest(file=record['file']):
                body=(LIVE/record['file']).read_bytes()
                self.assertEqual(hashlib.sha256(body).hexdigest(),record['sha256'])
                self.assertTrue(record['checked_at_utc'])
                self.assertTrue(record['query'].startswith('t'))
                self.assertEqual(record['http_status'],200)
                self.assertEqual(record['outcome'],'success')
                APIContract().validate_response(record['endpoint'],json.loads(body.decode('utf-8-sig')))

if __name__=='__main__': unittest.main(verbosity=2)
