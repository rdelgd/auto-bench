"""Version 1 interchange: schemas, pure decoding/encoding, and wire-boundary rules."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

import lasm_core
from corpus_support import json_equal, load_cases
from lasm_core import (
    DOCUMENT_KINDS,
    decode_document,
    encode_document,
    evaluate_conformance,
    normalize_trace,
    validate_conformance_case,
    validate_document,
    validate_trace,
    wrap_document,
)
from lasm_core._schema_v1 import DOCUMENT_DEFINITIONS, schema_files
from lasm_core.fixtures import routine_maintenance_conformance_case, routine_maintenance_evaluation

SCHEMA_DIR = Path(lasm_core.__file__).parent / "schemas" / "v1"
CHECKED_IN = {path.name: json.loads(path.read_text(encoding="utf-8")) for path in SCHEMA_DIR.glob("*.json")}
REGISTRY: Registry = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema)) for schema in CHECKED_IN.values()
)
CASES = load_cases()


def schema_validator(kind: str) -> Draft202012Validator:
    return Draft202012Validator(CHECKED_IN[f"{kind}.schema.json"], registry=REGISTRY)


def accepted_by_both(document: Any, kind: str) -> bool:
    python = validate_document(document, kind)  # type: ignore[arg-type]
    reference = schema_validator(kind).is_valid(document)
    assert python["valid"] == reference, (python["findings"], [error.message for error in schema_validator(kind).iter_errors(document)])
    return reference


def case_document(**changes: Any) -> dict[str, Any]:
    value = copy.deepcopy(routine_maintenance_conformance_case)
    value.update(changes)
    return wrap_document(value, "conformance-case")


# Schema artifacts ----------------------------------------------------------------------


def test_checked_in_schemas_are_rendered_from_the_python_definitions() -> None:
    assert CHECKED_IN == schema_files()


def test_schemas_are_valid_draft_2020_12_documents() -> None:
    for schema in CHECKED_IN.values():
        Draft202012Validator.check_schema(schema)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_document_kinds_match_the_schema_set() -> None:
    assert set(DOCUMENT_KINDS) == set(DOCUMENT_DEFINITIONS)
    assert {f"{kind}.schema.json" for kind in DOCUMENT_KINDS} | {"domain.schema.json"} == set(CHECKED_IN)


# Corpus payloads are structurally valid, including semantically invalid ones --------------

INPUT_KINDS = {
    "evaluateConformance": "conformance-case",
    "validateConformanceCase": "conformance-case",
    "validateLogicalAssembly": "logical-assembly",
    "normalizeTrace": "raw-trace",
    "validateTrace": "raw-trace",
}
OUTPUT_KINDS = {
    "evaluateConformance": "conformance-evaluation",
    "normalizeTrace": "trace-normalization-result",
    **{name: "validation-result" for name in {case["function"] for case in CASES} if name.startswith("validate")},
    "validationResult": "validation-result",
}


@pytest.mark.parametrize("case", [case for case in CASES if case["function"] in INPUT_KINDS], ids=lambda case: case["id"])
def test_corpus_inputs_decode_and_keep_domain_findings(case: dict[str, Any]) -> None:
    kind = INPUT_KINDS[case["function"]]
    document = wrap_document(case["args"][0], kind)  # type: ignore[arg-type]
    assert accepted_by_both(document, kind)

    decoded = decode_document(json.dumps(document), kind)  # type: ignore[arg-type]
    assert decoded["valid"] and json_equal(decoded["value"], case["args"][0])
    function = {
        "evaluateConformance": evaluate_conformance,
        "validateConformanceCase": validate_conformance_case,
        "validateLogicalAssembly": lasm_core.validate_logical_assembly,
        "normalizeTrace": normalize_trace,
        "validateTrace": validate_trace,
    }[case["function"]]
    assert json_equal(json.loads(json.dumps(function(decoded["value"]))), case["expected"])


@pytest.mark.parametrize("case", [case for case in CASES if case["function"] in OUTPUT_KINDS], ids=lambda case: case["id"])
def test_reference_outputs_conform_to_result_schemas(case: dict[str, Any]) -> None:
    kind = OUTPUT_KINDS[case["function"]]
    assert accepted_by_both(wrap_document(case["expected"], kind), kind)  # type: ignore[arg-type]


def test_fixture_case_and_evaluation_round_trip() -> None:
    case_text = encode_document(routine_maintenance_conformance_case, "conformance-case", indent=2)
    evaluation_text = encode_document(routine_maintenance_evaluation, "conformance-evaluation")
    assert case_text["valid"] and evaluation_text["valid"]

    decoded_case = decode_document(case_text["text"], "conformance-case")
    decoded_evaluation = decode_document(evaluation_text["text"], "conformance-evaluation")
    assert decoded_case["valid"] and decoded_evaluation["valid"]
    assert json_equal(decoded_case["value"], json.loads(json.dumps(routine_maintenance_conformance_case)))
    assert json_equal(evaluate_conformance(decoded_case["value"]), decoded_evaluation["value"])
    assert schema_validator("conformance-case").is_valid(json.loads(case_text["text"]))


# Wire rules --------------------------------------------------------------------------------


def test_omitted_optional_fields_stay_omitted_and_json_nulls_stay_null() -> None:
    transitions = copy.deepcopy(routine_maintenance_conformance_case["transitions"])
    del transitions[0]["eventId"]
    del transitions[0]["before"]
    transitions[1]["after"] = {"appointmentStatus": None, "flags": [False, 0, ""]}
    fields = copy.deepcopy(routine_maintenance_conformance_case["initialState"]["fields"])
    fields[0]["value"] = None
    document = case_document(transitions=transitions, initialState={**routine_maintenance_conformance_case["initialState"], "fields": fields})

    decoded = decode_document(json.dumps(document), "conformance-case")
    assert decoded["valid"]
    value = decoded["value"]
    assert "eventId" not in value["transitions"][0] and "before" not in value["transitions"][0]
    assert value["transitions"][1]["after"] == {"appointmentStatus": None, "flags": [False, 0, ""]}
    assert type(value["transitions"][1]["after"]["flags"][0]) is bool
    assert value["initialState"]["fields"][0]["value"] is None
    assert json.loads(encode_document(value, "conformance-case")["text"]) == document


def test_key_order_and_whitespace_are_not_semantic() -> None:
    document = wrap_document(list(routine_maintenance_conformance_case["trace"]), "raw-trace")
    reordered = json.dumps({"value": document["value"], "kind": "raw-trace", "schemaVersion": 1}, indent=4, sort_keys=True)
    decoded = decode_document(f"\n  {reordered}\n", "raw-trace")
    assert decoded["valid"] and json_equal(decoded["value"], document["value"])


def test_arbitrary_keys_are_permitted_inside_evidence_and_value_maps() -> None:
    trace = [{"type": "evidence.linked", "actorId": "a", "evidence": {"weird key!": {"nested": [1, None, {"": True}]}, "type": "x"}}]
    assert accepted_by_both(wrap_document(trace, "raw-trace"), "raw-trace")


def test_accepts_python_tuples_as_arrays() -> None:
    assert validate_document(wrap_document((routine_maintenance_conformance_case["trace"][0],), "raw-trace"), "raw-trace")["valid"]


def with_path(document: dict[str, Any], path: list[Any], value: Any) -> dict[str, Any]:
    document = copy.deepcopy(document)
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    if value is DELETE:
        del target[path[-1]]
    else:
        target[path[-1]] = value
    return document


DELETE = object()
BASE = case_document()

REJECTED: list[tuple[str, dict[str, Any], str, str, str]] = [
    ("unsupported-version", with_path(BASE, ["schemaVersion"], 2), "conformance-case", "format.unsupported_version", "$.schemaVersion"),
    ("string-version", with_path(BASE, ["schemaVersion"], "1"), "conformance-case", "format.unsupported_version", "$.schemaVersion"),
    ("boolean-version", with_path(BASE, ["schemaVersion"], True), "conformance-case", "format.unsupported_version", "$.schemaVersion"),
    ("unwrapped-payload", copy.deepcopy(dict(routine_maintenance_conformance_case)), "conformance-case", "format.missing_schema_version", "$.schemaVersion"),
    ("kind-mismatch", with_path(BASE, ["kind"], "logical-assembly"), "conformance-case", "format.kind_mismatch", "$.kind"),
    ("unknown-kind", with_path(BASE, ["kind"], "benchmark"), "conformance-case", "format.unknown_kind", "$.kind"),
    ("missing-value", with_path(BASE, ["value"], DELETE), "conformance-case", "format.missing_property", "$.value"),
    ("envelope-extra", with_path(BASE, ["metadata"], {}), "conformance-case", "format.unknown_property", "$.metadata"),
    ("string-sequence", with_path(BASE, ["value", "trace", 0, "sequence"], "1"), "conformance-case", "format.invalid_type", "$.value.trace[0].sequence"),
    ("boolean-sequence", with_path(BASE, ["value", "trace", 0, "sequence"], True), "conformance-case", "format.invalid_type", "$.value.trace[0].sequence"),
    ("number-for-boolean", with_path(BASE, ["value", "transitions", 0, "required"], 1), "conformance-case", "format.invalid_type", "$.value.transitions[0].required"),
    ("null-optional", with_path(BASE, ["value", "transitions", 0, "eventId"], None), "conformance-case", "format.invalid_type", "$.value.transitions[0].eventId"),
    ("null-required-string", with_path(BASE, ["value", "scenario", "title"], None), "conformance-case", "format.invalid_type", "$.value.scenario.title"),
    ("missing-required", with_path(BASE, ["value", "scenario", "title"], DELETE), "conformance-case", "format.missing_property", "$.value.scenario.title"),
    ("unknown-structural-property", with_path(BASE, ["value", "assembly", "concepts", 0, "aliases"], []), "conformance-case", "format.unknown_property", "$.value.assembly.concepts[0].aliases"),
    ("unknown-enum", with_path(BASE, ["value", "assembly", "provenance", 0, "status"], "unknown"), "conformance-case", "format.invalid_value", "$.value.assembly.provenance[0].status"),
    ("wrong-entry-kind", with_path(BASE, ["value", "assembly", "concepts", 0, "kind"], "relation"), "conformance-case", "format.invalid_value", "$.value.assembly.concepts[0].kind"),
    ("unknown-required-trace-type", with_path(BASE, ["value", "scenario", "evaluation", "requiredTraceTypes", 0], "custom.event"), "conformance-case", "format.invalid_value", "$.value.scenario.evaluation.requiredTraceTypes[0]"),
    ("string-for-array", with_path(BASE, ["value", "observations"], "none"), "conformance-case", "format.invalid_type", "$.value.observations"),
    ("unsafe-evidence-integer", with_path(BASE, ["value", "trace", 0, "evidence", "count"], 9007199254740992), "conformance-case", "format.unsafe_integer", "$.value.trace[0].evidence.count"),
    ("unsafe-nested-integer", with_path(BASE, ["value", "trace", 0, "evidence", "list"], [1, [-9007199254740992]]), "conformance-case", "format.unsafe_integer", "$.value.trace[0].evidence.list[1][0]"),
    ("unsafe-sequence", with_path(BASE, ["value", "trace", 0, "sequence"], 2**60), "conformance-case", "format.unsafe_integer", "$.value.trace[0].sequence"),
    ("unsafe-integer-valued-float", with_path(BASE, ["value", "initialState", "fields", 0, "value"], 1e300), "conformance-case", "format.unsafe_integer", "$.value.initialState.fields[0].value"),
    ("not-an-object", [], "conformance-case", "format.invalid_type", "$"),  # type: ignore[list-item]
]


@pytest.mark.parametrize(("name", "document", "kind", "code", "path"), REJECTED, ids=[row[0] for row in REJECTED])
def test_incompatible_documents_are_rejected_before_evaluation(name: str, document: Any, kind: str, code: str, path: str) -> None:
    result = decode_document(json.dumps(document), kind)  # type: ignore[arg-type]
    assert not result["valid"]
    assert "value" not in result
    assert (code, path) in [(finding["code"], finding["path"]) for finding in result["findings"]], result["findings"]
    assert all(finding["severity"] == "error" for finding in result["findings"])
    assert not schema_validator(kind).is_valid(document)


@pytest.mark.parametrize(
    ("text", "code", "path"),
    [
        ('{"schemaVersion": 1, "kind": "raw-trace", "value": [{"type": "task.completed", "sequence": NaN}]}', "format.non_finite_number", "$.value[0].sequence"),
        ('{"schemaVersion": 1, "kind": "raw-trace", "value": [{"type": "task.completed", "evidence": {"x": Infinity}}]}', "format.non_finite_number", "$.value[0].evidence.x"),
        ('{"schemaVersion": 1, "kind": "raw-trace", "value": [{"type": "task.completed", "evidence": {"x": -Infinity}}]}', "format.non_finite_number", "$.value[0].evidence.x"),
        ('{"schemaVersion": 1, "kind": "raw-trace", "value": [{"type": "task.completed", "sequence": 1e400}]}', "format.non_finite_number", "$.value[0].sequence"),
        ('{"schemaVersion": 1, "kind": "raw-trace", "value": [}', "format.invalid_json", "$"),
        ("", "format.invalid_json", "$"),
    ],
)
def test_non_finite_numbers_and_invalid_json_are_rejected(text: str, code: str, path: str) -> None:
    result = decode_document(text, "raw-trace")
    assert not result["valid"] and "value" not in result
    assert [(finding["code"], finding["path"]) for finding in result["findings"]] == [(code, path)]


def test_numbers_are_not_coerced() -> None:
    decoded = decode_document('{"schemaVersion": 1, "kind": "raw-trace", "value": [{"type": "task.completed", "sequence": 2.0, "evidence": {"n": 1, "b": true}}]}', "raw-trace")
    assert decoded["valid"]
    event = decoded["value"][0]
    assert type(event["sequence"]) is float and type(event["evidence"]["n"]) is int and type(event["evidence"]["b"]) is bool


def test_integer_valued_and_fractional_numbers_within_range_are_accepted() -> None:
    trace = [{"type": "task.completed", "sequence": -9007199254740991, "evidence": {"f": 1e300 + 0.5, "g": 0.25, "h": 9007199254740991.0}}]
    result = decode_document(json.dumps(wrap_document(trace, "raw-trace")), "raw-trace")
    # 1e300 + 0.5 is still integer-valued and therefore out of range.
    assert [(finding["code"], finding["path"]) for finding in result["findings"]] == [("format.unsafe_integer", "$.value[0].evidence.f")]
    trace[0]["evidence"] = {"g": 0.25, "h": 9007199254740991.0}
    assert accepted_by_both(wrap_document(trace, "raw-trace"), "raw-trace")


def test_any_kind_is_accepted_when_no_kind_is_expected() -> None:
    result = decode_document(json.dumps(wrap_document([], "raw-trace")))
    assert result["valid"] and result["kind"] == "raw-trace" and result["value"] == []


def test_encoding_refuses_nonconforming_payloads() -> None:
    result = encode_document({**routine_maintenance_conformance_case, "trace": [{"type": "x", "sequence": float("nan")}]}, "conformance-case")
    assert not result["valid"] and "text" not in result
    assert [finding["code"] for finding in result["findings"]] == ["format.non_finite_number"]
    assert not encode_document({"not": "an assembly"}, "logical-assembly")["valid"]


def test_semantically_invalid_payloads_reach_domain_validation() -> None:
    trace = [
        {"type": "custom.event", "sequence": -1.5},
        {"type": "task.completed", "sequence": -1.5, "actorId": ""},
    ]
    decoded = decode_document(json.dumps(wrap_document(trace, "raw-trace")), "raw-trace")
    assert decoded["valid"]
    assert [finding["code"] for finding in validate_trace(decoded["value"])["findings"]] == [
        "fixture.duplicate_id",
        "trace.unknown_event_type",
        "trace.missing_actor",
        "trace.invalid_sequence",
        "trace.missing_actor",
        "trace.invalid_sequence",
    ]
