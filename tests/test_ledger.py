"""The policy aggregate and the decision-rule projection."""

from __future__ import annotations

import copy
import json
from typing import Any

from lasm_core import (
    AcceptPolicy,
    RecordedEvent,
    application_stream_id,
    decide_policy,
    policy_stream_id,
    project_decision_rules,
)

TEARDOWN: AcceptPolicy = {
    "policyId": "paseo-core.application.teardown",
    "binding": "paseo-core",
    "action": "application.teardown",
    "decision": "deny",
    "reason": "Contact an operator to tear down an application.",
    "acceptedBy": "operator@example.com",
}
RETIRE: AcceptPolicy = {
    "policyId": "paseo-core.agent.retire",
    "binding": "paseo-core",
    "action": "agent.retire",
    "decision": "allow",
    "acceptedBy": "operator@example.com",
}
WORKSPACE_DELETE: AcceptPolicy = {
    "policyId": "paseo-core.workspace.delete",
    "binding": "paseo-core",
    "action": "workspace.delete",
    "decision": "allow",
    "acceptedBy": "operator@example.com",
}


def record(command: AcceptPolicy, stream_version: int, past: list[RecordedEvent] | None = None) -> RecordedEvent:
    """Decide a command and record its event as the ledger would return it."""
    result = decide_policy(past or [], command)
    assert result["accepted"], result["findings"]
    (event,) = result["events"]
    return {
        "streamId": policy_stream_id(command["policyId"]),
        "streamVersion": stream_version,
        "type": event["type"],
        "schemaVersion": event["schemaVersion"],
        "data": dict(event["data"]),
    }


def codes(result: Any) -> list[tuple[str, str]]:
    return [(item["code"], item["path"]) for item in result["findings"]]


def test_stream_ids() -> None:
    assert policy_stream_id("paseo-core.agent.retire") == "policy:paseo-core.agent.retire"
    assert application_stream_id("app-7") == "application:app-7"


# Aggregate ---------------------------------------------------------------


def test_accept_onto_an_empty_stream() -> None:
    result = decide_policy([], TEARDOWN)
    assert result == {
        "accepted": True,
        "events": [{"type": "policy.accepted", "schemaVersion": 1, "data": dict(TEARDOWN)}],
        "findings": [],
    }


def test_allow_without_reason_omits_reason() -> None:
    (event,) = decide_policy([], RETIRE)["events"]
    assert "reason" not in event["data"]


def test_every_rejection_is_reported() -> None:
    command: Any = {
        "policyId": "teardown-needs-a-human",
        "binding": "reffy",
        "action": "application.teardown",
        "decision": "deny",
        "reason": "  ",
        "acceptedBy": " ",
    }
    result = decide_policy([], command)
    assert not result["accepted"] and result["events"] == []
    assert codes(result) == [
        ("policy.invalid_binding", "command.binding"),
        ("policy.id_mismatch", "command.policyId"),
        ("fixture.required", "command.acceptedBy"),
        ("policy.reason_required", "command.reason"),
    ]


def test_unknown_action_and_missing_deny_reason() -> None:
    command: Any = {**TEARDOWN, "action": "application.restart", "policyId": "paseo-core.application.restart"}
    del command["reason"]
    assert codes(decide_policy([], command)) == [
        ("policy.invalid_action", "command.action"),
        ("policy.reason_required", "command.reason"),
    ]


def test_malformed_command_is_rejected_by_shape() -> None:
    command: Any = {**TEARDOWN, "decision": "maybe", "statement": "x"}
    assert codes(decide_policy([], command)) == [
        ("format.invalid_value", "command.decision"),
        ("format.unknown_property", "command.statement"),
    ]


def test_identical_reacceptance_is_unchanged_even_by_another_accepter() -> None:
    past = [record(TEARDOWN, 1)]
    for command in [TEARDOWN, {**TEARDOWN, "acceptedBy": "someone-else@example.com"}]:
        result = decide_policy(past, command)
        assert not result["accepted"] and result["events"] == []
        assert codes(result) == [("policy.unchanged", "command")]


def test_changed_content_is_accepted_against_the_latest_acceptance() -> None:
    past = [record(WORKSPACE_DELETE, 1)]
    deny: AcceptPolicy = {**WORKSPACE_DELETE, "decision": "deny", "reason": "Workspaces hold records."}
    past.append(record(deny, 2, past))
    # Going back to the first content is a change relative to the latest acceptance.
    assert decide_policy(past, WORKSPACE_DELETE)["accepted"]
    reworded: AcceptPolicy = {**deny, "reason": "Workspaces hold an organization's records."}
    assert decide_policy(past, reworded)["accepted"]
    assert codes(decide_policy(past, deny)) == [("policy.unchanged", "command")]


