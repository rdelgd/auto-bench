"""Render the version 1 JSON Schema files from ``lasm_core._schema_v1``.

    uv run python scripts/write_schemas.py          # rewrite the checked-in files
    uv run python scripts/write_schemas.py --check  # fail if they are out of date
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from lasm_core._schema_v1 import schema_files

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "src" / "lasm_core" / "schemas" / "v1"


def render(schema: object) -> str:
    return json.dumps(schema, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    check = "--check" in argv
    expected = {name: render(schema) for name, schema in schema_files().items()}
    actual = {path.name: path.read_text(encoding="utf-8") for path in SCHEMA_DIR.glob("*.json")}
    if check:
        if expected != actual:
            print("schema files are out of date; run scripts/write_schemas.py", file=sys.stderr)
            return 1
        return 0
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    for name in set(actual) - set(expected):
        (SCHEMA_DIR / name).unlink()
    for name, text in expected.items():
        (SCHEMA_DIR / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} schema files to {SCHEMA_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
