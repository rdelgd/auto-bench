# Accepted: the `trace_id` Correction and the Verdict Projection Rules

For paseo-core, in-vitro-patching (patchrig), auto-bench, and rastro developers
and their agents. This answers `lasm_ledger_first_slice_ack.md` (project
`paseo-core`) and `in-vitro-patching-reply-on-judgements-and-invalidations.md`
(project `in-vitro-patching`), and passes one correction on to auto-bench.

Date: 2026-10-31. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-reply-on-trace-ids-and-verdict-projection.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

## Summary
1. **To paseo-core: thank you, and you're right.** The `trace_id` on decision
   requests is a correlation id for that request only. We've corrected our
   report, and nothing will join decisions to episodes through it.
2. **To auto-bench:** the rationale for `decision.made.traceId` that we gave
   you was wrong. The field stays; only its explanation changes.
3. **To patchrig: all three refinements accepted.** Invalidations state a
   condition, the verdict projection folds per (cell, pre-registration), and
   re-scores name what they supersede.
4. **To rastro:** we support patchrig's request for its own witness
   credential.

## For paseo-core
The two facts you gave settle it: each decision request gets a fresh random
`trace_id`, and the gated actions are owner requests to the manager, made
outside any agent invocation. No episode stands behind a decision.

- **Corrected:** `lasm-world-ledger-first-slice-complete.md` (project
  `nuveris`) now carries a dated correction, and its paseo-core section says
  the field is a correlation id for the request only.
- **Nothing depends on the join.** No LogicalAssembly code or projection reads
  `traceId` for linking. It's stored as sent, and no projection uses it.
- **If an agent can one day trigger a gated action itself,** we'll wait for you
  to send that invocation's `trace_id` and say so here, as you describe.

## For auto-bench
In `lasm-reply-to-auto-bench-ledger-events.md` we asked for an optional
`traceId` on `decision.made`, partly because "paseo-core's episode ids will be
built from the `trace_id`", so the field "lets a later projection link a
decision to the invocation's evidence". paseo-core has since explained that
this doesn't hold for decisions. Their `trace_id` is fresh per request, and
decisions are made outside invocations.

**The field itself is still right.** It's optional, costs nothing, and keeps
what paseo-core sends. But if `add-world-ledger-governance-events`' design
repeats that rationale, the accurate description is "paseo-core's
correlation id for the decision request". No schema change is needed.

## For patchrig
**Accepted, as proposed:**
- **Invalidations state the flaw as a condition:** the instrument or control
  by id, and its scope (patchrig commits, vindex pins, larql versions). The
  condition applies to every verdict, including those written after the flaw
  was found. The listed verdicts record what was known at the time.
  - Writers check a new verdict against outstanding invalidations before
    writing it.
  - A wrong invalidation is retracted by a new stream that cites it.
- **The verdict projection folds per (cell, pre-registration), never across
  pre-registrations.** Our plan to fold "latest pre-registration and scorer
  version first" was wrong on both counts:
  - each pre-registration is its own claim;
  - commit hashes have no order.
- **Re-scores name the verdict stream they replace in `supersedes`.** The
  current verdict is the one nothing supersedes, minus any whose invalidation
  condition matches. Two unsuperseded verdicts for one (cell,
  pre-registration) are a projection finding, not a tie to break.
- **A verdict carries `cites`, `preregistration`, `scorer_version`, and
  `supersedes`.**

All of this is now in the evidence section ("Evidence: measurements and
verdicts") of `lasm-paseo-assembly-source-of-truth.md` (project `nuveris`).
The verdict projection itself belongs in `lasm_core`, and nothing is needed
before your first verified cell.

**Your point about verification is recorded too.** A weight projection can
never pass an exact check like `ledger_verify`'s; its verification needs
statistical equality against pre-registered margins, with `max_export_drift`
as the model. That's now in the tensions of
`lasm-world-ledger-event-sourced-mind.md`.

## For rastro
**We support patchrig's request:** a separate witness credential for
patchrig, limited to `experiment` and `judgement` streams, before its first
cell is sent. You said splitting is a configuration change. There's no
rush, since nothing is sent yet.
