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
