"""Offline tests for the explicitly supported Trafikanalys contract subset."""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

from api_contract import APIContract


def node(name, kind, parent=None, children=None):
    return {'Name': name, 'Type': kind, 'ParentName': parent,
            'Selected': True, 'Option': True, 'StructureItems': children or []}


def structure_payload():
    # Product variables are siblings of P, while their values can be nested.
    return {'DataCount': 1, 'StructureItems': [
        node('t10036', 'P'),
        node('ar', 'D', 't10036', [node('2026', 'DV', 'ar')]),
        node('region', 'H', 't10036', [
            node('lan', 'D', 'region', [node('01', 'DV', 'lan')])]),
    ]}


def statistics_payload():
    return {
        'Header': {'Column': [{'Name': 'nyreg', 'Type': 'M', 'Unit': None}]},
        'Rows': [{'Cell': [
            {'Column': 'ar', 'Name': '2026', 'Value': '2026', 'IsMeasure': False},
            {'Column': 'nyreg', 'Value': '14096', 'IsMeasure': True,
             'NoteIds': [1, 'source'], 'Versions': [{'revision': 'a', 'extra': None}]},
        ], 'IsTotal': None}],
        'Errors': None,
        'Notes': {'source': {'text': 'A note with unspecified additional fields'}},
    }


class APIContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = APIContract()
        cls.document = json.loads(cls.contract.path.read_text(encoding='utf-8'))

    def changed_contract(self, change):
        document = copy.deepcopy(self.document)
        change(document)
        folder = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(folder.cleanup)
        path = Path(folder.name) / 'contract.json'
        path.write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')
        return APIContract(path)

    def root_schema(self, schema):
        return self.changed_contract(lambda doc: doc['components']['schemas'].__setitem__(
            'StatisticsResponse', schema))

    def test_version_path_and_raw_file_hash(self):
        self.assertEqual(self.contract.version, '2.1.0')
        self.assertEqual(self.contract.path.name, 'openapi-trafa.json')
        self.assertEqual(self.contract.sha256, hashlib.sha256(self.contract.path.read_bytes()).hexdigest())
        for item in self.document['paths'].values():
            self.assertLessEqual(len(item['get']['description']), 300)

    def test_request_encodes_exact_query_without_network(self):
        query = 't10036|nyreg|ar:2026|manad:09|drivm:103'
        request = self.contract.request('data', query)
        parts = urlsplit(request['url'])
        self.assertEqual(parts.scheme, 'https')
        self.assertEqual(parts.netloc, 'api.trafa.se')
        self.assertEqual(parts.path, '/api/data')
        self.assertEqual(parse_qs(parts.query), {'query': [query], 'lang': ['sv']})
        self.assertEqual(request['method'], 'GET')
        self.assertEqual(request['headers'], {'Accept': 'application/json'})

    def test_product_list_omits_query(self):
        request = self.contract.request('/structure')
        self.assertEqual(parse_qs(urlsplit(request['url']).query), {'lang': ['sv']})

    def test_request_constraints_come_from_schema(self):
        for endpoint, query, lang in [
            ('data', None, 'sv'), ('data', '', 'sv'), ('structure', '', 'sv'),
            ('data', True, 'sv'), ('data', 't10036|nyreg', 'xx'),
        ]:
            with self.subTest(endpoint=endpoint, query=query, lang=lang):
                with self.assertRaises(ValueError):
                    self.contract.request(endpoint, query, lang)
        with self.assertRaisesRegex(ValueError, 'not declared'):
            self.contract.request('made-up-endpoint', 'q')

    def test_server_path_method_and_language_change_with_contract(self):
        def change(doc):
            doc['servers'][0]['url'] = 'https://example.invalid/changed-base'
            operation = doc['paths'].pop('/data')['get']
            doc['paths']['/observations'] = {'head': operation}
            for parameter in operation['parameters']:
                if parameter['name'] == 'lang':
                    parameter['schema']['enum'].append('fi')
        contract = self.changed_contract(change)
        request = contract.request('observations', 'q', 'fi')
        parts = urlsplit(request['url'])
        self.assertEqual(parts.netloc, 'example.invalid')
        self.assertEqual(parts.path, '/changed-base/observations')
        self.assertEqual(request['method'], 'HEAD')
        self.assertEqual(parse_qs(parts.query)['lang'], ['fi'])

    def test_valid_nested_and_sibling_structure(self):
        self.assertIsNone(self.contract.validate_response('structure', structure_payload()))

    def test_bool_is_not_integer(self):
        payload = structure_payload()
        payload['DataCount'] = True
        with self.assertRaisesRegex(ValueError, 'DataCount.*integer'):
            self.contract.validate_response('structure', payload)
        payload['DataCount'] = 1
        payload['StructureItems'][0]['Id'] = False
        with self.assertRaisesRegex(ValueError, 'Id.*integer'):
            self.contract.validate_response('structure', payload)

    def test_integral_json_number_is_integer(self):
        payload = structure_payload()
        payload['DataCount'] = 1.0
        self.contract.validate_response('structure', payload)
        payload['DataCount'] = 1.5
        with self.assertRaises(ValueError):
            self.contract.validate_response('structure', payload)

    def test_dimension_value_code_must_keep_string_type(self):
        payload = structure_payload()
        payload['StructureItems'][1]['StructureItems'][0]['Name'] = 2026
        with self.assertRaisesRegex(ValueError, 'Name.*string'):
            self.contract.validate_response('structure', payload)

    def test_unknown_structure_type_fails_enum(self):
        payload = structure_payload()
        payload['StructureItems'][0]['Type'] = 'MadeUpType'
        with self.assertRaisesRegex(ValueError, 'enum'):
            self.contract.validate_response('structure', payload)

    def test_missing_required_structure_field(self):
        payload = structure_payload()
        del payload['StructureItems'][1]['Option']
        with self.assertRaisesRegex(ValueError, 'missing required property Option'):
            self.contract.validate_response('structure', payload)

    def test_nullable_fields_and_numeric_strings_are_preserved(self):
        payload = statistics_payload()
        self.contract.validate_response('data', payload)
        for value in [None, '14096', 14096, 14096.5]:
            payload['Rows'][0]['Cell'][1]['Value'] = value
            self.contract.validate_response('data', payload)
        self.contract.validate_response('data', {'Header': None, 'Rows': None, 'Errors': None})

    def test_boolean_measure_is_not_numeric(self):
        payload = statistics_payload()
        payload['Rows'][0]['Cell'][1]['Value'] = True
        with self.assertRaisesRegex(ValueError, 'Value.*string/number/null'):
            self.contract.validate_response('data', payload)

    def test_nonfinite_measure_is_not_json_number(self):
        for value in [float('nan'), float('inf')]:
            with self.subTest(value=value):
                payload = statistics_payload()
                payload['Rows'][0]['Cell'][1]['Value'] = value
                with self.assertRaises(ValueError):
                    self.contract.validate_response('data', payload)

    def test_http_200_errors_are_valid_body_shape(self):
        self.contract.validate_response('data', {
            'Header': None, 'Rows': [], 'Errors': ['Ogiltigt urval'],
        })
        with self.assertRaisesRegex(ValueError, 'Errors'):
            self.contract.validate_response('data', {'Header': None, 'Rows': [], 'Errors': [42]})

    def test_missing_rows_and_cell_value_fail(self):
        payload = statistics_payload()
        del payload['Rows']
        with self.assertRaisesRegex(ValueError, 'missing required property Rows'):
            self.contract.validate_response('data', payload)
        payload = statistics_payload()
        del payload['Rows'][0]['Cell'][0]['Value']
        with self.assertRaisesRegex(ValueError, 'missing required property Value'):
            self.contract.validate_response('data', payload)

    def test_extra_response_fields_are_allowed(self):
        payload = statistics_payload()
        payload['FutureField'] = {'metadata': [1, None, {'comment': 'extra'}]}
        payload['Rows'][0]['Cell'][0]['FutureCellField'] = 'retained'
        self.contract.validate_response('data', payload)

    def test_no_invented_response_length_limit(self):
        payload = statistics_payload()
        payload['Rows'][0]['Cell'][1]['Value'] = 'x' * 120000
        self.contract.validate_response('data', payload)

    def test_unknown_keyword_in_unused_schema_is_rejected(self):
        def change(doc):
            doc['components']['schemas']['FutureUnusedSchema'] = {'type': 'string', 'pattern': '^x'}
        with self.assertRaisesRegex(ValueError, 'Unsupported schema keyword.*pattern'):
            self.changed_contract(change)

    def test_unknown_keyword_inside_anyof_is_rejected_before_use(self):
        def change(doc):
            doc['components']['schemas']['StatisticsHeader']['properties']['NewField'] = {
                'anyOf': [{'type': 'null'}, {'type': 'number', 'minimum': 0}],
            }
        with self.assertRaisesRegex(ValueError, 'Unsupported schema keyword.*minimum'):
            self.changed_contract(change)

    def test_anyof_rejects_invalid_header(self):
        payload = statistics_payload()
        payload['Header'] = 'not an object'
        with self.assertRaisesRegex(ValueError, 'anyOf'):
            self.contract.validate_response('data', payload)

    def test_enum_boolean_number_distinction(self):
        contract = self.root_schema({'enum': [1, {'x': [2]}]})
        contract.validate_response('data', 1.0)
        contract.validate_response('data', {'x': [2.0]})
        for payload in [True, {'x': [True]}]:
            with self.assertRaises(ValueError):
                contract.validate_response('data', payload)

    def test_additional_properties_false_and_schema(self):
        strict = self.root_schema({'type': 'object', 'properties': {'known': {'type': 'string'}},
                                   'additionalProperties': False})
        strict.validate_response('data', {'known': 'ok'})
        with self.assertRaises(ValueError):
            strict.validate_response('data', {'extra': 'no'})
        typed = self.root_schema({'type': 'object', 'additionalProperties': {'type': 'integer'}})
        typed.validate_response('data', {'extra': 1})
        with self.assertRaises(ValueError):
            typed.validate_response('data', {'extra': True})

    def test_ref_siblings_and_escaped_json_pointer(self):
        def change(doc):
            schemas = doc['components']['schemas']
            schemas['Text/Value~'] = {'type': 'string'}
            schemas['StatisticsResponse'] = {'$ref': '#/components/schemas/Text~1Value~0', 'minLength': 2}
        contract = self.changed_contract(change)
        contract.validate_response('data', 'ok')
        with self.assertRaisesRegex(ValueError, 'minLength'):
            contract.validate_response('data', 'x')

    def test_external_and_broken_refs_are_rejected_without_network(self):
        for ref in ['https://example.invalid/schema.json', '#/components/schemas/DoesNotExist']:
            with self.subTest(ref=ref):
                with self.assertRaises(ValueError):
                    self.root_schema({'$ref': ref})

    def test_unsupported_parameter_serialization_is_rejected(self):
        def change(doc):
            doc['paths']['/data']['get']['parameters'][0]['allowReserved'] = True
        with self.assertRaisesRegex(ValueError, 'Unsupported parameter definition'):
            self.changed_contract(change)


if __name__ == '__main__':
    unittest.main()
