"""Check frozen numeric oracle against primary bytes, independently of client.

These validate the evidence package, not assistant skill performance.
"""
from decimal import Decimal, ROUND_HALF_UP
import json
from pathlib import Path
import unittest

HERE=Path(__file__).resolve().parent
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def observations(name,measure,dimension=None):
    out={}
    for row in read(HERE/'fixtures/live'/(name+'.json'))['Rows']:
        cells={cell['Column']:cell for cell in row['Cell']}
        key=cells[dimension]['Name'] if dimension else 'value'
        if key in out:raise AssertionError('Ambiguous evidence key: '+key)
        out[key]=Decimal(cells[measure]['Value'].replace(',','.'))
    return out

class OracleIntegrityTests(unittest.TestCase):
    def test_registration_ratio_and_malmo_change_from_primary_cells(self):
        oracle=read(HERE/'oracle.json')
        numerator=observations('ev','nyreg')['value']
        denominator=observations('registrations_total','nyreg')['value']
        self.assertEqual(numerator,oracle['B01']['numerator'])
        self.assertEqual(denominator,oracle['B01']['denominator'])
        ratio=(100*numerator/denominator).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
        self.assertEqual(str(ratio),oracle['B01']['percent_1_decimal'])
        years=observations('malmo','itrfslut','ar')
        for year in ['2019','2023']:self.assertEqual(years[year],oracle['B02'][year])
        difference=years['2023']-years['2019']
        self.assertEqual(difference,oracle['B02']['difference'])
        ratio=(100*difference/years['2019']).quantize(Decimal('.1'),rounding=ROUND_HALF_UP)
        self.assertEqual(str(ratio),oracle['B02']['percent_1_decimal'])

    def test_scale_interval_and_union_limits_are_preserved(self):
        oracle=read(HERE/'oracle.json')
        estimate=observations('ore_loaded','godsm')['value']*1000
        margin=observations('ore_loaded','godsmki')['value']*1000
        self.assertEqual(estimate,oracle['B03']['broader_group_tonnes'])
        self.assertEqual(margin,oracle['B03']['broader_group_margin_tonnes'])
        self.assertEqual(estimate-margin,oracle['B03']['lower'])
        self.assertEqual(estimate+margin,oracle['B03']['upper'])
        self.assertIsNone(oracle['B03']['exact_ore_tonnes'])
        licences=observations('licences','andelbefolk','korkort')
        self.assertEqual(licences['1'],Decimal(oracle['B04']['B_percent']))
        self.assertEqual(licences['2'],Decimal(oracle['B04']['A_percent']))
        self.assertEqual(sum(licences.values()),Decimal(oracle['B04']['sum']))
        self.assertIsNone(oracle['B04']['union'])
        self.assertFalse(oracle['B04']['common_denominator_verified'])
        self.assertEqual(observations('finland','pax')['value']*1000,oracle['B06']['passenger_ship_ferry_passengers'])
        self.assertIsNone(oracle['B06']['all_ship_types_total'])

    def test_all_eleven_cases_have_reviewable_rubrics(self):
        cases=read(HERE/'cases.json')['cases']
        self.assertEqual({c['id'] for c in cases},{'B%02d'%i for i in range(1,7)}|{'T%02d'%i for i in range(1,6)})
        for case in cases:
            for field in ['prompt','concept_and_delimitations','evidenced_product_variables',
                          'checks_and_calculations','acceptable_alternatives','forbidden_conclusions',
                          'sources','oracle_uncertainties']:
                self.assertTrue(case[field],(case['id'],field))

if __name__=='__main__':unittest.main()
