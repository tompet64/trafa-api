"""Exercise metadata routing with synthetic, schema-valid HTTP responses only."""
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

import trafa_client as client
from api_contract import APIContract
from structure_routing import StructureSizeLimit


QUERY = 't10036|nyreg|ar:2026|drivm:103|manad:09'


def _node(name, kind, parent, children=None):
    return {'Name': name, 'Type': kind, 'ParentName': parent,
            'Selected': True, 'Option': True, 'StructureItems': children or []}


def structure_fixture(description=''):
    """A synthetic one-observation selection, not an actual API observation."""
    product = _node('t10036', 'P', None)
    product['Description'] = description
    dimensions = [_node(name, 'D', 't10036', [_node(code, 'DV', name)])
                  for name, code in [('ar', '2026'), ('drivm', '103'), ('manad', '09')]]
    return {'DataCount': 1, 'StructureItems': [product, *dimensions, _node('nyreg', 'M', 't10036')]}


def data_fixture():
    dimensions = [('ar', '2026', '2026'), ('drivm', '103', 'El'), ('manad', '09', 'september')]
    columns = [{'Name': name, 'Type': 'D', 'Filters': [code], 'Value': name}
               for name, code, _ in dimensions]
    columns.append({'Name': 'nyreg', 'Type': 'M', 'Filters': None,
                    'Value': 'Antal nyregistreringar', 'Unit': ''})
    cells = [{'Column': name, 'Name': code, 'Value': label, 'IsMeasure': False,
              'NoteIds': [], 'Versions': []} for name, code, label in dimensions]
    cells.append({'Column': 'nyreg', 'Name': '', 'Value': '123', 'IsMeasure': True,
                  'NoteIds': [], 'Versions': []})
    return {'Name': 'Personbilar', 'OriginalName': 'T10036',
            'Header': {'Column': columns}, 'Rows': [{'Cell': cells, 'IsTotal': False}],
            'Errors': None, 'Notes': {}}


def api_error_fixture(endpoint):
    errors = ['synthetic invalid combination']
    if endpoint == 'structure':
        return {'DataCount': 0, 'StructureItems': [], 'Errors': errors}
    return {'Header': None, 'Rows': None, 'Errors': errors}


