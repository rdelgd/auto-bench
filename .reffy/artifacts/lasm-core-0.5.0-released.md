# Released: `lasm-core` 0.5.0, Evidence and Verdict Events

For LogicalAssembly, in-vitro-patching (patchrig), and Rastro developers and
their agents. This closes the `add-evidence-and-verdict-events` change
(project `auto-bench`).

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-0.5.0-released.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **`v0.5.0` is tagged.** Pin it with:
   ```
   lasm-core @ git+ssh://git@github.com/rdelgd/auto-bench.git@v0.5.0
   ```
2. **Four event types:** `evidence.recorded`, `verdict.recorded`,
   `verdict.invalidated`, and `invalidation.retracted`. Each has a version 1
   data schema in `lasm_core/schemas/ledger/`.
3. **One projection:** `project_verdicts(events)`, the current verdict per
   (`cellId`, `attempt`, `preregistration`).
4. **Additive:** the 0.4.0 governance events and their schemas are
   unchanged.

## What's in It
Every agreement from these notes is in the schemas or the projection:
- **Verdicts:** `holds`, `inconclusive`, `fails`, `cannot-tell`.
- **`cannotTellReason`:** one of `no-probes`, `too-few-values`,
  `degenerate-stratum`, `instrument-gate-failed`, or `no-eligible-chains`.
  It's required with `cannot-tell` and rejected on any other verdict, and a
  violation is reported at the field (`verdict.reason_required`,
  `verdict.reason_not_allowed`). `detail` is optional on any verdict.
- **Measurements** require:
  - `patchrigCommit`, `larqlVersion`, and `larqlBinarySha256`;
  - `claimScope`, a description that is never matched against;
  - `cellId` without the attempt, with `attempt` as its own field.
- **Invalidation scopes** have four lists, and every present list must match:

  | List | Matches |
  | --- | --- |
  | `patchrigCommits` | the measurement's `patchrigCommit` |
  | `scorerVersions` | the verdict's `scorerVersion` |
  | `vindexPins` | the measurement's `vindexPin` |
  | `larqlVersions` | the measurement's `larqlVersion` |

- **Conventions:** camelCase keys, kebab-case values, and absent optional
  fields omitted, never `null`.

The projection works in this order:
1. **Grouping:** one group per (cell, attempt, pre-registration). Groups never
   fold across attempts or pre-registrations.
2. **Supersession:** applied first, and permanent. A cycle removes every
   verdict in it, and is reported.
3. **Invalidation:** removes the verdicts it cites, plus every verdict its
   condition matches, including verdicts written later. An empty scope
   matches by citation only.
4. **Retraction:** makes an invalidation inert.
5. **Status:** each group gets exactly one:

   | Status | Meaning |
   | --- | --- |
   | `current` | one verdict remains |
   | `conflicting` | several remain; listed, reported, never tie-broken |
   | `invalidated` | invalidations removed what remained |
   | `unresolved` | nothing remains for another reason (a cycle, or unknown measurements); findings explain why |

It reads citations, never stream ids, and ignores event types it doesn't own.

## For Each of You

**LogicalAssembly**
- **Pin `v0.5.0`** when you start projecting verdicts. The 0.4.0 API is
  unchanged, so moving the pin doesn't touch the governance projection.
- **Gate as you described:** don't act on a group that is `conflicting` or
  `unresolved`, or that has a finding addressed to one of its events.
- **`manipulationCheck`** is copied onto each projected verdict and never
  acted on. Whether it counts is your judgement.

**Patchrig**
- **Build event data to the checked-in schemas:**
  - `schemas/ledger/evidence.recorded.v1.schema.json`
  - `schemas/ledger/verdict.recorded.v1.schema.json`
  - `schemas/ledger/verdict.invalidated.v1.schema.json`
  - `schemas/ledger/invalidation.retracted.v1.schema.json`

  They're plain JSON Schema 2020-12 files, so your Rust event builder can
  test against them without Python.
- **Map at export:** snake_case keys and values in your records become
  camelCase keys and kebab-case values in event data. For example,
  `cannot_tell` becomes `cannot-tell`, and `no_probes` becomes `no-probes`.
- **A new reason code** still follows the agreed order: you propose it, we
  release, LogicalAssembly updates its pin, and then you emit it.

**Rastro**
- **Authorize the event types for `patchrig-witness`:**

  | Stream kind | Event types |
  | --- | --- |
  | `experiment` | `evidence.recorded` |
  | `judgement` | `verdict.recorded`, `verdict.invalidated`, `invalidation.retracted` |

  `invalidation.retracted` is the one type that wasn't settled when you
  wrote the witness configuration. There's no rush: patchrig sends nothing
  before its first verified cell.

## What's Not in It
- **`evidence.recorded` on `evaluation:` streams,** for auto-bench's own
  findings. That needs its own shape, in a later version.
- **A generic pin map** for a second measuring witness. That would be a
  version 2 of `evidence.recorded`.
- **Narrowing an invalidation by instrument.** That needs measurements to
  list their instruments.
- **Ranking criteria, or deciding what a verdict means for a policy.**
  Those stay in the rig and in LogicalAssembly.
