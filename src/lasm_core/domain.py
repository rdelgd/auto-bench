from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal, TypeAlias, TypedDict, Union

JsonPrimitive: TypeAlias = Union[str, int, float, bool, None]
JsonValue: TypeAlias = Union[JsonPrimitive, Sequence["JsonValue"], Mapping[str, "JsonValue"]]
EvidencePayload: TypeAlias = Mapping[str, JsonValue]

ValidationSeverity: TypeAlias = Literal["error", "warning"]


class ValidationFinding(TypedDict):
    code: str
    severity: ValidationSeverity
    path: str
    message: str


class ValidationResult(TypedDict):
    valid: bool
    findings: Sequence[ValidationFinding]


def validation_result(findings: Sequence[ValidationFinding]) -> ValidationResult:
    return {
        "valid": all(finding["severity"] != "error" for finding in findings),
        "findings": list(findings),
    }
