# Reply: Five Adjustments to the Finding's Event Data

For in-vitro-patching (patchrig) developers and their agents, copied to
LogicalAssembly and Rastro. This answers
`in-vitro-patching-reply-to-auto-bench-on-findings-schema.md` (project
`in-vitro-patching`).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-findings-event-data.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **Thank you for real data.** Two runs and four claims gives four groups of
   one, so the grouping is right.
2. **The draft change is up:** `add-findings-evidence-v2`, for `v0.6.0`.
3. **Five adjustments to your draft,** below. We'd like your agreement before
   implementing.
4. **Everything else is adopted as drafted:**
   - the run identity, and the `adapter` object with `route`;
   - two gateways counting as two adapters;
   - `tunedThreshold` as a named field per measurement;
   - the fields you dropped.

Read the design with:

```bash
reffy remote cat .reffy/reffyspec/changes/add-findings-evidence-v2/design.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## The Five Adjustments

### 1. Full commit hashes, in both fields
Your draft has `patchrigCommit: "ec8e708727c6"` (12 characters) and
`scorerVersion: "two-step@ec8e708727c6"`. In October we agreed that
`patchrigCommit` is the full hash. That matters because scope matching is
exact string equality: an invalidation naming the full hash would silently
miss a finding carrying the short one.

Please send:
- **the full 40-character hash** in `patchrigCommit`;
- **`scorerVersion` as the plain full commit,** without the `two-step@`
  prefix. The run kind is already in `runKind`. A plain commit means
  `patchrigCommits` and `scorerVersions` lists use the same identifiers.

The schema can't enforce the length, so this is a rule for your event builder.

### 2. `cites` is an event reference
A verdict cites its measurement as `{"streamId": "…", "streamVersion": 1}`, as
in version 1. Your draft shows a `runId` there, and says an event id in
practice, but the projection follows neither. The run id stays in the
verdict's own `runId`.

### 3. `predicted` as a list of verdict values
Keep it: writing the prediction down first is what made this a finding. As a
list, the schema checks the values, and anyone can compare the prediction
with the verdict without parsing text:
- `"predicted": ["holds"]`
- `"predicted": ["inconclusive", "fails"]`, in place of
  `"inconclusive or fails"`

### 4. The verdict's numbers go in `statistics`
`margin`, `gain`, `lo`, and `hi` go in one free-form `statistics` object,
rather than at the top level. They're your scorer's numbers, and named
top-level keys would make every future scorer's numbers a schema change. The
`claim` text stays named and required, beside `claimId`.

### 5. Adapter scopes match by equality, not a date range
You suggested a scope entry like "this gateway's Jev before date X". The
projection never orders dates, because `served` and `preregistration` are
strings people write. So an `adapters` entry matches when every field it
gives is equal:

```json
"scope": {
  "adapters": [
    { "model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh" },
    { "model": "gpt-6-luna", "host": "api.openai.com", "served": "2026-11-04" }
  ]
}
```

**For "before date X",** list one entry per served date. Nothing is lost:
- An invalidation is written after the flaw is found, so the affected dates
  are known.
- Later findings were served later, and shouldn't match.

`kind` and `route` can narrow an entry the same way. Please keep `served` as
`YYYY-MM-DD`, since `2026-11-4` wouldn't match.

## A Corrected Verdict, for Reference

```json
{
  "runId": "two-step-20261104-092458",
  "attempt": 1,
  "claimId": "two-step/gpt-6-luna/explanation-and-training",
  "claim": "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10",
  "cites": { "streamId": "experiment:two-step-20261104-092458@1", "streamVersion": 1 },
  "preregistration": "2026-11-03 — pre-registered: the two-step observer",
  "scorerVersion": "<full 40-character commit>",
  "verdict": "inconclusive",
  "predicted": ["inconclusive", "fails"],
  "statistics": { "margin": 0.10, "gain": 0.0667, "lo": 0.0333, "hi": 0.1000 }
}
```

The stream id in `cites` is illustrative, since naming is yours. One more
thing: `preregistration` is grouped on by exact equality, em dash included,
so write it identically on every verdict.

## Next
- **Patchrig:** agree to the five points, or push back, and we implement.
- **LogicalAssembly:** review the design, as before. Projected findings
  arrive in a new `runs` list beside `cells`, so your 0.5.0 code keeps
  type-checking.
- **We release `v0.6.0`** before your first append.
