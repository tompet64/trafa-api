"""Offline checks of saved measurement provenance and metadata routing."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from urllib.parse import parse_qs, urlsplit

from structure_routing import DEFAULT_INVENTORY, StructureSizeLimit, _check_source, plan_metadata, size_evidence


class SourcePointerTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix='trafa-size-source-test-')
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.source_number = 0
        self.measurement = {
            'endpoint': 'structure', 'query': 't10036', 'lang': 'sv',
            'scope': 'full_product', 'complete': True,
            'checked_at_utc': '2026-10-09T15:00:00Z',
            'requested_format': 'json', 'observed_format': 'json',
            'response_characters': 110000,
        }

    def sourced(self, measurement=None, *, document=None, pointer='/T10036/0'):
        record = copy.deepcopy(measurement if measurement is not None else self.measurement)
        document = {'T10036': [copy.deepcopy(record)]} if document is None else document
        raw = json.dumps(document, ensure_ascii=False).encode('utf-8')
        self.source_number += 1
        path = self.root / ('source-' + str(self.source_number) + '.json')
        path.write_bytes(raw)
        record['source'] = {'file': path.name, 'sha256': hashlib.sha256(raw).hexdigest(),
                            'json_pointer': pointer}
        return record

    def inventory(self, *records):
        path = self.root / 'inventory.json'
        path.write_text(json.dumps({'schema_version': 1, 'measurements': list(records)}), encoding='utf-8')
        return path

    def test_array_index_selects_the_requested_measurement(self):
        other = dict(self.measurement, response_characters=2000)
        record = self.sourced(document={'T10036': [other, self.measurement]}, pointer='/T10036/1')
        _check_source(record, self.root)
        evidence = size_evidence('t10036', inventory_path=self.inventory(record))
        self.assertEqual(evidence['characters'], 110000)

    def test_escaped_tokens_empty_keys_and_literal_tilde_one(self):
        cases = [
            ({'a/b': {'~key': [{'': self.measurement}]}}, '/a~1b/~0key/0/'),
            ({'~1': [self.measurement]}, '/~01/0'),
            ({'01': self.measurement}, '/01'),
        ]
        for document, pointer in cases:
            with self.subTest(pointer=pointer):
                _check_source(self.sourced(document=document, pointer=pointer), self.root)

    def test_empty_pointer_checks_the_root_measurement(self):
        record = self.sourced(document=self.measurement, pointer='')
        _check_source(record, self.root)
        record['response_characters'] += 1
        with self.assertRaisesRegex(ValueError, 'response_characters'):
            _check_source(record, self.root)

    def test_invalid_pointer_syntax_is_rejected_as_value_error(self):
        for pointer in [None, 0, True, [], 'T10036/0', '#/T10036/0', '/T10036~2/0', '/T10036~/0']:
            with self.subTest(pointer=pointer):
                with self.assertRaisesRegex(ValueError, 'JSON pointer'):
                    _check_source(self.sourced(pointer=pointer), self.root)

    def test_invalid_array_indices_do_not_use_python_index_rules(self):
        for token in ['-1', '+0', '00', '01', '-', '', '1.0', ' 0', '\u0660', '1']:
            with self.subTest(token=token):
                with self.assertRaisesRegex(ValueError, 'JSON pointer'):
                    _check_source(self.sourced(pointer='/T10036/' + token), self.root)

    def test_missing_path_scalar_traversal_and_nonobject_targets_are_clear_errors(self):
        cases = [
            ({'T10036': [self.measurement]}, '/missing/0'),
            ({'T10036': [7]}, '/T10036/0/query'),
            ({'T10036': [7]}, '/T10036/0'),
            ({'T10036': [self.measurement]}, '/T10036'),
        ]
        for document, pointer in cases:
            with self.subTest(pointer=pointer, document=document):
                with self.assertRaisesRegex(ValueError, 'JSON pointer'):
                    _check_source(self.sourced(document=document, pointer=pointer), self.root)

    def test_changed_source_hash_stops_routing(self):
        record = self.sourced()
        path = self.root / record['source']['file']
        path.write_bytes(path.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'source has changed'):
            plan_metadata('t10036', max_chars=80000, inventory_path=self.inventory(record))

    def test_changed_inventory_measurement_fields_stop_validation(self):
        changes = {'query': 't10026', 'checked_at_utc': '2026-10-10T00:00:00Z',
                   'requested_format': 'xml', 'observed_format': 'xml', 'response_characters': 110001}
        for field, value in changes.items():
            with self.subTest(field=field):
                record = self.sourced()
                record[field] = value
                with self.assertRaisesRegex(ValueError, 'saved measurement: ' + field):
                    _check_source(record, self.root)

    def test_source_cannot_escape_inventory_directory(self):
        record = self.sourced()
        record['source']['file'] = '../outside-source.json'
        with self.assertRaisesRegex(ValueError, 'inside its inventory directory'):
            _check_source(record, self.root)

    def test_exact_evidence_takes_precedence_over_full_product_precaution(self):
        query = 't10036|nyreg|ar:2026|manad:09'
        full = self.sourced()
        exact = self.sourced(dict(self.measurement, query=query, scope='exact_query', response_characters=2000))
        path = self.inventory(full, exact)
        plan = plan_metadata(query, max_chars=80000, inventory_path=path)
        self.assertEqual(plan['metadata_source'], 'structure')
        self.assertEqual(plan['size_evidence']['match'], 'exact_query')
        self.assertEqual(plan['size_evidence']['characters'], 2000)

    def test_full_product_precaution_does_not_claim_a_filtered_measurement(self):
        path = self.inventory(self.sourced())
        query = 't10036|nyreg|ar:2026|manad:09'
        auto = plan_metadata(query, max_chars=80000, inventory_path=path)
        self.assertEqual(auto['metadata_source'], 'references')
        self.assertEqual(auto['reason'], 'full_product_size_precaution')
        self.assertEqual(auto['size_evidence']['measurement']['query'], 't10036')
        explicit = plan_metadata(query, mode='structure', max_chars=80000, inventory_path=path)
        self.assertEqual(explicit['metadata_source'], 'structure')
        self.assertEqual(explicit['reason'], 'explicit_bounded_structure_probe')
        with self.assertRaises(StructureSizeLimit):
            plan_metadata('t10036', mode='structure', max_chars=80000, inventory_path=path)

    def test_language_and_response_format_must_match(self):
        path = self.inventory(self.sourced())
        self.assertIsNone(size_evidence('t10036', lang='en', inventory_path=path))
        for field in ['requested_format', 'observed_format']:
            with self.subTest(field=field):
                measurement = dict(self.measurement, **{field: 'xml'})
                path = self.inventory(self.sourced(measurement))
                self.assertIsNone(size_evidence('t10036', inventory_path=path))

    def test_invalid_recorded_sizes_are_rejected(self):
        for count in [True, False, 0, -1, 2000.5, '2000', None]:
            with self.subTest(count=count):
                record = self.sourced(dict(self.measurement, response_characters=count))
                with self.assertRaisesRegex(ValueError, 'positive integer'):
                    size_evidence('t10036', inventory_path=self.inventory(record))

    def test_size_at_budget_is_allowed_and_no_budget_keeps_python_route(self):
        path = self.inventory(self.sourced())
        self.assertEqual(plan_metadata('t10036', max_chars=110000, inventory_path=path)['metadata_source'], 'structure')
        self.assertEqual(plan_metadata('t10036', max_chars=109999, inventory_path=path)['metadata_source'], 'references')
        self.assertEqual(plan_metadata('t10036', inventory_path=path)['metadata_source'], 'structure')


class BundledInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = DEFAULT_INVENTORY.parent
        source_path = cls.root / 'structure_measurements_20261009.json'
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        cls.inventory = json.loads(DEFAULT_INVENTORY.read_text(encoding='utf-8'))
        cls.records = cls.inventory['measurements']
        cls.products = json.loads((cls.root / 'produktlista_aktuell.json').read_text(encoding='utf-8'))['products']

    def test_all_56_current_products_have_valid_source_pointers_and_exact_sizes(self):
        expected = {product['Name'] for product in self.products}
        self.assertEqual(len(expected), 56)
        self.assertEqual(len(self.records), 56)
        self.assertEqual({record['query'] for record in self.records}, expected)
        for record in self.records:
            with self.subTest(query=record['query']):
                _check_source(record, self.root)
                evidence = size_evidence(record['query'])
                self.assertEqual(evidence['match'], 'exact_query')
                self.assertEqual(evidence['characters'], record['response_characters'])
                self.assertEqual(evidence['measurement'], record)
                self.assertEqual(record['lang'], 'sv')
                self.assertEqual(record['scope'], 'full_product')
                self.assertEqual(record['requested_format'], 'json')
                self.assertEqual(record['observed_format'], 'json')
                self.assertIs(record['complete'], True)
                self.assertEqual(parse_qs(urlsplit(record['url']).query)['lang'], ['sv'])

    def test_historical_product_and_other_language_are_not_matched(self):
        self.assertIsNone(size_evidence('t0401'))
        self.assertIsNone(size_evidence('t0401|example'))
        for record in self.records:
            with self.subTest(query=record['query']):
                self.assertIsNone(size_evidence(record['query'], lang='en'))

    def test_t10036_uses_references_at_80000_with_full_product_provenance(self):
        query = 't10036|nyreg|ar:2026|drivm:103|manad:09'
        plan = plan_metadata(query, max_chars=80000)
        self.assertEqual(plan['metadata_source'], 'references')
        self.assertEqual(plan['reason'], 'full_product_size_precaution')
        self.assertEqual(plan['size_evidence']['match'], 'full_product_precaution')
        self.assertEqual(plan['size_evidence']['measurement']['query'], 't10036')
        self.assertGreater(plan['size_evidence']['characters'], 80000)
        self.assertEqual(plan_metadata(query, lang='en', max_chars=80000)['metadata_source'], 'structure')


if __name__ == '__main__':
    unittest.main()
