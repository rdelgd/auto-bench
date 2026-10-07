"""Weight patches as Lasm projections: validation, evaluation, interchange, and the sales fixture."""

from __future__ import annotations

import copy
import json
from typing import Any

import lasm_core
from lasm_core import decode_document, encode_document, evaluate_conformance, validate_conformance_case, validate_weight_patch
from lasm_core.fixtures import (
    new_vehicle_units_assembly,
    new_vehicle_units_conformance_case,
    new_vehicle_units_evaluation,
    new_vehicle_units_initial_state,
    new_vehicle_units_weight_patch,
    routine_maintenance_conformance_case,
    routine_maintenance_evaluation,
)

PATCH_ID = new_vehicle_units_weight_patch["id"]


def dimension(evaluation: Any, name: str) -> Any:
    return next(result for result in evaluation["dimensions"] if result["dimension"] == name)


def codes(result: Any) -> list[str]:
    return [finding["code"] for finding in result["findings"]]


def finding(result: Any, code: str) -> Any:
    return next(finding for finding in result["findings"] if finding["code"] == code)


def conformant_case() -> Any:
    """The sales fixture with every probe passed, the correct scope reported, and no divergence."""
    case = copy.deepcopy(new_vehicle_units_conformance_case)
    trace = []
    for event in case["trace"]:
        if event["type"] == "patch.probed":
            event = {**event, "evidence": {**event["evidence"], "passed": True}}
        if event["type"] in ("lasm.divergence_detected", "lasm.failure_attributed"):
            continue
        if event["type"] == "outcome.observed":
            event = {**event, "subjectId": "outcome.all-stock-types-reported"}
        trace.append(event)
    case["trace"] = trace
    return case


# Validation --------------------------------------------------------------------------------


def test_fixture_weight_patch_and_case_validate() -> None:
    assert validate_weight_patch(new_vehicle_units_weight_patch, new_vehicle_units_assembly, new_vehicle_units_initial_state)["valid"]
    assert validate_conformance_case(new_vehicle_units_conformance_case) == {"valid": True, "findings": []}


def test_weight_patch_validation_reports_required_fields_and_projection_references() -> None:
    patch = {
        **new_vehicle_units_weight_patch,
        "digest": " ",
        "baseModelId": "",
        "projection": {"assemblyEntryIds": ["concept.missing"], "stateFieldIds": ["field.missing"]},
    }
    result = validate_weight_patch(patch, new_vehicle_units_assembly, new_vehicle_units_initial_state)  # type: ignore[arg-type]
    assert result["valid"] is False
    assert [(f["code"], f["path"]) for f in result["findings"]] == [
        ("fixture.required", "weightPatch.baseModelId"),
        ("fixture.required", "weightPatch.digest"),
        ("projection.unknown_assembly_entry", "weightPatch.projection.assemblyEntryIds[0]"),
        ("projection.unknown_state_field", "weightPatch.projection.stateFieldIds[0]"),
    ]

    empty = validate_weight_patch({**new_vehicle_units_weight_patch, "projection": {"assemblyEntryIds": []}})
    assert [(f["code"], f["path"]) for f in empty["findings"]] == [("projection.empty", "weightPatch.projection")]


def test_case_validation_reports_unknown_expected_and_duplicate_weight_patches() -> None:
    case = copy.deepcopy(new_vehicle_units_conformance_case)
    case["weightPatches"] = [new_vehicle_units_weight_patch, new_vehicle_units_weight_patch]
    case["scenario"]["expectedControlSurfaces"]["weightPatchIds"] = [PATCH_ID, "patch.missing"]
    result = validate_conformance_case(case)
    assert result["valid"] is False
    assert [(f["code"], f["path"]) for f in result["findings"]] == [
        ("scenario.unknown_weight_patch", "scenario.expectedControlSurfaces.weightPatchIds[1]"),
        ("fixture.duplicate_id", "weightPatches"),
    ]

    duplicate_expected = copy.deepcopy(new_vehicle_units_conformance_case["scenario"])
    duplicate_expected["expectedControlSurfaces"]["weightPatchIds"] = [PATCH_ID, PATCH_ID]
    assert [f["code"] for f in lasm_core.validate_scenario(duplicate_expected)["findings"]] == ["fixture.duplicate_id"]


