# Change: Migrate Lasm Core to Python

## Why

Lasm's proposed workbench places evaluation, scheduled checks, source comparison, and data-platform integration around the core library. A Python implementation would let Python adapters, notebooks, and evaluation workflows invoke the same domain logic directly, without introducing a Node process or service solely to call Lasm.

The current implementation is a private `0.1.0` TypeScript package with no runtime dependencies and approximately 1,350 lines of core source, excluding fixtures and tests. This is a contained opportunity to change implementation language before integrations grow. The rationale is integration fit; the domain model and its correctness do not depend on Python.

The accepted direction is a behavior-preserving port of the entire core, followed by retirement of the TypeScript implementation. Lasm remains the domain library, and Auto Bench remains the automotive workbench that evaluates it.

## What Changes

- **BREAKING:** Replace the private npm package `@lasm/core` with the Python distribution `lasm-core`, imported as `lasm_core`. Public Python functions use snake_case; domain type names retain their existing meaning.
- Port all public models, helpers, validators, evidence normalization, evaluation mechanics, and the automotive reference fixtures, retaining the deterministic Sans I/O boundary.
- Define versioned JSON interchange contracts for assemblies, conformance cases, traces, and results. Preserve existing payload field names, identifiers, enum values, finding codes, paths, and evidence references.
- Capture the TypeScript implementation's outputs in a shared regression corpus and require differential parity before retiring it. Keep that corpus as Python regression coverage after cutover.
- Keep one canonical evaluator after migration. TypeScript consumers may use the JSON contracts through adapters; an npm compatibility wrapper, generated TypeScript client, and browser evaluator are outside this change.
- Replace core build/test/package tooling and update active documentation and project conventions when the migration ships. Historical artifacts and archived changes remain historical records.

## Impact

- Affected capability: `establish-auto-bench-sans-io-core`; its established capability identifier remains unchanged.
- Affected implementation: `src/*.ts`, `src/fixtures/`, `test/`, `package.json`, `package-lock.json`, `tsconfig.json`, and generated TypeScript build output; replacement Python package, tests, schema artifacts, and packaging configuration.
- Affected active documentation: README, project context, development commands, package/import examples, and the canonical capability purpose and requirements at archive time.
- Compatibility: npm imports and JavaScript execution are intentionally discontinued at cutover. Existing JSON payload vocabulary is preserved inside a new versioned interchange envelope. There is no claim of Python API source compatibility with TypeScript imports.
- Release scope: build and verify installable local Python artifacts. Public registry publication, a Databricks deployment, and live integration work are excluded.
- This proposal creates planning files only. Implementation tasks remain pending, and canonical specifications continue to describe the shipped TypeScript library until implementation and archival.

## Supersedes

- `establish-sarb-sans-io-core` — supersedes the original TypeScript/Node implementation choice while retaining the Sans I/O architecture.
- `center-reality-validation-stack` — supersedes the TypeScript implementation and npm package identity while retaining Lasm's domain model and Auto Bench's role.
- `finish-lasm-identity-migration` — updates active import/package references from `@lasm/core` to the Python package; the Lasm name remains unchanged.

## Reffy References

- `lasm-reality-workbench-on-databricks.md` — motivates direct use from evaluation and data-platform workflows, and establishes that orchestration, storage, integrations, and UI stay outside the core.

The language decision and the requirement to preserve behavior were agreed in the September 22, 2026 discussion accompanying this proposal. The workbench artifact remains exploratory; this migration does not approve or implement its broader architecture.
