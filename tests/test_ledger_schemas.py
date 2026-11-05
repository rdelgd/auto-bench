"""Ledger event-data schemas: checked-in files, the pure validator, and jsonschema agree."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

import lasm_core
from lasm_core import LEDGER_EVENT_SCHEMA_VERSIONS, LEDGER_EVENT_TYPES, validate_ledger_event_data
from lasm_core._schema_ledger import schema_files

SCHEMA_DIR = Path(lasm_core.__file__).parent / "schemas" / "ledger"
CHECKED_IN = {path.name: json.loads(path.read_text(encoding="utf-8")) for path in SCHEMA_DIR.glob("*.json")}

POLICY_ACCEPTED: dict[str, Any] = {
    "policyId": "paseo-core.application.teardown",
    "binding": "paseo-core",
    "action": "application.teardown",
    "decision": "deny",
    "reason": "Contact an operator to tear down an application.",
    "acceptedBy": "operator@example.com",
}
DECISION_MADE: dict[str, Any] = {
    "decisionId": "dec-42",
    "applicationId": "app-7",
    "action": "workspace.delete",
    "resource": {"workspaceId": "ws-1", "labels": ["reffy"], "size": 3, "archived": None},
    "requestedBy": "owner@example.com",
    "requestedAt": "2026-10-18T14:02:11Z",
    "decision": "allow",
    "basis": "rule",
    "policy": {"streamId": "policy:paseo-core.workspace.delete", "streamVersion": 1},
    "projectionPosition": 118,
    "traceId": "trace-abc",
}
APPLICATION_REMOVED: dict[str, Any] = {
    "applicationId": "app-7",
    "removedAt": "2026-10-19T09:00:00Z",
    "removedBy": "operator@example.com",
    "approval": {"decisionId": "dec-43", "bypassed": False, "required": True},
    "registered": True,
}
VALID: dict[str, dict[str, Any]] = {
    "policy.accepted": POLICY_ACCEPTED,
    "decision.made": DECISION_MADE,
    "application.removed": APPLICATION_REMOVED,
}


def without(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key not in keys}


def with_value(data: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    return {**copy.deepcopy(data), key: value}


def schema_validator(event_type: str) -> Draft202012Validator:
    return Draft202012Validator(CHECKED_IN[f"{event_type}.v1.schema.json"])


def assert_agrees(event_type: str, data: Any) -> bool:
    python = validate_ledger_event_data(event_type, 1, data)
    reference = schema_validator(event_type).is_valid(data)
    assert python["valid"] == reference, (python["findings"], [error.message for error in schema_validator(event_type).iter_errors(data)])
    return reference


def test_checked_in_schemas_are_rendered_from_the_python_definitions() -> None:
    assert CHECKED_IN == schema_files()


def test_schemas_are_valid_self_contained_draft_2020_12_documents() -> None:
    for name, schema in CHECKED_IN.items():
        Draft202012Validator.check_schema(schema)
        event_type, version = name.removesuffix(".schema.json").rsplit(".v", 1)
        assert schema["$id"] == f"urn:lasm-core:ledger:{event_type}:v{version}"


def test_schema_versions_match_the_schema_set() -> None:
    assert set(LEDGER_EVENT_TYPES) == {
        "policy.accepted",
        "decision.made",
        "application.removed",
        "evidence.recorded",
        "verdict.recorded",
        "verdict.invalidated",
        "invalidation.retracted",
    }
    two_versions = {"evidence.recorded", "verdict.recorded"}
    assert dict(LEDGER_EVENT_SCHEMA_VERSIONS) == {
        event_type: (1, 2) if event_type in two_versions else (1,) for event_type in LEDGER_EVENT_TYPES
    }
    assert {
        f"{event_type}.v{version}.schema.json"
        for event_type, versions in LEDGER_EVENT_SCHEMA_VERSIONS.items()
        for version in versions
    } == set(CHECKED_IN)


ACCEPTED_CASES = [
    ("policy.accepted", POLICY_ACCEPTED),
    ("policy.accepted-allow-without-reason", without({**POLICY_ACCEPTED, "decision": "allow"}, "reason")),
    # Shape only: a deny without a reason is rejected by decide_policy, not the schema.
    ("policy.accepted-deny-without-reason", without(POLICY_ACCEPTED, "reason")),
    ("decision.made", DECISION_MADE),
    ("decision.made-backfilled-fail-closed", {
        **without(DECISION_MADE, "policy", "projectionPosition", "traceId"),
        "decision": "deny",
        "basis": "no-rule",
        "reason": "No rule for this action.",
    }),
    ("decision.made-empty-resource", with_value(DECISION_MADE, "resource", {})),
    ("application.removed", APPLICATION_REMOVED),
    ("application.removed-without-provenance", without(APPLICATION_REMOVED, "removedBy", "approval")),
    ("application.removed-empty-approval", with_value(APPLICATION_REMOVED, "approval", {})),
    ("application.removed-bypass-only", with_value(APPLICATION_REMOVED, "approval", {"bypassed": True})),
]


@pytest.mark.parametrize(("label", "data"), ACCEPTED_CASES, ids=[label for label, _ in ACCEPTED_CASES])
def test_valid_data_is_accepted_by_both_validators(label: str, data: dict[str, Any]) -> None:
    event_type = label.split("-")[0]
    assert assert_agrees(event_type, data)
    assert validate_ledger_event_data(event_type, 1, data)["findings"] == []


REJECTED_CASES = [
    ("policy.accepted", without(POLICY_ACCEPTED, "acceptedBy"), "format.missing_property", "data.acceptedBy"),
    ("policy.accepted", with_value(POLICY_ACCEPTED, "decision", "maybe"), "format.invalid_value", "data.decision"),
    ("policy.accepted", with_value(POLICY_ACCEPTED, "statement", "x"), "format.unknown_property", "data.statement"),
    ("policy.accepted", with_value(POLICY_ACCEPTED, "reason", 7), "format.invalid_type", "data.reason"),
    ("decision.made", without(DECISION_MADE, "basis"), "format.missing_property", "data.basis"),
    ("decision.made", with_value(DECISION_MADE, "basis", "rule:workspace.delete"), "format.invalid_value", "data.basis"),
    ("decision.made", with_value(DECISION_MADE, "resource", "ws-1"), "format.invalid_type", "data.resource"),
    ("decision.made", with_value(DECISION_MADE, "bypassed", False), "format.unknown_property", "data.bypassed"),
    ("decision.made", with_value(DECISION_MADE, "projectionPosition", 1.5), "format.invalid_type", "data.projectionPosition"),
    ("decision.made", with_value(DECISION_MADE, "projectionPosition", True), "format.invalid_type", "data.projectionPosition"),
    ("decision.made", with_value(DECISION_MADE, "policy", {"streamId": "policy:x"}), "format.missing_property", "data.policy.streamVersion"),
    ("application.removed", with_value(APPLICATION_REMOVED, "approval", {"bypassed": "yes"}), "format.invalid_type", "data.approval.bypassed"),
    ("application.removed", without(APPLICATION_REMOVED, "registered"), "format.missing_property", "data.registered"),
]


@pytest.mark.parametrize(("event_type", "data", "code", "path"), REJECTED_CASES)
def test_invalid_data_is_rejected_by_both_validators(event_type: str, data: dict[str, Any], code: str, path: str) -> None:
    assert not assert_agrees(event_type, data)
    findings = validate_ledger_event_data(event_type, 1, data)["findings"]
    assert {"code": code, "path": path} in [{"code": item["code"], "path": item["path"]} for item in findings]


def test_non_finite_numbers_in_resource_are_rejected() -> None:
    result = validate_ledger_event_data("decision.made", 1, with_value(DECISION_MADE, "resource", {"size": float("nan")}))
    assert [(item["code"], item["path"]) for item in result["findings"]] == [("format.non_finite_number", "data.resource.size")]


@pytest.mark.parametrize(
    ("event_type", "version", "path"),
    [("policy.proposed", 1, "type"), ("policy.accepted", 2, "schemaVersion"), ("decision.made", 0, "schemaVersion")],
)
def test_unknown_type_or_version_is_unsupported(event_type: str, version: int, path: str) -> None:
    result = validate_ledger_event_data(event_type, version, POLICY_ACCEPTED)
    assert not result["valid"]
    assert [(item["code"], item["path"]) for item in result["findings"]] == [("ledger.unsupported_event", path)]
