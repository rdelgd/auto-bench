"""Render the JSON Schema files from ``lasm_core._schema_v1`` and ``lasm_core._schema_ledger``.

    uv run python scripts/write_schemas.py          # rewrite the checked-in files
    uv run python scripts/write_schemas.py --check  # fail if they are out of date
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from lasm_core import _schema_ledger, _schema_v1

SCHEMA_ROOT = Path(__file__).resolve().parents[1] / "src" / "lasm_core" / "schemas"
SCHEMA_SETS = {"v1": _schema_v1.schema_files, "ledger": _schema_ledger.schema_files}


def render(schema: object) -> str:
    return json.dumps(schema, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv
    stale = False
    for directory, schema_files in SCHEMA_SETS.items():
        schema_dir = SCHEMA_ROOT / directory
        expected = {name: render(schema) for name, schema in schema_files().items()}
        actual = {path.name: path.read_text(encoding="utf-8") for path in schema_dir.glob("*.json")}
        if check:
            stale = stale or expected != actual
            continue
        schema_dir.mkdir(parents=True, exist_ok=True)
        for name in set(actual) - set(expected):
            (schema_dir / name).unlink()
        for name, text in expected.items():
            (schema_dir / name).write_text(text, encoding="utf-8")
        print(f"wrote {len(expected)} schema files to {schema_dir}")
    if stale:
        print("schema files are out of date; run scripts/write_schemas.py", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
