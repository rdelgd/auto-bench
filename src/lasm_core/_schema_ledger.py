"""Ledger event-data schemas, defined once as JSON Schema Draft 2020-12 data.

Each (event type, schema version) pair has its own schema describing the event's ``data``
only; the ledger owns the envelope. These are versioned per event type, independently of
the version 1 interchange documents. The checked-in files under ``lasm_core/schemas/ledger/``
are rendered from these definitions (``python scripts/write_schemas.py``), and
``lasm_core.ledger`` checks data against the same definitions.

Schemas describe shape, not business validity: a ``deny`` without a reason and blank
strings remain for ``decide_policy`` to reject.
"""

from __future__ import annotations

from ._json_schema import JsonSchema
from ._schema_v1 import BOOLEAN, DEFINITIONS, DRAFT, STRING, STRINGS, _enum, _record, _ref

POLICY_DECISIONS = ("allow", "deny")
DECISION_BASES = ("rule", "unknown-action", "unknown-application", "no-rule")
VERDICT_VALUES = ("holds", "inconclusive", "fails", "cannot-tell")
CANNOT_TELL_REASONS = (
    "no-probes",
    "too-few-values",
    "degenerate-stratum",
    "instrument-gate-failed",
    "no-eligible-chains",
)
MANIPULATION_CHECKS = ("passed", "failed", "not-applicable")

JSON_OBJECT: JsonSchema = {"type": "object", "additionalProperties": _ref("JsonValue")}


def _verdict_recorded() -> JsonSchema:
    schema = _record(
        {
            "cellId": STRING,
            "attempt": _ref("SafeInteger"),
            "cites": _ref("LedgerEventRef"),
            "preregistration": STRING,
            "scorerVersion": STRING,
            "verdict": _ref("VerdictValue"),
        },
        {
            "supersedes": STRING,
            "cannotTellReason": _ref("CannotTellReason"),
            "detail": STRING,
            "policyEvent": _ref("LedgerEventRef"),
        },
    )
    # A reason is required with cannot-tell and forbidden with every other verdict.
    schema["if"] = {"properties": {"verdict": {"const": "cannot-tell"}}, "required": ["verdict"]}
    schema["then"] = {"required": ["cannotTellReason"]}
    schema["else"] = {"not": {"required": ["cannotTellReason"]}}
    return schema


