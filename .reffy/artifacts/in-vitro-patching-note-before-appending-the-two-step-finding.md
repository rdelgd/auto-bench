# Note: Three Points Before We Append the Two-Step Finding

For auto-bench (`lasm-core`) developers and their agents, copied to
LogicalAssembly and Rastro. This follows `lasm-core-0.6.0-released.md`
(project `auto-bench`) and LogicalAssembly's instructions for appending to
the local Rastro.

Date: 2026-11-05. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-note-before-appending-the-two-step-finding.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **The six events are built and validated, but not sent.** There are two
   `evidence.recorded` and four `verdict.recorded` events, all version 2.
   - `lasm-core` 0.6.0's validator accepts all six.
   - `project_verdicts` gives four `current` runs, with no findings.
2. **They differ from the data we agreed in three places.** Ledger events
   can't be edited once appended, so we'd like you to confirm these first.

## The Three Points

### 1. Jev's combined-carrier prediction
**We'd send `["inconclusive", "fails"]`, not `["fails"]`.**

The pre-registration predicted that "the combined cells do not reach the
margin", for both models alike. Our result table, and then our agreement
reply, narrowed Jev's prediction to Fails. That narrowing was written after
the run.

`predicted` should be what was written before the run, so the builder takes
it from the pre-registration. Both combined cells carry
`["inconclusive", "fails"]`, and both chart cells carry `["holds"]`. Jev's
verdict, Fails, is within its prediction either way.

### 2. No `route` on Jev's adapter
**We'd leave it out.**

We proposed `route` as the gateway's resolved provider. But the runs never
recorded it, so the `"typesafe-ai"` in our draft was a guess. `route` is
optional, and we'd rather not fill a field from memory.

The adapter would be:
`{"kind": "decisions", "model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "served": "2026-11-04"}`.

### 3. Numbers at full precision
**We'd send the numbers exactly as the run's `metrics.json` holds them,** for
example `"gain": 0.24270833333333336`. Our draft rounded them to four
places.

Unrounded, they recompute from the records exactly. `lasm-core` doesn't
interpret `measurements` or `statistics`, so this changes nothing for
projections.

## Also Settled by the Builder, for Information
- **Streams.**
  - Evidence: `experiment:<run id>`.
  - Verdicts: `judgement:<claim id>@2026-11-03@<commit>`, Rastro's documented
    form, with the claim id as the cell id.
- **`scorerVersion`** is the bare 40-character commit, which the exact length
  requires.
- **Event ids** are `patchrig:<stream id>#1`, deterministic, so a re-send is
  a replay.
- **`tier`** is `hosted`, and `fixture` is `{"generatorVersion": 4, "n": 12}`.
- **`served`** is the date the confirmation check started.
- **A second attempt** made from the same commit would reuse a judgement
  stream's name. When there is one, we'll add the attempt to the stream id.

## What We Need
A yes, or corrections, on points 1 to 3. Then we append, evidence first, as
LogicalAssembly described.
