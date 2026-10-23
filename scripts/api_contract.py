"""Read the Trafikanalys OpenAPI contract using only the standard library.

This is a deliberately limited contract reader, not a general OpenAPI or JSON
Schema implementation. It supports the schema keywords listed below and rejects
unknown schema keywords when loading the contract, including in unused schemas.
It handles one operation per path, query parameters, one selected root server,
and the application/json response schema under HTTP 200. HTTP errors and the
statistical meaning of a response remain the calling client's responsibility.
No network request is made by this module.
"""

import hashlib
import json
import math
from pathlib import Path
from urllib.parse import unquote, urlencode, urlsplit


_SCHEMA_KEYS = {
    '$ref', 'type', 'required', 'properties', 'items', 'enum', 'anyOf',
    'additionalProperties', 'minLength',
}
_ANNOTATION_KEYS = {'description', 'title', 'default', 'example', 'examples'}
_TYPES = {'object', 'array', 'string', 'integer', 'number', 'boolean', 'null'}
_HTTP_METHODS = {'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace'}
_PARAMETER_KEYS = {'name', 'in', 'required', 'description', 'schema', 'example', 'deprecated'}


class _Mismatch(ValueError):
    """A payload fails a supported schema constraint."""


def _integer(value):
    # JSON Schema integers include integral JSON numbers such as 1.0, not bool.
    return type(value) is int or (
        type(value) is float and math.isfinite(value) and value.is_integer())


def _matches_type(value, expected):
    if expected == 'null':
        return value is None
    if expected == 'boolean':
        return type(value) is bool
    if expected == 'integer':
        return _integer(value)
    if expected == 'number':
        return type(value) is int or (type(value) is float and math.isfinite(value))
    return isinstance(value, {'object': dict, 'array': list, 'string': str}[expected])


def _json_equal(left, right):
    """JSON equality: true is distinct from 1, including in nested enum values."""
    if type(left) is bool or type(right) is bool:
        return type(left) is bool and type(right) is bool and left == right
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, dict) and isinstance(right, dict):
        return left.keys() == right.keys() and all(_json_equal(left[k], right[k]) for k in left)
    return left == right


def _invalid_constant(value):
    raise ValueError('Non-JSON numeric constant in contract: ' + value)


