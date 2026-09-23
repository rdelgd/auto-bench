# Migrating from `@lasm/core` (npm) to `lasm-core` (Python)

`lasm-core` 0.2.0 replaces the private npm package `@lasm/core` 0.1.0. This is a breaking change:
there is no npm package, compatibility wrapper, generated TypeScript client, or in-process JavaScript
evaluator. Lasm's behavior and payload vocabulary are unchanged.

## What changed

| Before | After |
| --- | --- |
| `npm install` | `uv sync` (or `pip install lasm-core` from a locally built wheel) |
| `import { evaluateConformance } from "@lasm/core"` | `from lasm_core import evaluate_conformance` |
| `import { routineMaintenanceConformanceCase } from "@lasm/core/fixtures"` | `from lasm_core.fixtures import routine_maintenance_conformance_case` |
| camelCase functions | snake_case functions ([full mapping](api-inventory.md)) |
| TypeScript interfaces | `TypedDict` records with the **same camelCase keys** |
| Node.js 22+ | Python 3.11+ |

## What did not change

- Record keys, IDs, event types, enum strings, finding codes, severities, paths, messages,
  dimension order, attribution values, and `trace:<position>` evidence references.
- Validation, trace normalization, evaluation, finding deduplication, and `valid`/`conformant`
  aggregation. The Python port was verified against outputs recorded from the TypeScript
  implementation (see `tests/corpus/PROVENANCE.md`).

## Intentional differences from TypeScript

Lasm uses Python semantics instead of emulating JavaScript. These differences only affect unusual inputs:

- Blank checks for required strings and trace actors use `str.strip()`. For example, `\x1c` and `\x85`
  count as blank, and a lone byte-order mark (`\ufeff`) counts as content.
- Unsequenced trace events sort after every numbered event. In TypeScript they sorted as
  `Number.MAX_SAFE_INTEGER`, so an explicit sequence of that value tied with them.
- Duplicate-sequence messages use Python number spelling (`Duplicate id: 1e-07`, not `1e-7`).

Sequences compare as numbers, so `1` and `1.0` are the same integer sequence, because JSON does not distinguish them.
Each affected reference case is listed with its reason in `tests/corpus/deviations.json`.

## Calling Lasm from TypeScript or other languages

Exchange JSON documents through an adapter, such as a subprocess, job, or service that you own. Lasm
does not ship a transport. Version 1 documents wrap an unchanged payload:

```json
{ "schemaVersion": 1, "kind": "conformance-case", "value": { "assembly": {}, "scenario": {} } }
```

`value` is abbreviated here. The kinds are `logical-assembly`, `conformance-case`, `raw-trace`,
`trace-normalization-result`, `validation-result`, and `conformance-evaluation`. JSON Schema
Draft 2020-12 definitions are packaged under `lasm_core/schemas/v1/`.

`schemaVersion` is the interchange format version. It is independent of the package version and of
`assembly.version`. The wire rules are:

- Optional fields are omitted, not `null`. `null` is valid only inside JSON-valued fields
  such as evidence, observed values, and state-field values.
- Array order is significant. Object-key order and whitespace are not.
- Numbers must be finite. Integer-valued numbers must lie within ±9007199254740991. Strings and
  booleans are never coerced to numbers.
- Unknown structural properties are rejected. Evidence and value maps accept arbitrary keys.
- An unwrapped payload is not a document. Wrap it explicitly (`wrap_document`).

Schemas check shape only. Empty strings, dangling IDs, unknown raw event types, missing raw actors,
and invalid sequences still decode, and the domain validators then report them as findings.

```python
from lasm_core import decode_document, encode_document, evaluate_conformance

decoded = decode_document(request_text, "conformance-case")
if not decoded["valid"]:
    reply(decoded["findings"])  # structured format.* findings; no payload is supplied
else:
    evaluation = evaluate_conformance(decoded["value"])
    reply(encode_document(evaluation, "conformance-evaluation")["text"])
```
