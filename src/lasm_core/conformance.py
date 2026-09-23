from __future__ import annotations

from collections.abc import Sequence
from typing import TypedDict

from .harness import HarnessDescriptor
from .lasm import LogicalAssemblySlice
from .mcp import McpSurfaceDescriptor
from .operational_state import ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation
from .scenario import Scenario
from .skill import SkillDescriptor
from .trace import RawTraceEvent


class ConformanceCase(TypedDict):
    assembly: LogicalAssemblySlice
    scenario: Scenario
    initialState: OperationalState
    observations: Sequence[ActorObservation]
    transitions: Sequence[StateTransitionExpectation]
    outcomes: Sequence[OutcomeExpectation]
    harnesses: Sequence[HarnessDescriptor]
    skills: Sequence[SkillDescriptor]
    mcpSurfaces: Sequence[McpSurfaceDescriptor]
    trace: Sequence[RawTraceEvent]