def test_unreadable_history_is_refused() -> None:
    accepted = record(TEARDOWN, 1)
    future: RecordedEvent = {**accepted, "streamVersion": 2, "schemaVersion": 2}
    foreign: RecordedEvent = {**accepted, "streamVersion": 3, "type": "policy.contested"}
    malformed: RecordedEvent = {**accepted, "streamVersion": 4, "data": {"policyId": "x"}}
    result = decide_policy([accepted, future, foreign, malformed], RETIRE)
    assert not result["accepted"]
    assert codes(result) == [
        ("policy.unsupported_event", "pastEvents[1]"),
        ("policy.unsupported_event", "pastEvents[2]"),
        ("policy.unsupported_event", "pastEvents[3]"),
    ]


def test_aggregate_does_not_mutate_inputs() -> None:
    past = [record(TEARDOWN, 1)]
    command: AcceptPolicy = {**TEARDOWN, "reason": "Ask an operator."}
    snapshot = copy.deepcopy((past, command))
    result = decide_policy(past, command)
    assert (past, command) == snapshot
    result["events"][0]["data"]["reason"] = "changed"
    assert command["reason"] == "Ask an operator."


# Projection --------------------------------------------------------------


def seeded() -> list[RecordedEvent]:
    return [record(TEARDOWN, 1), record(RETIRE, 1), record(WORKSPACE_DELETE, 1)]


def test_seeded_rules_reproduce_todays_table() -> None:
    projection = project_decision_rules(seeded())
    assert projection["findings"] == []
    assert projection["rules"] == [
        {
            "binding": "paseo-core", "action": "agent.retire", "decision": "allow",
            "policyId": "paseo-core.agent.retire",
            "policy": {"streamId": "policy:paseo-core.agent.retire", "streamVersion": 1},
        },
        {
            "binding": "paseo-core", "action": "application.teardown", "decision": "deny",
            "reason": "Contact an operator to tear down an application.",
            "policyId": "paseo-core.application.teardown",
            "policy": {"streamId": "policy:paseo-core.application.teardown", "streamVersion": 1},
        },
        {
            "binding": "paseo-core", "action": "workspace.delete", "decision": "allow",
            "policyId": "paseo-core.workspace.delete",
            "policy": {"streamId": "policy:paseo-core.workspace.delete", "streamVersion": 1},
        },
    ]


def test_latest_acceptance_wins_and_is_cited() -> None:
    first = record(WORKSPACE_DELETE, 1)
    deny: AcceptPolicy = {**WORKSPACE_DELETE, "decision": "deny", "reason": "Workspaces hold records."}
    second = record(deny, 2, [first])
    (rule,) = project_decision_rules([first, second])["rules"]
    assert rule["decision"] == "deny" and rule["reason"] == "Workspaces hold records."
    assert rule["policy"] == {"streamId": "policy:paseo-core.workspace.delete", "streamVersion": 2}
    # Fold order is ledger order, not stream version.
    (rule,) = project_decision_rules([second, first])["rules"]
    assert rule["decision"] == "allow" and "reason" not in rule


def test_foreign_events_are_ignored() -> None:
    decision: RecordedEvent = {
        "streamId": application_stream_id("app-7"), "streamVersion": 1, "type": "decision.made", "schemaVersion": 1,
        "data": {"not": "read"},
    }
    other: RecordedEvent = {"streamId": "trace:1", "streamVersion": 9, "type": "patch.applied", "schemaVersion": 3, "data": None}
    events = seeded()
    assert project_decision_rules([decision, *events, other]) == project_decision_rules(events)


def test_unreadable_policy_events_are_reported_and_skipped() -> None:
    events = seeded()
    future: RecordedEvent = {**events[0], "streamVersion": 2, "schemaVersion": 2, "data": {"appliesTo": {}}}
    malformed: RecordedEvent = {**events[0], "streamVersion": 3, "data": {**events[0]["data"], "decision": "maybe"}}  # type: ignore[dict-item]
    projection = project_decision_rules([*events, future, malformed])
    assert projection["rules"] == project_decision_rules(events)["rules"]
    assert codes(projection) == [
        ("ledger.unsupported_event", "events[3].schemaVersion"),
        ("ledger.invalid_event_data", "events[4].data"),
    ]
    assert "events[4].data.decision" in projection["findings"][1]["message"]


def test_replay_is_deterministic_and_incremental() -> None:
    events = seeded()
    deny: AcceptPolicy = {**WORKSPACE_DELETE, "decision": "deny", "reason": "Workspaces hold records."}
    events.append(record(deny, 2, [events[2]]))
    first = json.dumps(project_decision_rules(events))
    assert json.dumps(project_decision_rules(copy.deepcopy(events))) == first
    assert project_decision_rules([]) == {"rules": [], "findings": []}
    # Folding a prefix then the remainder sees the same final rules as folding everything.
    by_action = {rule["action"]: rule for rule in project_decision_rules(events[:2])["rules"]}
    by_action.update({rule["action"]: rule for rule in project_decision_rules(events[2:])["rules"]})
    assert [by_action[key] for key in sorted(by_action)] == project_decision_rules(events)["rules"]


def test_projection_does_not_mutate_inputs() -> None:
    events = seeded()
    snapshot = copy.deepcopy(events)
    project_decision_rules(events)
    assert events == snapshot
