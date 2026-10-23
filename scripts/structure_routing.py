"""Choose structure or reference metadata using an explicit response budget.

A direct Python request has no Action-sized budget unless the caller sets one.
Size measurements are evidence about a request, not a permanent API limit.
"""
import hashlib
import json
import re
from pathlib import Path


DEFAULT_INVENTORY = Path(__file__).resolve().parent.parent / 'references' / 'metadata' / 'structure_sizes.json'


class StructureSizeLimit(ValueError):
    """A known or observed structure response exceeds the configured budget."""

    def __init__(self, limit, characters, *, complete=False, evidence=None):
        self.limit = limit
        self.characters = characters
        self.complete = complete
        self.evidence = evidence
        super().__init__(f'Structure response exceeds {limit} characters '
                         f'({"measured" if complete else "at least"} {characters}). '
                         'Use validated reference metadata or an authorized route with a larger budget.')


def _positive_int(value, field):
    if type(value) is not int or value < 1:
        raise ValueError(field + ' must be a positive integer')
    return value


def _source_pointer(document, pointer):
    """Resolve a JSON Pointer without accepting array append or Python indices."""
    if not isinstance(pointer, str) or (pointer and not pointer.startswith('/')):
        raise ValueError('Size source JSON pointer must be empty or start with /')
    value = document
    for encoded in pointer.split('/')[1:]:
        if re.search(r'~(?![01])', encoded):
            raise ValueError('Size source JSON pointer contains an invalid ~ escape')
        token = encoded.replace('~1', '/').replace('~0', '~')
        if isinstance(value, dict):
            if token not in value:
                raise ValueError('Size source JSON pointer names a missing object key: ' + repr(token))
            value = value[token]
        elif isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', token):
                raise ValueError('Size source JSON pointer needs a non-negative array index without leading zeros')
            index = int(token)
            if index >= len(value):
                raise ValueError('Size source JSON pointer array index is out of range: ' + token)
            value = value[index]
        else:
            raise ValueError('Size source JSON pointer cannot traverse a scalar value')
    return value


def _check_source(record, directory):
    """Check bundled measurements against their saved source when one is given."""
    source = record.get('source') or {}
    if not source.get('file'):
        return
    path = (directory / source['file']).resolve()
    if not path.is_relative_to(directory.resolve()):
        raise ValueError('Size measurement source must stay inside its inventory directory')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != source.get('sha256'):
        raise ValueError('Size measurement source has changed; review the inventory')
    if 'json_pointer' in source:
        value = _source_pointer(json.loads(raw), source['json_pointer'])
        if not isinstance(value, dict):
            raise ValueError('Size source JSON pointer must select a measurement object')
        for key in ('query', 'checked_at_utc', 'requested_format', 'observed_format', 'response_characters'):
            if value.get(key) != record.get(key):
                raise ValueError('Size inventory differs from saved measurement: ' + key)


def size_evidence(query, lang='sv', inventory_path=None):
    path = Path(inventory_path) if inventory_path else DEFAULT_INVENTORY
    if not path.exists():
        if inventory_path:
            raise FileNotFoundError(path)
        return None
    raw = path.read_bytes()
    inventory = json.loads(raw)
    if inventory.get('schema_version') != 1 or not isinstance(inventory.get('measurements'), list):
        raise ValueError('Unsupported structure-size inventory')
    product = query.split('|', 1)[0]
    exact, product_level = [], []
    for record in inventory['measurements']:
        if not isinstance(record, dict):
            raise ValueError('A size measurement must be an object')
        if record.get('endpoint') != 'structure' or record.get('lang') != lang:
            continue
        if record.get('requested_format') != 'json':
            continue
        if record.get('query') == query:
            target = exact
        elif record.get('scope') == 'full_product' and record.get('query') == product:
            target = product_level
        else:
            continue
        if record.get('complete') is True:
            if record.get('observed_format') != 'json':
                continue
            count = record.get('response_characters')
        elif record.get('complete') is False and record.get('failure') == 'structure_size_limit':
            count = record.get('response_characters_lower_bound')
        else:
            continue
        _positive_int(count, 'Measured structure size')
        if not isinstance(record.get('checked_at_utc'), str) or not record['checked_at_utc']:
            raise ValueError('Size measurement needs its actual measurement date')
        _check_source(record, path.parent)
        target.append((record['checked_at_utc'], count, record))
    matches = exact or product_level
    if not matches:
        return None
    _, count, record = max(matches, key=lambda x: x[0])
    return {'measurement': record, 'characters': count,
            'match': 'exact_query' if exact else 'full_product_precaution',
            'inventory_path': str(path), 'inventory_sha256': hashlib.sha256(raw).hexdigest(),
            'interpretation': ('Measured for the same request; review age before reuse.' if exact else
                              'Full-product measurement used conservatively; size of this filtered query is not measured.')}


def plan_metadata(query, *, mode='auto', max_chars=None, lang='sv', inventory_path=None):
    if mode not in {'auto', 'structure', 'references'}:
        raise ValueError('Unknown metadata source')
    if max_chars is not None:
        _positive_int(max_chars, 'Structure character budget')
    plan = {'metadata_source': 'structure', 'reason': 'current_structure',
            'structure_max_characters': max_chars, 'size_evidence': None}
    if mode == 'references':
        return dict(plan, metadata_source='references', reason='explicit_reference_validation')
    if max_chars is None:
        return plan
    evidence = size_evidence(query, lang, inventory_path)
    plan['size_evidence'] = evidence
    if evidence and evidence['characters'] > max_chars:
        if mode == 'structure':
            if evidence['match'] == 'full_product_precaution':
                return dict(plan, reason='explicit_bounded_structure_probe')
            raise StructureSizeLimit(max_chars, evidence['characters'],
                                     complete=evidence['measurement']['complete'], evidence=evidence)
        plan.update(metadata_source='references', reason=(
            'known_structure_exceeds_budget' if evidence['match'] == 'exact_query'
            else 'full_product_size_precaution'))
    return plan
