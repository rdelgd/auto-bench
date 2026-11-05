# Note: `lasm-core` 0.6.0 Is Ready for Review

For LogicalAssembly and Rastro developers and their agents, copied to
in-vitro-patching (patchrig).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-note-on-0.6.0-ready-for-review.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **0.6.0 is implemented,** for patchrig's hosted-adapter findings, as
   LogicalAssembly asked. Patchrig has agreed to the schema adjustments.
2. **LogicalAssembly: please review the design.** We're holding the
   `v0.6.0` tag until you do.
3. **Rastro: nothing is needed from you.** No new event types and no new
   grants.

## What 0.6.0 Adds
- **Version 2 of `evidence.recorded` and `verdict.recorded`.** Each has:
  - a run identity (`runId`, `attempt`), and an adapter identity (`kind`,
    `model`, `host`, `served`, and optional `route`);
  - one verdict per claim (`claimId`), with `predicted` and free-form
    `statistics`.
- **An optional `adapters` list in an invalidation's scope.** An entry
  matches by equality on model and host, plus `kind`, `route`, or `served`
  when given.
- **`project_verdicts` reads both versions.**
  - Version 2 groups come back in a new `runs` list.
  - `cells` and its types are unchanged.

Patchrig's two-step finding (two runs, four claims) projects as four
`current` groups with no findings.

Read the design with:

```bash
reffy remote cat .reffy/reffyspec/changes/add-findings-evidence-v2/design.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## For LogicalAssembly
The points most worth a look:
- **`runs` beside `cells`,** rather than one record type with an optional
  `cellId`. This keeps your 0.5.0 code type-checking.
- **Scope lists reach only measurements that carry their field:**
  - larql and vindex lists never touch hosted findings;
  - `adapters` never touches weight-rig cells;
  - commit and scorer lists reach both.
- **A verdict citing the other version's measurement** is reported
  (`verdict.measurement_version_mismatch`) and isn't a candidate.
- **The same gate applies to runs:** don't act on a group that is
  `conflicting` or `unresolved`, or that has a finding.

## For Rastro
Version 2 events use the same event types on the same streams, so the
`patchrig-witness` grants already cover them. The schema version is in your
envelope, and you never read `data`.
