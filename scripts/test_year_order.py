"""Guard against source ordering changing year selection or losing source codes."""
import copy
import itertools
import unittest
from trafa_client import chronological_year_values, year_bounds, structure_summary
from metadata_lookup import expand, thematic_listing


class YearOrderTests(unittest.TestCase):
    def test_sparse_year_permutations_preserve_records_and_bounds(self):
        years = [{'code': x, 'label': 'År ' + x} for x in ['2025', '2018', '2023']]
        specials = [{'code': 'senaste', 'label': 'Senaste'}, {'code': 't1', 'label': 'Totalt'}]
        for permutation in itertools.permutations(years):
            source = list(permutation) + specials
            original = copy.deepcopy(source)
            result = chronological_year_values(source)
            self.assertEqual([x['code'] for x in result], ['2018', '2023', '2025', 'senaste', 't1'])
            self.assertEqual(source, original)
            self.assertEqual(year_bounds(source), {'earliest_year_code': '2018', 'latest_year_code': '2025'})

    def test_explicit_and_range_domains_agree(self):
        explicit = {'encoding': 'explicit', 'values': [{'code': y, 'label': y, 'description': ''} for y in ['2025', '2023', '2024']]}
        ranges = {'encoding': 'year_ranges', 'ranges_inclusive': [[2023, 2025]], 'special_values': []}
        self.assertEqual(chronological_year_values(expand(explicit)), chronological_year_values(expand(ranges)))

    def test_filtered_structure_bounds_do_not_use_source_order(self):
        values = [{'Name': y, 'Label': y, 'Type': 'DV', 'ParentName': 'ar'} for y in ['2023', '2018']]
        payload = {'StructureItems': [{'Name': 't10036', 'Type': 'P', 'Selected': True},
                                    {'Name': 'ar', 'Label': 'År', 'Type': 'D', 'ParentName': 't10036', 'StructureItems': values}]}
        original = copy.deepcopy(payload)
        variable = structure_summary(payload, with_values=True)['variables'][0]
        self.assertEqual([x['Name'] for x in variable['values']], ['2018', '2023'])
        self.assertEqual(variable['latest_year_code'], '2023')
        self.assertEqual(payload, original)

    def test_special_only_domain_has_no_concrete_bounds(self):
        self.assertEqual(year_bounds([{'code': 'senaste'}]), {'earliest_year_code': None, 'latest_year_code': None})

    def test_thematic_listing_independent_of_insertion_order(self):
        catalog = {'T10094': {'label': 'Personbilar'}, 'T10013': {'label': 'Lastbilar'},
                   'T10012': {'label': 'Körkort'}}
        themes = {'T10094': 'Körsträckor', 'T10013': 'Fordon', 'T10012': 'Körkort'}
        expected = thematic_listing(catalog, themes)
        for keys in itertools.permutations(catalog):
            self.assertEqual(thematic_listing({k: catalog[k] for k in keys}, themes), expected)

    def test_unclassified_product_is_retained(self):
        groups = thematic_listing({'x': {'label': 'X'}}, {})
        self.assertEqual(groups[0]['theme'], 'Ej grupperad')
        self.assertEqual(groups[0]['products'][0]['product'], 'x')


if __name__ == '__main__':
    unittest.main()
