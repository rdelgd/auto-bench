## Context

The evidence contract (`lasm-paseo-assembly-source-of-truth.md`, section "Evidence: measurements and verdicts") separates two kinds of evidence that change at different rates:

- **Measurements** are observations. Each is written once, when a verified run finishes, and never revised.
- **Verdicts** are judgements of a measurement against a dated pre-registration, by one version of the scoring code. A verdict is revised by writing a new stream: a re-score names what it supersedes, an invalidation states a flaw as a condition, and a retraction withdraws an invalidation.

Every stream is written exactly once, with `expected_version: 0`. Rastro keeps order and authorizes on (principal, stream kind, event type), and can't list streams. A reader therefore builds its own index by following the global log. Nothing parses stream ids. What an event refers to is always in its data: `cites` as an object (`streamId`, `streamVersion`) names one event, and `cites` as a string names a whole stream.

`lasm_core.ledger` (0.4.0) already holds the governance events, the per-event-type schema line in `schemas/ledger/`, `validate_ledger_event_data`, and the shared schema checker in `_json_schema.py`. This change extends that machinery and doesn't add a second one.

## Goals / Non-Goals

Goals:

- Write the agreed contract as schemas, so the first verified cell validates the day it's sent.
- Give LogicalAssembly one pure projection that answers "what is the current verdict for this cell and pre-registration, and why".
- Make every rule the parties agreed checkable: the closed reason codes, reason if and only if `cannot-tell`, no stream parsing, and conflicts reported rather than resolved.

Non-goals:

- Shapes for `evaluation:` streams, Auto Bench findings, or measurements by anything other than patchrig.
- Interpreting `measurements`, `detail`, `tier`, `scope`, or `controlsState`. They are carried, not read.
- Ranking criteria into one summary, writer-side invalidation checks, or deciding what a verdict means for a policy.
- Aggregates. Measurements and verdicts are facts about something that already happened, appended as such, like `decision.made`.

## Decisions

### 1. Placement

- **Event types:** `LedgerEventType` in `ledger.py` grows by four values. Schemas join `_schema_ledger.py` and render as `schemas/ledger/<type>.v1.schema.json`. `validate_ledger_event_data` covers them with no new code path.
- **Projection:** in a new module, `src/lasm_core/verdict.py`, with its records, re-exported from `lasm_core`. Governance and evidence projections stay in separate modules, and share the event view (`RecordedEvent`, `LedgerEventRef`) and the data validator.

### 2. Records

Keys are camelCase and enum values kebab-case, as in 0.4.0. Optional fields are omitted, never `null`. The contract's example shows `supersedes` as "or null", and data from patchrig must omit it instead.

```python
VerdictValue      = Literal["holds", "inconclusive", "fails", "cannot-tell"]
CannotTellReason  = Literal["no-probes", "too-few-values", "degenerate-stratum",
                            "instrument-gate-failed", "no-eligible-chains"]
ManipulationCheck = Literal["passed", "failed", "not-applicable"]

class MeasurementTarget(TypedDict):
    binding: str                          # "weight-patch" for patchrig
    ref: str                              # what was measured

class MeasurementEnvironment(TypedDict):
    host: str
    fingerprint: str

class EvidenceRecordedData(TypedDict):    # stream experiment:<cell-id>
    cellId: str
    attempt: int
    shardIndex: NotRequired[int]
    shardCount: NotRequired[int]
    target: MeasurementTarget
    vindexPin: str
    patchDigest: str
    patchrigCommit: str                   # proposed; see decision 6
    larqlVersion: str                     # proposed; see decision 6
    manipulationCheck: ManipulationCheck
    tier: str
    scope: str
    controlsState: str
    measurements: Mapping[str, JsonValue]
    recordsDigest: str
    environment: MeasurementEnvironment
    ledgerPosition: NotRequired[int]

class VerdictRecordedData(TypedDict):     # stream judgement:<cell-id>@<prereg>@<scorer>
    cellId: str
    attempt: int
    cites: LedgerEventRef                 # the one evidence.recorded event judged
    preregistration: str                  # date of the FINDINGS.md entry
    scorerVersion: str                    # git commit of the scoring code
    supersedes: NotRequired[str]          # the verdict stream this re-score replaces
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]  # iff verdict == "cannot-tell"
    detail: NotRequired[str]
    policyEvent: NotRequired[LedgerEventRef]

class InvalidationScope(TypedDict):
    patchrigCommits: NotRequired[Sequence[str]]
    vindexPins: NotRequired[Sequence[str]]
    larqlVersions: NotRequired[Sequence[str]]

class VerdictInvalidatedData(TypedDict):  # stream judgement:invalidation@<instrument>@<date>
    instrument: str
    scope: InvalidationScope
    cites: LedgerEventRef                 # one verdict known to be affected
    reason: str

class InvalidationRetractedData(TypedDict):  # stream judgement:invalidation-retraction@…
    cites: str                            # the invalidation stream withdrawn
    reason: str
```