# Evaluation --------------------------------------------------------------------------------


def test_fixture_attributes_the_lost_distinction_to_the_patch() -> None:
    evaluation = new_vehicle_units_evaluation
    assert evaluation["valid"] is True and evaluation["conformant"] is False
    assert [(r["dimension"], r["status"]) for r in evaluation["dimensions"]] == [
        ("intent-fidelity", "pass"),
        ("semantic-fidelity", "fail"),
        ("reality-model-validity", "pass"),
        ("state-and-outcome-validity", "fail"),
        ("control-surface-quality", "fail"),
        ("reality-coverage", "pass"),
        ("evidence-and-attribution", "pass"),
        ("governance", "pass"),
    ]

    probe = finding(dimension(evaluation, "control-surface-quality"), "control.weight_patch_probe_failed")
    assert probe["attribution"] == "projection"
    assert probe["assemblyEntryIds"] == list(new_vehicle_units_weight_patch["projection"]["assemblyEntryIds"])
    assert probe["evidenceRefs"] == ["trace:7"] and "(paraphrase)" in probe["message"]

    named = finding(dimension(evaluation, "semantic-fidelity"), "semantic.divergence_in_weight_patch")
    assert named["attribution"] == "projection" and PATCH_ID in named["message"]
    assert named["assemblyEntryIds"] == ["concept.net-new-vehicle-units"]

    assert "outcome.prohibited_observed" in codes(dimension(evaluation, "state-and-outcome-validity"))


def test_fixture_is_repeatable_and_unchanged_by_evaluation() -> None:
    before = copy.deepcopy(new_vehicle_units_conformance_case)
    assert evaluate_conformance(new_vehicle_units_conformance_case) == new_vehicle_units_evaluation
    assert new_vehicle_units_conformance_case == before


def test_conformant_variant_passes_control_surface_and_semantic_fidelity() -> None:
    evaluation = evaluate_conformance(conformant_case())
    assert evaluation["conformant"] is True
    control = dimension(evaluation, "control-surface-quality")
    assert control["status"] == "pass" and codes(control) == ["control.expected_surfaces_used"]
    assert "trace:5" in control["findings"][0]["evidenceRefs"]  # the patch.applied event counts as expected-surface use
    assert dimension(evaluation, "semantic-fidelity")["status"] == "pass"


def test_digest_mismatch_is_a_control_surface_finding() -> None:
    case = conformant_case()
    case["trace"] = [
        {**e, "evidence": {**e["evidence"], "digest": "sha256:other"}} if e["type"] == "patch.applied" else e for e in case["trace"]
    ]
    control = dimension(evaluate_conformance(case), "control-surface-quality")
    mismatch = finding(control, "control.weight_patch_digest_mismatch")
    assert control["status"] == "fail"
    assert mismatch["attribution"] == "control-surface" and mismatch["evidenceRefs"] == ["trace:5"]
    assert dimension(evaluate_conformance(case), "reality-model-validity")["status"] == "pass"


def test_probe_without_a_boolean_verdict_is_not_a_pass() -> None:
    case = conformant_case()
    case["trace"] = [
        {**e, "evidence": {"probe": "removal"}} if e["type"] == "patch.probed" and e["sequence"] == 6 else e for e in case["trace"]
    ]
    control = dimension(evaluate_conformance(case), "control-surface-quality")
    assert "(removal)" in finding(control, "control.weight_patch_probe_failed")["message"]


def test_expected_unused_and_unmodeled_patches_are_reported() -> None:
    unused = conformant_case()
    unused["trace"] = [e for e in unused["trace"] if e["type"] != "patch.applied"]
    unused["scenario"]["evaluation"]["requiredTraceTypes"] = [t for t in unused["scenario"]["evaluation"]["requiredTraceTypes"] if t != "patch.applied"]
    assert "control.weight_patch_not_used" in codes(dimension(evaluate_conformance(unused), "control-surface-quality"))

    unmodeled = conformant_case()
    unmodeled["weightPatches"] = []
    unmodeled["scenario"]["expectedControlSurfaces"]["weightPatchIds"] = []
    control = dimension(evaluate_conformance(unmodeled), "control-surface-quality")
    assert finding(control, "control.weight_patch_unmodeled")["attribution"] == "control-surface"

    missing_fixture = conformant_case()
    missing_fixture["weightPatches"] = []
    assert validate_conformance_case(missing_fixture)["valid"] is False
    assert "control.weight_patch_fixture_missing" in codes(dimension(evaluate_conformance(missing_fixture), "control-surface-quality"))


