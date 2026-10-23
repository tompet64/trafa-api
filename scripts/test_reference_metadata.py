"""Offline reference evidence must not become an invented live selection."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from reference_metadata import validate_reference_selection


SCRIPTS = Path(__file__).resolve().parent
REFERENCES = SCRIPTS.parent / 'references' / 'metadata'
FILES = ['variabelkatalog_kompakt.json', 'kombinationer.json', 'vardemangder.json']
MONTH_QUERY = 't10036|nyreg|ar:2026|drivm:103|manad:09'


class ReferenceMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source_hashes = {
            name: hashlib.sha256((REFERENCES / name).read_bytes()).hexdigest()
            for name in FILES
        }
        originals = {
            name: json.loads((REFERENCES / name).read_text(encoding='utf-8'))
            for name in FILES
        }
        catalog = {key: originals[FILES[0]][key] for key in ['T10036', 'T10026']}
        refs = {variable['value_set_ref'] for product in catalog.values()
                for variable in product['variables'] if variable.get('value_set_ref')}
        cls.fixture = {
            FILES[0]: catalog,
            FILES[1]: {key: originals[FILES[1]][key] for key in catalog},
            FILES[2]: {key: originals[FILES[2]][key] for key in refs},
        }

    @classmethod
    def tearDownClass(cls):
        after = {name: hashlib.sha256((REFERENCES / name).read_bytes()).hexdigest()
                 for name in FILES}
        if after != cls.source_hashes:
            raise AssertionError('Source metadata files changed during offline tests')

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='trafa-reference-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.documents = copy.deepcopy(self.fixture)
        self.write_fixture()

    def write_fixture(self):
        for name, document in self.documents.items():
            (self.root / name).write_text(json.dumps(document, ensure_ascii=False), encoding='utf-8')

    def variable(self, name, product='T10036'):
        return next(v for v in self.documents[FILES[0]][product]['variables']
                    if v['api_name'] == name)

    def validate(self, query=MONTH_QUERY, **kwargs):
        return validate_reference_selection(query, root=self.root, **kwargs)

    def cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPTS / 'metadata_lookup.py'), '--root', str(self.root), *arguments],
            text=True, capture_output=True, check=False,
        )

    def test_real_monthly_selection_has_dated_receipt_and_file_hashes(self):
        result = validate_reference_selection(MONTH_QUERY, root=REFERENCES)
        self.assertEqual(result['validation_source'], 'references')
        self.assertEqual(result['query'], MONTH_QUERY)
        self.assertEqual(result['lang'], 'sv')
        self.assertEqual(result['product'], 't10036')
        self.assertEqual(result['measures'], ['nyreg'])
        self.assertEqual(result['filters']['manad'], ['09'])
        self.assertIsNone(result['DataCount'])
        self.assertEqual(result['documented_combination'], 'nyreg|ar|drivm|manad')
        self.assertEqual(result['combination_status'], 'historical_documentation')
        self.assertEqual(result['reference_metadata_checked_at_utc'],
                         '2026-10-09T15:15:20.741329+00:00')
        self.assertIsNotNone(datetime.fromisoformat(result['validated_at_utc']).tzinfo)
        self.assertNotEqual(result['validated_at_utc'], result['reference_metadata_checked_at_utc'])
        self.assertEqual({x['path']: x['sha256'] for x in result['reference_files']}, self.source_hashes)
        self.assertNotIn('Selected', result)
        self.assertNotIn('Option', result)

    def test_real_regional_measures_share_one_documented_table(self):
        query = 't10026|itrfslut|nyregunder|ar:2019,2023|reglan:01|drivmedel:103'
        result = validate_reference_selection(query, root=REFERENCES, lang='en')
        self.assertEqual(result['measures'], ['itrfslut', 'nyregunder'])
        self.assertEqual(result['filters']['ar'], ['2019', '2023'])
        self.assertEqual(result['filters']['reglan'], ['01'])
        self.assertEqual(result['lang'], 'en')
        self.assertEqual(result['documented_combination'], 'itrfslut|nyregunder|ar|drivmedel|reglan')

    def test_real_regional_parent_chain_and_explicit_total(self):
        query = 't10026|itrfslut|agarkat:t1|ar:2019,2023|reglan:12|regkom:1280'
        result = validate_reference_selection(query, root=REFERENCES)
        self.assertEqual(result['filters']['agarkat'], ['t1'])
        self.assertEqual(result['documented_combination'], 'itrfslut|agarkat|ar|reglan|regkom')
        self.assertNotIn('regpl', result['dimensions'])

    def test_subset_of_explicit_measure_list_is_supported(self):
        result = self.validate('t10036|itrf|ar:2026|manad:09')
        self.assertEqual(result['measures'], ['itrf'])
        self.assertEqual(result['documented_combination'], 'avreg|avst|itrf|nyreg|ar|manad')

    def test_query_syntax_rejects_empty_duplicate_and_filtered_measure(self):
        invalid = [None, '', '|nyreg', 't10036|', 't10036||nyreg',
                   't10036|nyreg|nyreg|ar:2026|manad:09',
                   't10036|nyreg|ar:2026|ar:2025|manad:09',
                   't10036|nyreg|ar:2026,2026|manad:09',
                   't10036|nyreg|ar:|manad:09',
                   't10036|nyreg|ar:2026,|manad:09',
                   't10036|nyreg|ar:2026::2025|manad:09',
                   't10036 |nyreg|ar:2026|manad:09',
                   't10036|nyreg:1|ar:2026|manad:09',
                   't10036|ar:2026|manad:09']
        for query in invalid:
            with self.subTest(query=query), self.assertRaises(ValueError):
                self.validate(query)

    def test_unknown_year_zero_prefix_case_and_variable_are_not_normalized(self):
        invalid = [MONTH_QUERY.replace('2026', '2027'),
                   MONTH_QUERY.replace('manad:09', 'manad:9'),
                   MONTH_QUERY.replace('t10036', 'T10036'),
                   MONTH_QUERY.replace('ar:2026', 'Ar:2026'),
                   MONTH_QUERY.replace('drivm:103', 'drivmedel:103')]
        for query in invalid:
            with self.subTest(query=query), self.assertRaises(ValueError):
                self.validate(query)

    def test_dynamic_filters_need_current_metadata(self):
        for query in [MONTH_QUERY.replace('2026', 'senaste'),
                      MONTH_QUERY.replace('manad:09', 'manad:forra')]:
            with self.subTest(query=query), self.assertRaisesRegex(ValueError, 'Dynamic filters'):
                self.validate(query)
        self.variable('ar')['dynamic_filters'].append({'code': 'custom_latest', 'type': 'F'})
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Dynamic filters'):
            self.validate(MONTH_QUERY.replace('2026', 'custom_latest'))

    def test_missing_dimension_and_extra_hierarchy_have_no_table_support(self):
        invalid = [MONTH_QUERY.replace('|manad:09', ''),
                   MONTH_QUERY + '|region',
                   't10026|itrfslut|ar:2023|reglan:01|drivmedel:103|regpl']
        for query in invalid:
            with self.subTest(query=query), self.assertRaisesRegex(ValueError, 'No single documented combination'):
                self.validate(query)

    def test_dimension_only_row_does_not_support_an_unlisted_measure(self):
        query = 't10036|itrf|ar:2026|drivm:103|manad:09|kommun:0180'
        with self.assertRaisesRegex(ValueError, 'No single documented combination'):
            self.validate(query)

    def test_two_marginal_tables_cannot_be_crossed(self):
        query = 't10036|nyreg|ar:2026|klimatb|drivm:103|manad:09'
        with self.assertRaisesRegex(ValueError, 'No single documented combination'):
            self.validate(query)
        query = 't10036|nyreg|akumunyreg|ar:2026|drivm:103|manad:09|kommun:0180'
        with self.assertRaisesRegex(ValueError, 'No single documented combination'):
            self.validate(query)

    def test_missing_foreign_and_measure_parents_are_rejected(self):
        for parent in ['missing_parent', 't10026', 'nyreg']:
            with self.subTest(parent=parent):
                self.variable('ar')['parent_name'] = parent
                self.write_fixture()
                with self.assertRaisesRegex(ValueError, 'parent'):
                    self.validate()

    def test_parent_cycle_is_rejected(self):
        self.variable('ar')['parent_name'] = 'manad'
        self.variable('manad')['parent_name'] = 'ar'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            self.validate()

    def test_product_flags_and_verified_names_are_required(self):
        for field in ['metadata_usable', 'api_metadata_complete']:
            with self.subTest(field=field):
                original = self.documents[FILES[0]]['T10036'][field]
                self.documents[FILES[0]]['T10036'][field] = False
                self.write_fixture()
                with self.assertRaisesRegex(ValueError, 'incomplete or unusable'):
                    self.validate()
                self.documents[FILES[0]]['T10036'][field] = original
        self.variable('drivm')['api_name_source'] = 'guessed_from_label'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'verified API Name'):
            self.validate()

    def test_product_identity_and_reference_time_are_required(self):
        self.documents[FILES[0]]['T10036']['manual_enrichment']['api_name_documented'] = 't10026'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Conflicting'):
            self.validate()
        self.documents[FILES[0]]['T10036']['manual_enrichment']['api_name_documented'] = 't10036'
        self.documents[FILES[0]]['T10036']['api_checked_at_utc'] = '2026-10-09T12:00:00'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'verification time'):
            self.validate()

    def test_wrong_variable_value_set_cannot_supply_valid_looking_codes(self):
        self.variable('drivm')['value_set_ref'] = self.variable('manad')['value_set_ref']
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'this product/variable'):
            self.validate(MONTH_QUERY.replace('drivm:103', 'drivm:09'))

    def test_year_range_gaps_and_explicit_year_gaps_are_preserved(self):
        domain = self.documents[FILES[2]][self.variable('ar')['value_set_ref']]
        definitions = [
            {'encoding': 'year_ranges', 'code_format': 'four_digit_string',
             'ranges_inclusive': [[2023, 2023], [2025, 2026]], 'special_values': []},
            {'encoding': 'explicit', 'values': [{'code': y} for y in ['2026', '2023', '2025']]},
        ]
        for definition in definitions:
            with self.subTest(encoding=definition['encoding']):
                domain['definition'] = definition
                self.write_fixture()
                self.assertEqual(self.validate()['filters']['ar'], ['2026'])
                with self.assertRaisesRegex(ValueError, 'Unknown reference value'):
                    self.validate(MONTH_QUERY.replace('2026', '2024'))

    def test_overlapping_ranges_and_duplicate_explicit_codes_are_rejected(self):
        domain = self.documents[FILES[2]][self.variable('ar')['value_set_ref']]
        domain['definition']['ranges_inclusive'] = [[2023, 2026], [2025, 2026]]
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Overlapping'):
            self.validate()
        domain['definition'] = {'encoding': 'explicit', 'values': [{'code': '2026'}, {'code': '2026'}]}
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Duplicate reference value'):
            self.validate()

    def test_missing_files_and_combination_identity_fail_closed(self):
        self.documents[FILES[1]]['T10036']['api_name'] = 't10026'
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'combination product Name'):
            self.validate()
        (self.root / FILES[1]).unlink()
        with self.assertRaisesRegex(ValueError, 'Cannot read reference file'):
            self.validate()

    def test_validation_has_no_network_dependency(self):
        with patch('urllib.request.urlopen', side_effect=AssertionError('Network not permitted')), \
                patch('socket.create_connection', side_effect=AssertionError('Network not permitted')):
            result = self.validate()
        self.assertEqual(result['validation_source'], 'references')

    def test_cli_reference_output_and_existing_lookup_paths(self):
        destination = self.root / 'output' / 'receipt.json'
        command = self.cli('--query', MONTH_QUERY, '--validate-reference', '--output', str(destination))
        self.assertEqual(command.returncode, 0, command.stderr)
        self.assertEqual(json.loads(command.stdout), json.loads(destination.read_text()))
        self.assertEqual(json.loads(command.stdout)['validation_source'], 'references')
        lookup = self.cli('--product', 't10036', '--section', 'combinations', '--variables', 'nyreg', 'drivm')
        self.assertEqual(lookup.returncode, 0, lookup.stderr)
        self.assertIn('nyreg|ar|drivm|manad', json.loads(lookup.stdout)['combinations'])
        self.assertIn('connection constraints', json.loads(lookup.stdout)['warning'])

    def test_cli_rejects_incomplete_mode_and_metadata_overwrite(self):
        for options in [('--query', MONTH_QUERY), ('--validate-reference',),
                        ('--query', MONTH_QUERY, '--validate-reference', '--product', 't10036'),
                        ('--query', MONTH_QUERY, '--validate-reference', '--output', str(self.root / FILES[0]))]:
            with self.subTest(options=options):
                command = self.cli(*options)
                self.assertEqual(command.returncode, 2)
                self.assertIn('error:', command.stderr)
        self.assertEqual(json.loads((self.root / FILES[0]).read_text()), self.documents[FILES[0]])


if __name__ == '__main__':
    unittest.main()
