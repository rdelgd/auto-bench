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
from ._schema_v1 import BOOLEAN, DEFINITIONS, DRAFT, STRING, _enum, _record, _ref

POLICY_DECISIONS = ("allow", "deny")
DECISION_BASES = ("rule", "unknown-action", "unknown-application", "no-rule")

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
            "resource": {"type": "object", "additionalProperties": _ref("JsonValue")},
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
}

# (event type, schema version) -> the definition describing that event's data.
EVENT_DATA_DEFINITIONS: dict[tuple[str, int], str] = {
    ("policy.accepted", 1): "PolicyAcceptedData",
    ("decision.made", 1): "DecisionMadeData",
    ("application.removed", 1): "ApplicationRemovedData",
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
