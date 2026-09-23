from __future__ import annotations

from typing import Any

import lasm_core
from lasm_core import evaluate_conformance, fixtures
from lasm_core.fixtures import routine_maintenance_conformance_case as base_case
from lasm_core.fixtures import routine_maintenance_evaluation


def dimension(evaluation: Any, name: str) -> Any:
    return next(result for result in evaluation["dimensions"] if result["dimension"] == name)


def test_fixture_evaluates_a_complete_lasm_episode_without_io_dependencies() -> None:
    assert routine_maintenance_evaluation["valid"] is True
    assert routine_maintenance_evaluation["conformant"] is True
    assert [(result["dimension"], result["status"]) for result in routine_maintenance_evaluation["dimensions"]] == [
        ("intent-fidelity", "pass"),
        ("semantic-fidelity", "pass"),
        ("reality-model-validity", "pass"),
        ("state-and-outcome-validity", "pass"),
        ("control-surface-quality", "pass"),
        ("reality-coverage", "pass"),
        ("evidence-and-attribution", "pass"),
        ("governance", "pass"),
    ]
    assert all(
        reference.startswith("trace:")
        for result in routine_maintenance_evaluation["dimensions"]
        for finding in result["findings"]
        for reference in finding["evidenceRefs"]
    )


def test_public_exports_expose_the_lasm_models_conformance_evaluator_and_fixture() -> None:
    assert lasm_core.evaluate_conformance is evaluate_conformance
    assert len(lasm_core.logical_assembly_entries(fixtures.service_scheduling_assembly)) == 10
    assert fixtures.routine_maintenance_conformance_case is base_case


def test_evaluation_explains_missing_confirmation_and_control_primitive() -> None:
    trace = [
        event for event in base_case["trace"]
        if event["type"] != "human.confirmation_received" and event.get("subjectId") != "tool.create-appointment"
    ]
    evaluation = evaluate_conformance({**base_case, "trace": trace})
    governance = dimension(evaluation, "governance")
    control = dimension(evaluation, "control-surface-quality")

    assert evaluation["conformant"] is False
    assert governance["status"] == "fail"
    assert any(finding["code"] == "governance.confirmation_missing" for finding in governance["findings"])
    assert control["status"] == "fail"
    assert any(finding["code"] == "control.mcp_primitive_not_used" for finding in control["findings"])


def test_governance_requires_confirmation_before_a_sensitive_tool_call() -> None:
    trace = [
        {**event, "sequence": 41} if event["type"] == "human.confirmation_received" else event
        for event in base_case["trace"]
    ]
    governance = dimension(evaluate_conformance({**base_case, "trace": trace}), "governance")

    assert governance["status"] == "fail"
    assert any(finding["code"] == "governance.confirmation_too_late" for finding in governance["findings"])


def test_reality_model_validity_identifies_stale_assembly_provenance() -> None:
    assembly = {
        **base_case["assembly"],
        "provenance": [
            {**source, "status": "stale"} if index == 0 else source
            for index, source in enumerate(base_case["assembly"]["provenance"])
        ],
    }
    reality = dimension(evaluate_conformance({**base_case, "assembly": assembly}), "reality-model-validity")

    assert reality["status"] == "fail"
    assert any(
        finding["code"] == "reality.stale_source" and finding.get("attribution") == "reality-model"
        for finding in reality["findings"]
    )


def test_reality_coverage_attributes_a_lossy_projection() -> None:
    def lossy(resource: Any) -> Any:
        if resource["id"] != "resource.vehicle-eligibility":
            return resource
        projection = resource["projection"]
        return {
            **resource,
            "projection": {
                **projection,
                "assemblyEntryIds": [id for id in projection["assemblyEntryIds"] if id != "relation.appointment-requires-eligibility"],
            },
        }

    mcp_surfaces = [{**surface, "resources": [lossy(resource) for resource in surface["resources"]]} for surface in base_case["mcpSurfaces"]]
    coverage = dimension(evaluate_conformance({**base_case, "mcpSurfaces": mcp_surfaces}), "reality-coverage")

    assert coverage["status"] == "fail"
    assert any(
        finding["code"] == "coverage.assembly_entry_not_projected"
        and finding.get("attribution") == "projection"
        and "relation.appointment-requires-eligibility" in finding["assemblyEntryIds"]
        for finding in coverage["findings"]
    )


def test_state_evaluation_rejects_prohibited_transitions_and_outcomes() -> None:
    trace = [
        *base_case["trace"],
        {
            "type": "state.transition_committed",
            "sequence": 41,
            "actorId": "appointment-system",
            "subjectId": "transition.create-unconfirmed-appointment",
            "evidence": {"appointmentStatus": "created"},
        },
        {
            "type": "outcome.observed",
            "sequence": 42,
            "actorId": "auto-bench",
            "subjectId": "outcome.unconfirmed-appointment-created",
            "evidence": {"consent": "unconfirmed"},
        },
    ]
    state = dimension(evaluate_conformance({**base_case, "trace": trace}), "state-and-outcome-validity")

    assert state["status"] == "fail"
    assert any(finding["code"] == "state.prohibited_transition_committed" for finding in state["findings"])
    assert any(finding["code"] == "outcome.prohibited_observed" for finding in state["findings"])


def test_evidence_evaluation_identifies_an_attribution_gap() -> None:
    trace = [
        *base_case["trace"],
        {
            "type": "lasm.divergence_detected",
            "sequence": 41,
            "actorId": "auto-bench",
            "subjectId": "constraint.confirm-before-booking",
            "evidence": {"reason": "projection omitted confirmation rule"},
        },
    ]
    evidence = dimension(evaluate_conformance({**base_case, "trace": trace}), "evidence-and-attribution")

    assert evidence["status"] == "fail"
    assert any(finding["code"] == "attribution.failure_unattributed" for finding in evidence["findings"])


def test_reality_coverage_identifies_missing_required_operational_facts() -> None:
    trace = [
        {**event, "evidence": {key: value for key, value in event.get("evidence", {}).items() if key != "businessFacts"}}
        for event in base_case["trace"]
    ]
    coverage = dimension(evaluate_conformance({**base_case, "trace": trace}), "reality-coverage")

    assert coverage["status"] == "fail"
    assert any(finding["code"] == "coverage.required_fact_missing" for finding in coverage["findings"])
