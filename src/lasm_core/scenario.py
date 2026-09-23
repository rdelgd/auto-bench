from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .trace import AgenticEventType

AutomotiveDomain: TypeAlias = Literal[
    "service",
    "parts",
    "sales",
    "finance",
    "customer-experience",
    "inventory",
    "warranty",
    "compliance",
    "operations",
]


class BusinessContext(TypedDict):
    domain: AutomotiveDomain
    summary: str
    stakeholders: Sequence[str]
    requiredFacts: Sequence[str]
    sensitivities: Sequence[str]


class UserIntent(TypedDict):
    explicitGoal: str
    constraints: Sequence[str]
    inferredGoals: NotRequired[Sequence[str]]


class ExpectedControlSurfaces(TypedDict):
    harnessIds: Sequence[str]
    skillIds: Sequence[str]
    mcpServerIds: Sequence[str]
    mcpPrimitiveIds: Sequence[str]


class RealityReferenceSet(TypedDict):
    assemblyId: str
    assemblyVersion: str
    assemblyEntryIds: Sequence[str]
    initialStateId: str
    observationIds: Sequence[str]
    transitionIds: Sequence[str]
    outcomeIds: Sequence[str]


class EvaluationExpectations(TypedDict):
    requiredTraceTypes: Sequence[AgenticEventType]
    requiresPolicyCheck: bool
    requiresHumanConfirmation: bool


class Scenario(TypedDict):
    id: str
    title: str
    businessContext: BusinessContext
    intent: UserIntent
    reality: RealityReferenceSet
    expectedControlSurfaces: ExpectedControlSurfaces
    evaluation: EvaluationExpectations
