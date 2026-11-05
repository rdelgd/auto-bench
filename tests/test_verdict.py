"""The verdict projection: grouping, supersession, invalidation, retraction, and findings."""

from __future__ import annotations

import copy
import json
from typing import Any

from lasm_core import RecordedEvent, project_verdicts

CELL = "fruitfly-1b.remove-exactness.single-hop"
PREREG = "2026-11-05"
COMMIT_X = "a" * 40
COMMIT_Y = "b" * 40


def measurement(attempt: int = 1, *, cell: str = CELL, commit: str = COMMIT_X, larql: str = "0.2.0", vindex: str = "pin-1") -> RecordedEvent:
    return {
        "streamId": f"experiment:{cell}@{attempt}",
        "streamVersion": 1,
        "type": "evidence.recorded",
        "schemaVersion": 1,
        "data": {
            "cellId": cell,
            "attempt": attempt,
            "target": {"binding": "weight-patch", "ref": "atlantis-capital"},
            "vindexPin": vindex,
            "patchDigest": "sha256:abc",
            "patchrigCommit": commit,
            "larqlVersion": larql,
            "larqlBinarySha256": "f" * 64,
            "manipulationCheck": "passed",
            "tier": "Tier 1",
            "claimScope": "Gemma 3 1B, N=10",
            "controlsState": "passing",
            "measurements": {"strength": 0.91},
            "recordsDigest": "sha256:def",
            "environment": {"host": "M5", "fingerprint": "m5"},
        },
    }


def verdict(
    name: str,
    value: str = "holds",
    *,
    of: RecordedEvent | None = None,
    prereg: str = PREREG,
    scorer: str = COMMIT_X,
    supersedes: str | None = None,
    **extra: Any,
) -> RecordedEvent:
    measured = of or measurement()
    measured_data: Any = measured["data"]
    data: dict[str, Any] = {
        "cellId": measured_data["cellId"],
        "attempt": measured_data["attempt"],
        "cites": {"streamId": measured["streamId"], "streamVersion": measured["streamVersion"]},
        "preregistration": prereg,
        "scorerVersion": scorer,
        "verdict": value,
        **extra,
    }
    if supersedes is not None:
        data["supersedes"] = supersedes
    return {"streamId": f"judgement:{name}", "streamVersion": 1, "type": "verdict.recorded", "schemaVersion": 1, "data": data}


def invalidation(name: str, scope: dict[str, list[str]], cites: RecordedEvent, *, version: int = 1, reason: str = "flawed") -> RecordedEvent:
    return {
        "streamId": f"judgement:invalidation@{name}",
        "streamVersion": version,
        "type": "verdict.invalidated",
        "schemaVersion": 1,
        "data": {
            "instrument": "in-context-gate",
            "scope": scope,
            "cites": {"streamId": cites["streamId"], "streamVersion": cites["streamVersion"]},
            "reason": reason,
        },
    }


def retraction(name: str, cites: str) -> RecordedEvent:
    return {
        "streamId": f"judgement:invalidation-retraction@{name}",
        "streamVersion": 1,
        "type": "invalidation.retracted",
        "schemaVersion": 1,
        "data": {"cites": cites, "reason": "it was sound"},
    }


def codes(projection: Any) -> list[tuple[str, str]]:
    return [(item["code"], item["path"]) for item in projection["findings"]]


def only_cell(projection: Any) -> Any:
    (cell,) = projection["cells"]
    return cell


def test_single_verdict_is_current_with_its_citations() -> None:
    m = measurement()
    v = verdict("v1", "cannot-tell", of=m, cannotTellReason="too-few-values", detail="one probe")
    projection = project_verdicts([m, v])
    assert projection["findings"] == []
    assert only_cell(projection) == {
        "cellId": CELL,
        "attempt": 1,
        "preregistration": PREREG,
        "status": "current",
        "current": {
            "cellId": CELL,
            "attempt": 1,
            "preregistration": PREREG,
            "scorerVersion": COMMIT_X,
            "verdict": "cannot-tell",
            "cannotTellReason": "too-few-values",
            "detail": "one probe",
            "manipulationCheck": "passed",
            "source": {"streamId": "judgement:v1", "streamVersion": 1},
            "measurement": {"streamId": m["streamId"], "streamVersion": 1},
        },
    }


