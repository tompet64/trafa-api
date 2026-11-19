"""Priority 1/5/6/9/10: deterministic checks, NOT an LLM behavior evaluation."""
import copy
import itertools
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from metadata_lookup import expand
from reference_metadata import validate_reference_selection
from statistics_checks import audit, coverage, plan_years, reconcile, compare_scopes, check_explanation

FIXTURES = ROOT / 'evaluation/fixtures/shipping'


class ShippingPriorityTests(unittest.TestCase):
    def test_01_year_domain_before_statistics_request(self):
        catalog = json.loads((ROOT / 'references/metadata/variabelkatalog_kompakt.json').read_text(encoding='utf-8'))
        domains = json.loads((ROOT / 'references/metadata/vardemangder.json').read_text(encoding='utf-8'))
        variable = next(v for v in catalog['T08021']['variables'] if v['api_name'] == 'ar')
        years = [v['code'] for v in expand(domains[variable['value_set_ref']]['definition'])]
        result = plan_years([str(y) for y in range(2016, 2027)], list(reversed(years)))
        self.assertEqual(result['excluded_requested'], ['2016', '2017', '2018', '2019'])
        self.assertEqual(result['domain_bounds'], ['2020', '2026'])
        self.assertEqual(result['observation_coverage'], 'not_assessed')
        with self.assertRaisesRegex(ValueError, 'Unknown reference value'):
            validate_reference_selection('t08021|godsvikt|ar:2016|kvartal')
        with self.assertRaises(ValueError):
            plan_years(['senaste'], years)

    def detail(self):
        raw = json.loads((FIXTURES / 'detail-2025.json').read_text(encoding='utf-8'))
        rows = []
        for row in raw['Rows']:
            cells = {c['Column']: c for c in row['Cell']}
            rows.append({'q': cells['kvartal']['Name'], 'direction': cells['godsrikt']['Name'],
                         'traffic': cells['rikth']['Name'], 'value': cells['godsvikt']['Value']})
        return rows

    def test_05_sparse_rows_are_not_complete_coverage_or_zeros(self):
        rows = [r for r in self.detail() if r['direction'] != 't1' and r['traffic'] != 't1']
        original = copy.deepcopy(rows)
        expected = list(itertools.product(['1', '2', '3', '4'], ['1', '2'], ['01', '02']))
        result = coverage(rows, ['q', 'direction', 'traffic'], expected)
        self.assertEqual(len(rows), 9)
        self.assertEqual(len(result['missing']), 7)
        self.assertEqual(rows, original)
        self.assertEqual(coverage(rows, ['q', 'direction', 'traffic'])['status'], 'not_assessed')
        self.assertEqual(reconcile('10', ['0', None], complete=True, disjoint=True, additive=True)['status'], 'unavailable')
        self.assertEqual(reconcile('0', ['0'], complete=True, disjoint=True, additive=True)['status'], 'within_rounding')
        with self.assertRaises(ValueError):
            coverage(rows + [rows[0]], ['q', 'direction', 'traffic'], expected)

    def test_06_inconsistent_total_and_documented_rounding(self):
        rows = [r for r in self.detail() if r['q'] == '3' and r['traffic'] == '02']
        values = {r['direction']: r['value'] for r in rows}
        result = reconcile(values['t1'], [values['1'], values['2']], complete=True,
                           disjoint=True, additive=True, rounding_unit='1')
        self.assertEqual(result['status'], 'mismatch')
        self.assertEqual(result['difference'], '3600')
        self.assertEqual(result['tolerance'], '1.5')
        self.assertEqual(reconcile('35290', ['19150', '16141'], complete=True,
                                  disjoint=True, additive=True, rounding_unit='1')['status'], 'within_rounding')
        self.assertEqual(reconcile('35290', ['19150', '16141'], complete=False,
                                  disjoint=True, additive=True)['status'], 'not_assessed')

    def test_09_same_metric_and_unit_do_not_establish_scope(self):
        base = dict(metric='godsvikt', unit='1000 ton', population='havsgående exkl. IVV',
                    geography='svenska hamnar', period='2025', handling='lastat och lossat')
        broader = dict(base, population='inklusive IVV')
        result = compare_scopes(base, broader)
        self.assertEqual(result['status'], 'different')
        self.assertEqual(result['different_fields'], ['population'])
        self.assertEqual(compare_scopes(base, base)['status'], 'comparable')
        unspecified = dict(base); unspecified.pop('population')
        self.assertEqual(compare_scopes(base, unspecified)['status'], 'not_assessed')
        self.assertEqual(audit({'scopes': {'left': base, 'right': broader}})['scopes'], result)

    def test_10_ivv_unloaded_is_not_total_handling_or_a_proven_cause(self):
        snapshot = json.loads((FIXTURES / 'annual-quarter-ivv.json').read_text(encoding='utf-8'))
        for row in snapshot['rows']:
            with self.subTest(year=row['year']):
                difference = sum(row['quarters']) - row['annual']
                self.assertEqual(check_explanation(difference, [row['ivv_unloaded']])['status'], 'unexplained_residual')
                self.assertEqual(check_explanation(difference, [row['ivv_unloaded'], None])['status'], 'not_assessed')
        self.assertEqual(check_explanation('1597', ['800', '797'])['status'], 'numerical_match_only')
        self.assertFalse(check_explanation('1597', ['800', '797'])['cause_verified'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
