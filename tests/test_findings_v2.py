"""Version 2 evidence and verdicts, built from patchrig's two-step finding of 2026-11-04."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator

import lasm_core
from lasm_core import RecordedEvent, project_verdicts, validate_ledger_event_data
from lasm_core.domain import ValidationFinding

SCHEMA_DIR = Path(lasm_core.__file__).parent / "schemas" / "ledger"
COMMIT = "ec8e708727c6760577e8ae1cceed0adce450528a"
PREREG = "2026-11-03 — pre-registered: the two-step observer"
CLAIM = "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10"
LUNA_RUN, JEV_RUN = "two-step-20261104-092458", "two-step-20261104-092604"
LUNA = {"kind": "decisions", "model": "gpt-6-luna", "host": "api.openai.com", "served": "2026-11-04"}
JEV = {"kind": "decisions", "model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "route": "typesafe-ai", "served": "2026-11-04"}


def measurement_data(run_id: str, adapter: dict[str, str], thresholds: tuple[float, float]) -> dict[str, Any]:
    return {
        "runId": run_id,
        "attempt": 1,
        "runKind": "two-step",
        "recordsDigest": "sha256:fad5f0568cd89679803ac73aebf23febdf1ee41bca8392e0378ed60c17e45f09",
        "patchrigCommit": COMMIT,
        "preregistration": PREREG,
        "claimScope": f"the two-step observer on {adapter['model']} as served 2026-11-04, fictional catalogues (corpus generator v4), seeds 110–149",
        "adapter": adapter,
        "inputs": [
            {"role": "tune", "runId": "check-20261104-092318", "recordsDigest": "sha256:10a3", "seeds": "100-109"},
            {"role": "confirm", "runId": "check-20261104-092348", "recordsDigest": "sha256:6943", "seeds": "110-149"},
        ],
        "fixture": {"generatorVersion": 4, "n": 12},
        "measurements": [
            {
                "carrier": "chart",
                "tunedThreshold": thresholds[0],
                "items": {"classification": 480, "abstention": 480},
                "asChosen": {"classification": 0.9979, "abstention": 0.3333, "balanced": 0.6656},
                "twoStep": {"classification": 0.9604, "abstention": 0.8563, "balanced": 0.9083},
                "gain": 0.2427, "lo": 0.2146, "hi": 0.2708,
            },
            {"carrier": "explanation-and-training", "tunedThreshold": thresholds[1], "gain": 0.0667, "lo": 0.0333, "hi": 0.1},
        ],
    }


def verdict_data(run_id: str, model: str, carrier: str, verdict: str, predicted: list[str], gain: float, **extra: Any) -> dict[str, Any]:
    return {
        "runId": run_id,
        "attempt": 1,
        "claimId": f"two-step/{model}/{carrier}",
        "claim": CLAIM,
        "cites": {"streamId": f"experiment:{run_id}@1", "streamVersion": 1},
        "preregistration": PREREG,
        "scorerVersion": COMMIT,
        "verdict": verdict,
        "predicted": predicted,
        "statistics": {"margin": 0.10, "gain": gain},
        **extra,
    }


def event(stream: str, event_type: str, data: dict[str, Any], version: int = 2) -> RecordedEvent:
    return {"streamId": stream, "streamVersion": 1, "type": event_type, "schemaVersion": version, "data": data}


def finding_log() -> list[RecordedEvent]:
    """The two-step finding: two confirmation runs, four claim verdicts."""
    return [
        event(f"experiment:{LUNA_RUN}@1", "evidence.recorded", measurement_data(LUNA_RUN, LUNA, (0.02, 0.20))),
        event(f"experiment:{JEV_RUN}@1", "evidence.recorded", measurement_data(JEV_RUN, JEV, (0.30, 0.30))),
        event("judgement:luna/chart", "verdict.recorded", verdict_data(LUNA_RUN, "gpt-6-luna", "chart", "holds", ["holds"], 0.2427)),
        event("judgement:jev/chart", "verdict.recorded", verdict_data(JEV_RUN, "typesafe-ai-jev", "chart", "holds", ["holds"], 0.2083)),
        event("judgement:luna/eat", "verdict.recorded", verdict_data(LUNA_RUN, "gpt-6-luna", "explanation-and-training", "inconclusive", ["inconclusive", "fails"], 0.0667)),
        event("judgement:jev/eat", "verdict.recorded", verdict_data(JEV_RUN, "typesafe-ai-jev", "explanation-and-training", "fails", ["fails"], 0.0312)),
    ]


def codes(projection: Any) -> list[tuple[str, str]]:
    return [(item["code"], item["path"]) for item in projection["findings"]]


def statuses(projection: Any) -> dict[str, str]:
    return {run["claimId"]: run["status"] for run in projection["runs"]}


# Schemas -------------------------------------------------------------------


def validator(event_type: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads((SCHEMA_DIR / f"{event_type}.v2.schema.json").read_text(encoding="utf-8")))


def agrees(event_type: str, data: Any) -> list[ValidationFinding]:
    python = validate_ledger_event_data(event_type, 2, data)
    reference = validator(event_type).is_valid(data)
    assert python["valid"] == reference, (python["findings"], [error.message for error in validator(event_type).iter_errors(data)])
    return list(python["findings"])


def test_the_finding_validates_as_version_2_and_not_as_version_1() -> None:
    for recorded in finding_log():
        assert agrees(recorded["type"], recorded["data"]) == []
        assert not validate_ledger_event_data(recorded["type"], 1, recorded["data"])["valid"]


MEASUREMENT = measurement_data(LUNA_RUN, LUNA, (0.02, 0.20))
VERDICT = verdict_data(LUNA_RUN, "gpt-6-luna", "chart", "holds", ["holds"], 0.2427)


def without(data: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {key: value for key, value in data.items() if key not in keys}


def with_value(data: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    return {**copy.deepcopy(data), key: value}


INVALID = [
    ("evidence.recorded", without(MEASUREMENT, "adapter"), "format.missing_property", "data.adapter"),
    ("evidence.recorded", with_value(MEASUREMENT, "adapter", without(LUNA, "served")), "format.missing_property", "data.adapter.served"),
    ("evidence.recorded", with_value(MEASUREMENT, "larqlVersion", "0.2.0"), "format.unknown_property", "data.larqlVersion"),
    ("evidence.recorded", with_value(MEASUREMENT, "manipulationCheck", "passed"), "format.unknown_property", "data.manipulationCheck"),
    ("evidence.recorded", with_value(MEASUREMENT, "measurements", [{"carrier": "chart", "tunedThreshold": "0.02"}]), "format.invalid_type", "data.measurements[0].tunedThreshold"),
    ("evidence.recorded", with_value(MEASUREMENT, "measurements", {"chart": 1}), "format.invalid_type", "data.measurements"),
    ("verdict.recorded", without(VERDICT, "claimId"), "format.missing_property", "data.claimId"),
    ("verdict.recorded", without(VERDICT, "claim"), "format.missing_property", "data.claim"),
    ("verdict.recorded", with_value(VERDICT, "predicted", "inconclusive or fails"), "format.invalid_type", "data.predicted"),
    ("verdict.recorded", with_value(VERDICT, "predicted", ["holds_weakly"]), "format.invalid_value", "data.predicted[0]"),
    ("verdict.recorded", with_value(VERDICT, "gain", 0.24), "format.unknown_property", "data.gain"),
    ("verdict.recorded", with_value(VERDICT, "cites", {"runId": LUNA_RUN}), "format.missing_property", "data.cites.streamId"),
    ("verdict.recorded", {**VERDICT, "verdict": "cannot-tell"}, "verdict.reason_required", "data.cannotTellReason"),
    ("verdict.recorded", {**VERDICT, "cannotTellReason": "no-probes"}, "verdict.reason_not_allowed", "data.cannotTellReason"),
    ("evidence.recorded", with_value(MEASUREMENT, "patchrigCommit", "ec8e708727c6"), "format.invalid_value", "data.patchrigCommit"),
    ("evidence.recorded", with_value(MEASUREMENT, "patchrigCommit", COMMIT + "0"), "format.invalid_value", "data.patchrigCommit"),
    ("verdict.recorded", with_value(VERDICT, "scorerVersion", "two-step@ec8e708727c6"), "format.invalid_value", "data.scorerVersion"),
    ("evidence.recorded", with_value(MEASUREMENT, "adapter", {**LUNA, "served": "2026-11-4"}), "format.invalid_value", "data.adapter.served"),
]


@pytest.mark.parametrize(("event_type", "data", "code", "path"), INVALID)
def test_named_fields_are_strict(event_type: str, data: dict[str, Any], code: str, path: str) -> None:
    findings = agrees(event_type, data)
    assert {"code": code, "path": path} in [{"code": item["code"], "path": item["path"]} for item in findings]


def test_free_form_objects_stay_open() -> None:
    measured = copy.deepcopy(MEASUREMENT)
    measured["fixture"] = {"anything": [1, {"nested": None}]}
    measured["measurements"].append({"newScorerNumber": 3, "notes": ["free"]})
    assert agrees("evidence.recorded", measured) == []
    assert agrees("verdict.recorded", with_value(VERDICT, "statistics", {"bootstrap": {"seed": 7, "draws": 10000}})) == []
    assert agrees("verdict.recorded", {**VERDICT, "verdict": "cannot-tell", "cannotTellReason": "too-few-values", "predicted": ["holds"]}) == []


def test_invalidation_scope_accepts_adapters_within_version_1() -> None:
    scope = {"adapters": [{"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh"}, {"model": "gpt-6-luna", "host": "api.openai.com", "served": "2026-11-04"}]}
    data = {"instrument": "decisions-adapter", "scope": scope, "cites": {"streamId": "judgement:x", "streamVersion": 1}, "reason": "r"}
    assert validate_ledger_event_data("verdict.invalidated", 1, data)["valid"]
    bad = copy.deepcopy(data)
    bad["scope"]["adapters"][0] = {"model": "typesafe-ai/jev"}
    assert [item["path"] for item in validate_ledger_event_data("verdict.invalidated", 1, bad)["findings"]] == ["data.scope.adapters[0].host"]
    unpadded = copy.deepcopy(data)
    unpadded["scope"]["adapters"][1]["served"] = "2026-11-4"
    assert [item["path"] for item in validate_ledger_event_data("verdict.invalidated", 1, unpadded)["findings"]] == ["data.scope.adapters[1].served"]


def test_version_1_keeps_accepting_any_commit_spelling() -> None:
    # Length rules are version 2 only; version 1 stays exactly as released in 0.5.0.
    verdict = cell_log()[1]
    short = {**dict(verdict["data"]), "scorerVersion": "ec8e708727c6"}  # type: ignore[arg-type]
    assert validate_ledger_event_data("verdict.recorded", 1, short)["valid"]


# Projection ----------------------------------------------------------------


def test_the_finding_projects_as_four_current_runs() -> None:
    projection = project_verdicts(finding_log())
    assert projection["findings"] == [] and projection["cells"] == []
    assert statuses(projection) == {
        "two-step/gpt-6-luna/chart": "current",
        "two-step/gpt-6-luna/explanation-and-training": "current",
        "two-step/typesafe-ai-jev/chart": "current",
        "two-step/typesafe-ai-jev/explanation-and-training": "current",
    }
    luna_eat = next(run for run in projection["runs"] if run["claimId"] == "two-step/gpt-6-luna/explanation-and-training")
    assert luna_eat["current"] == {
        "runId": LUNA_RUN,
        "attempt": 1,
        "claimId": "two-step/gpt-6-luna/explanation-and-training",
        "claim": CLAIM,
        "preregistration": PREREG,
        "scorerVersion": COMMIT,
        "verdict": "inconclusive",
        "predicted": ["inconclusive", "fails"],
        "statistics": {"margin": 0.10, "gain": 0.0667},
        "adapter": LUNA,
        "source": {"streamId": "judgement:luna/eat", "streamVersion": 1},
        "measurement": {"streamId": f"experiment:{LUNA_RUN}@1", "streamVersion": 1},
    }


def test_claims_on_one_run_never_conflict_but_two_verdicts_for_one_claim_do() -> None:
    log = finding_log()
    again = event("judgement:luna/chart-again", "verdict.recorded", verdict_data(LUNA_RUN, "gpt-6-luna", "chart", "fails", ["holds"], 0.01))
    projection = project_verdicts([*log, again])
    assert statuses(projection)["two-step/gpt-6-luna/chart"] == "conflicting"
    assert [code for code, _ in codes(projection)] == ["verdict.conflict", "verdict.conflict"]
    rescore = event(
        "judgement:luna/chart-rescore", "verdict.recorded",
        verdict_data(LUNA_RUN, "gpt-6-luna", "chart", "holds", ["holds"], 0.25, supersedes="judgement:luna/chart"),
    )
    projection = project_verdicts([*log, rescore])
    chart = next(run for run in projection["runs"] if run["claimId"] == "two-step/gpt-6-luna/chart")
    assert chart["status"] == "current" and chart["current"]["source"]["streamId"] == "judgement:luna/chart-rescore"


def invalidation(name: str, scope: dict[str, Any], cites: str) -> RecordedEvent:
    data = {"instrument": "decisions-adapter", "scope": scope, "cites": {"streamId": cites, "streamVersion": 1}, "reason": "flawed"}
    return event(f"judgement:invalidation@{name}", "verdict.invalidated", data, version=1)


def test_an_adapter_invalidation_reaches_one_gateway_only() -> None:
    inv = invalidation("jev@2026-11-05", {"adapters": [{"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh"}]}, "judgement:jev/chart")
    projection = project_verdicts([*finding_log(), inv])
    assert statuses(projection) == {
        "two-step/gpt-6-luna/chart": "current",
        "two-step/gpt-6-luna/explanation-and-training": "current",
        "two-step/typesafe-ai-jev/chart": "invalidated",
        "two-step/typesafe-ai-jev/explanation-and-training": "invalidated",
    }
    assert projection["findings"] == []


@pytest.mark.parametrize(
    ("entry", "jev_invalidated"),
    [
        ({"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "served": "2026-11-04"}, True),
        ({"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "served": "2026-11-05"}, False),
        ({"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "route": "typesafe-ai"}, True),
        ({"model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "route": "other-provider"}, False),
        ({"model": "typesafe-ai/jev", "host": "api.typesafe.ai"}, False),
        ({"model": "gpt-6-luna", "host": "ai-gateway.vercel.sh"}, False),
    ],
)
def test_adapter_entries_match_every_given_field(entry: dict[str, str], jev_invalidated: bool) -> None:
    log = [event(f"experiment:{JEV_RUN}@1", "evidence.recorded", measurement_data(JEV_RUN, JEV, (0.3, 0.3))), finding_log()[3]]
    # Cite a stream that isn't in the log, so only the condition can remove the verdict.
    projection = project_verdicts([*log, invalidation("x@d", {"adapters": [entry]}, "judgement:elsewhere")])
    assert (projection["runs"][0]["status"] == "invalidated") is jev_invalidated


def test_several_entries_are_alternatives() -> None:
    entries = [{"model": "nobody", "host": "nowhere"}, {"model": "gpt-6-luna", "host": "api.openai.com"}]
    projection = project_verdicts([*finding_log(), invalidation("x@d", {"adapters": entries}, "judgement:elsewhere")])
    assert {claim: status for claim, status in statuses(projection).items() if "luna" in claim} == {
        "two-step/gpt-6-luna/chart": "invalidated",
        "two-step/gpt-6-luna/explanation-and-training": "invalidated",
    }


# Versions side by side -------------------------------------------------------


def cell_log() -> list[RecordedEvent]:
    measured = {
        "cellId": "fruitfly-1b.single-hop", "attempt": 1,
        "target": {"binding": "weight-patch", "ref": "atlantis"},
        "vindexPin": "pin-1", "patchDigest": "sha256:p", "patchrigCommit": COMMIT,
        "larqlVersion": "0.2.0", "larqlBinarySha256": "f" * 64, "manipulationCheck": "passed",
        "tier": "Tier 1", "claimScope": "toy", "controlsState": "passing",
        "measurements": {}, "recordsDigest": "sha256:r", "environment": {"host": "M5", "fingerprint": "m5"},
    }
    judged = {
        "cellId": "fruitfly-1b.single-hop", "attempt": 1,
        "cites": {"streamId": "experiment:fruitfly@1", "streamVersion": 1},
        "preregistration": PREREG, "scorerVersion": COMMIT, "verdict": "holds",
    }
    return [
        event("experiment:fruitfly@1", "evidence.recorded", measured, version=1),
        event("judgement:fruitfly", "verdict.recorded", judged, version=1),
    ]


def test_versions_project_side_by_side() -> None:
    projection = project_verdicts([*cell_log(), *finding_log()])
    assert projection["findings"] == []
    assert [cell["status"] for cell in projection["cells"]] == ["current"]
    assert set(statuses(projection).values()) == {"current"}
    assert projection["cells"] == project_verdicts(cell_log())["cells"]


@pytest.mark.parametrize(
    ("scope", "cell_invalidated", "runs_invalidated"),
    [
        ({"larqlVersions": ["0.2.0"]}, True, False),
        ({"vindexPins": ["pin-1"]}, True, False),
        ({"adapters": [{"model": "gpt-6-luna", "host": "api.openai.com"}]}, False, True),
        ({"patchrigCommits": [COMMIT]}, True, True),
        ({"scorerVersions": [COMMIT]}, True, True),
        ({"larqlVersions": ["0.2.0"], "adapters": [{"model": "gpt-6-luna", "host": "api.openai.com"}]}, False, False),
    ],
)
def test_scope_lists_reach_only_measurements_with_their_field(scope: dict[str, Any], cell_invalidated: bool, runs_invalidated: bool) -> None:
    projection = project_verdicts([*cell_log(), *finding_log(), invalidation("x@d", scope, "judgement:elsewhere")])
    assert (projection["cells"][0]["status"] == "invalidated") is cell_invalidated
    luna = [run["status"] for run in projection["runs"] if "luna" in run["claimId"]]
    assert all(status == ("invalidated" if runs_invalidated else "current") for status in luna)


def test_cross_version_citations_and_supersessions_are_reported() -> None:
    cells = cell_log()
    v2_citing_v1 = event("judgement:mixed", "verdict.recorded", {**VERDICT, "claimId": "mixed", "cites": {"streamId": "experiment:fruitfly@1", "streamVersion": 1}})
    v2_superseding_v1 = event("judgement:cross", "verdict.recorded", {**VERDICT, "claimId": "cross", "supersedes": "judgement:fruitfly"})
    projection = project_verdicts([*cells, *finding_log(), v2_citing_v1, v2_superseding_v1])
    assert ("verdict.measurement_version_mismatch", "events[8].data.cites") in codes(projection)
    assert ("verdict.invalid_supersedes", "events[9].data.supersedes") in codes(projection)
    assert {run["claimId"]: run["status"] for run in projection["runs"]}["mixed"] == "unresolved"
    assert projection["cells"][0]["status"] == "current"


def test_equal_ids_across_versions_never_meet() -> None:
    cells = cell_log()
    same_id = event("judgement:same", "verdict.recorded", {
        **VERDICT, "runId": "fruitfly-1b.single-hop", "claimId": "c", "cites": {"streamId": f"experiment:{LUNA_RUN}@1", "streamVersion": 1},
    })
    projection = project_verdicts([*cells, finding_log()[0], same_id])
    assert projection["findings"] == []
    assert [cell["status"] for cell in projection["cells"]] == ["current"]
    assert [run["status"] for run in projection["runs"]] == ["current"]


def test_projection_of_runs_is_deterministic_and_non_mutating() -> None:
    log = [*finding_log(), *cell_log()]
    snapshot = copy.deepcopy(log)
    first = json.dumps(project_verdicts(log))
    assert json.dumps(project_verdicts(copy.deepcopy(log))) == first
    assert log == snapshot
    assert [run["runId"] for run in project_verdicts(log)["runs"]] == [LUNA_RUN, LUNA_RUN, JEV_RUN, JEV_RUN]
