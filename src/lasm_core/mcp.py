from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .lasm import LasmProjectionReferences

McpRisk: TypeAlias = Literal["low", "moderate", "high"]


class McpPrimitiveDescriptor(TypedDict):
    id: str
    name: str
    purpose: str
    risk: McpRisk
    requiredPermission: NotRequired[str]
    projection: NotRequired[LasmProjectionReferences]


class McpSurfaceDescriptor(TypedDict):
    id: str
    name: str
    purpose: str
    tools: Sequence[McpPrimitiveDescriptor]
    resources: Sequence[McpPrimitiveDescriptor]
    prompts: Sequence[McpPrimitiveDescriptor]
    projection: NotRequired[LasmProjectionReferences]


def mcp_primitives(surface: McpSurfaceDescriptor) -> list[McpPrimitiveDescriptor]:
    return [*surface["tools"], *surface["resources"], *surface["prompts"]]