def test_rescore_supersedes_the_original() -> None:
    m = measurement()
    projection = project_verdicts([m, verdict("v1", of=m), verdict("v2", "fails", of=m, scorer=COMMIT_Y, supersedes="judgement:v1")])
    cell = only_cell(projection)
    assert cell["status"] == "current" and cell["current"]["verdict"] == "fails"
    assert cell["current"]["source"]["streamId"] == "judgement:v2"


def test_preregistrations_and_attempts_never_fold_together() -> None:
    m1, m2 = measurement(1), measurement(2)
    projection = project_verdicts([
        m1, m2,
        verdict("a1-p1", of=m1), verdict("a1-p2", of=m1, prereg="2026-12-01"),
        verdict("a2-p1", "fails", of=m2),
    ])
    assert projection["findings"] == []
    assert [(cell["attempt"], cell["preregistration"], cell["status"]) for cell in projection["cells"]] == [
        (1, PREREG, "current"), (1, "2026-12-01", "current"), (2, PREREG, "current"),
    ]


def test_unsuperseded_verdicts_conflict_without_a_tie_break() -> None:
    m = measurement()
    projection = project_verdicts([m, verdict("v1", of=m), verdict("v2", "fails", of=m, scorer=COMMIT_Y)])
    cell = only_cell(projection)
    assert cell["status"] == "conflicting" and "current" not in cell
    assert cell["candidates"] == [{"streamId": "judgement:v1", "streamVersion": 1}, {"streamId": "judgement:v2", "streamVersion": 1}]
    assert codes(projection) == [("verdict.conflict", "events[1]"), ("verdict.conflict", "events[2]")]


def test_invalid_supersedes_is_ignored_and_reported() -> None:
    m1, m2 = measurement(1), measurement(2)
    other_attempt = verdict("other", of=m2)
    projection = project_verdicts([
        m1, m2, other_attempt,
        verdict("v1", of=m1),
        verdict("v2", of=m1, supersedes="judgement:missing"),
        verdict("v3", of=m1, supersedes="judgement:other"),
    ])
    groups = {cell["attempt"]: cell for cell in projection["cells"]}
    assert groups[1]["status"] == "conflicting" and len(groups[1]["candidates"]) == 3
    assert groups[2]["status"] == "current"
    assert ("verdict.invalid_supersedes", "events[4].data.supersedes") in codes(projection)
    assert ("verdict.invalid_supersedes", "events[5].data.supersedes") in codes(projection)


def test_supersession_cycles_are_unresolved() -> None:
    m = measurement()
    projection = project_verdicts([m, verdict("a", of=m, supersedes="judgement:b"), verdict("b", of=m, supersedes="judgement:a")])
    assert only_cell(projection)["status"] == "unresolved"
    assert codes(projection) == [("verdict.supersedes_cycle", "events[1].data.supersedes"), ("verdict.supersedes_cycle", "events[2].data.supersedes")]

    projection = project_verdicts([m, verdict("self", of=m, supersedes="judgement:self")])
    assert only_cell(projection)["status"] == "unresolved"
    assert codes(projection) == [("verdict.supersedes_cycle", "events[1].data.supersedes")]

    # A verdict outside the cycle that supersedes into it stays a candidate.
    projection = project_verdicts([
        m, verdict("a", of=m, supersedes="judgement:b"), verdict("b", of=m, supersedes="judgement:a"),
        verdict("c", "fails", of=m, supersedes="judgement:a"),
    ])
    assert only_cell(projection)["current"]["source"]["streamId"] == "judgement:c"