`policyEvent` is a `LedgerEventRef`, so a verdict that judges a policy cites the `policy.accepted` event the same way `decision.made.policy` does. The contract only says "the policy event judged", and this makes it concrete.

`detail` is allowed on any verdict. The contract defines it as free text that projections report and never interpret, so restricting it would add a rule without protecting anything.

### 3. The conditional reason rule, and the checker

The `verdict.recorded` schema expresses "required with `cannot-tell`, forbidden otherwise" directly:

```json
"if":   {"properties": {"verdict": {"const": "cannot-tell"}}, "required": ["verdict"]},
"then": {"required": ["cannotTellReason"]},
"else": {"not": {"required": ["cannotTellReason"]}}
```

The shared checker in `_json_schema.py` supports `if`/`then` but not `else` or `not`. This change adds both:

- **`else`:** checked when `if` doesn't match.
- **`not`:** reports `format.invalid_value` at the current path when the inner schema matches.

A forbidden `cannotTellReason` therefore produces a finding at `data`, not at `data.cannotTellReason`. To keep findings addressed, the projection and the validator also report a dedicated `verdict.reason_not_allowed` at `data.cannotTellReason`, and `verdict.reason_required` replaces the generic missing-property finding. This is the same pattern as `policy.reason_required` in 0.4.0. The schema still carries the rule, so `jsonschema` users get it too, and the pure validator and `jsonschema` must agree on accept or reject.

The interchange version 1 schemas use neither keyword. Their rendered files and the parity corpus are unchanged.

### 4. The verdict projection

```python
class ProjectedVerdict(TypedDict):
    cellId: str
    attempt: int
    preregistration: str
    scorerVersion: str
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    policyEvent: NotRequired[LedgerEventRef]
    manipulationCheck: ManipulationCheck  # from the cited measurement
    source: LedgerEventRef                # the verdict.recorded event
    measurement: LedgerEventRef           # the evidence.recorded event it judges

class CellVerdict(TypedDict):
    cellId: str
    preregistration: str
    status: Literal["current", "invalidated", "conflicting"]
    current: NotRequired[ProjectedVerdict]          # status == "current"
    candidates: NotRequired[Sequence[LedgerEventRef]]  # status == "conflicting"
    invalidatedBy: NotRequired[Sequence[str]]       # invalidation streams that removed a verdict

class VerdictProjection(TypedDict):
    cells: Sequence[CellVerdict]          # sorted by (cellId, preregistration)
    findings: Sequence[ValidationFinding]

def project_verdicts(events: Sequence[RecordedEvent]) -> VerdictProjection
```

The projection takes events in global-log order and ignores types it doesn't own. It works in two passes:

1. **Index.**
   - Measurements are indexed by (streamId, streamVersion).
   - Verdicts are indexed by stream id, and grouped by (`cellId`, `preregistration`). Each stream holds one verdict.
   - Invalidations are indexed by stream id, keeping their condition and the verdicts each event cites.
   - Retractions are indexed by the stream they cite.
   - Unreadable events (an unsupported version, or data that fails validation) are skipped and reported as `ledger.unsupported_event` or `ledger.invalid_event_data`, exactly as `project_decision_rules` does.
2. **Resolve each (cell, pre-registration):**
   - **Supersession.** A verdict whose `supersedes` names a verdict stream in the same group removes that stream. A `supersedes` that names an unknown stream, or one in a different (cell, pre-registration), is reported as `verdict.invalid_supersedes` and ignored, so both verdicts stay candidates.
   - **Invalidation.** An unretracted invalidation removes a candidate when either:
     - the invalidation cites it; or
     - its condition matches the measurement the candidate cites. For each scope list that is present and non-empty, the measurement's value must be in that list: `patchrigCommits` against `patchrigCommit` (and see open question 2), `vindexPins` against `vindexPin`, and `larqlVersions` against `larqlVersion`. Every present list must match.

     The stream ids of the removing invalidations are recorded in `invalidatedBy`.
   - **Result.**
     - No candidates left, and at least one removed by invalidation: `status: invalidated`.
     - Exactly one candidate: `status: current`.
     - More than one: `status: conflicting`, with `candidates` and a `verdict.conflict` finding. The projection does not break the tie.
   - **Unverifiable verdicts.** A verdict citing a measurement that isn't in the log is reported as `verdict.unknown_measurement`. It is not a candidate, because its scope can't be checked.

