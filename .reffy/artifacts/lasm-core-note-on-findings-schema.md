# Note: Schemas for patchrig's Findings, Built From Real Data

For in-vitro-patching (patchrig) and LogicalAssembly developers and their
agents, copied to Rastro. This answers the auto-bench section of
`lasm-reply-to-patchrig-pivots-and-first-finding.md` (project `nuveris`), on
`in-vitro-patching-update-two-pivots-and-a-first-finding.md` (project
`in-vitro-patching`).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-note-on-findings-schema.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **Agreed: findings need a version 2,** and version 1 stays readable for
   the shelved LARQL rig.
2. **One gap: `verdict.recorded` needs a version 2 too.** One verdict per
   claim, as proposed, would make the projection report the first finding as
   a conflict.
3. **One request to patchrig:** post the event data you'd append for the
   two-step finding. We'll write the version 2 schemas to fit it.
4. **Receipts wait for `observer/1`,** as LogicalAssembly said.

And congratulations on the first finding. Four claims, all four outcomes,
all predicted in advance: that's the vocabulary working as intended.

## 1. Agreed
`evidence.recorded` version 1 is the LARQL rig's shape. Hosted adapters have
no larql, no vindex, no patch, and no cell. So version 2 needs:
- **a run identity** in place of `cellId` and `attempt`;
- **an adapter identity** in place of the larql and vindex fields;
- **a scope list** so an invalidation can reach findings measured through a
  flawed adapter.

`project_verdicts` will read versions 1 and 2. That's already supported by
`LEDGER_EVENT_SCHEMA_VERSIONS`.

## 2. The Gap: One Measurement, Four Claims
The projection groups verdicts by (`cellId`, `attempt`, `preregistration`),
and two unsuperseded verdicts in one group are a conflict. The two-step
finding is one confirmation run under one pre-registration, with four claims:

| Claim | Verdict |
| --- | --- |
| Luna, catalogue only | `holds` |
| Jev, catalogue only | `holds` |
| Luna, rules and drills in context | `inconclusive` |
| Jev, rules and drills in context | `fails` |

Under version 1, all four would cite the same measurement, fall into one
group, and come out as `conflicting`, with no current verdict. That isn't
what happened: each claim has its own answer.

So a verdict needs to say **which claim** it judges. We propose a
`verdict.recorded` version 2 with a `claimId`. The projection then groups by
(run, claim, pre-registration), and a re-score supersedes within one claim
only. Version 1 verdicts keep grouping as they do now.

## 3. The Request: Your Draft Event Data
Rather than design version 2 from a field list, we'd like to fit it to the
events you'd actually append. Please post, as JSON:
- **the `evidence.recorded` data** for the confirmation run;
- **the four `verdict.recorded` data objects,** one per claim.

Use whatever field names feel right. We'll map them to `lasm-core`
conventions, and say where we changed something and why.

While drafting, these are the points we can't settle without you:
- **Run identity:** what identifies a confirmation run, and can one run be
  re-done (an attempt)?
- **Adapter identity:** you listed kind, model, endpoint host, and the date
  served. Is that enough to tell two adapters apart? For example, would the
  same model through two gateways count as two adapters?
- **The tuned threshold:**
  - The thresholds don't transfer (0.02 for Luna, 0.30 for Jev), so each
    finding depends on its adapter's threshold.
  - Is it part of the measurement, or of the claim?
  - Should it be a named field rather than sitting inside the free-form
    `measurements`?
- **Fields that may not apply:** do `manipulationCheck`, `tier`,
  `controlsState`, and `environment` still apply to a hosted-adapter run? Any
  that don't will be optional or absent in version 2.

We'll keep version 2 to what this finding needs, and add nothing for checks
or receipts.

## 4. Receipts
We agree with LogicalAssembly:
- **Receipts are records** of what an observer answered, not verdicts.
- **Their volume** looks like episode ingest, not write-once judgements.
- **Their shape** should wait until `observer/1` settles.

When it does, propose `receipt.recorded` through the usual process, and we'll
define it then.

## Next
- **Patchrig:** post the draft event data and your answers to section 3.
- **auto-bench:** then a small change: `evidence.recorded` v2,
  `verdict.recorded` v2 with `claimId`, one adapter scope list, and the
  projection reading both versions. It lands before your first append, and
  we'll release it as `v0.6.0`.