def test_only_unknown_measurements_is_unresolved() -> None:
    projection = project_verdicts([verdict("v1", of=measurement())])
    assert only_cell(projection)["status"] == "unresolved"
    assert codes(projection) == [("verdict.unknown_measurement", "events[0].data.cites")]


def test_invalidation_by_citation() -> None:
    m = measurement()
    v = verdict("v1", of=m)
    inv = invalidation("gate@2026-11-06", {"vindexPins": ["pin-1"]}, v)
    cell = only_cell(project_verdicts([m, v, inv]))
    assert cell["status"] == "invalidated" and "current" not in cell
    assert cell["invalidatedBy"] == ["judgement:invalidation@gate@2026-11-06"]


def test_invalidation_condition_reaches_later_verdicts_only_in_scope() -> None:
    m_old, m_new = measurement(1, larql="0.2.0"), measurement(2, larql="0.2.1")
    seed = verdict("seed", of=m_old)
    inv = invalidation("gate@2026-11-06", {"larqlVersions": ["0.2.0"]}, seed)
    m_later = measurement(3, larql="0.2.0")
    projection = project_verdicts([m_old, seed, inv, m_new, verdict("new", of=m_new), m_later, verdict("later", of=m_later)])
    statuses = {cell["attempt"]: cell["status"] for cell in projection["cells"]}
    assert statuses == {1: "invalidated", 2: "current", 3: "invalidated"}
    assert projection["findings"] == []


def test_every_present_scope_list_must_match() -> None:
    m = measurement(commit=COMMIT_X, larql="0.2.0", vindex="pin-1")
    m9 = measurement(9, larql="0.2.0", vindex="pin-2")
    cited = verdict("cited", of=m9)
    narrow = invalidation("narrow@d", {"larqlVersions": ["0.2.0"], "vindexPins": ["pin-2"]}, cited)
    # Attempt 1 matches the larql version but not the vindex pin, so it stays current.
    projection = project_verdicts([m, m9, verdict("v", of=m), cited, narrow])
    assert {cell["attempt"]: cell["status"] for cell in projection["cells"]} == {1: "current", 9: "invalidated"}
    assert projection["findings"] == []


def test_scorer_and_measuring_commits_match_separately() -> None:
    m = measurement(commit=COMMIT_X)
    original = verdict("orig", of=m, scorer=COMMIT_X)
    rescore = verdict("fixed", "fails", of=m, scorer=COMMIT_Y, supersedes="judgement:orig")
    by_scorer = invalidation("scorer@d", {"scorerVersions": [COMMIT_X]}, original)
    cell = only_cell(project_verdicts([m, original, rescore, by_scorer]))
    assert cell["status"] == "current" and cell["current"]["source"]["streamId"] == "judgement:fixed"

    by_measuring = invalidation("measuring@d", {"patchrigCommits": [COMMIT_X]}, original)
    cell = only_cell(project_verdicts([m, original, rescore, by_measuring]))
    assert cell["status"] == "invalidated"


def test_superseded_verdict_does_not_return_and_retraction_restores_the_replacement() -> None:
    m = measurement()
    a = verdict("a", of=m)
    b = verdict("b", "fails", of=m, scorer=COMMIT_Y, supersedes="judgement:a")
    inv = invalidation("b-flaw@d", {"scorerVersions": [COMMIT_Y]}, b)
    cell = only_cell(project_verdicts([m, a, b, inv]))
    assert cell["status"] == "invalidated" and "current" not in cell

    cell = only_cell(project_verdicts([m, a, b, inv, retraction("r@d", inv["streamId"])]))
    assert cell["status"] == "current" and cell["current"]["source"]["streamId"] == "judgement:b"
    assert "invalidatedBy" not in cell


