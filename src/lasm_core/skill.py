from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .lasm import LasmProjectionReferences

SkillReferenceKind: TypeAlias = Literal["instruction", "reference", "script", "asset"]


class SkillReference(TypedDict):
    kind: SkillReferenceKind
    name: str


class SkillDescriptor(TypedDict):
    id: str
    name: str
    purpose: str
    applicability: Sequence[str]
    capabilities: Sequence[str]
    references: NotRequired[Sequence[SkillReference]]
    projection: NotRequired[LasmProjectionReferences]
