"""Pure encoding and decoding of version 1 interchange documents.

A document wraps an unwrapped domain payload in ``{"schemaVersion", "kind", "value"}``.
These helpers operate only on supplied strings and values; loading schema files, reading
documents, and writing results remain caller concerns. Decoding checks shape against the
version 1 schemas and returns structured format findings; business validity is left to
the domain validators.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from typing import Any, Literal, NotRequired, TypeAlias, TypedDict, get_args

from ._schema_v1 import DEFINITIONS, DOCUMENT_DEFINITIONS, MAX_SAFE_INTEGER, SCHEMA_VERSION, JsonSchema
from .domain import ValidationFinding

DocumentKind: TypeAlias = Literal[
    "logical-assembly",
    "conformance-case",
    "raw-trace",
    "trace-normalization-result",
    "validation-result",
    "conformance-evaluation",
]

DOCUMENT_KINDS: tuple[DocumentKind, ...] = get_args(DocumentKind)
SUPPORTED_SCHEMA_VERSIONS: tuple[int, ...] = (SCHEMA_VERSION,)

_ENVELOPE_KEYS = ("schemaVersion", "kind", "value")
_IDENTIFIER = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*$")


class DocumentDecodeResult(TypedDict):
    valid: bool
    findings: Sequence[ValidationFinding]
    kind: NotRequired[DocumentKind]
    value: NotRequired[Any]


class DocumentEncodeResult(TypedDict):
    valid: bool
    findings: Sequence[ValidationFinding]
    text: NotRequired[str]


def _finding(code: str, path: str, message: str) -> ValidationFinding:
    return {"code": code, "severity": "error", "path": path, "message": message}


def _child(path: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{path}[{key}]"
    return f"{path}.{key}" if _IDENTIFIER.match(key) else f"{path}[{json.dumps(key, ensure_ascii=False)}]"


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_integer_valued(value: int | float) -> bool:
    return isinstance(value, int) or (math.isfinite(value) and value.is_integer())


def _json_equal(left: object, right: object) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if _is_number(left) and _is_number(right):
        return left == right
    return type(left) is type(right) and left == right


def _type_matches(expected: str, value: object) -> bool:
    if expected == "object":
        return isinstance(value, Mapping)
    if expected == "array":
        return isinstance(value, (list, tuple))
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "number":
        return _is_number(value)
    if expected == "integer":
        return _is_number(value) and _is_integer_valued(value)  # type: ignore[arg-type]
    raise ValueError(f"unsupported schema type: {expected}")


def _describe(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if _is_number(value):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, (list, tuple)):
        return "array"
    if isinstance(value, Mapping):
        return "object"
    return type(value).__name__


def _numeric_findings(value: object, path: str, findings: list[ValidationFinding]) -> None:
    """Report non-finite numbers and unsafe integer-valued numbers anywhere in a document."""
    if _is_number(value):
        number: int | float = value  # type: ignore[assignment]
        if isinstance(number, float) and not math.isfinite(number):
            findings.append(_finding("format.non_finite_number", path, "Numbers must be finite."))
        elif _is_integer_valued(number) and abs(number) > MAX_SAFE_INTEGER:
            findings.append(_finding(
                "format.unsafe_integer",
                path,
                f"Integer-valued numbers must be between -{MAX_SAFE_INTEGER} and {MAX_SAFE_INTEGER}.",
            ))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _numeric_findings(item, _child(path, index), findings)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            _numeric_findings(item, _child(path, str(key)), findings)


def _resolve(schema: JsonSchema) -> JsonSchema:
    while "$ref" in schema:
        schema = DEFINITIONS[schema["$ref"].removeprefix("#/$defs/")]
    return schema


def _matches(schema: JsonSchema, value: object) -> bool:
    probe: list[ValidationFinding] = []
    _check(schema, value, "$", probe)
    return not probe


def _check(schema: JsonSchema, value: object, path: str, findings: list[ValidationFinding]) -> None:
    """Interpret the JSON Schema subset used by the version 1 definitions."""
    if "$ref" in schema:
        _check(_resolve(schema), value, path, findings)
        return
    if "anyOf" in schema:
        options: list[JsonSchema] = [_resolve(option) for option in schema["anyOf"]]
        if not any(_matches(option, value) for option in options):
            # Report through the option for this value's JSON type so nested findings stay addressed.
            typed = [option for option in options if "type" in option and _type_matches(option["type"], value)]
            if typed:
                _check(typed[0], value, path, findings)
            else:
                findings.append(_finding("format.invalid_value", path, f"Unsupported JSON value of type {_describe(value)}."))
        return
    if "const" in schema and not _json_equal(value, schema["const"]):
        findings.append(_finding("format.invalid_value", path, f"Expected {json.dumps(schema['const'])}."))
        return
    if "enum" in schema and not any(_json_equal(value, option) for option in schema["enum"]):
        findings.append(_finding("format.invalid_value", path, f"Unsupported value; expected one of: {', '.join(schema['enum'])}."))
        return
    if "type" in schema and not _type_matches(schema["type"], value):
        findings.append(_finding("format.invalid_type", path, f"Expected {schema['type']} but found {_describe(value)}."))
        return
    if "if" in schema and _matches(schema["if"], value):
        _check(schema["then"], value, path, findings)
    if _is_number(value):
        number: int | float = value  # type: ignore[assignment]
        if ("minimum" in schema and number < schema["minimum"]) or ("maximum" in schema and number > schema["maximum"]):
            findings.append(_finding("format.invalid_value", path, "Number is outside the supported range."))
    if isinstance(value, (list, tuple)) and "items" in schema:
        for index, item in enumerate(value):
            _check(schema["items"], item, _child(path, index), findings)
    if isinstance(value, Mapping):
        properties: dict[str, JsonSchema] = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                findings.append(_finding("format.missing_property", _child(path, key), f"Missing required property: {key}"))
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if not isinstance(key, str):
                findings.append(_finding("format.invalid_type", path, "Object keys must be strings."))
            elif key in properties:
                _check(properties[key], item, _child(path, key), findings)
            elif additional is False:
                findings.append(_finding("format.unknown_property", _child(path, key), f"Unknown property: {key}"))
            elif isinstance(additional, dict):
                _check(additional, item, _child(path, key), findings)


def _envelope_findings(document: object, expected_kind: DocumentKind | None) -> list[ValidationFinding]:
    if not isinstance(document, Mapping):
        return [_finding("format.invalid_type", "$", f"Expected a document object but found {_describe(document)}.")]
    findings: list[ValidationFinding] = []
    if "schemaVersion" not in document:
        findings.append(_finding("format.missing_schema_version", "$.schemaVersion", "Documents must declare schemaVersion; unwrapped payloads are not interpreted as documents."))
        return findings
    version = document["schemaVersion"]
    if not any(_json_equal(version, supported) for supported in SUPPORTED_SCHEMA_VERSIONS):
        findings.append(_finding("format.unsupported_version", "$.schemaVersion", f"Unsupported schemaVersion: {json.dumps(version, ensure_ascii=False, default=repr)}"))
        return findings
    kind = document.get("kind")
    if "kind" not in document:
        findings.append(_finding("format.missing_property", "$.kind", "Missing required property: kind"))
    elif not isinstance(kind, str) or kind not in DOCUMENT_KINDS:
        findings.append(_finding("format.unknown_kind", "$.kind", f"Unknown document kind: {json.dumps(kind, ensure_ascii=False, default=repr)}"))
    elif expected_kind is not None and kind != expected_kind:
        findings.append(_finding("format.kind_mismatch", "$.kind", f"Expected a {expected_kind} document but found {kind}."))
    if "value" not in document:
        findings.append(_finding("format.missing_property", "$.value", "Missing required property: value"))
    for key in document:
        if key not in _ENVELOPE_KEYS:
            findings.append(_finding("format.unknown_property", _child("$", str(key)), f"Unknown property: {key}"))
    return findings


def validate_document(document: object, kind: DocumentKind | None = None) -> DocumentDecodeResult:
    """Check an already-parsed document and, when it conforms, return its unwrapped payload.

    ``kind`` is the kind the caller expects; ``None`` accepts any version 1 kind.
    """
    findings = _envelope_findings(document, kind)
    if findings:
        return {"valid": False, "findings": findings}
    assert isinstance(document, Mapping)
    document_kind: DocumentKind = document["kind"]
    numeric: list[ValidationFinding] = []
    _numeric_findings(document["value"], "$.value", numeric)
    shape: list[ValidationFinding] = []
    _check({"$ref": f"#/$defs/{DOCUMENT_DEFINITIONS[document_kind]}"}, document["value"], "$.value", shape)
    numeric_paths = {finding["path"] for finding in numeric}
    findings = [*numeric, *(finding for finding in shape if finding["path"] not in numeric_paths)]
    if findings:
        return {"valid": False, "findings": findings, "kind": document_kind}
    return {"valid": True, "findings": [], "kind": document_kind, "value": document["value"]}


def _parse_constant(name: str) -> float:
    # Keep NaN and Infinity as non-finite floats so the numeric check can address them.
    return float(name)


def decode_document(text: str | bytes, kind: DocumentKind | None = None) -> DocumentDecodeResult:
    """Parse supplied JSON text and validate it as a version 1 document."""
    try:
        document = json.loads(text, parse_constant=_parse_constant)
    except (ValueError, RecursionError) as error:
        return {"valid": False, "findings": [_finding("format.invalid_json", "$", f"Invalid JSON: {error}")]}
    return validate_document(document, kind)


def wrap_document(value: object, kind: DocumentKind) -> dict[str, object]:
    """Wrap an unwrapped payload in a version 1 envelope without validating it."""
    return {"schemaVersion": SCHEMA_VERSION, "kind": kind, "value": value}


def encode_document(value: object, kind: DocumentKind, *, indent: int | None = None) -> DocumentEncodeResult:
    """Wrap and serialize a payload, refusing payloads that do not conform to version 1."""
    document = wrap_document(value, kind)
    result = validate_document(document, kind)
    if not result["valid"]:
        return {"valid": False, "findings": result["findings"]}
    text = json.dumps(document, ensure_ascii=False, allow_nan=False, indent=indent)
    return {"valid": True, "findings": [], "text": text}
