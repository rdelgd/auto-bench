from __future__ import annotations

from lasm_core import (
    validate_actor_observation,
    validate_conformance_case,
    validate_harness,
    validate_logical_assembly,
    validate_mcp_surface,
    validate_operational_state,
    validate_outcome,
    validate_scenario,
    validate_skill,
    validate_state_transition,
    validate_trace,
)
from lasm_core.fixtures import (
    dealership_operations_mcp,
    routine_maintenance_conformance_case,
    routine_maintenance_scenario,
    routine_maintenance_trace,
    service_advisor_harness,
    service_scheduling_assembly,
    service_scheduling_initial_state,
    service_scheduling_observations,
    service_scheduling_outcomes,
    service_scheduling_skill,
    service_scheduling_transitions,
)


def test_representative_lasm_projections_state_episode_and_evidence_pass_validation() -> None:
    assembly, state = service_scheduling_assembly, service_scheduling_initial_state
    assert validate_logical_assembly(assembly)["valid"] is True
    assert validate_operational_state(state, assembly)["valid"] is True
    assert validate_actor_observation(service_scheduling_observations[0], state)["valid"] is True
    assert validate_state_transition(service_scheduling_transitions[0], state, assembly)["valid"] is True
    assert validate_outcome(service_scheduling_outcomes[0], state)["valid"] is True
    assert validate_scenario(routine_maintenance_scenario)["valid"] is True
    assert validate_harness(service_advisor_harness, assembly, state)["valid"] is True
    assert validate_skill(service_scheduling_skill, assembly, state)["valid"] is True
    assert validate_mcp_surface(dealership_operations_mcp, assembly, state)["valid"] is True
    assert validate_trace(routine_maintenance_trace)["valid"] is True
    assert validate_conformance_case(routine_maintenance_conformance_case)["valid"] is True


def test_validators_return_structured_findings_for_malformed_scenarios_and_traces() -> None:
    scenario_result = validate_scenario({
        **routine_maintenance_scenario,
        "title": "",
        "reality": {**routine_maintenance_scenario["reality"], "outcomeIds": []},
    })
    assert scenario_result["valid"] is False
    assert [(finding["code"], finding["path"]) for finding in scenario_result["findings"]] == [
        ("fixture.required", "scenario.title"),
        ("fixture.non_empty", "scenario.reality.outcomeIds"),
    ]

    trace_result = validate_trace([{"type": "custom.event", "sequence": -1}])
    assert trace_result["valid"] is False
    assert {finding["code"] for finding in trace_result["findings"]} == {
        "trace.unknown_event_type",
        "trace.missing_actor",
        "trace.invalid_sequence",
    }


def test_logical_assembly_validation_reports_duplicate_and_dangling_semantic_references() -> None:
    duplicate_concept = {**service_scheduling_assembly["concepts"][0], "name": "Duplicate consent"}
    assembly = {
        **service_scheduling_assembly,
        "concepts": [*service_scheduling_assembly["concepts"], duplicate_concept],
        "evaluations": [
            {**evaluation, "addressedEntryIds": [*evaluation["addressedEntryIds"], "constraint.missing"]}
            for evaluation in service_scheduling_assembly["evaluations"]
        ],
    }
    result = validate_logical_assembly(assembly)

    assert result["valid"] is False
    assert any(finding["code"] == "fixture.duplicate_id" and finding["path"] == "assembly.entries" for finding in result["findings"])
    assert any(finding["code"] == "assembly.unknown_entry" for finding in result["findings"])


def test_projection_validation_reports_references_outside_the_assembly_and_state() -> None:
    skill = {**service_scheduling_skill, "projection": {"assemblyEntryIds": ["policy.missing"], "stateFieldIds": ["field.missing"]}}
    result = validate_skill(skill, service_scheduling_assembly, service_scheduling_initial_state)

    assert result["valid"] is False
    assert {finding["code"] for finding in result["findings"]} == {"projection.unknown_assembly_entry", "projection.unknown_state_field"}


def test_conformance_case_validation_reports_mismatched_and_missing_reality_inputs() -> None:
    scenario = {
        **routine_maintenance_scenario,
        "reality": {**routine_maintenance_scenario["reality"], "assemblyVersion": "stale-version", "transitionIds": ["transition.missing"]},
    }
    result = validate_conformance_case({**routine_maintenance_conformance_case, "scenario": scenario})

    assert result["valid"] is False
    assert any(finding["code"] == "scenario.version_mismatch" for finding in result["findings"])
    assert any(finding["code"] == "scenario.unknown_transition" for finding in result["findings"])
