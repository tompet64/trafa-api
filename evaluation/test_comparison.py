"""Regression coverage for transport budgets and trace evidence, not LLM behavior."""
import copy
import importlib.util
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent

def module(name):
    spec=importlib.util.spec_from_file_location(name,HERE/'comparison'/(name+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

replay=module('run_replay')
report=module('trace_report')

class ComparisonTests(unittest.TestCase):
    def test_representative_routes_use_one_validation_and_one_data_request(self):
        for _,name in replay.CASES:
            with self.subTest(name=name):
                run=replay.direct(name)
                self.assertEqual([e['endpoint'] for e in run['events']],['structure','data'])
                self.assertTrue(run['result']['sample_complete'])

    def test_raw_values_and_calculations_remain_identifiable(self):
        from decimal import Decimal
        def values(name, measure):
            return [r['measures'][measure] for r in replay.direct(name)['result']['row_sample']]
        numerator=Decimal(values('ev','nyreg')[0]); denominator=Decimal(values('registrations_total','nyreg')[0])
        self.assertEqual((100*numerator/denominator).quantize(Decimal('.1')), Decimal('47.2'))
        a,b=map(Decimal,values('malmo','itrfslut'))
        self.assertEqual(b-a,Decimal(4421))
        # A+B is an arithmetic sum; it is not the unknown union of holders.
        self.assertEqual(sum(map(Decimal,(v.replace(',','.') for v in values('licences','andelbefolk')))),Decimal('102.4'))

    def test_metadata_json_files_are_complete_parseable_documents(self):
        # Prevent output-truncation markers from being committed as metadata again.
        for path in (HERE.parent/'references/metadata').glob('*.json'):
            with self.subTest(path=path.name):
                self.assertIsInstance(json.loads(path.read_text(encoding='utf-8-sig')), (dict,list))

    @unittest.skipUnless(shutil.which('node'), 'Node needed to exercise the MCP replay harness')
    def test_worker_console_logs_do_not_corrupt_json_report(self):
        with tempfile.TemporaryDirectory() as directory:
            worker=Path(directory)/'worker.mjs'
            worker.write_text("console.info('synthetic info'); console.error('synthetic error'); "
                "export default { async fetch() { console.log('synthetic call'); "
                "return Response.json({result:{isError:false,structuredContent:{ok:true}}}); } };",
                encoding='utf-8')
            proc=subprocess.run(['node',str(HERE/'comparison/replay_mcp.mjs'),str(worker),
                                 str(HERE/'fixtures/live'),'ev'],check=True,text=True,capture_output=True)
            result=json.loads(proc.stdout)
            self.assertEqual(result['status'],'success')
            self.assertEqual([x['level'] for x in result['server_logs']],['info','error','log'])
            self.assertEqual(proc.stderr,'')

    @unittest.skipUnless(shutil.which('node'), 'Node needed to exercise MCP schema negotiation')
    def test_unfiltered_dimension_is_sent_only_if_worker_schema_supports_it(self):
        for supported in (False,True):
            with self.subTest(supported=supported), tempfile.TemporaryDirectory() as directory:
                worker=Path(directory)/'worker.mjs'
                worker.write_text("export default { async fetch(request) { const q=await request.json(); "
                    "if(q.method==='tools/list') return Response.json({result:{tools:[{name:'get_statistics',inputSchema:{properties:"
                    + ("{dimensions:{type:'array'}}" if supported else "{}") + "}}]}}); "
                    "if(q.params.arguments.dimensions[0]!=='skeppstyp') throw Error('Missing dimension'); "
                    "return Response.json({result:{isError:false,structuredContent:{ok:true}}}); } };",encoding='utf-8')
                proc=subprocess.run(['node',str(HERE/'comparison/replay_mcp.mjs'),str(worker),
                                     str(HERE/'fixtures/live'),'finland'],check=True,text=True,capture_output=True)
                result=json.loads(proc.stdout)
                self.assertEqual(result['status'],'success' if supported else 'unsupported')

    def trace(self):
        return dict(schema_version=1,coverage={'host':'complete','upstream':'complete'},events=[
            dict(id='tool1',kind='tool',start_ms=0,duration_ms=100,outcome='success'),
            dict(id='http1',parent_id='tool1',kind='http',start_ms=10,duration_ms=40,
                 outcome='success',endpoint='structure',query='t|m|ar:2023',lang='sv')])

    def test_nested_spans_not_added_to_total(self):
        result=report.summarize(self.trace())
        self.assertEqual(result['observed_busy_ms'],100)
        self.assertEqual(result['web_actions'],0)
        self.assertEqual(result['statistical_grade'],'unassessed')

    def test_missing_host_or_upstream_coverage_is_unknown(self):
        trace=self.trace();trace['coverage']={}
        result=report.summarize(trace)
        self.assertIsNone(result['web_actions']);self.assertIsNone(result['upstream_http'])

    def test_repeated_success_flagged_but_failed_retry_not_duplicate(self):
        trace=self.trace();second=copy.deepcopy(trace['events'][1]);second['id']='http2'
        trace['events'].append(second)
        self.assertEqual(report.summarize(trace)['repeated_successful_requests'][0]['count'],2)
        second['outcome']='error'
        self.assertEqual(report.summarize(trace)['repeated_successful_requests'],[])

    def test_web_gap_required_and_search_count_includes_opens(self):
        trace=self.trace();trace['events'].append(dict(id='web1',kind='web_open',start_ms=100,duration_ms=5,outcome='success'))
        self.assertEqual(report.summarize(trace)['web_actions'],1)
        self.assertTrue(report.summarize(trace)['warnings'])
        trace['events'][-1]['reason']='Publication date absent from API'
        self.assertFalse(report.summarize(trace)['warnings'])

    def test_invalid_spans_and_parent_cycles_rejected(self):
        for bad in [-1,float('nan'),True]:
            trace=self.trace();trace['events'][0]['duration_ms']=bad
            with self.assertRaises(ValueError):report.summarize(trace)
        trace=self.trace();trace['events'][0]['parent_id']='http1'
        with self.assertRaises(ValueError):report.summarize(trace)

if __name__=='__main__':unittest.main(verbosity=2)
