# Change: Add Version 2 Evidence and Verdict Events for Findings

## Why

Patchrig pivoted on 2026-11-03, from testing weight edits to checking observers through hosted adapters, and it has a first pre-registered finding ready to append. `lasm-core` 0.5.0 can't carry it:

- **`evidence.recorded` version 1 is the LARQL rig's shape.** It requires `larqlVersion`, `larqlBinarySha256`, `vindexPin`, `patchDigest`, and a cell. A hosted-adapter run has none of them.
- **`verdict.recorded` version 1 has no claim identity.** The finding is two runs, each answering two claims. Under version 1, two claims on one run fall into one group and are reported as a conflict.

LogicalAssembly asked for this in `lasm-reply-to-patchrig-pivots-and-first-finding.md`. Patchrig supplied the draft event data, with real numbers, in `in-vitro-patching-reply-to-auto-bench-on-findings-schema.md`. This change fits version 2 to that data and nothing more.

## What Changes

- **Add `evidence.recorded` version 2,** for a run measured through an adapter. It carries:
  - the run identity: `runId`, `attempt`, and `runKind`;
  - `recordsDigest`, `patchrigCommit`, and `claimScope`;
  - an `adapter` identity: `kind`, `model`, `host`, optional `route`, and `served`;
  - a list of `measurements` items, with named `carrier` and `tunedThreshold`, the rest free-form;
  - optional `inputs`, `fixture`, `preregistration`, and `tier`.
- **Add `verdict.recorded` version 2:**
  - it adds `claimId` and a required `claim`, an optional `predicted` (a list of verdict values), and an optional free-form `statistics`;
  - it keeps the four verdict values, the closed `cannotTellReason` rule, `detail`, `supersedes`, and `policyEvent`.
- **Add an optional `adapters` list to `verdict.invalidated` version 1's scope.** Each entry matches by equality on `model` and `host`, plus `kind`, `route`, and `served` when given. This is additive, since no invalidation has been written yet.
- **Extend `project_verdicts` to read versions 1 and 2 side by side.**
  - Version 2 groups are per (`runId`, `attempt`, `claimId`, `preregistration`), returned in a new `runs` list next to `cells`.
  - A verdict citing a measurement of the other version is reported, and is not a candidate.
  - Each scope list matches only measurements that carry its field.
- **Keep version 1 readable and unchanged,** for anything the shelved LARQL rig may write.
- **Bump the package to `0.6.0`.**

## Impact

- Affected capability: `findings-evidence-v2` (new). `evidence-and-verdict-events` from `add-evidence-and-verdict-events` is unchanged in behavior, apart from the additive scope list and the additive `runs` key on the projection result.
- Affected implementation:
  - `src/lasm_core/_schema_ledger.py`, `src/lasm_core/verdict.py`, `src/lasm_core/ledger.py` (version table only), and `__init__.py`;
  - the rendered schemas: two new files, and `verdict.invalidated.v1.schema.json` gaining `adapters`;
  - `tests/`, docs, and `pyproject.toml`.
- Compatibility:
  - Every 0.5.0 event validates and projects exactly as before.
  - A 0.5.0 reader rejects version 2 events as unsupported, and rejects an invalidation that uses `adapters`. Both are expected, and nothing has been written yet.
  - LogicalAssembly pins `v0.6.0` before projecting findings.
- Out of scope:
  - `receipt.recorded`, which waits for `observer/1`;
  - checks, which never enter the ledger;
  - `evidence.recorded` on `evaluation:` streams;
  - ordering dates;
  - interpreting `statistics`, `measurements`, `inputs`, or `fixture`.

## Supersedes

None

## Reffy References

- `lasm-reply-to-patchrig-pivots-and-first-finding.md` (project `nuveris`) - LogicalAssembly's request: `evidence.recorded` version 2 with a run identity and an adapter identity, version 1 kept readable, an adapter scope list, and the projection reading both versions
- `in-vitro-patching-update-two-pivots-and-a-first-finding.md` (project `in-vitro-patching`) - the pivot, and the first finding with its four claims
- `in-vitro-patching-reply-to-auto-bench-on-findings-schema.md` (project `in-vitro-patching`) - the draft event data, and patchrig's answers on run identity, adapter identity, the tuned threshold, and fields that no longer apply
- `lasm-core-note-on-findings-schema.md` - the claim-grouping gap, and the request for real data
- `lasm-core-reply-on-findings-event-data.md` - the five adjustments to patchrig's draft
- `in-vitro-patching-reply-agreeing-to-findings-adjustments.md` (project `in-vitro-patching`) - patchrig's agreement, the full commit hash, and the definition of `served`
