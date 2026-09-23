## 1. Establish the Migration Baseline

- [x] 1.1 Inventory all public root and fixture exports, map them to Python names/types, and audit repository consumers plus known integration references.
- [x] 1.2 Run the existing TypeScript build, typecheck, and tests; record source revision, relevant working-tree diff, runtime/tool versions, and reproduction commands.
- [x] 1.3 Export language-independent JSON inputs and expected outputs from the TypeScript implementation for every public behavioral function and existing behavioral test, explicitly encoding set-valued helper results without losing membership.
- [x] 1.4 Extend the corpus with migration-sensitive ordering, omission, numeric/boolean, provenance, invalid-input, and non-mutation cases described in the design; preserve reference provenance.

## 2. Establish Interchange Contracts

- [x] 2.1 Define version 1 JSON Schemas for the document envelope and all public domain records used by assemblies, cases, traces, and results; preserve current payload names.
- [x] 2.2 Define structural rejection findings and test version/kind handling, optional omission versus null, arbitrary evidence maps, scalar types, finite/safe numeric bounds, and unknown fields.
- [x] 2.3 Verify schemas admit the corpus's structurally valid but semantically invalid cases so domain validators retain responsibility for their findings.

## 3. Implement the Python Core

- [x] 3.1 Add `pyproject.toml`, `src/lasm_core/`, typed-package metadata, development tooling, and Python 3.11 minimum support; keep platform/framework packages out of runtime dependencies.
- [x] 3.2 Port all domain records, constants, and helper functions from the export inventory with explicit typing and preserved wire keys.
- [x] 3.3 Port every individual validator and aggregate conformance-case validation, preserving codes, paths, messages, severity, and finding order.
- [x] 3.4 Port trace validation/normalization, ordering and position rules, omitted-sequence handling, event filtering, and evidence references.
- [x] 3.5 Port the eight evaluation dimensions, attribution, finding deduplication, and `valid`/`conformant` aggregation without semantic redesign.
- [x] 3.6 Port the service-scheduling reference fixture and its public exports into `lasm_core.fixtures`, separate from root imports.
- [x] 3.7 Implement pure versioned-document encoding/decoding with structured format findings, preserving payload round trips and the Sans I/O boundary.

## 4. Prove Parity and Packaging Before Retirement

- [x] 4.1 Run both implementations against the recorded corpus using a type-aware JSON comparator; require equality of all result fields and ordered arrays, including finding messages and evidence references.
- [x] 4.2 Run Python static checks, schema validation, accepted/rejected document tests, repeatability tests, and nested input non-mutation tests on the minimum and selected development interpreters.
- [x] 4.3 Verify domain calls run with application-level I/O unavailable, no platform credentials or SDKs, and no fixture initialization through the core root import.
- [x] 4.4 Build wheel and source distributions; install each into a clean environment outside the source tree and verify root/fixture imports, schema assets, and a full conformance evaluation.
- [x] 4.5 Record the parity and packaging results (`tests/corpus/VERIFICATION.md`); resolve every unexplained mismatch before cutover and record unrelated evaluator defects separately.

## 5. Cut Over to One Canonical Implementation

- [x] 5.1 Update in-scope consumers and document the npm-to-Python migration, including the wire envelope and the absence of an npm compatibility wrapper.
- [x] 5.2 Retain the JSON regression corpus and reference-source provenance; remove the retired TypeScript core, Node-based tests/build configuration, obsolete core package metadata/lockfile, and scoped obsolete build artifacts only after section 4 passes.
- [x] 5.3 Update the README, development commands, package examples, and project context for Python while preserving historical artifacts and archived changes.
- [x] 5.4 Run the retained Python regression, typing, schema, and package-install checks after removal; verify normal build/test/evaluation workflows do not need Node.

## 6. Reconcile Planning and Close the Change

- [x] 6.1 Run `reffy plan validate migrate-lasm-core-to-python` and `reffy validate`; verify artifact links and affected capability paths.
- [x] 6.2 Preview archival and verify the `TypeScript Sans I/O Core` rename and all package-reference updates apply to `establish-auto-bench-sans-io-core` without introducing a second capability.
- [x] 6.3 After implementation and verification are complete, archive the change and update the canonical capability purpose to describe the Python core; leave existing archives unchanged.
