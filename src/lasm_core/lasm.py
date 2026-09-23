from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict, Union

ProvenanceKind: TypeAlias = Literal["schema", "code", "policy", "practice", "incident", "commitment", "judgment"]
ProvenanceStatus: TypeAlias = Literal["current", "stale", "disputed"]


class ProvenanceSource(TypedDict):
    id: str
    kind: ProvenanceKind
    title: str
    locator: str
    owner: NotRequired[str]
    version: NotRequired[str]
    observedAt: NotRequired[str]
    status: ProvenanceStatus


class LasmEntryBase(TypedDict):
    id: str
    name: str
    description: str
    sourceIds: Sequence[str]


class ConceptEntry(LasmEntryBase):
    kind: Literal["concept"]


class RelationEntry(LasmEntryBase):
    kind: Literal["relation"]
    fromConceptId: str
    toConceptId: str
    predicate: str


class ConstraintEntry(LasmEntryBase):
    kind: Literal["constraint"]
    appliesToEntryIds: Sequence[str]
    rule: str


class EventEntry(LasmEntryBase):
    kind: Literal["event"]
    subjectConceptIds: Sequence[str]


class PolicyEntry(LasmEntryBase):
    kind: Literal["policy"]
    appliesToEntryIds: Sequence[str]
    authorityRoles: Sequence[str]
    commitment: str


RuntimeEvaluationMode: TypeAlias = Literal["gate", "check"]


class RuntimeEvaluationDescriptor(LasmEntryBase):
    kind: Literal["evaluation"]
    mode: RuntimeEvaluationMode
    addressedEntryIds: Sequence[str]
    evaluatorId: str


LogicalAssemblyEntry: TypeAlias = Union[
    ConceptEntry,
    RelationEntry,
    ConstraintEntry,
    EventEntry,
    PolicyEntry,
    RuntimeEvaluationDescriptor,
]


class LogicalAssemblySlice(TypedDict):
    id: str
    version: str
    title: str
    description: str
    provenance: Sequence[ProvenanceSource]
    concepts: Sequence[ConceptEntry]
    relations: Sequence[RelationEntry]
    constraints: Sequence[ConstraintEntry]
    events: Sequence[EventEntry]
    policies: Sequence[PolicyEntry]
    evaluations: Sequence[RuntimeEvaluationDescriptor]


class LasmProjectionReferences(TypedDict):
    assemblyEntryIds: Sequence[str]
    stateFieldIds: NotRequired[Sequence[str]]


def logical_assembly_entries(assembly: LogicalAssemblySlice) -> list[LogicalAssemblyEntry]:
    return [
        *assembly["concepts"],
        *assembly["relations"],
        *assembly["constraints"],
        *assembly["events"],
        *assembly["policies"],
        *assembly["evaluations"],
    ]


def logical_assembly_entry_ids(assembly: LogicalAssemblySlice) -> frozenset[str]:
    return frozenset(entry["id"] for entry in logical_assembly_entries(assembly))
