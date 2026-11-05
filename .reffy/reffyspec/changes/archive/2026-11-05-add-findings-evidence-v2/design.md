## Context

`lasm-core` 0.5.0 defines the evidence and verdict events around patchrig's LARQL rig. A measurement is one cell, with weight-rig pins. A verdict judges one measurement under one pre-registration. The projection groups verdicts by (`cellId`, `attempt`, `preregistration`).

Patchrig now checks observers through hosted adapters (OpenAI's Decisions API, the Vercel AI Gateway). Its first finding is one pre-registration, two confirmation runs (Luna and Jev), and four claims, one per (model, carrier):

| Run | Claim | Verdict |
| --- | --- | --- |
| `two-step-20261104-092458` (Luna) | chart | `holds` |
| `two-step-20261104-092458` (Luna) | explanation and training | `inconclusive` |
| `two-step-20261104-092604` (Jev) | chart | `holds` |
| `two-step-20261104-092604` (Jev) | explanation and training | `fails` |

Version 2 is designed from patchrig's draft event data for exactly this finding.

## Goals / Non-Goals

Goals:

- The two-step finding validates and projects as four `current` groups, with no findings.
- Version 1 keeps working unchanged, alongside version 2.
- Invalidations can reach findings through a flawed adapter, and never cross into the other version's fields by accident.

Non-goals:

- Receipts, checks, evaluation evidence, a general pin map for other witnesses, or date ranges.
- Interpreting rig-specific numbers. They're carried in free-form objects, and only fields a reader must have are named.

## Decisions

### 1. Two new versions, one additive field

- **`evidence.recorded` and `verdict.recorded` get version 2,** because their required fields change. `LEDGER_EVENT_SCHEMA_VERSIONS` becomes `(1, 2)` for both.
- **`verdict.invalidated` stays version 1** and gains an optional `adapters` scope list. No invalidation has been written, so adding the field within the version breaks no data. This follows the rule already used for reason codes: readers upgrade before writers use the new field.

### 2. `evidence.recorded` version 2

```python
class AdapterIdentity(TypedDict):
    kind: str                 # e.g. "decisions"
    model: str                # e.g. "gpt-6-luna"
    host: str                 # e.g. "api.openai.com"
    route: NotRequired[str]   # a gateway's resolved provider
    served: str               # UTC start date of the run, YYYY-MM-DD; one date per run

class RunInput(TypedDict):    # descriptive; never read by the projection
    role: str                 # e.g. "tune", "confirm"
    runId: str
    recordsDigest: str
    seeds: NotRequired[str]

class MeasurementItem(TypedDict, total=False):  # open: other keys are free-form JSON
    carrier: str
    tunedThreshold: float

class EvidenceRecordedDataV2(TypedDict):
    runId: str
    attempt: int
    runKind: str
    recordsDigest: str
    patchrigCommit: str       # full 40-character commit; see decision 5
    claimScope: str
    adapter: AdapterIdentity
    measurements: Sequence[MeasurementItem]
    inputs: NotRequired[Sequence[RunInput]]
    fixture: NotRequired[Mapping[str, JsonValue]]
    preregistration: NotRequired[str]   # descriptive; the verdict's is the one grouped on
    tier: NotRequired[str]
```

**Why these fields:**
- **`measurements` is a list of items.** In schema terms, each item is an object whose `carrier` (string) and `tunedThreshold` (number) are typed, with any other key allowed as a JSON value. Patchrig asked for `tunedThreshold` as a named field because a result can't be read without it. It's optional because other run kinds may have no threshold.
- **`fixture` is free-form.** It describes the rig's fixtures (a generator version, a catalogue size). Nothing matches on it.
- **Fields dropped from version 1:** `manipulationCheck`, `controlsState`, `environment`, and the four weight-rig pins. Patchrig confirmed none of them applies to a hosted-adapter run.

### 3. `verdict.recorded` version 2

```python
class VerdictRecordedDataV2(TypedDict):
    runId: str
    attempt: int
    claimId: str
    claim: str                          # the claim judged, as pre-registered
    cites: LedgerEventRef               # the evidence.recorded v2 event judged
    preregistration: str
    scorerVersion: str                  # full 40-character commit; see decision 5
    verdict: VerdictValue
    supersedes: NotRequired[str]
    cannotTellReason: NotRequired[CannotTellReason]  # iff verdict == "cannot-tell"
    detail: NotRequired[str]
    predicted: NotRequired[Sequence[VerdictValue]]
    statistics: NotRequired[Mapping[str, JsonValue]]
    policyEvent: NotRequired[LedgerEventRef]
```

**Decisions on these fields:**
- **`claimId`** is what makes one verdict per claim possible. Like stream ids, it's opaque: nothing parses it.
- **`predicted`** is a list of verdict values, not text. Patchrig's "inconclusive or fails" becomes `["inconclusive", "fails"]`, so the schema checks it and a reader can compare it with `verdict` without parsing. It's kept because writing the prediction down first is what made this a finding.
- **`statistics`** is one free-form object for numbers the scorer used, such as `margin`, `gain`, `lo`, and `hi`. They aren't top-level keys, because they're rig-specific.
- **The `cannotTellReason` rule** is the version 1 rule, through the same `if`/`then`/`else`, with the same addressed findings.
- **`cites` is a `LedgerEventRef`,** as in version 1. Patchrig's draft shows a run id there, which the projection can't follow.

### 4. The `adapters` scope list

```python
class AdapterMatch(TypedDict):
    model: str
    host: str
    kind: NotRequired[str]
    route: NotRequired[str]
    served: NotRequired[str]

class InvalidationScope(TypedDict):     # version 1, extended
    patchrigCommits: NotRequired[Sequence[str]]
    scorerVersions: NotRequired[Sequence[str]]
    vindexPins: NotRequired[Sequence[str]]
    larqlVersions: NotRequired[Sequence[str]]
    adapters: NotRequired[Sequence[AdapterMatch]]
```

**How an entry matches.** An entry matches a measurement's `adapter` when every field the entry gives is equal. The scope list matches when any entry matches.

**Equality, not a date range.** Patchrig suggested a "before date X" bound, but the projection never orders dates (`preregistration` and `served` are strings written by people). An invalidation reaching several served dates lists one entry per date. This loses nothing: an invalidation is written after the fact, so the affected served dates are known, and later findings, served later, shouldn't match it.

**Matching across versions.** Every present list must match, as before. A list whose field the measurement doesn't carry never matches:

| List | Matches on version 1 | Matches on version 2 |
| --- | --- | --- |
| `patchrigCommits` | measurement `patchrigCommit` | measurement `patchrigCommit` |
| `scorerVersions` | verdict `scorerVersion` | verdict `scorerVersion` |
| `vindexPins`, `larqlVersions` | measurement fields | never |
| `adapters` | never | measurement `adapter` |

So an invalidation of a larql version can't reach a hosted finding, and an adapter invalidation can't reach a LARQL cell.

### 5. Full commit hashes

**What patchrig's draft sent:** `patchrigCommit: "ec8e708727c6"` (12 characters), and `scorerVersion: "two-step@ec8e708727c6"`. In October, patchrig agreed that `patchrigCommit` is the full commit hash.

**Why it matters:** scope matching is exact string equality, so an invalidation naming the full hash would silently miss a short one, and vice versa.

**What version 2 asks for:** the full 40-character hash in both fields, with `scorerVersion` as the plain commit. The run kind is already in `runKind`.

**What the schema enforces:** exact lengths, at LogicalAssembly's suggestion in `lasm-review-findings-evidence-v2.md`:
- 40 characters for `patchrigCommit` and `scorerVersion`;
- 10 characters for `served`, in both `AdapterIdentity` and `AdapterMatch`.

The shared checker gains `minLength` and `maxLength` for this, kept in agreement with `jsonschema`, which also counts code points. It isn't full validation, since a 40-character non-hex string passes, but it turns the two likeliest mistakes (a short hash, and an unpadded date) into rejected events, instead of invalidations that silently miss. `pattern` stays unsupported, because regular-expression dialects differ between the checker and `jsonschema`.

The rule applies to version 2 fields only. Version 1 stays exactly as released in 0.5.0.

### 6. The projection

`VerdictProjection` gains `runs: Sequence[RunVerdict]` beside `cells`:

```python
class ProjectedRunVerdict(TypedDict):
    runId: str
    attempt: int
    claimId: str
    claim: str
    preregistration: str
    scorerVersion: str
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    predicted: NotRequired[Sequence[VerdictValue]]
    statistics: NotRequired[Mapping[str, JsonValue]]
    policyEvent: NotRequired[LedgerEventRef]
    adapter: AdapterIdentity            # from the cited measurement
    source: LedgerEventRef
    measurement: LedgerEventRef

class RunVerdict(TypedDict):
    runId: str
    attempt: int
    claimId: str
    preregistration: str
    status: CellVerdictStatus
    current: NotRequired[ProjectedRunVerdict]
    candidates: NotRequired[Sequence[LedgerEventRef]]
    invalidatedBy: NotRequired[Sequence[str]]
```

**Why a separate list:** `cells` and its record types are unchanged, so LogicalAssembly's 0.5.0 code keeps type-checking. Version 1 and version 2 groups have different identities, and a single record type would make `cellId` optional for everyone.

**What stays the same:** the resolution is shared, so both versions get the same rules:
- grouping;
- permanent supersession, with cycles reported;
- invalidation by citation and by condition, and retraction;
- the four statuses and every finding code.

**Grouping across versions:** groups are keyed with their version, so a `cellId` and a `runId` that happen to be equal never meet. A version 2 verdict whose `supersedes` names a version 1 verdict (or the reverse) is in another group, and is reported as `verdict.invalid_supersedes`.

**Citing across versions:** a verdict citing a measurement of the other version is reported as `verdict.measurement_version_mismatch` at its `cites`, and is not a candidate.

`project_verdicts([])` returns `{"cells": [], "runs": [], "findings": []}`.

### 7. Package

Version `0.6.0`. The new exports are:
- the records and literals above: `AdapterIdentity`, `RunInput`, `MeasurementItem`, `EvidenceRecordedDataV2`, `VerdictRecordedDataV2`, `AdapterMatch`, `ProjectedRunVerdict`, and `RunVerdict`.

They go in the API inventory. No new callables are added.

## Risks

- **Free-form objects hide drift.** Anything in `statistics`, `measurements` items, or `fixture` can change shape without a schema version. That's intended, because only named fields are contracts. The remedy, if a reader comes to depend on a free-form key, is to name it in a later version.
- **Length is not format.** A 40-character string that isn't a hash, or a 10-character string that isn't a date, still passes (decision 5). Patchrig's writer-side rules cover the rest.

## Resolved Questions

Patchrig agreed to all five adjustments in `in-vitro-patching-reply-agreeing-to-findings-adjustments.md`:

1. **Commit hashes:** full 40-character hashes, unprefixed in `scorerVersion`. The two-step finding's commit is `ec8e708727c6760577e8ae1cceed0adce450528a`.
2. **`cites`:** an event reference, with the run id in `runId`.
3. **`predicted`:** a list. The four verdicts carry `["holds"]`, `["holds"]`, `["inconclusive", "fails"]`, and `["fails"]`.
4. **Numbers:** the scorer's numbers go in `statistics`. `claim`, `claimId`, and `tunedThreshold` stay named.
5. **Adapter scopes:** equality, with one entry per served date.

**`served` defined:**
- It's the UTC date the run started, written `YYYY-MM-DD`.
- A run that crosses midnight carries its start date, so every event from one run matches the same scope entry.
- Patchrig defines it in its `observer/1` change. For the two-step finding, it's `2026-11-04` for both runs.

**`preregistration` spelling:** patchrig writes it from one constant, so its spelling is identical on every verdict.

LogicalAssembly accepted the design in `lasm-review-findings-evidence-v2.md`. It suggested exact lengths for commits and `served`, which decision 5 adopts, and extended its gate to `runs`.

## Open Questions

None.