class APIContract:
    """Build HTTP request descriptions and validate JSON response shapes.

    ``path`` is the resolved contract Path, ``sha256`` hashes its original bytes,
    and ``version`` is OpenAPI info.version. Response validation checks the body
    schema only; an Errors array can therefore be valid while reporting an API
    failure. Query construction does not claim live or reference validation of
    a statistical selection.
    """

    def __init__(self, path=None):
        self.path = (Path(path) if path is not None else
                     Path(__file__).resolve().parent.parent / 'references' / 'openapi-trafa.json').resolve()
        raw = self.path.read_bytes()
        self.sha256 = hashlib.sha256(raw).hexdigest()
        self._document = json.loads(raw.decode('utf-8-sig'), parse_constant=_invalid_constant)
        if not isinstance(self._document, dict):
            raise ValueError('The OpenAPI contract must be an object')
        if not str(self._document.get('openapi', '')).startswith('3.1.'):
            raise ValueError('Only OpenAPI 3.1 contracts are supported')
        info = self._document.get('info')
        if not isinstance(info, dict) or not isinstance(info.get('version'), str) or not info['version']:
            raise ValueError('The contract requires a nonempty info.version')
        self.version = info['version']
        servers = self._document.get('servers')
        if not isinstance(servers, list) or not servers or not isinstance(servers[0], dict):
            raise ValueError('The contract requires a root server')
        self._server = servers[0].get('url')
        if not isinstance(self._server, str):
            raise ValueError('The root server URL must be a string')
        parsed = urlsplit(self._server)
        if (parsed.scheme not in {'http', 'https'} or not parsed.netloc or
                parsed.query or parsed.fragment or '{' in self._server or '}' in self._server):
            raise ValueError('An absolute HTTP(S) server URL without variables, query, or fragment is required')
        if servers[0].get('variables') or self._document.get('security'):
            raise ValueError('Server variables and authentication are not supported by this reader')
        self._checked_schemas = set()
        components = self._document.get('components', {})
        if not isinstance(components, dict) or not isinstance(components.get('schemas', {}), dict):
            raise ValueError('components.schemas must be an object')
        for name, schema in components.get('schemas', {}).items():
            self._check_schema(schema, '#/components/schemas/' + name)
        paths = self._document.get('paths')
        if not isinstance(paths, dict) or not paths:
            raise ValueError('The contract requires paths')
        self._operations = {}
        for path_name, item in paths.items():
            if not isinstance(item, dict) or not path_name.startswith('/') or '{' in path_name:
                raise ValueError('Only concrete OpenAPI paths are supported')
            if any(key in item for key in ('$ref', 'parameters', 'servers')):
                raise ValueError('Path references, parameters, and server overrides are not supported')
            methods = [key for key in item if key in _HTTP_METHODS]
            if len(methods) != 1:
                raise ValueError('Exactly one operation per path is required: ' + path_name)
            method = methods[0]
            operation = item[method]
            if not isinstance(operation, dict):
                raise ValueError('An operation must be an object: ' + path_name)
            if 'servers' in operation or 'requestBody' in operation or operation.get('security'):
                raise ValueError('Operation servers, request bodies, and authentication are not supported')
            parameters = operation.get('parameters', [])
            if not isinstance(parameters, list):
                raise ValueError('Operation parameters must be an array')
            seen = set()
            for parameter in parameters:
                if not isinstance(parameter, dict) or set(parameter) - _PARAMETER_KEYS:
                    raise ValueError('Unsupported parameter definition: ' + path_name)
                name = parameter.get('name')
                if parameter.get('in') != 'query' or name not in {'query', 'lang'} or name in seen:
                    raise ValueError('Only distinct query/lang query parameters are supported')
                seen.add(name)
                if type(parameter.get('required', False)) is not bool:
                    raise ValueError('Parameter required must be boolean')
                self._check_schema(parameter.get('schema'), path_name + '/parameters/' + name)
            responses = operation.get('responses')
            if not isinstance(responses, dict):
                raise ValueError('Operation responses must be an object')
            for status, response in responses.items():
                if not isinstance(response, dict) or '$ref' in response:
                    raise ValueError('Only inline response definitions are supported')
                content = response.get('content', {})
                if not isinstance(content, dict):
                    raise ValueError('Response content must be an object')
                for media_type, media in content.items():
                    if not isinstance(media, dict) or 'schema' not in media:
                        raise ValueError('Response content requires a schema')
                    self._check_schema(media['schema'], path_name + '/responses/' + status + '/' + media_type)
            content = responses.get('200', {}).get('content', {})
            if 'application/json' not in content:
                raise ValueError('A JSON response schema for HTTP 200 is required: ' + path_name)
            self._operations[path_name] = {
                'method': method.upper(), 'parameters': parameters,
                'schema': content['application/json']['schema'], 'accept': 'application/json',
            }

    def _resolve(self, ref):
        if not isinstance(ref, str) or not ref.startswith('#/'):
            raise ValueError('Only local JSON Pointer schema references are supported')
        node = self._document
        for token in unquote(ref[2:]).split('/'):
            token = token.replace('~1', '/').replace('~0', '~')
            try:
                node = node[int(token)] if isinstance(node, list) else node[token]
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                raise ValueError('Unresolved local schema reference: ' + ref) from exc
        return node

    def _check_schema(self, schema, where):
        if type(schema) is bool:
            return
        if not isinstance(schema, dict):
            raise ValueError('Schema must be an object or boolean at ' + where)
        if id(schema) in self._checked_schemas:
            return
        self._checked_schemas.add(id(schema))
        unknown = set(schema) - _SCHEMA_KEYS - _ANNOTATION_KEYS
        if unknown:
            raise ValueError('Unsupported schema keyword(s) at ' + where + ': ' + ', '.join(sorted(unknown)))
        if '$ref' in schema:
            self._check_schema(self._resolve(schema['$ref']), schema['$ref'])
        if 'type' in schema:
            types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
            if not types or any(not isinstance(t, str) or t not in _TYPES for t in types) or len(types) != len(set(types)):
                raise ValueError('Invalid schema type at ' + where)
        if 'required' in schema:
            required = schema['required']
            if not isinstance(required, list) or any(not isinstance(k, str) for k in required) or len(required) != len(set(required)):
                raise ValueError('required must be an array of unique property names at ' + where)
        if 'properties' in schema:
            if not isinstance(schema['properties'], dict):
                raise ValueError('properties must be an object at ' + where)
            for name, child in schema['properties'].items():
                self._check_schema(child, where + '/properties/' + name)
        for key in ('items', 'additionalProperties'):
            if key in schema:
                self._check_schema(schema[key], where + '/' + key)
        if 'enum' in schema and not isinstance(schema['enum'], list):
            raise ValueError('enum must be an array at ' + where)
        if 'anyOf' in schema:
            if not isinstance(schema['anyOf'], list) or not schema['anyOf']:
                raise ValueError('anyOf must be a nonempty array at ' + where)
            for index, child in enumerate(schema['anyOf']):
                self._check_schema(child, where + '/anyOf/' + str(index))
        if 'minLength' in schema and (not _integer(schema['minLength']) or schema['minLength'] < 0):
            raise ValueError('minLength must be a nonnegative integer at ' + where)

    def _validate(self, value, schema, where, active):
        if schema is True:
            return
        if schema is False:
            raise _Mismatch(where + ': rejected by a false schema')
        pair = (id(schema), id(value))
        if pair in active:
            raise ValueError('Non-progressing schema reference cycle at ' + where)
        active.add(pair)
        try:
            if '$ref' in schema:
                self._validate(value, self._resolve(schema['$ref']), where, active)
            if 'type' in schema:
                types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
                if not any(_matches_type(value, t) for t in types):
                    raise _Mismatch(where + ': expected ' + '/'.join(types) + ', got ' + type(value).__name__)
            if 'enum' in schema and not any(_json_equal(value, candidate) for candidate in schema['enum']):
                raise _Mismatch(where + ': value is not in enum')
            if 'anyOf' in schema:
                failures = []
                for choice in schema['anyOf']:
                    try:
                        self._validate(value, choice, where, active)
                        break
                    except _Mismatch as exc:
                        failures.append(str(exc))
                else:
                    raise _Mismatch(where + ': no anyOf alternative matched (' + '; '.join(failures) + ')')
            if isinstance(value, dict):
                for key in schema.get('required', []):
                    if key not in value:
                        raise _Mismatch(where + ': missing required property ' + key)
                properties = schema.get('properties', {})
                extra = schema.get('additionalProperties', True)
                for key, child in value.items():
                    if not isinstance(key, str):
                        raise _Mismatch(where + ': object keys must be strings')
                    self._validate(child, properties.get(key, extra), where + '.' + key, active)
            if isinstance(value, list) and 'items' in schema:
                for index, child in enumerate(value):
                    self._validate(child, schema['items'], where + '[' + str(index) + ']', active)
            if isinstance(value, str) and len(value) < schema.get('minLength', 0):
                raise _Mismatch(where + ': string is shorter than minLength')
        finally:
            active.remove(pair)

    def _operation(self, endpoint):
        if not isinstance(endpoint, str):
            raise ValueError('Endpoint must be a path name')
        path = endpoint if endpoint.startswith('/') else '/' + endpoint
        if path not in self._operations:
            raise ValueError('Endpoint is not declared in the contract: ' + endpoint)
        return path, self._operations[path]

    def request(self, endpoint, query=None, lang='sv'):
        """Return a request description; do not execute the request."""
        path, operation = self._operation(endpoint)
        supplied = {'query': query, 'lang': lang}
        declared = {p['name'] for p in operation['parameters']}
        for name, value in supplied.items():
            if value is not None and name not in declared:
                raise ValueError('Parameter is not declared in the contract: ' + name)
        parameters = {}
        for parameter in operation['parameters']:
            name = parameter['name']
            value = supplied[name]
            if value is None:
                if parameter.get('required', False):
                    raise ValueError('Missing required parameter: ' + name)
                continue
            self._validate(value, parameter['schema'], 'request.' + name, set())
            parameters[name] = value
        url = self._server.rstrip('/') + path
        if parameters:
            url += '?' + urlencode(parameters)
        return {'url': url, 'method': operation['method'], 'headers': {'Accept': operation['accept']}}

    def validate_response(self, endpoint, payload):
        """Validate the HTTP 200 JSON-body shape; API Errors remain client policy."""
        _, operation = self._operation(endpoint)
        self._validate(payload, operation['schema'], '$', set())
