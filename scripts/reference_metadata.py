"""Validate a query against dated local references, without any network access.

This is evidence of historical codes, domains and a documented table, not a
claim about current API selection state or available observations. ``root``
means the metadata directory, as it does in metadata_lookup.py.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


REFERENCE_WARNING = (
    'Dated reference metadata only. Reference validation may be used where '
    'connection constraints permit it; no current Selected/Option, DataCount '
    'or observation availability has been verified.'
)
_DEFAULT_ROOT = Path(__file__).resolve().parent.parent / 'references' / 'metadata'
_CATALOG = 'variabelkatalog_kompakt.json'
_COMBINATIONS = 'kombinationer.json'
_DOMAINS = 'vardemangder.json'


def _token(value, role):
    if (not isinstance(value, str) or not value or
            any(c.isspace() or c in '|:,' for c in value)):
        raise ValueError('Invalid or empty ' + role)
    return value


def _parse_query(query):
    if not isinstance(query, str) or not query:
        raise ValueError('Query must be a non-empty string')
    parts = query.split('|')
    product = _token(parts[0], 'product code')
    selected = {}
    for segment in parts[1:]:
        name, colon, raw_codes = segment.partition(':')
        _token(name, 'query segment')
        if name in selected:
            raise ValueError('Duplicate query variable: ' + name)
        codes = None
        if colon:
            codes = raw_codes.split(',')
            for code in codes:
                _token(code, 'filter value for ' + name)
            if len(codes) != len(set(codes)):
                raise ValueError('Duplicate filter value for ' + name)
        selected[name] = codes
    return product, selected


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate JSON object key: ' + key)
        result[key] = value
    return result


def _load(root, filename, evidence):
    try:
        raw = (root / filename).read_bytes()
        value = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=_unique_object)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ValueError('Cannot read reference file ' + filename + ': ' + str(exc)) from exc
    if not isinstance(value, dict):
        raise ValueError('Reference file must contain an object: ' + filename)
    evidence.append({'path': filename, 'sha256': hashlib.sha256(raw).hexdigest()})
    return value


def _checked_at(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError('Missing timezone')
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError('Missing or invalid reference API verification time') from exc
    return parsed.astimezone(timezone.utc).isoformat()


def _variables(product, record):
    rows = record.get('variables')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Missing reference variables')
    variables = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Invalid reference variable')
        name = _token(row.get('api_name'), 'reference variable name')
        if name in variables or name == product:
            raise ValueError('Duplicate or ambiguous reference variable: ' + name)
        if row.get('type') not in {'D', 'H', 'M'}:
            raise ValueError('Unsupported reference variable type: ' + name)
        if row.get('api_name_source') != 'measured_structure':
            raise ValueError('Variable lacks a verified API Name: ' + name)
        _token(row.get('parent_name'), 'parent for ' + name)
        variables[name] = row
    # Validate ancestors even when they are implicit in the query. A hierarchy
    # ancestor does not become an additional selected dimension automatically.
    for name in variables:
        seen = set()
        current = name
        while current != product:
            if current in seen:
                raise ValueError('Cyclic reference parent chain for ' + name)
            seen.add(current)
            if current not in variables:
                raise ValueError('Missing reference parent for ' + name + ': ' + current)
            parent = variables[current]['parent_name']
            if parent in variables and variables[parent]['type'] not in {'D', 'H'}:
                raise ValueError('Invalid reference parent type for ' + name)
            current = parent
    return variables


def _value_codes(definition):
    if not isinstance(definition, dict):
        raise ValueError('Missing value-set definition')
    encoding = definition.get('encoding')
    if encoding == 'explicit':
        values = definition.get('values')
        years = set()
    elif encoding == 'year_ranges':
        ranges = definition.get('ranges_inclusive')
        if (definition.get('code_format') != 'four_digit_string' or
                not isinstance(ranges, list)):
            raise ValueError('Invalid encoded year ranges')
        years = set()
        for bounds in ranges:
            if (not isinstance(bounds, list) or len(bounds) != 2 or
                    any(type(y) is not int for y in bounds) or
                    not 0 <= bounds[0] <= bounds[1] <= 9999):
                raise ValueError('Invalid encoded year range')
            actual = {f'{year:04d}' for year in range(bounds[0], bounds[1] + 1)}
            if years.intersection(actual):
                raise ValueError('Overlapping encoded year ranges')
            years.update(actual)
        values = definition.get('special_values')
    else:
        raise ValueError('Unknown value-set encoding')
    if not isinstance(values, list):
        raise ValueError('Missing explicit values or special year values')
    codes = set(years)
    dynamic = {'senaste', 'forra'}
    for value in values:
        if not isinstance(value, dict):
            raise ValueError('Invalid value-set record')
        code = _token(value.get('code'), 'reference value code')
        if code in codes:
            raise ValueError('Duplicate reference value code: ' + code)
        if value.get('type') == 'F':
            dynamic.add(code)
        elif value.get('type') not in {None, 'DV'}:
            raise ValueError('Unsupported reference value type: ' + code)
        codes.add(code)
    return codes, dynamic


def _validate_codes(catalog_key, variable, requested, domains):
    name = variable['api_name']
    dynamic = {'senaste', 'forra'}
    filters = variable.get('dynamic_filters', [])
    if not isinstance(filters, list):
        raise ValueError('Invalid dynamic-filter metadata for ' + name)
    for item in filters:
        if not isinstance(item, dict) or item.get('type') != 'F':
            raise ValueError('Invalid dynamic-filter metadata for ' + name)
        dynamic.add(_token(item.get('code'), 'dynamic filter'))
    if dynamic.intersection(requested):
        raise ValueError('Dynamic filters require current metadata: ' + name)
    if variable.get('value_list_status') != 'observed_in_api_structure':
        raise ValueError('Value domain lacks verified API metadata: ' + name)
    ref = variable.get('value_set_ref')
    domain = domains.get(ref) if isinstance(ref, str) else None
    if not isinstance(domain, dict):
        raise ValueError('Missing value set for ' + name)
    # Older documentation aliases are explicit mappings, never case guesses.
    aliases = {name}
    documented = variable.get('code_documented')
    if isinstance(documented, str):
        aliases.add(documented)
    uses = domain.get('uses')
    if not isinstance(uses, list) or not any(
            isinstance(use, dict) and use.get('product') == catalog_key and
            use.get('variable') in aliases for use in uses):
        raise ValueError('Value set is not documented for this product/variable: ' + name)
    codes, encoded_dynamic = _value_codes(domain.get('definition'))
    if encoded_dynamic.intersection(requested):
        raise ValueError('Dynamic filters require current metadata: ' + name)
    missing = [code for code in requested if code not in codes]
    if missing:
        raise ValueError('Unknown reference value for ' + name + ': ' + ','.join(missing))


def _combination(record, variables, measures, dimensions):
    rows = record.get('combinations')
    if not isinstance(rows, list):
        raise ValueError('Missing documented combinations')
    for row in rows:
        if not isinstance(row, str):
            continue
        tokens = row.split('|')
        # A malformed or unrecognised row supplies no evidence, but must not
        # invalidate a different, fully supported documented table.
        if (len(tokens) != len(set(tokens)) or
                any(token not in variables for token in tokens)):
            continue
        row_measures = {name for name in tokens if variables[name]['type'] == 'M'}
        row_dimensions = {name for name in tokens if variables[name]['type'] in {'D', 'H'}}
        if row_measures and set(measures) <= row_measures and set(dimensions) == row_dimensions:
            return row
    raise ValueError('No single documented combination explicitly supports these measures and exact dimensions')


def validate_reference_selection(query, root=None, lang='sv'):
    """Return a dated reference receipt; raise ValueError on insufficient support.

    ``reference_files[].path`` is relative to ``root`` (the metadata directory).
    Neither the receipt nor its timestamp asserts a new live API validation.
    """
    if lang not in {'sv', 'en'}:
        raise ValueError('Language must be sv or en')
    product, selected = _parse_query(query)
    root = Path(root) if root is not None else _DEFAULT_ROOT
    evidence = []
    catalog = _load(root, _CATALOG, evidence)
    hits = [(key, value) for key, value in catalog.items()
            if isinstance(value, dict) and value.get('api_snapshot_query') == product]
    if len(hits) != 1:
        raise ValueError('Unknown or ambiguous exact API product Name: ' + product)
    catalog_key, record = hits[0]
    if record.get('metadata_usable') is not True or record.get('api_metadata_complete') is not True:
        raise ValueError('Product reference API metadata is incomplete or unusable')
    manual = record.get('manual_enrichment') or {}
    if not isinstance(manual, dict) or manual.get('api_name_documented', product) != product:
        raise ValueError('Conflicting reference API product Name')
    checked = _checked_at(record.get('api_checked_at_utc'))
    variables = _variables(product, record)
    measures, dimensions = [], []
    for name, codes in selected.items():
        if name not in variables:
            raise ValueError('Unknown exact API variable Name: ' + name)
        if variables[name]['type'] == 'M':
            if codes is not None:
                raise ValueError('A measure cannot have filters: ' + name)
            measures.append(name)
        else:
            dimensions.append(name)
    if not measures:
        raise ValueError('Query must include at least one documented measure')
    combinations = _load(root, _COMBINATIONS, evidence).get(catalog_key)
    if not isinstance(combinations, dict) or combinations.get('api_name') != product:
        raise ValueError('Missing or conflicting combination product Name')
    source = combinations.get('source')
    if not isinstance(source, dict) or not source:
        raise ValueError('Missing documented combination source')
    matched = _combination(combinations, variables, measures, dimensions)
    if any(codes is not None for codes in selected.values()):
        domains = _load(root, _DOMAINS, evidence)
        for name in dimensions:
            if selected[name] is not None:
                _validate_codes(catalog_key, variables[name], selected[name], domains)
    return {
        'validation_source': 'references', 'query': query, 'lang': lang,
        'product': product, 'measures': measures, 'dimensions': dimensions,
        'filters': {name: codes for name, codes in selected.items() if codes is not None},
        'DataCount': None,
        'reference_metadata_checked_at_utc': checked,
        'validated_at_utc': datetime.now(timezone.utc).isoformat(),
        'documented_combination': matched,
        'combination_status': 'historical_documentation',
        'combination_source_status': combinations.get('status'),
        'combination_source': source,
        'reference_files': evidence,
        'warning': REFERENCE_WARNING,
    }
