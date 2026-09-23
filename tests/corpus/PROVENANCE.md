# Reference Corpus Provenance

`reference/*.json` holds inputs and expected outputs recorded from the TypeScript `@lasm/core`
implementation before it was retired. It is never edited. `tests/test_parity.py` requires the Python
implementation to reproduce every expected output, after applying the reviewed deviations in
[`deviations.json`](deviations.json). **Never regenerate expected outputs from Python.** A mismatch is
either a defect to fix, or a deliberate behavior change. A deliberate change adds a deviation entry with
its reason and ReffySpec change.

## Reference source

| Item | Value |
| --- | --- |
| Package | `@lasm/core@0.1.0` (private) |
| Source revision | `56460752edfe8a17e4f761d141ec2bb7a0f704f4` (`docs(reffy): add LASM workbench research`) |
| Working-tree diff in `src/`, `test/`, `package*.json`, `tsconfig.json` | None. The only uncommitted changes were Reffy planning files. |
| Node.js | v24.12.0 |
| TypeScript | 5.9.3 (`typescript@^5.8.0`, `@types/node@^24.0.0`, from `package-lock.json`) |
| Platform | macOS (darwin 25.5.0, arm64) |
| Recorded | 2026-09-22 |
| Baseline | `npm run typecheck` passed; `npm test` passed 17/17 |

## Reproduction

```sh
git worktree add ../lasm-ts-reference 56460752edfe8a17e4f761d141ec2bb7a0f704f4
cd ../lasm-ts-reference
npm ci && npm run build
node <this-repo>/tests/corpus/generator/generate-reference-corpus.mjs dist/src <output-dir>
diff -r <output-dir> <this-repo>/tests/corpus/reference
```

The generator was run twice at the recorded revision and produced identical output. It rejects its own
cases if a call mutates its recorded arguments, or if a value falls outside the corpus domain (non-finite
numbers, `-0`, `undefined`, or integers beyond the safe range).

## Encoding

Each case is `{id, function, description, args, expected}`. `function` is the TypeScript export
name; `fixture:<name>` cases record a fixture export. `logicalAssemblyEntryIds` returns a
JavaScript `Set`, which `JSON.stringify` would erase, so it is recorded as `{"$set": [sorted members]}`
and compared by membership. No other result is sorted.

## Comparison rules

Parsed payloads are compared with a type-aware comparator (`tests/corpus_support.py`). It ignores
object-key order and numeric spelling of the same number, and nothing else: booleans never equal
numbers, missing keys never equal `null`, and every array must match in order, including events,
findings, messages, paths, attribution, and evidence references.

## Coverage

129 cases across every public behavioral export, the reference fixture, and each existing
TypeScript test. Migration-sensitive edges include:

- equal-sequence ties, omitted sequences, and an explicit `MAX_SAFE_INTEGER` sequence tying with the omitted-sequence sentinel
- negative, fractional, and duplicate sequences, with messages that depend on JavaScript number spelling
- findings addressed by original input index
- whitespace JavaScript trims (`\u00a0`, `\ufeff`, `\u2028`) and characters it does not trim (`\u200b`, `\u001c`, `\u0085`, `\u180e`)
- stale, disputed, and mixed provenance; omitted and lossy projections; missing facts
- missing, late, and absent confirmation and policy gates; low- and high-risk tools
- prohibited transitions and outcomes; attributed, unattributed, and subjectless failures
- unmodeled and missing control surfaces; normalization findings deduplicated against validation
- empty collections, omitted optional fields, and nested evidence containing `false`, `0`, `""`, and `null`

## Deviations

`deviations.json` maps case IDs to a `reason` and JSON Patch operations (`add`, `remove`, `replace`)
applied to the recorded `expected` value. The test suite rejects entries for unknown cases, entries
without a reason, and entries that change nothing. The current entries come from
`adopt-python-native-text-and-number-semantics`, which replaced JavaScript whitespace, number-spelling,
and omitted-sequence-sentinel emulation with Python semantics (6 of 129 cases).

## Parity result

See [VERIFICATION.md](VERIFICATION.md): 129/129 cases matched with no unexplained mismatches.
