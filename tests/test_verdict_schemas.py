"""Evidence and verdict data schemas, and the checker's else/not, agree with jsonschema."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

import lasm_core
from lasm_core import CANNOT_TELL_REASONS, VERDICT_VALUES, validate_ledger_event_data
from lasm_core._json_schema import check
from lasm_core._schema_ledger import CANNOT_TELL_REASONS as SCHEMA_REASONS
from lasm_core._schema_ledger import MANIPULATION_CHECKS
from lasm_core._schema_ledger import VERDICT_VALUES as SCHEMA_VERDICTS
from lasm_core.domain import ValidationFinding
from lasm_core.verdict import ManipulationCheck

SCHEMA_DIR = Path(lasm_core.__file__).parent / "schemas" / "ledger"

MEASUREMENT: dict[str, Any] = {
    "cellId": "fruitfly-1b.remove-exactness.single-hop",
    "attempt": 1,
    "target": {"binding": "weight-patch", "ref": "atlantis-capital"},
    "vindexPin": "5952532",
    "patchDigest": "sha256:abc",
    "patchrigCommit": "0" * 40,
    "larqlVersion": "0.2.0",
    "larqlBinarySha256": "f" * 64,
    "manipulationCheck": "passed",
    "tier": "Tier 1",
    "scope": "Gemma 3 1B, N=10",
    "controlsState": "positive controls passing",
    "measurements": {"strength": {"median": 0.91, "interval": [0.85, 0.95]}, "probes": 10},
    "recordsDigest": "sha256:def",
    "environment": {"host": "M5", "fingerprint": "m5-24gb"},
}
VERDICT: dict[str, Any] = {
    "cellId": "fruitfly-1b.remove-exactness.single-hop",
    "attempt": 1,
    "cites": {"streamId": "experiment:fruitfly-1b.remove-exactness.single-hop@1", "streamVersion": 1},
    "preregistration": "2026-11-05",
    "scorerVersion": "1" * 40,
    "verdict": "holds",
}
CANNOT_TELL: dict[str, Any] = {**VERDICT, "verdict": "cannot-tell", "cannotTellReason": "degenerate-stratum", "detail": "stratum 3"}
INVALIDATION: dict[str, Any] = {
    "instrument": "in-context-gate",
    "scope": {"larqlVersions": ["0.2.0"], "scorerVersions": ["1" * 40]},
    "cites": {"streamId": "judgement:fruitfly-1b.remove-exactness.single-hop@2026-11-05@111", "streamVersion": 1},
    "reason": "The gate compared against the wrong baseline.",
}
RETRACTION: dict[str, Any] = {"cites": "judgement:invalidation@in-context-gate@2026-11-06", "reason": "The baseline was right."}


def validator(event_type: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads((SCHEMA_DIR / f"{event_type}.v1.schema.json").read_text(encoding="utf-8")))


def agrees(event_type: str, data: Any) -> list[ValidationFinding]:
    python = validate_ledger_event_data(event_type, 1, data)
    reference = validator(event_type).is_valid(data)
    assert python["valid"] == reference, (python["findings"], [error.message for error in validator(event_type).iter_errors(data)])
    return list(python["findings"])


def with_value(data: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    return {**copy.deepcopy(data), key: value}


def without(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key not in keys}


def test_python_vocabularies_match_the_schemas() -> None:
    assert VERDICT_VALUES == SCHEMA_VERDICTS == ("holds", "inconclusive", "fails", "cannot-tell")
    assert CANNOT_TELL_REASONS == SCHEMA_REASONS
    assert len(CANNOT_TELL_REASONS) == 5
    assert ManipulationCheck.__args__ == MANIPULATION_CHECKS  # type: ignore[attr-defined]


VALID = [
    ("evidence.recorded", MEASUREMENT),
    ("evidence.recorded", {**MEASUREMENT, "shardIndex": 0, "shardCount": 4, "ledgerPosition": 12}),
    ("evidence.recorded", with_value(MEASUREMENT, "manipulationCheck", "not-applicable")),
    *[("verdict.recorded", with_value(VERDICT, "verdict", value)) for value in ("holds", "inconclusive", "fails")],
    *[("verdict.recorded", with_value(CANNOT_TELL, "cannotTellReason", reason)) for reason in CANNOT_TELL_REASONS],
    ("verdict.recorded", without(CANNOT_TELL, "detail")),
    ("verdict.recorded", {**VERDICT, "detail": "close to the bar", "supersedes": "judgement:x", "policyEvent": {"streamId": "policy:p", "streamVersion": 2}}),
    ("verdict.invalidated", INVALIDATION),
    ("verdict.invalidated", with_value(INVALIDATION, "scope", {})),
    ("invalidation.retracted", RETRACTION),
]


@pytest.mark.parametrize(("event_type", "data"), VALID)
def test_valid_data_is_accepted_by_both_validators(event_type: str, data: dict[str, Any]) -> None:
    assert agrees(event_type, data) == []


INVALID = [
    ("evidence.recorded", without(MEASUREMENT, "patchrigCommit"), "format.missing_property", "data.patchrigCommit"),
    ("evidence.recorded", without(MEASUREMENT, "larqlVersion"), "format.missing_property", "data.larqlVersion"),
    ("evidence.recorded", without(MEASUREMENT, "larqlBinarySha256"), "format.missing_property", "data.larqlBinarySha256"),
    ("evidence.recorded", with_value(MEASUREMENT, "manipulationCheck", "not_applicable"), "format.invalid_value", "data.manipulationCheck"),
    ("evidence.recorded", with_value(MEASUREMENT, "attempt", "1"), "format.invalid_type", "data.attempt"),
    ("verdict.recorded", without(CANNOT_TELL, "cannotTellReason"), "verdict.reason_required", "data.cannotTellReason"),
    ("verdict.recorded", with_value(CANNOT_TELL, "cannotTellReason", "no_probes"), "format.invalid_value", "data.cannotTellReason"),
    ("verdict.recorded", with_value(CANNOT_TELL, "cannotTellReason", "engine-error"), "format.invalid_value", "data.cannotTellReason"),
    *[
        ("verdict.recorded", {**VERDICT, "verdict": value, "cannotTellReason": "no-probes"}, "verdict.reason_not_allowed", "data.cannotTellReason")
        for value in ("holds", "inconclusive", "fails")
    ],
    ("verdict.recorded", with_value(VERDICT, "verdict", "holds-weakly"), "format.invalid_value", "data.verdict"),
    ("verdict.recorded", with_value(VERDICT, "verdict", "holds_weakly"), "format.invalid_value", "data.verdict"),
    ("verdict.recorded", with_value(VERDICT, "supersedes", None), "format.invalid_type", "data.supersedes"),
    ("verdict.recorded", with_value(VERDICT, "policyEvent", "policy:p@2"), "format.invalid_type", "data.policyEvent"),
    ("verdict.invalidated", with_value(INVALIDATION, "scope", {"larqlBinaries": ["x"]}), "format.unknown_property", "data.scope.larqlBinaries"),
    ("verdict.invalidated", with_value(INVALIDATION, "cites", "judgement:x"), "format.invalid_type", "data.cites"),
    ("invalidation.retracted", with_value(RETRACTION, "cites", {"streamId": "judgement:x", "streamVersion": 1}), "format.invalid_type", "data.cites"),
]


@pytest.mark.parametrize(("event_type", "data", "code", "path"), INVALID)
def test_invalid_data_is_rejected_by_both_validators(event_type: str, data: dict[str, Any], code: str, path: str) -> None:
    findings = agrees(event_type, data)
    assert {"code": code, "path": path} in [{"code": item["code"], "path": item["path"]} for item in findings]


def test_reason_findings_replace_the_generic_ones() -> None:
    findings = agrees("verdict.recorded", {**VERDICT, "cannotTellReason": "no-probes"})
    assert [(item["code"], item["path"]) for item in findings] == [("verdict.reason_not_allowed", "data.cannotTellReason")]
    findings = agrees("verdict.recorded", without(CANNOT_TELL, "cannotTellReason"))
    assert [(item["code"], item["path"]) for item in findings] == [("verdict.reason_required", "data.cannotTellReason")]


# The checker's else and not, beyond the verdict schema ---------------------

ELSE_NOT: list[tuple[dict[str, Any], Any]] = [
    ({"if": {"type": "string"}, "then": {"const": "a"}, "else": {"type": "integer"}}, "a"),
    ({"if": {"type": "string"}, "then": {"const": "a"}, "else": {"type": "integer"}}, "b"),
    ({"if": {"type": "string"}, "then": {"const": "a"}, "else": {"type": "integer"}}, 3),
    ({"if": {"type": "string"}, "then": {"const": "a"}, "else": {"type": "integer"}}, 3.5),
    ({"if": {"type": "string"}, "else": {"type": "integer"}}, "anything"),
    ({"not": {"type": "string"}}, "x"),
    ({"not": {"type": "string"}}, 1),
    ({"not": {"not": {"type": "string"}}}, "x"),
    ({"not": {"not": {"type": "string"}}}, 1),
    ({"type": "array", "items": {"not": {"required": ["x"]}}}, [{"y": 1}, {"x": 1}]),
    ({"type": "array", "items": {"not": {"required": ["x"]}}}, [{"y": 1}]),
    ({"type": "object", "properties": {"a": {"if": {"type": "integer"}, "then": {"minimum": 0}, "else": {"not": {"type": "null"}}}}}, {"a": -1}),
    ({"type": "object", "properties": {"a": {"if": {"type": "integer"}, "then": {"minimum": 0}, "else": {"not": {"type": "null"}}}}}, {"a": None}),
    ({"type": "object", "properties": {"a": {"if": {"type": "integer"}, "then": {"minimum": 0}, "else": {"not": {"type": "null"}}}}}, {"a": "s"}),
]


@pytest.mark.parametrize(("schema", "value"), ELSE_NOT)
def test_else_and_not_agree_with_jsonschema(schema: dict[str, Any], value: Any) -> None:
    findings: list[ValidationFinding] = []
    check(schema, value, "$", findings, {})
    assert (not findings) == Draft202012Validator(schema).is_valid(value)