def encoded(payload, bom=False):
    body = json.dumps(payload, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return (b'\xef\xbb\xbf' if bom else b'') + body


class FakeResponse:
    """Byte stream that can split UTF-8 sequences across read boundaries."""
    def __init__(self, body, *, content_type='application/json; charset=utf-8', chunk_size=None):
        self.body = body
        self.stream = io.BytesIO(body)
        self.status = 200
        self.headers = {'Content-Type': content_type}
        self.chunk_size = chunk_size
        self.read_sizes = []

    def read(self, size=-1):
        self.read_sizes.append(size)
        if self.chunk_size is not None and size >= 0:
            size = min(size, self.chunk_size)
        return self.stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stream.close()


class ClientRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='trafa-client-routing-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.output = self.root / 'result.json'
        self.contract = APIContract()
        # Confirm that the success fixtures match the actual bundled contract.
        self.contract.validate_response('structure', structure_fixture())
        self.contract.validate_response('data', data_fixture())
        blocker = patch('socket.create_connection', side_effect=AssertionError('Real networking is forbidden in routing tests'))
        blocker.start()
        self.addCleanup(blocker.stop)

    def inventory(self, count=None, query=QUERY, scope='exact_query'):
        measurements = [] if count is None else [{
            'endpoint': 'structure', 'query': query, 'lang': 'sv', 'scope': scope,
            'requested_format': 'json', 'observed_format': 'json', 'complete': True,
            'response_characters': count, 'checked_at_utc': '2026-10-18T12:00:00+00:00',
        }]
        path = self.root / 'inventory.json'
        path.write_text(json.dumps({'schema_version': 1, 'measurements': measurements}), encoding='utf-8')
        return path

    def endpoint(self, request):
        parsed = urlsplit(request.full_url)
        self.assertEqual(parsed.netloc, 'api.trafa.se')
        self.assertEqual(parse_qs(parsed.query)['query'], [QUERY])
        self.assertEqual(parse_qs(parsed.query)['lang'], ['sv'])
        self.assertEqual(request.get_method(), 'GET')
        self.assertEqual(request.get_header('Accept'), 'application/json')
        return parsed.path.rsplit('/', 1)[-1]

    def log(self, path):
        return json.loads(Path(str(path) + '.request.json').read_text(encoding='utf-8'))

    def extract(self, **options):
        return client.extract(QUERY, self.output, sample_rows=1, **options)

    def test_known_oversize_auto_validates_references_before_only_data_request(self):
        events = []
        real_validation = client.validate_reference_selection

        def reference_validation(*args, **kwargs):
            result = real_validation(*args, **kwargs)
            events.append('references_validated')
            return result

        def respond(request, **_):
            self.assertEqual(self.endpoint(request), 'data')
            events.append('data_requested')
            saved = json.loads((self.root / 'result.validation.json').read_text())
            self.assertEqual(saved['validation_source'], 'references')
            self.assertEqual(saved['query'], QUERY)
            return FakeResponse(encoded(data_fixture()))

        with patch.object(client, 'urlopen', side_effect=respond) as http, \
                patch.object(client, 'validate_reference_selection', side_effect=reference_validation) as validate:
            result = self.extract(structure_max_chars=1000, structure_inventory=self.inventory(5000))
        self.assertEqual(http.call_count, 1)
        self.assertEqual(validate.call_count, 1)
        self.assertEqual(events, ['references_validated', 'data_requested'])
        self.assertIsNone(result['structure_path'])
        self.assertIsNone(result['selection']['DataCount'])
        self.assertEqual(result['selection']['metadata_plan']['reason'], 'known_structure_exceeds_budget')
        self.assertEqual(result['row_sample'][0]['measures'], {'nyreg': '123'})
        self.assertFalse((self.root / 'result.structure.json').exists())
        self.assertFalse((self.root / 'result.structure.json.request.json').exists())

    def test_full_product_measurement_is_precaution_not_exact_query_limit(self):
        body = encoded(structure_fixture())
        budget = len(body.decode('utf-8')) + 10
        inventory = self.inventory(budget + 1000, query='t10036', scope='full_product')
        cases = [
            ('auto', 'references', 'full_product_size_precaution', ['data']),
            ('structure', 'structure', 'explicit_bounded_structure_probe', ['structure', 'data']),
        ]
        for mode, source, reason, expected_endpoints in cases:
            with self.subTest(mode=mode):
                self.output = self.root / (mode + '.json')
                endpoints = []

                def respond(request, **_):
                    endpoint = self.endpoint(request)
                    endpoints.append(endpoint)
                    return FakeResponse(body if endpoint == 'structure' else encoded(data_fixture()))

                with patch.object(client, 'urlopen', side_effect=respond), \
                        patch.object(client, 'validate_reference_selection', wraps=client.validate_reference_selection) as validate:
                    result = self.extract(metadata_source=mode, structure_max_chars=budget,
                                          structure_inventory=inventory)
                self.assertEqual(endpoints, expected_endpoints)
                self.assertEqual(validate.call_count, 1 if source == 'references' else 0)
                self.assertEqual(result['selection']['validation_source'], source)
                plan = result['selection']['metadata_plan']
                self.assertEqual(plan['reason'], reason)
                self.assertEqual(plan['size_evidence']['match'], 'full_product_precaution')

    def test_explicit_structure_still_stops_for_exact_measured_oversize_query(self):
        with patch.object(client, 'urlopen') as http, \
                patch.object(client, 'validate_reference_selection') as validate:
            with self.assertRaises(StructureSizeLimit) as raised:
                self.extract(metadata_source='structure', structure_max_chars=1000,
                             structure_inventory=self.inventory(5000))
        self.assertEqual(raised.exception.evidence['match'], 'exact_query')
        http.assert_not_called()
        validate.assert_not_called()
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / 'result.validation.json').exists())

    def test_unknown_oversize_saves_evidence_and_can_reuse_it_without_structure(self):
        endpoints = []
        body = encoded(structure_fixture('Stor struktur ' * 400))

        def respond(request, **_):
            endpoint = self.endpoint(request)
            endpoints.append(endpoint)
            if endpoint == 'structure':
                return FakeResponse(body)
            self.assertEqual(endpoint, 'data')
            return FakeResponse(encoded(data_fixture()))

        with patch.object(client, 'urlopen', side_effect=respond), \
                patch.object(client, 'validate_reference_selection', wraps=client.validate_reference_selection) as validate:
            result = self.extract(structure_max_chars=1000, structure_inventory=self.inventory())
            self.assertEqual(validate.call_count, 1)
            size_path = self.root / 'result.structure.json.size.json'
            measurement = json.loads(size_path.read_text())['measurements'][0]
            self.assertEqual(measurement['query'], QUERY)
            self.assertEqual(measurement['failure'], 'structure_size_limit')
            self.assertFalse(measurement['complete'])
            self.assertGreater(measurement['response_characters_lower_bound'], 1000)
            self.assertIsNotNone(measurement['checked_at_utc'])
            self.assertFalse((self.root / 'result.structure.json').exists())
            self.assertEqual(self.log(self.root / 'result.structure.json')['outcome'], 'structure_size_limit')
            self.assertEqual(result['selection']['metadata_plan']['reason'], 'observed_structure_exceeds_budget')
            second = client.extract(QUERY, self.root / 'second.json', structure_max_chars=1000,
                                    structure_inventory=size_path)
            self.assertEqual(validate.call_count, 2)
        self.assertEqual(endpoints, ['structure', 'data', 'data'])
        self.assertEqual(second['selection']['metadata_plan']['reason'], 'known_structure_exceeds_budget')

    def test_direct_python_without_budget_accepts_more_than_100000_characters(self):
        endpoints = []
        body = encoded(structure_fixture('x' * 100500))
        self.assertGreater(len(body.decode('utf-8')), 100000)

        def respond(request, **_):
            endpoint = self.endpoint(request)
            endpoints.append(endpoint)
            return FakeResponse(body if endpoint == 'structure' else encoded(data_fixture()))

        with patch.object(client, 'urlopen', side_effect=respond), \
                patch.object(client, 'validate_reference_selection') as validate:
            result = self.extract(structure_inventory=self.inventory(2000000))
        validate.assert_not_called()
        self.assertEqual(endpoints, ['structure', 'data'])
        self.assertEqual(result['selection']['validation_source'], 'structure')
        self.assertIsNone(result['selection']['metadata_plan']['structure_max_characters'])
        structure_path = self.root / 'result.structure.json'
        self.assertEqual(structure_path.read_bytes(), body)
        record = self.log(structure_path)
        self.assertIsNone(record['response_limit_characters'])
        self.assertEqual(record['response_characters'], len(body.decode('utf-8')))
        self.assertEqual(record['sha256'], hashlib.sha256(body).hexdigest())

    def test_character_budget_is_not_utf8_byte_budget_even_across_split_sequences(self):
        body = encoded(structure_fixture('åäö漢😀' * 40), bom=True)
        characters = len(body.decode('utf-8-sig'))
        self.assertGreater(len(body), characters)
        response = FakeResponse(body, chunk_size=1)

        def respond(request, **_):
            endpoint = self.endpoint(request)
            return response if endpoint == 'structure' else FakeResponse(encoded(data_fixture()))

        with patch.object(client, 'urlopen', side_effect=respond) as http, \
                patch.object(client, 'validate_reference_selection') as validate:
            result = self.extract(structure_max_chars=characters, structure_inventory=self.inventory())
        self.assertEqual(http.call_count, 2)
        validate.assert_not_called()
        self.assertEqual(result['selection']['validation_source'], 'structure')
        record = self.log(self.root / 'result.structure.json')
        self.assertEqual(record['response_characters'], characters)
        self.assertEqual(record['response_utf8_bytes'], len(body))
        self.assertGreater(len(response.read_sizes), 1)

    def test_observed_unicode_limit_records_characters_not_bytes(self):
        body = encoded(structure_fixture('漢😀' * 300))
        characters = len(body.decode('utf-8'))
        budget = characters - 1

        def respond(request, **_):
            return FakeResponse(body if self.endpoint(request) == 'structure' else encoded(data_fixture()))

        with patch.object(client, 'urlopen', side_effect=respond):
            result = self.extract(structure_max_chars=budget, structure_inventory=self.inventory())
        measurement = result['selection']['metadata_plan']['size_evidence']['measurement']
        self.assertEqual(measurement['response_characters_lower_bound'], characters)
        self.assertLess(measurement['response_characters_lower_bound'], len(body))
        self.assertEqual(result['selection']['validation_source'], 'references')

    def test_network_and_http_failures_do_not_fall_back_to_references(self):
        cases = [
            ('network', URLError('synthetic connection failure'), 1),
            ('permission', PermissionError('synthetic denied socket'), 1),
            ('http403', HTTPError('https://api.trafa.se/api/structure', 403, 'synthetic forbidden', {}, None), 1),
            ('http503', HTTPError('https://api.trafa.se/api/structure', 503, 'synthetic unavailable', {'Retry-After': '0'}, None), 3),
            ('http503_no_headers', HTTPError('https://api.trafa.se/api/structure', 503, 'synthetic unavailable', None, None), 3),
        ]
        for label, failure, expected_calls in cases:
            with self.subTest(label=label):
                self.output = self.root / (label + '.json')
                with patch.object(client, 'urlopen', side_effect=failure) as http, \
                        patch.object(client, 'validate_reference_selection') as validate, \
                        patch.object(client.time, 'sleep'):
                    with self.assertRaises(type(failure)) as raised:
                        self.extract(structure_max_chars=100000, structure_inventory=self.inventory())
                self.assertIs(raised.exception, failure)
                self.assertEqual(http.call_count, expected_calls)
                self.assertTrue(all(self.endpoint(call.args[0]) == 'structure' for call in http.call_args_list))
                validate.assert_not_called()
                self.assertFalse(self.output.exists())
                if isinstance(failure, HTTPError):
                    record = self.log(self.output.with_name(self.output.stem + '.structure.json'))
                    self.assertEqual(record['outcome'], 'http_error')
                    self.assertEqual(record['http_status'], failure.code)
                    self.assertEqual(record['attempts'], expected_calls)
                    if failure.headers is None:
                        self.assertIsNone(record['content_type'])

    def test_json_schema_and_declared_format_failures_do_not_fall_back(self):
        invalid_schema = structure_fixture()
        del invalid_schema['DataCount']
        cases = [
            ('schema', encoded(invalid_schema), 'application/json'),
            ('malformed_json', b'{"DataCount":', 'application/json'),
            ('wrong_format', encoded(structure_fixture()), 'application/xml'),
            ('invalid_utf8', b'\xff\xfe', 'application/json'),
        ]
        for label, body, content_type in cases:
            with self.subTest(label=label):
                self.output = self.root / (label + '.json')
                response = FakeResponse(body, content_type=content_type)
                with patch.object(client, 'urlopen', return_value=response) as http, \
                        patch.object(client, 'validate_reference_selection') as validate:
                    with self.assertRaises(ValueError):
                        self.extract(structure_max_chars=100000, structure_inventory=self.inventory())
                self.assertEqual(http.call_count, 1)
                self.assertEqual(self.endpoint(http.call_args.args[0]), 'structure')
                validate.assert_not_called()
                self.assertFalse(self.output.exists())

    def test_reference_validation_failure_stops_before_any_data_request(self):
        invalid_query = QUERY.replace('ar:2026', 'ar:2027')
        with patch.object(client, 'urlopen') as http, \
                patch.object(client, 'validate_reference_selection', wraps=client.validate_reference_selection) as validate:
            with self.assertRaisesRegex(ValueError, 'Unknown reference value'):
                client.extract(invalid_query, self.output, structure_max_chars=1000,
                               structure_inventory=self.inventory(5000, query=invalid_query))
        http.assert_not_called()
        self.assertEqual(validate.call_count, 1)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / 'result.validation.json').exists())

    def test_selected_and_option_rejections_are_semantic_stops(self):
        cases = [
            ('ar', 'Selected', False), ('ar', 'Option', False), ('ar', 'Option', None),
            ('2026', 'Selected', False), ('2026', 'Option', False), ('2026', 'Option', None),
            ('nyreg', 'Option', False), ('t10036', 'Selected', False),
        ]
        for index, (name, field, value) in enumerate(cases):
            with self.subTest(name=name, field=field, value=value):
                payload = structure_fixture()
                nodes = payload['StructureItems'] + [
                    child for node in payload['StructureItems'] for child in node['StructureItems']]
                next(node for node in nodes if node['Name'] == name)[field] = value
                # These are valid schema values; the semantic selection gate must reject them.
                self.contract.validate_response('structure', payload)
                self.output = self.root / ('semantic-' + str(index) + '.json')
                with patch.object(client, 'urlopen', return_value=FakeResponse(encoded(payload))) as http, \
                        patch.object(client, 'validate_reference_selection') as validate:
                    with self.assertRaises(ValueError):
                        self.extract(structure_max_chars=100000, structure_inventory=self.inventory())
                self.assertEqual(http.call_count, 1)
                self.assertEqual(self.endpoint(http.call_args.args[0]), 'structure')
                validate.assert_not_called()
                self.assertFalse(self.output.exists())

    def test_http200_api_error_is_not_reclassified_as_a_size_failure(self):
        for failing_endpoint in ('structure', 'data'):
            with self.subTest(endpoint=failing_endpoint):
                payload = api_error_fixture(failing_endpoint)
                self.contract.validate_response(failing_endpoint, payload)
                body = encoded(payload)
                self.output = self.root / (failing_endpoint + '-error.json')
                endpoints = []

                def respond(request, **_):
                    endpoint = self.endpoint(request)
                    endpoints.append(endpoint)
                    return FakeResponse(body if endpoint == failing_endpoint else encoded(structure_fixture()))

                with patch.object(client, 'urlopen', side_effect=respond), \
                        patch.object(client, 'validate_reference_selection') as validate:
                    with self.assertRaisesRegex(client.APIResponseError, 'API Errors'):
                        self.extract(structure_max_chars=100000, structure_inventory=self.inventory())
                self.assertEqual(endpoints, ['structure'] if failing_endpoint == 'structure' else ['structure', 'data'])
                validate.assert_not_called()
                raw_path = (self.output.with_name(self.output.stem + '.structure.json')
                            if failing_endpoint == 'structure' else self.output)
                self.assertEqual(raw_path.read_bytes(), body)
                record = self.log(raw_path)
                self.assertEqual(record['outcome'], 'api_error')
                self.assertTrue(record['schema_validated'])
                self.assertEqual(record['http_status'], 200)
                self.assertEqual(record['sha256'], hashlib.sha256(body).hexdigest())
                self.assertFalse(Path(str(raw_path) + '.size.json').exists())

    def test_api_error_cannot_be_summarized_as_empty_success_including_saved_input(self):
        for endpoint, summarize in [('structure', client.structure_summary), ('data', client.data_summary)]:
            with self.subTest(endpoint=endpoint):
                payload = api_error_fixture(endpoint)
                self.contract.validate_response(endpoint, payload)
                with self.assertRaises(client.APIResponseError):
                    summarize(payload)
                source = self.root / (endpoint + '-input.json')
                source.write_bytes(encoded(payload))
                summary_path = self.root / (endpoint + '-summary.json')
                args = ['trafa_client.py', endpoint, '--input', str(source), '--raw', str(self.output),
                        '--summary', str(summary_path)]
                if endpoint == 'data':
                    selection_path = self.root / 'input-selection.json'
                    selection_path.write_bytes(encoded(structure_fixture()))
                    args.extend(['--query', QUERY, '--structure', str(selection_path)])
                with patch('sys.argv', args), patch('sys.stdout', new_callable=io.StringIO) as stdout, \
                        patch.object(client, 'urlopen') as http:
                    with self.assertRaises(client.APIResponseError):
                        client.main()
                http.assert_not_called()
                self.assertEqual(stdout.getvalue(), '')
                self.assertFalse(summary_path.exists())

    def test_null_cell_row_can_be_sampled_without_fabricating_cells(self):
        payload = data_fixture()
        payload['Rows'] = [{'Cell': None}]
        self.contract.validate_response('data', payload)

        def respond(request, **_):
            return FakeResponse(encoded(structure_fixture() if self.endpoint(request) == 'structure' else payload))

        with patch.object(client, 'urlopen', side_effect=respond) as http:
            result = self.extract(structure_inventory=self.inventory())
        self.assertEqual(http.call_count, 2)
        self.assertEqual(result['row_count'], 1)
        self.assertEqual(result['row_sample'], [{'dimensions': {}, 'measures': {},
                                                'is_total': None, 'note_ids': []}])
        self.assertTrue(result['sample_complete'])

    def test_explicit_structure_mode_does_not_override_user_choice_on_size_failure(self):
        body = encoded(structure_fixture('x' * 2000))
        with patch.object(client, 'urlopen', return_value=FakeResponse(body)) as http, \
                patch.object(client, 'validate_reference_selection') as validate:
            with self.assertRaises(StructureSizeLimit):
                self.extract(metadata_source='structure', structure_max_chars=1000,
                             structure_inventory=self.inventory())
        self.assertEqual(http.call_count, 1)
        validate.assert_not_called()
        self.assertTrue((self.root / 'result.structure.json.size.json').exists())
        self.assertFalse(self.output.exists())

    def test_live_zero_datacount_stops_without_fabricating_missing_data(self):
        payload = structure_fixture()
        payload['DataCount'] = 0
        with patch.object(client, 'urlopen', return_value=FakeResponse(encoded(payload))) as http, \
                patch.object(client, 'validate_reference_selection') as validate:
            result = self.extract(structure_inventory=self.inventory())
        self.assertEqual(http.call_count, 1)
        validate.assert_not_called()
        self.assertEqual(result['selection']['validation_source'], 'structure')
        self.assertFalse(result['data_requested'])
        self.assertTrue(result['empty_selection'])
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
