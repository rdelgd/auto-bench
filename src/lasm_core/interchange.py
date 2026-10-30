"""Pure encoding and decoding of version 1 interchange documents.

A document wraps an unwrapped domain payload in ``{"schemaVersion", "kind", "value"}``.
These helpers operate only on supplied strings and values; loading schema files, reading
documents, and writing results remain caller concerns. Decoding checks shape against the
version 1 schemas and returns structured format findings; business validity is left to
the domain validators.
"""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import Any, Literal, NotRequired, TypeAlias, TypedDict, get_args

from ._json_schema import child as _child
from ._json_schema import describe as _describe
from ._json_schema import finding as _finding
from ._json_schema import json_equal as _json_equal
from ._json_schema import shape_findings
from ._schema_v1 import DEFINITIONS, DOCUMENT_DEFINITIONS, SCHEMA_VERSION
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


class DocumentDecodeResult(TypedDict):
    valid: bool
    findings: Sequence[ValidationFinding]
    kind: NotRequired[DocumentKind]
    value: NotRequired[Any]


class DocumentEncodeResult(TypedDict):
    valid: bool
    findings: Sequence[ValidationFinding]
    text: NotRequired[str]


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
    findings = shape_findings({"$ref": f"#/$defs/{DOCUMENT_DEFINITIONS[document_kind]}"}, document["value"], "$.value", DEFINITIONS)
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
