"""Shared loading and comparison for the TypeScript reference corpus."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import lasm_core
from lasm_core import fixtures

CORPUS_DIR = Path(__file__).parent / "corpus" / "reference"
DEVIATIONS_PATH = Path(__file__).parent / "corpus" / "deviations.json"

# TypeScript export name -> Python equivalent (see docs/api-inventory.md).
FUNCTIONS: dict[str, Callable[..., Any]] = {
    "validationResult": lasm_core.validation_result,
    "logicalAssemblyEntries": lasm_core.logical_assembly_entries,
    "logicalAssemblyEntryIds": lasm_core.logical_assembly_entry_ids,
    "mcpPrimitives": lasm_core.mcp_primitives,
    "isAgenticEventType": lasm_core.is_agentic_event_type,
    "traceEvidenceRef": lasm_core.trace_evidence_ref,
    "normalizeTrace": lasm_core.normalize_trace,
    "validateLogicalAssembly": lasm_core.validate_logical_assembly,
    "validateOperationalState": lasm_core.validate_operational_state,
    "validateActorObservation": lasm_core.validate_actor_observation,
    "validateStateTransition": lasm_core.validate_state_transition,
    "validateOutcome": lasm_core.validate_outcome,
    "validateScenario": lasm_core.validate_scenario,
    "validateHarness": lasm_core.validate_harness,
    "validateSkill": lasm_core.validate_skill,
    "validateMcpSurface": lasm_core.validate_mcp_surface,
    "validateTrace": lasm_core.validate_trace,
    "validateConformanceCase": lasm_core.validate_conformance_case,
    "evaluateConformance": lasm_core.evaluate_conformance,
}

CONSTANTS: dict[str, Any] = {
    "agenticEventTypes": list(lasm_core.AGENTIC_EVENT_TYPES),
}

FIXTURES: dict[str, Any] = {
    "dealershipOperationsMcp": fixtures.dealership_operations_mcp,
    "routineMaintenanceConformanceCase": fixtures.routine_maintenance_conformance_case,
    "routineMaintenanceEvaluation": fixtures.routine_maintenance_evaluation,
    "routineMaintenanceScenario": fixtures.routine_maintenance_scenario,
    "routineMaintenanceTrace": fixtures.routine_maintenance_trace,
    "serviceAdvisorHarness": fixtures.service_advisor_harness,
    "serviceSchedulingAssembly": fixtures.service_scheduling_assembly,
    "serviceSchedulingInitialState": fixtures.service_scheduling_initial_state,
    "serviceSchedulingObservations": fixtures.service_scheduling_observations,
    "serviceSchedulingOutcomes": fixtures.service_scheduling_outcomes,
    "serviceSchedulingSkill": fixtures.service_scheduling_skill,
    "serviceSchedulingTransitions": fixtures.service_scheduling_transitions,
}


def load_deviations() -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = json.loads(DEVIATIONS_PATH.read_text(encoding="utf-8"))["cases"]
    return cases


def apply_patch(value: Any, ops: list[dict[str, Any]]) -> Any:
    """Apply JSON Patch add/remove/replace operations to a copy of ``value``."""
    result = copy.deepcopy(value)
    for op in ops:
        *parents, last = [part.replace("~1", "/").replace("~0", "~") for part in op["path"].split("/")[1:]]
        target = result
        for part in parents:
            target = target[int(part) if isinstance(target, list) else part]
        key: Any = int(last) if isinstance(target, list) else last
        if op["op"] == "remove":
            del target[key]
        elif op["op"] == "add" and isinstance(target, list):
            target.insert(key, op["value"])
        elif op["op"] in ("add", "replace"):
            if op["op"] == "replace" and (key not in target if isinstance(target, dict) else key >= len(target)):
                raise KeyError(op["path"])
            target[key] = op["value"]
        else:
            raise ValueError(f"unsupported patch operation: {op['op']}")
    return result


def load_cases() -> list[dict[str, Any]]:
    """Corpus cases with reviewed deviations applied; the TypeScript record stays in ``typescriptExpected``."""
    deviations = load_deviations()
    cases: list[dict[str, Any]] = []
    for path in sorted(CORPUS_DIR.glob("*.json")):
        for case in json.loads(path.read_text(encoding="utf-8")):
            case["typescriptExpected"] = case["expected"]
            if case["id"] in deviations:
                case["expected"] = apply_patch(case["expected"], deviations[case["id"]]["ops"])
            cases.append(case)
    return cases


def encode_result(value: Any) -> Any:
    """Apply the corpus's explicit encoding for set-valued helper results."""
    if isinstance(value, (set, frozenset)):
        return {"$set": sorted(value)}
    return value


def run_case(case: Mapping[str, Any]) -> Any:
    name: str = case["function"]
    if name.startswith("fixture:"):
        return FIXTURES[name.removeprefix("fixture:")]
    if name in CONSTANTS:
        return CONSTANTS[name]
    return encode_result(FUNCTIONS[name](*case["args"]))


def json_equal(left: Any, right: Any) -> bool:
    """Type-aware JSON equality.

    Object-key order and equivalent numeric spelling are ignored. Booleans never equal
    numbers, missing keys never equal nulls, and array order is significant. A ``$set``
    encoding compares membership only.
    """
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left == right
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    if isinstance(left, Mapping) and isinstance(right, Mapping):
        if set(left) == {"$set"} and set(right) == {"$set"}:
            return sorted(left["$set"]) == sorted(right["$set"]) and len(set(left["$set"])) == len(left["$set"])
        return set(left) == set(right) and all(json_equal(left[key], right[key]) for key in left)
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        return len(left) == len(right) and all(json_equal(a, b) for a, b in zip(left, right))
    return type(left) is type(right) and left == right


def first_difference(left: Any, right: Any, path: str = "$") -> str | None:
    if json_equal(left, right):
        return None
    if isinstance(left, Mapping) and isinstance(right, Mapping) and "$set" not in left:
        for key in sorted(set(left) | set(right)):
            if key not in left or key not in right:
                return f"{path}.{key}: present only in {'actual' if key in left else 'expected'}"
            difference = first_difference(left[key], right[key], f"{path}.{key}")
            if difference:
                return difference
    if isinstance(left, (list, tuple)) and isinstance(right, (list, tuple)):
        if len(left) != len(right):
            return f"{path}: length {len(left)} != {len(right)}"
        for index, (a, b) in enumerate(zip(left, right)):
            difference = first_difference(a, b, f"{path}[{index}]")
            if difference:
                return difference
    return f"{path}: {json.dumps(left, default=repr)[:200]} != {json.dumps(right, default=repr)[:200]}"
