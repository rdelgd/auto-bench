from __future__ import annotations

import sys
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib

ROOT = Path(__file__).resolve().parents[1]


def test_active_package_metadata_and_readme_use_the_lasm_identity() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert project["name"] == "lasm-core"
    assert "operational meaning" in project["description"]
    assert project["requires-python"] == ">=3.11"
    assert project["dependencies"] == []
    assert "from lasm_core import" in readme
    assert "Nuveris Core" not in readme and "@nuveris/core" not in readme


def test_api_inventory_documents_every_public_symbol() -> None:
    import lasm_core
    import lasm_core.fixtures

    inventory = (ROOT / "docs" / "api-inventory.md").read_text(encoding="utf-8")
    missing = [name for name in [*lasm_core.__all__, *lasm_core.fixtures.__all__] if f"`{name}`" not in inventory]
    assert missing == []
