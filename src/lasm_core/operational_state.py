from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .domain import EvidencePayload, JsonValue


class OperationalStateField(TypedDict):
    id: str
    conceptId: str
    value: JsonValue


class OperationalState(TypedDict):
    id: str
    assemblyId: str
    assemblyVersion: str
    fields: Sequence[OperationalStateField]


class ActorObservation(TypedDict):
    id: str
    actorId: str
    fieldIds: Sequence[str]
    observedValues: EvidencePayload


TransitionDisposition: TypeAlias = Literal["permitted", "prohibited"]


class StateTransitionExpectation(TypedDict):
    id: str
    description: str
    disposition: TransitionDisposition
    required: bool
    eventId: NotRequired[str]
    fieldIds: Sequence[str]
    before: NotRequired[EvidencePayload]
    after: NotRequired[EvidencePayload]


OutcomeDisposition: TypeAlias = Literal["acceptable", "prohibited"]


class OutcomeExpectation(TypedDict):
    id: str
    description: str
    disposition: OutcomeDisposition
    required: bool
    fieldIds: Sequence[str]