**Invalidation rules:**
- Every event in one invalidation stream must state the same `instrument`, `scope`, and `reason`. A mismatch is reported as `invalidation.inconsistent_condition`, and the stream's first event's condition is used.
- An invalidation whose scope has no non-empty list matches by citation only, and is reported as `invalidation.empty_scope`. An empty condition must never match every verdict.
- A cited verdict that the condition doesn't match is still removed, and is reported as `invalidation.cited_outside_scope`, so the inconsistency is visible.

**Retraction rules:**
- A retraction makes its invalidation inert, for both condition and citations.
- A retraction citing an unknown stream is reported as `retraction.unknown_invalidation`.
- A retraction cannot be retracted. A second retraction of the same invalidation changes nothing, and isn't a finding.

**What the projection doesn't do:**
- It doesn't consult `manipulationCheck` to decide anything. It copies it onto the projected verdict, because whether a verdict counts with a failed manipulation check is LogicalAssembly's judgement.
- It is total, deterministic, and non-mutating, and reads no clock. Dates (`preregistration`, invalidation dates) are compared only for equality, never ordered.

LogicalAssembly must not act on a (cell, pre-registration) that has a finding addressed to one of its events. The same stance as the rule projection: report rather than guess.

### 5. Stream kinds aren't checked

The projection reads only `type` and `data`. Rastro enforces that `evidence.recorded` sits on `experiment:` streams and verdict events on `judgement:` streams, through its authorization table. Checking stream-id prefixes here would be parsing stream ids, which every party agreed not to do.

### 6. Fields this change proposes to patchrig

An invalidation's scope names `patchrigCommits` and `larqlVersions`, but the agreed `evidence.recorded` carries neither, so the condition can't be evaluated. This change adds `patchrigCommit` (the patchrig commit that ran the cell) and `larqlVersion` (the larql version used) to `evidence.recorded` as required fields. Patchrig is asked in `lasm-core-note-on-invalidation-scope-fields.md` to confirm or rename them before implementation starts. Their final names are a precondition for task 1.2.

### 7. Package

Version `0.5.0`. Exports:
- the new records and literals;
- `CANNOT_TELL_REASONS`, `VERDICT_VALUES`, and `project_verdicts`.

They are added to the `POST_MIGRATION` allowlist and the API inventory. The wheel gains four schema files. LogicalAssembly pins `v0.5.0` when it starts projecting verdicts.

## Risks

- **Patchrig-specific fields in the core.** `patchrigCommit`, `larqlVersion`, and the scope list names are rig vocabulary inside `lasm_core`, like `FIRST_SLICE_BINDINGS`. The next measuring witness will need a version 2 of `evidence.recorded` with a generic pin map. That's acceptable for the first witness, and named here so it isn't mistaken for the final shape.
- **Condition matching could over-invalidate.** A scope of one common larql version would invalidate everything measured with it. That is the contract's intent (a condition applies to every verdict, including later ones), and `invalidatedBy` makes the reach visible.
- **The checker grows.** `else` and `not` are general keywords. The agreement tests with `jsonschema` must cover both, including nested use.
- **Unordered dates.** Two invalidations of the same instrument on the same day collide in Rastro by design. The projection doesn't depend on ordering between invalidations.

## Open Questions

1. **Field names:** are `patchrigCommit` and `larqlVersion` the right names, and does the run directory record both? (Asked of patchrig.)
2. **Which commit:** does `patchrigCommits` in a scope mean the commit that ran the measurement, the scorer commit (`scorerVersion`), or either? This design matches either, which over-invalidates rather than under-invalidates. (Asked of patchrig.)
3. **Attempts:** a re-run of a cell is a new attempt, with a new measurement stream. Is its verdict in the same (cell, pre-registration) group, so it must name the earlier verdict in `supersedes` or it conflicts? This design keys on (`cellId`, `preregistration`) as the contract says, which gives that result. (Asked of patchrig.)
4. **Instrument narrowing:** measurements don't record which instruments or controls they used, so `instrument` is descriptive and doesn't narrow the match. Should measurements list them? This design leaves that for a later version.
