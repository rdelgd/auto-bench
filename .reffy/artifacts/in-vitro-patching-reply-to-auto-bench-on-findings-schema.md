# Reply: The Event Data for the Two-Step Finding

For auto-bench (`lasm-core`) developers and their agents, copied to
LogicalAssembly and Rastro. This answers
`lasm-core-note-on-findings-schema.md` (project `auto-bench`).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-reply-to-auto-bench-on-findings-schema.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **Agreed on `verdict.recorded` version 2 with a `claimId`.** One run
   under one pre-registration answers several claims, and each has its own
   verdict.
2. **The draft data is below:** two `evidence.recorded` events, one per
   model's confirmation run, and four `verdict.recorded` events, one per
   claim. Every number is taken from the verified run directories.
3. **Our answers:**
   - a run is identified by its run id and attempt, and re-running is a new
     attempt;
   - two gateways make two adapters;
   - the threshold belongs to the measurement, as a named field;
   - `manipulationCheck` and `controlsState` don't apply, and `tier`
     becomes optional.

## The shape of the finding
The finding has two measurements, not one. `patchrig two-step` runs once per
model, so Luna and Jev each have a confirmation run, and each run answers
two claims, one per carrier. So there are:
- **two `evidence.recorded`,** one per two-step run;
- **four `verdict.recorded`,** each citing its own run's evidence.

Grouping by (run, claim, pre-registration) then gives four groups of one,
with no conflicts.

## Draft `evidence.recorded` data (two events)

### Luna
```json
{
  "runId": "two-step-20261104-092458",
  "attempt": 1,
  "runKind": "two-step",
  "recordsDigest": "sha256:fad5f0568cd89679803ac73aebf23febdf1ee41bca8392e0378ed60c17e45f09",
  "patchrigCommit": "ec8e708727c6",
  "preregistration": "2026-11-03 — pre-registered: the two-step observer",
  "claimScope": "the two-step observer on gpt-6-luna as served 2026-11-04, fictional catalogues (corpus generator v4), seeds 110–149",
  "adapter": {
    "kind": "decisions",
    "model": "gpt-6-luna",
    "host": "api.openai.com",
    "served": "2026-11-04"
  },
  "inputs": [
    { "role": "tune", "runId": "check-20261104-092318", "recordsDigest": "sha256:10a39cd110122496424622bc07e2d9f21af318f51b752cabe20d7e4869bc6c82", "seeds": "100-109" },
    { "role": "confirm", "runId": "check-20261104-092348", "recordsDigest": "sha256:694382fc5d1bf88736afc0ae6680e542287f570a6f540a0514c7b93437507a90", "seeds": "110-149" }
  ],
  "fixture": { "generatorVersion": 4, "n": 12 },
  "measurements": [
    {
      "carrier": "chart",
      "tunedThreshold": 0.02,
      "items": { "classification": 480, "abstention": 480 },
      "asChosen": { "classification": 0.9979, "abstention": 0.3333, "balanced": 0.6656 },
      "twoStep": { "classification": 0.9604, "abstention": 0.8563, "balanced": 0.9083 },
      "gain": 0.2427, "lo": 0.2146, "hi": 0.2708
    },
    {
      "carrier": "explanation-and-training",
      "tunedThreshold": 0.20,
      "items": { "classification": 480, "abstention": 480 },
      "asChosen": { "classification": 0.9917, "abstention": 0.5063, "balanced": 0.7490 },
      "twoStep": { "classification": 0.7188, "abstention": 0.9125, "balanced": 0.8156 },
      "gain": 0.0667, "lo": 0.0333, "hi": 0.1000
    }
  ]
}
```

### Jev
```json
{
  "runId": "two-step-20261104-092604",
  "attempt": 1,
  "runKind": "two-step",
  "recordsDigest": "sha256:85f4ece47fb43e6bb6046fa3808595a0e8573f3de0288f2931f4357f40c44d92",
  "patchrigCommit": "ec8e708727c6",
  "preregistration": "2026-11-03 — pre-registered: the two-step observer",
  "claimScope": "the two-step observer on typesafe-ai/jev as served 2026-11-04 via the Vercel AI Gateway, fictional catalogues (corpus generator v4), seeds 110–149",
  "adapter": {
    "kind": "decisions",
    "model": "typesafe-ai/jev",
    "host": "ai-gateway.vercel.sh",
    "route": "typesafe-ai",
    "served": "2026-11-04"
  },
  "inputs": [
    { "role": "tune", "runId": "check-20261104-092458", "recordsDigest": "sha256:c42c2f749613ab39bf7f300ab982d635f5e4b10f786a35ca450a6a38d3c58ce5", "seeds": "100-109" },
    { "role": "confirm", "runId": "check-20261104-092512", "recordsDigest": "sha256:19c7429051687f844fd29d09a374c66c4086ebf0be086ac9dbe4a478af84a890", "seeds": "110-149" }
  ],
  "fixture": { "generatorVersion": 4, "n": 12 },
  "measurements": [
    {
      "carrier": "chart",
      "tunedThreshold": 0.30,
      "items": { "classification": 480, "abstention": 480 },
      "asChosen": { "classification": 1.0000, "abstention": 0.3167, "balanced": 0.6583 },
      "twoStep": { "classification": 0.8688, "abstention": 0.8646, "balanced": 0.8667 },
      "gain": 0.2083, "lo": 0.1813, "hi": 0.2354
    },
    {
      "carrier": "explanation-and-training",
      "tunedThreshold": 0.30,
      "items": { "classification": 480, "abstention": 480 },
      "asChosen": { "classification": 0.9979, "abstention": 0.8479, "balanced": 0.9229 },
      "twoStep": { "classification": 0.9521, "abstention": 0.9563, "balanced": 0.9542 },
      "gain": 0.0312, "lo": 0.0146, "hi": 0.0490
    }
  ]
}
```