def test_empty_scope_matches_by_citation_only() -> None:
    m1, m2 = measurement(1), measurement(2)
    cited = verdict("cited", of=m1)
    inv = invalidation("empty@d", {}, cited)
    projection = project_verdicts([m1, m2, cited, verdict("other", of=m2), inv])
    assert {cell["attempt"]: cell["status"] for cell in projection["cells"]} == {1: "invalidated", 2: "current"}
    assert codes(projection) == [("invalidation.empty_scope", "events[4].data.scope")]


def test_inconsistent_condition_uses_the_first_event() -> None:
    m1, m2 = measurement(1, larql="0.2.0"), measurement(2, larql="0.2.1")
    v1, v2 = verdict("v1", of=m1), verdict("v2", of=m2)
    first = invalidation("gate@d", {"larqlVersions": ["0.2.0"]}, v1)
    second = invalidation("gate@d", {"larqlVersions": ["0.2.1"]}, v2, version=2)
    projection = project_verdicts([m1, m2, v1, v2, first, second])
    statuses = {cell["attempt"]: cell["status"] for cell in projection["cells"]}
    # v2 is still removed by citation, and the mismatch is reported; v2 is also outside the first condition.
    assert statuses == {1: "invalidated", 2: "invalidated"}
    assert codes(projection) == [
        ("invalidation.inconsistent_condition", "events[5].data"),
        ("invalidation.cited_outside_scope", "events[5].data.cites"),
    ]


def test_cited_outside_scope_is_removed_and_reported() -> None:
    m = measurement(larql="0.2.1")
    v = verdict("v", of=m)
    projection = project_verdicts([m, v, invalidation("gate@d", {"larqlVersions": ["0.2.0"]}, v)])
    assert only_cell(projection)["status"] == "invalidated"
    assert codes(projection) == [("invalidation.cited_outside_scope", "events[2].data.cites")]


def test_retraction_of_an_unknown_invalidation_is_reported() -> None:
    m = measurement()
    v = verdict("v", of=m)
    r = retraction("r@d", "judgement:invalidation@nothing@d")
    projection = project_verdicts([m, v, r, retraction("rr@d", r["streamId"])])
    assert only_cell(projection)["status"] == "current"
    assert codes(projection) == [
        ("retraction.unknown_invalidation", "events[2].data.cites"),
        ("retraction.unknown_invalidation", "events[3].data.cites"),
    ]


def test_unreadable_and_foreign_events() -> None:
    m = measurement()
    v = verdict("v", of=m)
    bad_reason = verdict("bad", "holds", of=m, cannotTellReason="no-probes")
    future: RecordedEvent = {**v, "streamId": "judgement:future", "schemaVersion": 3}
    foreign: RecordedEvent = {"streamId": "policy:x", "streamVersion": 1, "type": "policy.accepted", "schemaVersion": 1, "data": {}}
    projection = project_verdicts([foreign, m, v, bad_reason, future])
    assert only_cell(projection)["status"] == "current"
    assert codes(projection) == [
        ("ledger.invalid_event_data", "events[3].data"),
        ("ledger.unsupported_event", "events[4].schemaVersion"),
    ]
    assert "verdict.reason_not_allowed" not in projection["findings"][0]["message"]
    assert "cannotTellReason" in projection["findings"][0]["message"]


def test_projection_is_deterministic_sorted_and_non_mutating() -> None:
    m1, m2 = measurement(1, cell="z-cell"), measurement(1, cell="a-cell")
    events = [m1, m2, verdict("z", of=m1), verdict("a", of=m2)]
    snapshot = copy.deepcopy(events)
    first = project_verdicts(events)
    assert json.dumps(project_verdicts(copy.deepcopy(events))) == json.dumps(first)
    assert events == snapshot
    assert [cell["cellId"] for cell in first["cells"]] == ["a-cell", "z-cell"]
    assert project_verdicts([]) == {"cells": [], "runs": [], "findings": []}
