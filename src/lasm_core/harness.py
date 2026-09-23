from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .lasm import LasmProjectionReferences

InteractionMode: TypeAlias = Literal["interactive", "autonomous", "delegated", "workflow"]
PermissionLevel: TypeAlias = Literal["read-only", "scoped-write", "privileged"]
ContextSensitivity: TypeAlias = Literal["public", "internal", "sensitive"]


class ContextSurface(TypedDict):
    id: str
    description: str
    sensitivity: ContextSensitivity
    projection: NotRequired[LasmProjectionReferences]


class HandoffBoundary(TypedDict):
    id: str
    description: str
    projection: NotRequired[LasmProjectionReferences]


class PermissionModel(TypedDict):
    defaultLevel: PermissionLevel
    scopedPermissions: Sequence[str]
    projection: NotRequired[LasmProjectionReferences]


class ApprovalFlow(TypedDict):
    requiredFor: Sequence[str]
    approverRoles: Sequence[str]
    projection: NotRequired[LasmProjectionReferences]


class HarnessDescriptor(TypedDict):
    id: str
    name: str
    purpose: str
    interactionMode: InteractionMode
    contextSurfaces: Sequence[ContextSurface]
    affordances: Sequence[str]
    permissionModel: PermissionModel
    approvalFlow: ApprovalFlow
    handoffBoundaries: Sequence[HandoffBoundary]
    projection: NotRequired[LasmProjectionReferences]