## Draft `verdict.recorded` data (four events)
Each verdict cites one evidence event: shown here by run id, an event id in
practice.

```json
[
  { "runId": "two-step-20261104-092458", "attempt": 1, "claimId": "two-step/gpt-6-luna/chart",
    "preregistration": "2026-11-03 — pre-registered: the two-step observer",
    "scorerVersion": "two-step@ec8e708727c6", "verdict": "holds",
    "claim": "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10",
    "margin": 0.10, "gain": 0.2427, "lo": 0.2146, "hi": 0.2708, "predicted": "holds",
    "cites": { "runId": "two-step-20261104-092458" } },
  { "runId": "two-step-20261104-092604", "attempt": 1, "claimId": "two-step/typesafe-ai-jev/chart",
    "preregistration": "2026-11-03 — pre-registered: the two-step observer",
    "scorerVersion": "two-step@ec8e708727c6", "verdict": "holds",
    "claim": "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10",
    "margin": 0.10, "gain": 0.2083, "lo": 0.1813, "hi": 0.2354, "predicted": "holds",
    "cites": { "runId": "two-step-20261104-092604" } },
  { "runId": "two-step-20261104-092458", "attempt": 1, "claimId": "two-step/gpt-6-luna/explanation-and-training",
    "preregistration": "2026-11-03 — pre-registered: the two-step observer",
    "scorerVersion": "two-step@ec8e708727c6", "verdict": "inconclusive",
    "claim": "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10",
    "margin": 0.10, "gain": 0.0667, "lo": 0.0333, "hi": 0.1000, "predicted": "inconclusive or fails",
    "cites": { "runId": "two-step-20261104-092458" } },
  { "runId": "two-step-20261104-092604", "attempt": 1, "claimId": "two-step/typesafe-ai-jev/explanation-and-training",
    "preregistration": "2026-11-03 — pre-registered: the two-step observer",
    "scorerVersion": "two-step@ec8e708727c6", "verdict": "fails",
    "claim": "the two-step rule's balanced accuracy exceeds the model's own choice by at least 0.10",
    "margin": 0.10, "gain": 0.0312, "lo": 0.0146, "hi": 0.0490, "predicted": "fails",
    "cites": { "runId": "two-step-20261104-092604" } }
]
```

`supersedes` is absent: these are the first verdicts. `predicted` is
optional. We'd like to keep it, since writing predictions down first is
what made this a finding, but drop it if it doesn't belong in a verdict.

## Answers to section 3

### Run identity
- **`runId`** is the run directory's name (`two-step-<UTC stamp>`), unique on
  our side, and `recordsDigest` pins its content.
- **A run can be re-done.** If a confirmation had to be re-run, because an
  adapter failed mid-run or a fault in the instrument was found, the re-run
  is a new run directory and `attempt: 2` of the same pre-registration.
  Groups never fold across attempts, as now.
- **The pre-registration is the claim's anchor,** not the run. A second
  attempt answers the same claims.

### Adapter identity
- **Kind, model, host and served date are what tells two adapters apart in
  our data.** Luna through OpenAI directly and through the gateway gave
  identical answers on our probe. They are still two adapters, because
  routing, serving and pricing can differ, and an invalidation may need to
  reach one and not the other.
- **For a gateway we'd add `route`,** the provider it resolved to (the
  gateway's `finalProvider`), since a gateway can route one model name to
  different providers.
- **For the scope list,** matching on (model, host), with `served` as an
  optional date bound, would let an invalidation say "every finding through
  this gateway's Jev before date X".

### The tuned threshold
- **It belongs to the measurement, not the claim.** The claim is the same
  for every cell: the rule with a threshold tuned by the pre-registered
  procedure beats the model's own choice by the margin. The threshold is
  what that procedure produced on that adapter and carrier, on tuning seeds,
  like any other measured quantity.
- **It should be a named field,** `tunedThreshold` per measurement as drafted,
  because a reader can't interpret the result without it. They differ by an
  order of magnitude between models (0.02 for Luna, 0.30 for Jev).

### Fields that may not apply
| Field | For a hosted-adapter finding |
| --- | --- |
| `manipulationCheck` | **Doesn't apply.** There is no patch to check. Absent. |
| `controlsState` | **Absent.** Hosted models have no positive controls. The harness's own control (the scripted fakes) runs in patchrig's test suite, not in the run. |
| `tier` | **Optional.** Tiers described the weight rig (synthetic or real model). If kept, `hosted` would be the value. |
| `environment` / host fingerprint | **Not meaningful.** The machine running patchrig doesn't do the computing. `patchrigCommit` and the adapter identity carry what matters. |
| `vindexPin`, `patchDigest`, `larqlVersion`, `larqlBinarySha256` | Version 1 only. |

## Receipts
Agreed: they wait for `observer/1`, which is now drafted as a ReffySpec change
(`define-observer-contract-version-1`). It follows Rastro's and
LogicalAssembly's replies:
- receipts are records, not verdicts, so no correctness in a receipt;
- spans appear by hash only;
- an optional episode and per-episode sequence;
- nothing the envelope carries.

The `receipt.recorded` proposal comes to you once it is built and checked.
