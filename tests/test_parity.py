"""Differential parity against outputs recorded from the TypeScript reference implementation.

Expected values are the TypeScript record with the reviewed deviations in corpus/deviations.json applied.
"""

from __future__ import annotations

import copy
import json
from typing import Any

import pytest

import lasm_core
from corpus_support import CONSTANTS, FIXTURES, FUNCTIONS, first_difference, json_equal, load_cases, load_deviations, run_case

CASES = load_cases()


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_python_matches_typescript_reference(case: dict[str, Any]) -> None:
    actual = json.loads(json.dumps(run_case(case), allow_nan=False))
    difference = first_difference(actual, case["expected"])
    assert difference is None, f"{case['id']}: {difference}"


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_calls_are_repeatable_and_do_not_mutate_inputs(case: dict[str, Any]) -> None:
    arguments = copy.deepcopy(case["args"])
    first = run_case({**case, "args": arguments})
    second = run_case({**case, "args": arguments})
    assert json_equal(json.loads(json.dumps(first)), json.loads(json.dumps(second)))
    assert json_equal(arguments, case["args"])
    assert repr(arguments) == repr(case["args"]), "argument scalar types or key order changed"


def test_corpus_covers_every_public_behavioral_export() -> None:
    covered = {case["function"] for case in CASES}
    assert set(FUNCTIONS) | set(CONSTANTS) <= covered
    assert {f"fixture:{name}" for name in FIXTURES} <= covered
    public_callables = {name for name in lasm_core.__all__ if callable(getattr(lasm_core, name)) and name[0].islower()}
    interchange = {"decode_document", "encode_document", "validate_document", "wrap_document"}
    assert public_callables - interchange == {function.__name__ for function in FUNCTIONS.values()}


def test_every_deviation_is_explained_and_changes_a_recorded_case() -> None:
    by_id = {case["id"]: case for case in CASES}
    for case_id, deviation in load_deviations().items():
        assert case_id in by_id, f"deviation for unknown case {case_id}"
        assert deviation["reason"].strip() and deviation["ops"]
        assert not json_equal(by_id[case_id]["expected"], by_id[case_id]["typescriptExpected"]), f"{case_id} deviation is a no-op"


def test_comparator_preserves_json_scalar_types_and_order() -> None:
    assert json_equal({"a": 1, "b": [1, 2]}, {"b": [1, 2.0], "a": 1.0})
    assert not json_equal(True, 1)
    assert not json_equal([False], [0])
    assert not json_equal({"a": None}, {})
    assert not json_equal([1, 2], [2, 1])
    assert not json_equal("1", 1)
    assert json_equal({"$set": ["b", "a"]}, {"$set": ["a", "b"]})
    assert not json_equal({"$set": ["a"]}, {"$set": ["a", "b"]})
