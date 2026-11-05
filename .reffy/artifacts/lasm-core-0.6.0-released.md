# Released: `lasm-core` 0.6.0, Version 2 Findings

For LogicalAssembly, in-vitro-patching (patchrig), and Rastro developers and
their agents. This closes `add-findings-evidence-v2` (project `auto-bench`).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-0.6.0-released.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **`v0.6.0` is tagged.** Pin it with:
   ```
   lasm-core @ git+ssh://git@github.com/rdelgd/auto-bench.git@v0.6.0
   ```
2. **Version 2 of `evidence.recorded` and `verdict.recorded`,** for findings
   measured through hosted adapters, one verdict per claim.
3. **One addition since the review:** exact lengths, as LogicalAssembly
   suggested. Short commit hashes and unpadded dates are now rejected.
4. **Additive.** Version 1, the governance events, and every 0.5.0 projection
   behave as before.

## What's in It
- **`evidence.recorded` version 2:**
  - `runId`, `attempt`, and `runKind`;
  - `recordsDigest`, `patchrigCommit`, and `claimScope`;
  - an `adapter`: `kind`, `model`, `host`, `served`, and optional `route`;
  - `measurements` items, with `carrier` and `tunedThreshold` named;
  - optional `inputs`, `fixture`, `preregistration`, and `tier`.
- **`verdict.recorded` version 2:**
  - `runId`, `attempt`, `claimId`, and `claim`;
  - `cites`, an event reference;
  - `preregistration`, `scorerVersion`, and `verdict`;
  - optional `predicted` (a list of verdict values), free-form `statistics`,
    `supersedes`, `cannotTellReason` (the same rule as version 1), `detail`,
    and `policyEvent`.
- **Exact lengths:** `patchrigCommit` and `scorerVersion` must be 40
  characters, and every `served` date 10, in both the adapter and adapter
  scope entries. That catches the two likeliest slips, a short hash and
  `2026-11-4`, which would otherwise make exact-match invalidations silently
  miss. It applies to version 2 only.
- **Invalidation scopes:** an optional `adapters` list. An entry matches when
  every field it gives is equal.
- **`project_verdicts`:**
  - version 2 groups, per (run, attempt, claim, pre-registration), come back
    in a new `runs` list beside `cells`;
  - scope lists reach only measurements that carry their field;
  - citations across versions are reported, not followed.

Patchrig's two-step finding projects as four `current` runs with no findings.

## For Each of You

**LogicalAssembly**
- Pin `v0.6.0` when you start projecting verdicts. The governance API is
  unchanged from 0.4.0.
- Your gate, as described, applies to both `cells` and `runs`.

**Patchrig**
- **Build the two-step finding** against
  `schemas/ledger/evidence.recorded.v2.schema.json` and
  `schemas/ledger/verdict.recorded.v2.schema.json`.
- **Include the corrections agreed earlier:**
  - the full commit `ec8e708727c6760577e8ae1cceed0adce450528a` in both
    commit fields;
  - `cites` as `{streamId, streamVersion}`;
  - `predicted` as lists;
  - numbers in `statistics`.
- **Send version 2 events with `schema_version: 2`** in Rastro's envelope.

**Rastro**
- Nothing to do. Version 2 uses the same event types on the same streams, so
  the `patchrig-witness` grants already cover it.

## What's Not in It
- `receipt.recorded`, which waits for `observer/1`.
- `evidence.recorded` on `evaluation:` streams.
- Any interpretation of `statistics`, `measurements`, `inputs`, or `fixture`.
