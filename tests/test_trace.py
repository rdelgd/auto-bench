from __future__ import annotations

from lasm_core import normalize_trace, validate_trace


def test_normalization_orders_events_deterministically_and_assigns_positions() -> None:
    result = normalize_trace([
        {"type": "task.completed", "sequence": 20, "actorId": "agent", "evidence": {"outcome": "done"}},
        {"type": "intent.submitted", "sequence": 10, "actorId": "customer", "evidence": {"goal": "service"}},
    ])

    assert [(event["type"], event["position"]) for event in result["events"]] == [("intent.submitted", 1), ("task.completed", 2)]
    assert result["findings"] == []


def test_normalization_reports_and_omits_unknown_or_malformed_events() -> None:
    result = normalize_trace([
        {"type": "unknown.event", "sequence": 1, "actorId": "agent"},
        {"type": "task.completed", "sequence": 2},
    ])

    assert result["events"] == []
    assert [finding["code"] for finding in result["findings"]] == ["trace.unknown_event_type", "trace.missing_actor"]


def test_sequences_compare_as_numbers() -> None:
    # JSON does not distinguish 1 from 1.0: both are valid integer sequences, and they collide.
    result = validate_trace([
        {"type": "task.completed", "sequence": 1, "actorId": "a"},
        {"type": "task.completed", "sequence": 1.0, "actorId": "a"},
        {"type": "task.completed", "sequence": 2.0, "actorId": "a"},
    ])

    assert [(finding["code"], finding["message"]) for finding in result["findings"]] == [("fixture.duplicate_id", "Duplicate id: 1.0")]
    assert [event["subjectId"] for event in normalize_trace([
        {"type": "task.completed", "sequence": 2.0, "actorId": "a", "subjectId": "second"},
        {"type": "task.completed", "sequence": 1, "actorId": "a", "subjectId": "first"},
    ])["events"]] == ["first", "second"]


def test_unsequenced_events_follow_all_numbered_events() -> None:
    result = normalize_trace([
        {"type": "task.completed", "actorId": "a", "subjectId": "unsequenced"},
        {"type": "task.completed", "sequence": 9007199254740991, "actorId": "a", "subjectId": "largest"},
        {"type": "task.completed", "sequence": -5, "actorId": "a", "subjectId": "negative"},
    ])

    assert [event["subjectId"] for event in result["events"]] == ["negative", "largest", "unsequenced"]


def test_blank_values_use_python_whitespace() -> None:
    result = validate_trace([
        {"type": "task.completed", "sequence": 1, "actorId": "\x1c\x85 \t"},
        {"type": "task.completed", "sequence": 2, "actorId": "\ufeff"},
    ])

    assert [finding["path"] for finding in result["findings"]] == ["trace[0].actorId"]
