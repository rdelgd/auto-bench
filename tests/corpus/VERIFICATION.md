# Migration Verification: TypeScript → Python

Parity and packaging results for the ReffySpec change `migrate-lasm-core-to-python`, recorded 2026-09-22.

## TypeScript baseline

| Item | Result |
| --- | --- |
| Source revision | `56460752edfe8a17e4f761d141ec2bb7a0f704f4`; no working-tree diff in core source, tests, or package configuration |
| Tooling | Node.js v24.12.0, TypeScript 5.9.3, macOS arm64 |
| `npm run typecheck` | Passed |
| `npm test` | 17/17 passed |
| Reference corpus | 129 cases in `tests/corpus/reference/`, produced by `tests/corpus/generator/generate-reference-corpus.mjs` from the compiled TypeScript. Two independent runs produced identical output. After cutover, the documented reproduction (a fresh `git worktree` at the recorded revision, then `npm ci`, a build, and the generator) reproduced the corpus byte-for-byte. |

The first corpus draft included the sequence `1e20`, an integer-valued number outside the wire safe-integer range. Both the Python decoder and `jsonschema` rejected that document, as the design requires. The case was outside the corpus domain the design defines, so it was replaced with `1e15`, the generator now refuses such values, and the corpus was regenerated from TypeScript. No expected output was ever produced from Python.

## Parity

| Check | Result |
| --- | --- |
| Python vs. TypeScript reference, type-aware comparison (`tests/test_parity.py`) | 129/129 match, 0 mismatches, on the first run of the port |
| Repeat-call equality and nested input non-mutation, every corpus case | 129/129 pass |
| Corpus covers every public behavioral export, constant, and fixture export | Pass |
| Unexplained mismatches | None |

No evaluator defects were found that need a separate behavior change. At cutover, the port kept these JavaScript behaviors. The later change `adopt-python-native-text-and-number-semantics` replaced them with Python semantics and recorded each affected case in `deviations.json`:

- JavaScript `String.prototype.trim` whitespace semantics for required-string and actor checks (`lasm_core._js.js_trim`). Python's `str.strip()` differs: it strips `\x1c`–`\x1f` and `\x85`, and it leaves `\ufeff` in place.
- JavaScript number spelling in duplicate-sequence messages (`1e-7`, `0.000001`, `1` for `1.0`).
- Treating an integer-valued float (`1.0`, as decoded from JSON) as JavaScript treats the number `1`.

## Python checks

| Check | Python 3.11.0 (minimum) | Python 3.13.11 (development) |
| --- | --- | --- |
| `pytest`: 507 tests covering parity, ported behavior tests, interchange, schemas, Sans I/O, and identity | Pass | Pass |
| `mypy --strict` over `src/lasm_core` and `scripts` | Pass | Pass |
| `scripts/write_schemas.py --check` | — | Pass |

The interchange tests validate every corpus input and reference output against the checked-in schemas using both `jsonschema` (Draft 2020-12, dev-only) and the pure Python decoder, and require the two to agree. They also cover 24 structural rejection cases plus non-finite and invalid-JSON text, omission versus `null`, scalar-type preservation, and arbitrary evidence keys. Semantically invalid payloads decode and still receive their domain findings.

The Sans I/O tests evaluate, validate, normalize, encode, and decode with `open`, `os` file and environment access, sockets, subprocesses, and clocks patched to raise. In a fresh interpreter, importing `lasm_core` loads only the standard library and does not import `lasm_core.fixtures`.

## Packaging

`uv build` produced `lasm_core-0.2.0-py3-none-any.whl` and `lasm_core-0.2.0.tar.gz`. Each was installed into a clean virtual environment outside the source tree, on 3.11 and on 3.13, and run with `PATH=/usr/bin:/bin`, so no Node.js or npm was available:

| Distribution | 3.11 | 3.13 |
| --- | --- | --- |
| Wheel: imported from site-packages; `py.typed` and 7 schema files present; fixture validated and evaluated (`conformant: true`); interchange round trip | Pass | Pass |
| Sdist (built from source): same checks | Pass | Pass |
| Declared runtime requirements | None | None |

The sdist's own test suite, including the parity corpus, passed 507/507 against the installed 3.11 wheel with the extracted `src/` removed.

## Consumer audit

No repository consumer or sibling-workspace consumer of `@lasm/core` exists. See `docs/api-inventory.md`, "Consumer Audit".

## Cutover

After the checks above passed, the TypeScript core, Node tests, and build configuration were removed, along with the package metadata, the lockfile, and the ignored `dist/` and `node_modules/` directories. `dist/` contained only `tsc` output; `node_modules/` contained only `typescript`, `@types/node`, and `undici-types`. The post-removal results are recorded below.

## Post-removal checks

Run with `PATH` limited to `~/.local/bin:/usr/bin:/bin`, so `node` is not on `PATH`:

| Check | Result |
| --- | --- |
| `uv run pytest` on 3.13.11, including the retained JSON corpus parity tests | 507 passed |
| `uv run pytest` on 3.11.0 | 507 passed |
| `uv run mypy` | Pass |
| `uv run python scripts/write_schemas.py --check` | Pass |
| `uv build` (wheel and sdist) | Pass |

Normal build, test, fixture, and evaluation workflows do not require Node.js. Only the provenance generator needs Node, and it runs against a checkout of the recorded TypeScript revision.
