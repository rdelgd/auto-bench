"""World-ledger semantics: governance event types, the policy aggregate, and the rule projection.

The ledger itself keeps order, durability, idempotency, and attribution, and treats an
event's type, schema version, and data as opaque. This module decides what those events
mean. Adapters read events back as ``RecordedEvent`` values, pass them in, and append what
an aggregate returns; event ids, positions, envelope metadata, and concurrency stay with
the adapter. Nothing here consults a clock: event times are carried as data.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict, cast, get_args

from ._json_schema import finding, json_equal, shape_findings
from ._schema_ledger import EVENT_DATA_DEFINITIONS, LEDGER_DEFINITIONS
from .domain import JsonValue, ValidationFinding, ValidationResult, validation_result

LedgerEventType: TypeAlias = Literal["policy.accepted", "decision.made", "application.removed"]
PolicyDecision: TypeAlias = Literal["allow", "deny"]
DecisionBasis: TypeAlias = Literal["rule", "unknown-action", "unknown-application", "no-rule"]

LEDGER_EVENT_TYPES: tuple[LedgerEventType, ...] = get_args(LedgerEventType)
LEDGER_EVENT_SCHEMA_VERSIONS: Mapping[LedgerEventType, tuple[int, ...]] = {
    event_type: tuple(sorted(version for known, version in EVENT_DATA_DEFINITIONS if known == event_type))
    for event_type in LEDGER_EVENT_TYPES
}

# The bindings and actions a first-slice policy may govern. Binding records replace this
# when policies become statements about concepts.
FIRST_SLICE_BINDINGS: Mapping[str, tuple[str, ...]] = {
    "paseo-core": ("application.teardown", "agent.retire", "workspace.delete"),
}

_POLICY_ACCEPTED_VERSION = 1


class LedgerEventRef(TypedDict):
    """Cites a recorded event by its stream and its version within that stream."""

    streamId: str
    streamVersion: int


class PolicyAcceptedData(TypedDict):
    policyId: str
    binding: str
    action: str
    decision: PolicyDecision
    reason: NotRequired[str]
    acceptedBy: str


class DecisionMadeData(TypedDict):
    decisionId: str
    applicationId: str
    action: str
    resource: Mapping[str, JsonValue]
    requestedBy: str
    requestedAt: str
    decision: PolicyDecision
    basis: DecisionBasis
    reason: NotRequired[str]
    policy: NotRequired[LedgerEventRef]
    projectionPosition: NotRequired[int]
    traceId: NotRequired[str]


class RemovalApproval(TypedDict):
    decisionId: NotRequired[str]
    bypassed: NotRequired[bool]
    required: NotRequired[bool]


class ApplicationRemovedData(TypedDict):
    applicationId: str
    removedAt: str
    removedBy: NotRequired[str]
    approval: NotRequired[RemovalApproval]
    registered: bool


class NewEvent(TypedDict):
    """An event an aggregate asks the adapter to append."""

    type: LedgerEventType
    schemaVersion: int
    data: PolicyAcceptedData


class RecordedEvent(TypedDict):
    """An event as read back from the ledger; ``type`` is open because the ledger holds other types."""

    streamId: str
    streamVersion: int
    type: str
    schemaVersion: int
    data: JsonValue


class AcceptPolicy(TypedDict):
    policyId: str
    binding: str
    action: str
    decision: PolicyDecision
    reason: NotRequired[str]
    acceptedBy: str


class PolicyCommandResult(TypedDict):
    accepted: bool
    events: Sequence[NewEvent]
    findings: Sequence[ValidationFinding]


class DecisionRuleRecord(TypedDict):
    binding: str
    action: str
    decision: PolicyDecision
    reason: NotRequired[str]
    policyId: str
    policy: LedgerEventRef


class DecisionRuleProjection(TypedDict):
    rules: Sequence[DecisionRuleRecord]
    findings: Sequence[ValidationFinding]


def policy_stream_id(policy_id: str) -> str:
    return f"policy:{policy_id}"


def application_stream_id(application_id: str) -> str:
    return f"application:{application_id}"


def _is_version(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _data_findings(event_type: object, schema_version: object, data: object, path: str) -> list[ValidationFinding] | None:
    """Shape findings for supported data under ``path``, or ``None`` when the type or version is unsupported."""
    if not isinstance(event_type, str) or not _is_version(schema_version):
        return None
    definition = EVENT_DATA_DEFINITIONS.get((event_type, cast(int, schema_version)))
    if definition is None:
        return None
    return shape_findings({"$ref": f"#/$defs/{definition}"}, data, path, LEDGER_DEFINITIONS)


def _unsupported_message(event_type: object, schema_version: object) -> str:
    if event_type in LEDGER_EVENT_TYPES:
        return f"Unsupported schema version {schema_version!r} for {event_type}."
    return f"Unsupported ledger event type: {event_type!r}"


def validate_ledger_event_data(event_type: str, schema_version: int, data: object) -> ValidationResult:
    """Check event data against the schema for its type and version. Shape only; no business rules."""
    findings = _data_findings(event_type, schema_version, data, "data")
    if findings is None:
        path = "schemaVersion" if event_type in LEDGER_EVENT_TYPES else "type"
        return validation_result([finding("ledger.unsupported_event", path, _unsupported_message(event_type, schema_version))])
    return validation_result(findings)


def _policy_content(data: Mapping[str, object]) -> tuple[object, ...]:
    # The accepter is not content: re-accepting the same rule under another name changes nothing.
    return (data["binding"], data["action"], data["decision"], data.get("reason"))


def _read_policy_stream(past_events: Sequence[RecordedEvent], findings: list[ValidationFinding]) -> Mapping[str, object] | None:
    current: Mapping[str, object] | None = None
    for index, event in enumerate(past_events):
        path = f"pastEvents[{index}]"
        event_type, version = event["type"], event["schemaVersion"]
        data_findings = _data_findings(event_type, version, event["data"], f"{path}.data") if event_type == "policy.accepted" else None
        if data_findings is None:
            findings.append(finding("policy.unsupported_event", path, _unsupported_message(event_type, version)))
        elif data_findings:
            findings.append(finding("policy.unsupported_event", path, f"Unreadable {event_type} data: {data_findings[0]['message']}"))
        else:
            current = cast(Mapping[str, object], event["data"])
    return current


def decide_policy(past_events: Sequence[RecordedEvent], command: AcceptPolicy) -> PolicyCommandResult:
    """Decide whether to accept a policy, given the events already on its stream.

    Returns one ``policy.accepted`` event to append, or every applicable rejection. The
    adapter appends at the stream version it read; on a conflict it re-reads and decides again.
    """
    findings: list[ValidationFinding] = []
    current = _read_policy_stream(past_events, findings)

    shape = _data_findings("policy.accepted", _POLICY_ACCEPTED_VERSION, command, "command")
    assert shape is not None
    if shape:
        return {"accepted": False, "events": [], "findings": [*findings, *shape]}

    binding, action, policy_id = command["binding"], command["action"], command["policyId"]
    actions = FIRST_SLICE_BINDINGS.get(binding)
    if actions is None:
        findings.append(finding("policy.invalid_binding", "command.binding", f"Unknown binding: {binding}"))
    elif action not in actions:
        findings.append(finding("policy.invalid_action", "command.action", f"Unknown {binding} action: {action}"))
    if policy_id != f"{binding}.{action}":
        findings.append(finding("policy.id_mismatch", "command.policyId", f"Policy id must be {binding}.{action}."))
    if not command["acceptedBy"].strip():
        findings.append(finding("fixture.required", "command.acceptedBy", "A non-empty value is required."))
    if command["decision"] == "deny" and not command.get("reason", "").strip():
        findings.append(finding("policy.reason_required", "command.reason", "A deny decision requires a reason."))
    if current is not None and all(json_equal(left, right) for left, right in zip(_policy_content(current), _policy_content(command))):
        findings.append(finding("policy.unchanged", "command", f"Policy {policy_id} already has this accepted content."))
    if findings:
        return {"accepted": False, "events": [], "findings": findings}

    data: PolicyAcceptedData = {
        "policyId": policy_id,
        "binding": binding,
        "action": action,
        "decision": command["decision"],
        "acceptedBy": command["acceptedBy"],
    }
    if "reason" in command:
        data["reason"] = command["reason"]
    return {
        "accepted": True,
        "events": [{"type": "policy.accepted", "schemaVersion": _POLICY_ACCEPTED_VERSION, "data": data}],
        "findings": [],
    }


def project_decision_rules(events: Sequence[RecordedEvent]) -> DecisionRuleProjection:
    """Fold ``policy.accepted`` events, in ledger order, into the current rule per (binding, action).

    Other event types are ignored. A policy event that cannot be read contributes no rule and
    is reported; adapters must not rewrite their rule table while findings are present.
    """
    findings: list[ValidationFinding] = []
    rules: dict[tuple[str, str], DecisionRuleRecord] = {}
    for index, event in enumerate(events):
        if event["type"] != "policy.accepted":
            continue
        path = f"events[{index}]"
        data_findings = _data_findings(event["type"], event["schemaVersion"], event["data"], f"{path}.data")
        if data_findings is None:
            findings.append(finding("ledger.unsupported_event", f"{path}.schemaVersion", _unsupported_message(event["type"], event["schemaVersion"])))
            continue
        if data_findings:
            findings.append(finding(
                "ledger.invalid_event_data",
                f"{path}.data",
                "; ".join(f"{item['path']}: {item['message']}" for item in data_findings),
            ))
            continue
        data = cast(PolicyAcceptedData, event["data"])
        rule: DecisionRuleRecord = {
            "binding": data["binding"],
            "action": data["action"],
            "decision": data["decision"],
            "policyId": data["policyId"],
            "policy": {"streamId": event["streamId"], "streamVersion": event["streamVersion"]},
        }
        if "reason" in data:
            rule["reason"] = data["reason"]
        rules[(data["binding"], data["action"])] = rule
    return {"rules": [rules[key] for key in sorted(rules)], "findings": findings}