def test_patch_only_projection_counts_toward_reality_coverage() -> None:
    case = conformant_case()
    narrowed = ["event.units-reported", "relation.units-span-stock-types"]
    case["skills"] = [{**s, "projection": {**s["projection"], "assemblyEntryIds": narrowed}} for s in case["skills"]]
    assert dimension(evaluate_conformance(case), "reality-coverage")["status"] == "pass"
    case["weightPatches"] = []
    case["scenario"]["expectedControlSurfaces"]["weightPatchIds"] = []
    case["trace"] = [e for e in case["trace"] if not e["type"].startswith("patch.")]
    case["scenario"]["evaluation"]["requiredTraceTypes"] = [t for t in case["scenario"]["evaluation"]["requiredTraceTypes"] if not t.startswith("patch.")]
    coverage = dimension(evaluate_conformance(case), "reality-coverage")
    assert coverage["status"] == "fail"
    unprojected = [f["assemblyEntryIds"][0] for f in coverage["findings"] if f["code"] == "coverage.assembly_entry_not_projected"]
    assert unprojected == ["concept.net-new-vehicle-units", "concept.stock-type", "constraint.include-all-stock-types"]


def test_cases_without_weight_patches_are_unchanged() -> None:
    assert evaluate_conformance(routine_maintenance_conformance_case) == routine_maintenance_evaluation
    with_empty = {**routine_maintenance_conformance_case, "weightPatches": []}
    assert evaluate_conformance(with_empty) == routine_maintenance_evaluation  # type: ignore[arg-type]


# Interchange -------------------------------------------------------------------------------


def test_case_with_weight_patches_round_trips_within_version_1() -> None:
    encoded = encode_document(new_vehicle_units_conformance_case, "conformance-case")
    assert encoded["valid"] and json.loads(encoded["text"])["schemaVersion"] == 1
    decoded = decode_document(encoded["text"], "conformance-case")
    assert decoded["valid"]
    assert json.loads(json.dumps(decoded["value"])) == json.loads(json.dumps(new_vehicle_units_conformance_case))
    assert evaluate_conformance(decoded["value"]) == new_vehicle_units_evaluation


def test_documents_without_weight_patches_decode_as_before() -> None:
    document = json.loads(encode_document(routine_maintenance_conformance_case, "conformance-case")["text"])
    assert "weightPatches" not in document["value"]
    assert "weightPatchIds" not in document["value"]["scenario"]["expectedControlSurfaces"]
    decoded = decode_document(json.dumps(document), "conformance-case")
    assert decoded["valid"] and "weightPatches" not in decoded["value"]


def test_malformed_weight_patch_documents_are_rejected_structurally() -> None:
    base = json.loads(encode_document(new_vehicle_units_conformance_case, "conformance-case")["text"])
    for drop in ("projection", "digest", "baseModelId"):
        document = copy.deepcopy(base)
        del document["value"]["weightPatches"][0][drop]
        assert not decode_document(json.dumps(document), "conformance-case")["valid"], drop
    unknown = copy.deepcopy(base)
    unknown["value"]["weightPatches"][0]["method"] = "lora"
    assert not decode_document(json.dumps(unknown), "conformance-case")["valid"]

    empty = copy.deepcopy(base)
    empty["value"]["weightPatches"][0]["projection"] = {"assemblyEntryIds": []}
    decoded = decode_document(json.dumps(empty), "conformance-case")
    assert decoded["valid"]
    assert [f["code"] for f in validate_weight_patch(decoded["value"]["weightPatches"][0])["findings"]] == ["projection.empty"]
