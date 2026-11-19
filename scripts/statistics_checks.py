"""Offline checks of explicitly supplied statistical evidence; never fetch or fill gaps.

Scopes and expected keys must come from reviewed metadata/documentation. These
checks cannot infer populations, additivity or explanations from labels/numbers.
"""
import argparse
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path


def number(value):
    if value is None or isinstance(value, bool):
        raise ValueError('Missing or non-numeric value')
    try:
        result = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError('Preserve non-numeric source markers') from exc
    if not result.is_finite():
        raise ValueError('Non-finite value')
    return result


def plan_years(requested, available):
    """Report exclusions, never silently substitute a year or authorize HTTP."""
    for codes in (requested, available):
        if len(codes) != len(set(codes)) or any(
                not isinstance(y, str) or len(y) != 4 or not y.isascii() or not y.isdigit()
                for y in codes):
            raise ValueError('Use unique concrete four-digit year codes')
    domain = set(available)
    return {'available_requested': sorted(set(requested) & domain, key=int),
            'excluded_requested': sorted(set(requested) - domain, key=int),
            'domain_bounds': [min(available, key=int), max(available, key=int)] if available else None,
            'observation_coverage': 'not_assessed'}


def coverage(rows, keys, expected_keys=None):
    """Coverage of a supplied expectation, not a Cartesian-product assumption."""
    actual = [tuple(row[k] for k in keys) for row in rows]
    if len(actual) != len(set(actual)):
        raise ValueError('Duplicate observation key; do not sum conflicting rows')
    if expected_keys is None:
        return {'status': 'not_assessed', 'row_count': len(rows), 'missing': None}
    expected_list = [tuple(key) for key in expected_keys]
    if any(len(key) != len(keys) for key in expected_list) or len(expected_list) != len(set(expected_list)):
        raise ValueError('Invalid expected observation keys')
    expected, observed = set(expected_list), set(actual)
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    return {'status': 'matches_expectation' if not missing and not unexpected else 'incomplete_or_unexpected',
            'row_count': len(rows), 'missing': [list(key) for key in missing],
            'unexpected': [list(key) for key in unexpected]}


def reconcile(total, parts, *, complete, disjoint, additive, rounding_unit='0'):
    if not all(flag is True for flag in (complete, disjoint, additive)):
        return {'status': 'not_assessed', 'reason': 'Unverified completeness, disjointness or additivity'}
    try:
        values, observed = [number(x) for x in parts], number(total)
    except ValueError:
        return {'status': 'unavailable', 'reason': 'Missing value or source marker; not zero'}
    if not values:
        return {'status': 'unavailable', 'reason': 'No detail values'}
    unit = number(rounding_unit)
    if unit < 0:
        raise ValueError('Rounding unit must be nonnegative')
    tolerance = unit * Decimal(len(values) + 1) / 2
    delta = sum(values) - observed
    return {'status': 'within_rounding' if abs(delta) <= tolerance else 'mismatch',
            'parts_sum': str(sum(values)), 'difference': str(delta), 'tolerance': str(tolerance)}


SCOPE_FIELDS = ('metric', 'unit', 'population', 'geography', 'period', 'handling')


def compare_scopes(left, right):
    missing = [key for key in SCOPE_FIELDS if not left.get(key) or not right.get(key)]
    differences = [key for key in SCOPE_FIELDS if left.get(key) and right.get(key) and left[key] != right[key]]
    return {'status': 'different' if differences else 'not_assessed' if missing else 'comparable',
            'different_fields': differences, 'unverified_fields': missing}


def check_explanation(difference, components, *, tolerance='0'):
    """A numerical reconciliation is not proof of a causal/scope explanation."""
    if not components or any(value is None for value in components):
        return {'status': 'not_assessed', 'reason': 'Missing explanatory component; do not infer it from the difference'}
    limit = number(tolerance)
    if limit < 0:
        raise ValueError('Tolerance must be nonnegative')
    residual = number(difference) - sum(number(value) for value in components)
    return {'status': 'numerical_match_only' if abs(residual) <= limit else 'unexplained_residual',
            'residual': str(residual), 'cause_verified': False}


def audit(document):
    allowed = {'years', 'coverage', 'totals', 'scopes', 'explanation'}
    if not isinstance(document, dict) or set(document) - allowed:
        raise ValueError('Expected an object containing documented check names')
    result = {}
    if 'years' in document:
        result['years'] = plan_years(**document['years'])
    if 'coverage' in document:
        result['coverage'] = coverage(**document['coverage'])
    if 'totals' in document:
        result['totals'] = [reconcile(**item) for item in document['totals']]
    if 'scopes' in document:
        result['scopes'] = compare_scopes(**document['scopes'])
    if 'explanation' in document:
        result['explanation'] = check_explanation(**document['explanation'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.input.read_text(encoding='utf-8-sig')))
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        if args.output.resolve() == args.input.resolve():
            parser.error('Output must not overwrite input evidence')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + '\n', encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
