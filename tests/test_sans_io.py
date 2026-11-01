"""The core computes over materialized values with application-level I/O unavailable."""

from __future__ import annotations

import builtins
import io
import json
import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from typing import Any

import pytest

import lasm_core
from lasm_core import fixtures


class IOAttempted(AssertionError):
    pass


def _forbidden(name: str) -> Any:
    def refuse(*args: Any, **kwargs: Any) -> Any:
        raise IOAttempted(f"core attempted {name}")

    return refuse


class _NoEnvironment(dict[str, str]):
    def __getitem__(self, key: str) -> str:
        raise IOAttempted(f"core read environment variable {key}")

    def get(self, key: str, default: Any = None) -> Any:
        raise IOAttempted(f"core read environment variable {key}")


@pytest.fixture
def io_unavailable(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for module, names in [
        (builtins, ["open", "input"]),
        (io, ["open", "open_code"]),
        (os, ["open", "listdir", "scandir", "stat", "getenv", "system", "popen", "fork"]),
        (socket, ["socket", "create_connection", "getaddrinfo"]),
        (subprocess, ["Popen", "run"]),
        (time, ["time", "time_ns", "monotonic", "perf_counter", "sleep"]),
    ]:
        for name in names:
            if hasattr(module, name):
                monkeypatch.setattr(module, name, _forbidden(f"{module.__name__}.{name}"))
    monkeypatch.setattr(os, "environ", _NoEnvironment())
    yield


def test_domain_and_interchange_calls_run_with_io_unavailable(io_unavailable: None) -> None:
    case = fixtures.routine_maintenance_conformance_case
    assembly, state = case["assembly"], case["initialState"]
    assert lasm_core.validate_conformance_case(case)["valid"]
    assert lasm_core.validate_logical_assembly(assembly)["valid"]
    assert lasm_core.validate_harness(case["harnesses"][0], assembly, state)["valid"]
    assert lasm_core.validate_skill(case["skills"][0], assembly, state)["valid"]
    assert lasm_core.validate_mcp_surface(case["mcpSurfaces"][0], assembly, state)["valid"]
    assert lasm_core.normalize_trace(case["trace"])["findings"] == []
    evaluation = lasm_core.evaluate_conformance(case)
    assert evaluation["conformant"]

    encoded = lasm_core.encode_document(case, "conformance-case")
    decoded = lasm_core.decode_document(encoded["text"], "conformance-case")
    assert decoded["valid"]
    assert lasm_core.evaluate_conformance(decoded["value"]) == evaluation
    assert lasm_core.encode_document(evaluation, "conformance-evaluation")["valid"]

    sales = fixtures.new_vehicle_units_conformance_case
    assert lasm_core.validate_conformance_case(sales)["valid"]
    assert lasm_core.validate_weight_patch(sales["weightPatches"][0], sales["assembly"], sales["initialState"])["valid"]
    assert lasm_core.evaluate_conformance(sales) == fixtures.new_vehicle_units_evaluation
    assert lasm_core.encode_document(sales, "conformance-case")["valid"]


def test_ledger_calls_run_with_io_unavailable(io_unavailable: None) -> None:
    command: lasm_core.AcceptPolicy = {
        "policyId": "paseo-core.application.teardown",
        "binding": "paseo-core",
        "action": "application.teardown",
        "decision": "deny",
        "reason": "Contact an operator to tear down an application.",
        "acceptedBy": "operator@example.com",
    }
    decided = lasm_core.decide_policy([], command)
    assert decided["accepted"]
    (event,) = decided["events"]
    assert lasm_core.validate_ledger_event_data(event["type"], event["schemaVersion"], event["data"])["valid"]
    recorded: lasm_core.RecordedEvent = {
        "streamId": lasm_core.policy_stream_id(command["policyId"]),
        "streamVersion": 1,
        "type": event["type"],
        "schemaVersion": event["schemaVersion"],
        "data": dict(event["data"]),
    }
    assert lasm_core.decide_policy([recorded], command)["findings"][0]["code"] == "policy.unchanged"
    projection = lasm_core.project_decision_rules([recorded])
    assert projection["findings"] == [] and len(projection["rules"]) == 1


def test_verdict_projection_runs_with_io_unavailable(io_unavailable: None) -> None:
    measured = {
        "cellId": "fruitfly-1b.remove-exactness.single-hop",
        "attempt": 1,
        "target": {"binding": "weight-patch", "ref": "atlantis-capital"},
        "vindexPin": "pin-1",
        "patchDigest": "sha256:abc",
        "patchrigCommit": "a" * 40,
        "larqlVersion": "0.2.0",
        "larqlBinarySha256": "f" * 64,
        "manipulationCheck": "passed",
        "tier": "Tier 1",
        "claimScope": "Gemma 3 1B, N=10",
        "controlsState": "passing",
        "measurements": {"strength": 0.91},
        "recordsDigest": "sha256:def",
        "environment": {"host": "M5", "fingerprint": "m5"},
    }
    judged = {
        "cellId": measured["cellId"],
        "attempt": 1,
        "cites": {"streamId": "experiment:cell@1", "streamVersion": 1},
        "preregistration": "2026-11-05",
        "scorerVersion": "a" * 40,
        "verdict": "cannot-tell",
        "cannotTellReason": "degenerate-stratum",
    }
    assert lasm_core.validate_ledger_event_data("verdict.recorded", 1, judged)["valid"]
    events: list[lasm_core.RecordedEvent] = [
        {"streamId": "experiment:cell@1", "streamVersion": 1, "type": "evidence.recorded", "schemaVersion": 1, "data": measured},
        {"streamId": "judgement:cell@1", "streamVersion": 1, "type": "verdict.recorded", "schemaVersion": 1, "data": judged},
    ]
    projection = lasm_core.project_verdicts(events)
    assert projection["findings"] == []
    assert projection["cells"][0]["status"] == "current"


def _run_python(code: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, "-I", "-c", code],
        capture_output=True,
        text=True,
        check=True,
        env={"PYTHONPATH": os.pathsep.join(sys.path)},
    )
    result: dict[str, Any] = json.loads(completed.stdout)
    return result


def test_root_import_loads_only_the_standard_library_and_not_fixtures() -> None:
    result = _run_python(
        "import json, sys\n"
        "before = set(sys.modules)\n"
        "import lasm_core\n"
        "loaded = sorted(set(sys.modules) - before)\n"
        "stdlib = sys.stdlib_module_names\n"
        "print(json.dumps({\n"
        "  'fixtures': 'lasm_core.fixtures' in sys.modules,\n"
        "  'third_party': [m for m in loaded if m.split('.')[0] not in stdlib and not m.startswith('lasm_core')],\n"
        "}))\n"
    )
    assert result == {"fixtures": False, "third_party": []}


def test_fixture_import_is_separate_and_self_contained() -> None:
    result = _run_python(
        "import json, sys\n"
        "before = set(sys.modules)\n"
        "from lasm_core.fixtures import routine_maintenance_evaluation\n"
        "loaded = set(sys.modules) - before\n"
        "print(json.dumps({'conformant': routine_maintenance_evaluation['conformant'],\n"
        "  'third_party': [m for m in loaded if m.split('.')[0] not in sys.stdlib_module_names and not m.startswith('lasm_core')]}))\n"
    )
    assert result == {"conformant": True, "third_party": []}