LEDGER_DEFINITIONS: dict[str, JsonSchema] = {
    "JsonNumber": DEFINITIONS["JsonNumber"],
    "JsonValue": DEFINITIONS["JsonValue"],
    "SafeInteger": DEFINITIONS["SafeInteger"],
    "PolicyDecision": _enum(*POLICY_DECISIONS),
    "DecisionBasis": _enum(*DECISION_BASES),
    "LedgerEventRef": _record({"streamId": STRING, "streamVersion": _ref("SafeInteger")}),
    "RemovalApproval": _record({}, {"decisionId": STRING, "bypassed": BOOLEAN, "required": BOOLEAN}),
    "PolicyAcceptedData": _record(
        {
            "policyId": STRING,
            "binding": STRING,
            "action": STRING,
            "decision": _ref("PolicyDecision"),
            "acceptedBy": STRING,
        },
        {"reason": STRING},
    ),
    "DecisionMadeData": _record(
        {
            "decisionId": STRING,
            "applicationId": STRING,
            "action": STRING,
            "resource": JSON_OBJECT,
            "requestedBy": STRING,
            "requestedAt": STRING,
            "decision": _ref("PolicyDecision"),
            "basis": _ref("DecisionBasis"),
        },
        {
            "reason": STRING,
            "policy": _ref("LedgerEventRef"),
            "projectionPosition": _ref("SafeInteger"),
            "traceId": STRING,
        },
    ),
    "ApplicationRemovedData": _record(
        {"applicationId": STRING, "removedAt": STRING, "registered": BOOLEAN},
        {"removedBy": STRING, "approval": _ref("RemovalApproval")},
    ),
    "VerdictValue": _enum(*VERDICT_VALUES),
    "CannotTellReason": _enum(*CANNOT_TELL_REASONS),
    "ManipulationCheck": _enum(*MANIPULATION_CHECKS),
    "MeasurementTarget": _record({"binding": STRING, "ref": STRING}),
    "MeasurementEnvironment": _record({"host": STRING, "fingerprint": STRING}),
    "InvalidationScope": _record(
        {},
        {"patchrigCommits": STRINGS, "scorerVersions": STRINGS, "vindexPins": STRINGS, "larqlVersions": STRINGS},
    ),
    "EvidenceRecordedData": _record(
        {
            "cellId": STRING,
            "attempt": _ref("SafeInteger"),
            "target": _ref("MeasurementTarget"),
            "vindexPin": STRING,
            "patchDigest": STRING,
            "patchrigCommit": STRING,
            "larqlVersion": STRING,
            "larqlBinarySha256": STRING,
            "manipulationCheck": _ref("ManipulationCheck"),
            "tier": STRING,
            "scope": STRING,
            "controlsState": STRING,
            "measurements": JSON_OBJECT,
            "recordsDigest": STRING,
            "environment": _ref("MeasurementEnvironment"),
        },
        {
            "shardIndex": _ref("SafeInteger"),
            "shardCount": _ref("SafeInteger"),
            "ledgerPosition": _ref("SafeInteger"),
        },
    ),
    "VerdictRecordedData": _verdict_recorded(),
    "VerdictInvalidatedData": _record({
        "instrument": STRING,
        "scope": _ref("InvalidationScope"),
        "cites": _ref("LedgerEventRef"),
        "reason": STRING,
    }),
    "InvalidationRetractedData": _record({"cites": STRING, "reason": STRING}),
}

# (event type, schema version) -> the definition describing that event's data.
EVENT_DATA_DEFINITIONS: dict[tuple[str, int], str] = {
    ("policy.accepted", 1): "PolicyAcceptedData",
    ("decision.made", 1): "DecisionMadeData",
    ("application.removed", 1): "ApplicationRemovedData",
    ("evidence.recorded", 1): "EvidenceRecordedData",
    ("verdict.recorded", 1): "VerdictRecordedData",
    ("verdict.invalidated", 1): "VerdictInvalidatedData",
    ("invalidation.retracted", 1): "InvalidationRetractedData",
}


def _references(schema: object, found: set[str]) -> None:
    if isinstance(schema, dict):
        reference = schema.get("$ref")
        if isinstance(reference, str) and reference.startswith("#/$defs/"):
            name = reference.removeprefix("#/$defs/")
            if name not in found:
                found.add(name)
                _references(LEDGER_DEFINITIONS[name], found)
        for value in schema.values():
            _references(value, found)
    elif isinstance(schema, list):
        for value in schema:
            _references(value, found)


def event_schema_id(event_type: str, version: int) -> str:
    return f"urn:lasm-core:ledger:{event_type}:v{version}"


def event_data_schema(event_type: str, version: int) -> JsonSchema:
    """A self-contained schema for one event type's data, carrying only the definitions it uses."""
    root = _ref(EVENT_DATA_DEFINITIONS[(event_type, version)])
    used: set[str] = set()
    _references(root, used)
    return {
        "$schema": DRAFT,
        "$id": event_schema_id(event_type, version),
        "title": f"Lasm {event_type} ledger event data, version {version}",
        "$defs": {name: LEDGER_DEFINITIONS[name] for name in sorted(used)},
        **root,
    }


def schema_files() -> dict[str, JsonSchema]:
    """The checked-in ledger schema files, keyed by file name."""
    return {
        f"{event_type}.v{version}.schema.json": event_data_schema(event_type, version)
        for event_type, version in EVENT_DATA_DEFINITIONS
    }
