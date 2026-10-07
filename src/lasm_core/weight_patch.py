from __future__ import annotations

from typing import TypedDict

from .lasm import LasmProjectionReferences


class WeightPatchDescriptor(TypedDict):
    """A compiled knowledge patch applied to a model's weights, modeled as a Lasm projection.

    The core records what a patch claims to carry and the digest that identifies the deployed
    artifact. It does not compute digests, compile, serve, or probe patches.
    """

    id: str
    name: str
    purpose: str
    baseModelId: str
    digest: str
    projection: LasmProjectionReferences
