# Reply: `invalidation.retracted` Accepted

For in-vitro-patching (patchrig), LogicalAssembly, and Rastro developers and
their agents. This answers `in-vitro-patching-reply-on-retracting-invalidations.md`
(project `in-vitro-patching`), which asked `lasm-core` to agree a name for
retracting an invalidation.

Date: 2026-10-31. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-retracting-invalidations.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **We accept `invalidation.retracted`,** in its own `judgement:` stream,
   written once, with `cites` and `reason`. Rastro can add it to
   `patchrig-witness` when LogicalAssembly agrees.
2. **We also accept both exclusions:** no retracting a retraction, and no
   retracting a verdict.
3. **Three points to settle the shape:**
   - `cites` names a stream, not one event;
   - projections read `cites` and never parse stream ids;
   - event data is camelCase.
4. **Nothing changes in `lasm-core` yet.** The name joins the vocabulary with
   `verdict.recorded` and `verdict.invalidated` when the verdict projection
   is built.

## Why the Name Works
- **It follows the ledger's pattern,** a noun and a past-tense verb, like
  `policy.accepted` and `decision.made` in `lasm-core` 0.4.0.
- **The noun is the thing withdrawn.** A retraction withdraws an
  invalidation, and the verdicts it covered are not touched.
- **The projection rule is simple.** An invalidation applies only while no
  `invalidation.retracted` cites it. The verdicts it covered then fall back
  to the existing rule: the current verdict per (cell, pre-registration) is
  the one nothing supersedes.

The exclusions are right too:
- **A wrong retraction** is honestly recorded as a new invalidation, with its
  own condition and date.
- **A wrong verdict** is already handled by a re-score naming it in
  `supersedes`, or by an invalidation.

## Three Points on the Shape

### 1. `cites` is a stream id, not an event reference
A verdict's `cites` points at one event, a stream id and a stream version,
because a measurement stream holds exactly one event. An invalidation stream
holds one `verdict.invalidated` event per affected verdict, all stating one
condition. A retraction withdraws that whole condition, so it cites the
invalidation **stream**:

```json
{
  "type": "invalidation.retracted",
  "data": {
    "cites": "judgement:invalidation@<instrument>@<date>",
    "reason": "The control was sound; the drift came from the export step."
  }
}
```

The two meanings then look different: `cites` as an object means "this
event", and `cites` as a string means "this stream".

### 2. Projections read `cites`, never stream names
The proposed stream id,
`judgement:invalidation-retraction@<invalidation stream id>@<date>`, embeds
another stream id that already contains `:` and `@`, so it can't be parsed
reliably. That's fine, because nothing should parse it. The name is for
people and for the one-per-day collision guard. The projection finds what a
retraction withdraws from `cites` alone. The same holds for every stream id
in the ledger, including the ones `lasm-core` 0.4.0 builds with
`policy_stream_id` and `application_stream_id`.

### 3. Event data is camelCase
The verdict and invalidation examples in `lasm-paseo-assembly-source-of-truth.md`
use snake_case (`stream_id`, `scorer_version`, `policy_event`).
`lasm-core` records use camelCase wire names. That's a project convention,
and the 0.4.0 ledger events already follow it: `policyId`, `streamId`,
`streamVersion`, `projectionPosition`. Once the verdict projection exists,
patchrig's events are validated against `lasm-core` schemas, so their data
should be camelCase from the first cell:

| Example today | `lasm-core` data |
| --- | --- |
| `cites.stream_id`, `cites.stream_version` | `cites.streamId`, `cites.streamVersion` |
| `scorer_version` | `scorerVersion` |
| `policy_event` | `policyEvent` |
| `manipulation_check`, `records_digest`, `ledger_position` | `manipulationCheck`, `recordsDigest`, `ledgerPosition` |

Rastro's envelope (`stream_id`, `expected_version`, `schema_version`) is
Rastro's and stays snake_case. Only `data` follows `lasm-core`.

## What Happens Next
- **LogicalAssembly:** if you agree to the name, say so, and Rastro can
  authorize it.
- **Rastro:** once LogicalAssembly agrees, add `invalidation.retracted` to
  `patchrig-witness` for `judgement` streams.
- **auto-bench:** a ReffySpec change for the verdict projection, adding
  `evidence.recorded`, `verdict.recorded`, `verdict.invalidated`, and
  `invalidation.retracted` with schemas, before patchrig's first verified
  cell. If patchrig can tell us roughly when that cell is due, we'll plan
  around it.
