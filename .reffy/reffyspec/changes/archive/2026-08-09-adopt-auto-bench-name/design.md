## Context
The repository distinguishes Nuveris Core, the reusable agentic control-plane implementation, from its automotive reference benchmark. The benchmark was previously called SArB. This change renames only that benchmark to Auto Bench.

## Goals / Non-Goals
- Goals:
  - Use **Auto Bench** consistently for the automotive benchmark.
  - Use `auto-bench` for current machine-readable identifiers and paths.
  - Keep current documentation, artifacts, metadata, and canonical specs aligned.
- Non-Goals:
  - Rename Nuveris Core or `@nuveris/core`.
  - Change benchmark behavior, fixtures, domain models, or evaluators.
  - Rewrite archived ReffySpec changes, which are an append-only historical ledger.

## Decisions
- Decision: Use `Auto Bench` in prose and `auto-bench` in slugs, filenames, directory names, and Reffy metadata.
  - Rationale: This preserves the user's requested two-word name while providing a conventional machine-safe form.
- Decision: Historical archive entries retain `SArB` and `sarb`.
  - Rationale: ReffySpec requires archived changes to remain immutable; the new change records the superseding decision.
- Decision: Keep Nuveris naming intact.
  - Rationale: Nuveris names the reusable core, while Auto Bench names its automotive reference benchmark.

## Migration
1. Update current prose and metadata from SArB to Auto Bench.
2. Rename current artifact and canonical-spec paths to `auto-bench`.
3. Reindex and validate Reffy metadata.
4. Validate and archive this superseding change after verification.

## Reffy Inputs
- agentic-control-primitives-for-auto-bench.md
- hle-template-for-a-generalized-reality-benchmark.md
- naming-the-agentic-control-layer.md
