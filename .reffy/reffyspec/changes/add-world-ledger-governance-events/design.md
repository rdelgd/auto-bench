## Context

The world ledger splits responsibility three ways:

- **Rastro** keeps events: order, durability, idempotency, and attribution. Its envelope carries `event_id`, `stream_id`, `stream_version`, `global_position`, `type`, `schema_version`, `data`, and `metadata`. It treats `type`, `schema_version`, and `data` as opaque.
- **`lasm_core`** decides what the events mean.
- **LogicalAssembly** runs `lasm_core`, talks to rastro, and owns the `DecisionRule` table that `/decisions` evaluates.

paseo-core governs three actions today: `application.teardown`, `agent.retire`, and `workspace.delete`. Each has one `DecisionRule` row (`allow`, or `deny` with a reason) that a superuser edits in place. The first slice replaces "edited in place" with "accepted as an event and projected". `/decisions` doesn't change.

`lasm_core` is a Sans I/O Python library. Records are `TypedDict`s with camelCase wire keys, optional fields are omitted rather than `None`, functions are pure, and the package has no runtime dependencies. Interchange version 1 schemas are rendered from `_schema_v1.py`, and one pure interpreter in `interchange.py` checks documents against them.

## Goals / Non-Goals

Goals:

- Give LogicalAssembly everything it needs to seed, backfill, project, and write forward the decision rules with no behavior change.
- Keep one implementation of the ledger's governance semantics, in `lasm_core`.
- Make the event schemas checkable three ways that agree: the checked-in files, the pure validator, and `jsonschema`.
- Leave room for concept-based policies as a later schema version of the same event type.

Non-goals:

- `policy.proposed`, `policy.contested`, `policy.superseded`, and policy status.
- Rule evaluation, a rastro client, envelope handling beyond the `RecordedEvent` view, event-id derivation, or clocks.
- Changes to interchange version 1, the evaluator, fixtures, or the parity corpus.

## Decisions

### 1. Module placement: a new `lasm_core.ledger` module (request question 1)

Ledger events are not interchange documents. They have no `schemaVersion`/`kind`/`value` envelope, because rastro owns the envelope, and they are versioned per event type rather than as a set. Putting them beside `ConformanceCase` and the other interchange records would blur that. A separate module also keeps the evaluation-side public API unchanged.

Module: `src/lasm_core/ledger.py`. Its schema definitions are in `src/lasm_core/_schema_ledger.py`, parallel to `_schema_v1.py`. The public names are also re-exported from `lasm_core`, as with every other module.

### 2. Schema versioning: a separate version line, one per event type (request question 2)

Rastro stores `schema_version` on each event, so each event type has its own version history. `policy.accepted` will reach version 2 when concept-based policies arrive. `decision.made` has no reason to change at the same time. Tying them to interchange version 1 would force unrelated bumps on both sides.

Rendered files go in `src/lasm_core/schemas/ledger/`, one per (type, version):

```
schemas/ledger/policy.accepted.v1.schema.json
schemas/ledger/decision.made.v1.schema.json
schemas/ledger/application.removed.v1.schema.json
```

Each has `$id` `urn:lasm-core:ledger:<type>:v<n>` and describes the `data` object only. `scripts/write_schemas.py` renders both directories and its `--check` mode covers both. `LEDGER_EVENT_SCHEMA_VERSIONS: Mapping[LedgerEventType, tuple[int, ...]]` names the versions this release understands: `(1,)` for each type.

The structural checker in `interchange.py` (`_check` and its helpers) is reused for ledger data rather than copied. It moves to a private shared module if that keeps the import graph clean. Its behavior doesn't change, and interchange tests keep it honest.

### 3. Policy entries: a governance record, not a `PolicyEntry` (request question 3)

The first slice's `policy.accepted` is keyed by a paseo action because today's rules are. A `PolicyEntry` in a `LogicalAssemblySlice` is a statement about concepts, with provenance. Shaping action-keyed rules as assembly entries now would mean either inventing concepts nobody accepted or changing `PolicyEntry` twice. So version 1 stays a governance record, and the open question of whether policies need a new entry kind moves to the concept-based change. That change will define `policy.accepted` version 2 and a projection from it into assembly entries.

Version 1 deliberately keeps `binding` and `action` as separate fields. Version 2 can then keep `binding` and replace `action` with `appliesTo`, so the mapping from version 1 to version 2 stays mechanical.

### 4. Distribution: a git dependency pinned to a release tag (request question 4)

`lasm-core` is `UNLICENSED` and classified `Private :: Do Not Upload`, and the repository has no package index. LogicalAssembly pins it as:

```
lasm-core @ git+ssh://git@github.com/rdelgd/auto-bench.git@v0.4.0
```

This change tags `v0.4.0` once it is verified. A private index can replace this later without any change to the package.

### 5. Records

```python
LedgerEventType = Literal["policy.accepted", "decision.made", "application.removed"]
PolicyDecision  = Literal["allow", "deny"]

class LedgerEventRef(TypedDict):          # cites a recorded event
    streamId: str
    streamVersion: int

class PolicyAcceptedData(TypedDict):
    policyId: str
    binding: str                          # "paseo-core" in version 1
    action: str                           # a paseo-core action
    decision: PolicyDecision
    reason: NotRequired[str]              # required when decision is "deny"
    acceptedBy: str

DecisionBasis = Literal["rule", "unknown-action", "unknown-application", "no-rule"]

class DecisionMadeData(TypedDict):
    decisionId: str
    applicationId: str
    action: str
    resource: Mapping[str, JsonValue]     # the resource object paseo-core sent
    requestedBy: str
    requestedAt: str                      # when it happened, not ledger order
    decision: PolicyDecision
    basis: DecisionBasis                  # a rule, or which fail-closed path answered
    reason: NotRequired[str]
    policy: NotRequired[LedgerEventRef]   # absent when no accepted policy answered
    projectionPosition: NotRequired[int]  # absent for backfilled decisions
    traceId: NotRequired[str]             # paseo-core's trace id, when it sent one

class RemovalApproval(TypedDict):
    decisionId: NotRequired[str]
    bypassed: NotRequired[bool]
    required: NotRequired[bool]

class ApplicationRemovedData(TypedDict):
    applicationId: str
    removedAt: str
    removedBy: NotRequired[str]           # absent when the removal didn't report it
    approval: NotRequired[RemovalApproval]
    registered: bool

class NewEvent(TypedDict):                # what an aggregate asks the adapter to append
    type: LedgerEventType
    schemaVersion: int
    data: PolicyAcceptedData              # widened to a union as aggregates are added

class RecordedEvent(TypedDict):           # what the adapter reads back from the ledger
    streamId: str
    streamVersion: int
    type: str                             # str, not LedgerEventType: the ledger holds other types
    schemaVersion: int
    data: JsonValue
```

The ledger records history as it was reported, so these fields are optional. The backfill would otherwise have to invent values:
- `decision.made.policy` and `reason`. Backfilled history includes fail-closed denials, which have no policy event to cite. A backfilled allow was decided by the rule as it was then, which a superuser may have edited since, so citing the seeded policy event would credit the decision to the wrong content.
- `application.removed.removedBy` and `approval`, plus every field inside `approval`. Removal provenance arrived in paseo-core's Phase 4, and its removal fields are parsed leniently, so older records can have an empty remover and an empty approval. Omitted means "not reported".
- `decision.made.traceId`. Older decisions may not have one.

`decision.made.basis` is required. It keeps the explanation LogicalAssembly's `ApplicationDecision.rule` holds today:

| `basis` | LogicalAssembly `rule` | Meaning |
| --- | --- | --- |
| `rule` | `rule:<action>` | Answered by the decision rule for the action. |
| `unknown-action` | `unknown-action` | Fail-closed: paseo-core asked about an unknown action. |
| `unknown-application` | `unknown-application` | Fail-closed: the application isn't registered. |
| `no-rule` | `no-rule` | Fail-closed: the action is known, but it has no rule. |

Without it, a backfilled fail-closed denial would look the same as a rule's denial. With it, LogicalAssembly can check on its side that every write-forward decision with basis `rule` cites a policy event. The schema doesn't enforce that, for the backfill reason above.

`decision.made.resource` is the JSON object paseo-core sends with the decision request. Its schema is an object with arbitrary JSON-compatible keys, like evidence payloads. `decision.made` has no `bypassed` field. A break-glass bypass belongs to a removal and is recorded as `application.removed.approval.bypassed`.

`requestedAt` and `removedAt` are strings and are not parsed or compared. The core never consults a clock.

`RecordedEvent` is the only envelope view `lasm_core` takes. The adapter maps rastro's snake_case envelope into it. `event_id`, `global_position`, and `metadata` stay with the adapter.

Stream-id helpers keep the naming in one place: `policy_stream_id(policy_id)` returns `policy:<policyId>`, and `application_stream_id(application_id)` returns `application:<applicationId>`.

### 6. The aggregate: `decide_policy`

```python
class AcceptPolicy(TypedDict):
    policyId: str
    binding: str
    action: str
    decision: PolicyDecision
    reason: NotRequired[str]
    acceptedBy: str

class PolicyCommandResult(TypedDict):
    accepted: bool
    events: Sequence[NewEvent]            # one event when accepted, none otherwise
    findings: Sequence[ValidationFinding] # rejection reasons, empty when accepted

def decide_policy(past_events: Sequence[RecordedEvent], command: AcceptPolicy) -> PolicyCommandResult
```

`past_events` are the events of the command's policy stream, in stream order. Rejections are ordinary `ValidationFinding`s with `error` severity and `command.`-prefixed paths. Validation does not stop at the first rejection, matching the library's validators:

| Code | When |
| --- | --- |
| `policy.invalid_binding` | `binding` isn't a known binding (`paseo-core` in version 1). |
| `policy.invalid_action` | `action` isn't one of the binding's actions: `application.teardown`, `agent.retire`, or `workspace.delete`. |
| `policy.id_mismatch` | `policyId` isn't `<binding>.<action>`. |
| `fixture.required` | `acceptedBy` is blank. |
| `policy.reason_required` | `decision` is `deny` and `reason` is absent or blank. |
| `policy.unchanged` | The stream's latest accepted `binding`, `action`, `decision`, and `reason` equal the command's. `acceptedBy` is not compared, so a replay by a different person is still a no-op. |
| `policy.unsupported_event` | A past event on the stream has a type or schema version this release doesn't understand, or data that fails its schema. The aggregate refuses to decide over history it can't read. |

Before these checks, the command is checked structurally against the `policy.accepted` version 1 schema, because it has the same fields. A malformed command (an unknown decision, an unknown property, a wrong type) returns only `format.*` findings with `command.` paths, since the business checks can't be applied to it.

The known bindings are a module constant, `FIRST_SLICE_BINDINGS = {"paseo-core": ("application.teardown", "agent.retire", "workspace.delete")}`. They are the one place paseo-core's vocabulary enters `lasm_core`, and the concept-based change replaces them with binding records.

Enforcing `policyId == f"{binding}.{action}"` makes "the latest acceptance for a policy" and "the rule for a (binding, action)" the same thing in version 1. That's what "no behavior change" needs. It also prevents two policies from racing for one action.

The aggregate doesn't see stream versions or handle concurrency. LogicalAssembly appends at the version it read, and on a conflict it re-reads and calls `decide_policy` again.

### 7. The projection: `project_decision_rules`

```python
class DecisionRuleRecord(TypedDict):
    binding: str
    action: str
    decision: PolicyDecision
    reason: NotRequired[str]
    policyId: str
    policy: LedgerEventRef                # the policy.accepted event the rule came from

class DecisionRuleProjection(TypedDict):
    rules: Sequence[DecisionRuleRecord]   # sorted by (binding, action)
    findings: Sequence[ValidationFinding]

def project_decision_rules(events: Sequence[RecordedEvent]) -> DecisionRuleProjection
```

- Events are folded in the order given, which is ledger order. For each (binding, action), the latest `policy.accepted` wins.
- Events of other types are skipped silently, so LogicalAssembly can fold the whole global feed.
- A `policy.accepted` event with an unsupported schema version, or with data that fails `validate_ledger_event_data`, is skipped and reported as `ledger.unsupported_event` (path `events[<index>].schemaVersion`) or `ledger.invalid_event_data` (path `events[<index>].data`, with the format findings in the message). LogicalAssembly must not rewrite `DecisionRule` while the findings are non-empty. Rewriting would silently drop or keep a governance rule.
- The function is total and deterministic. Replaying from an empty list gives no rules, and replaying the same events gives byte-identical serialized output.

Missing rules stay the adapter's concern. `/decisions` already denies an action with no rule, and the projection doesn't fill in defaults.

### 8. Validation of event data

`validate_ledger_event_data(type, schema_version, data) -> ValidationResult` reports structural findings from the shared checker (`format.*` codes, `data.`-prefixed paths), plus `ledger.unsupported_event` for an unknown type or version. Like the interchange decoder, it checks shape only. Business rules such as "deny requires a reason" belong to `decide_policy`, so the `policy.accepted` schema lists `reason` as optional.

LogicalAssembly calls it before appending backfilled `decision.made` and `application.removed` data, which no aggregate checks in this slice.

### 9. Tests

- `tests/test_ledger_schemas.py`: the checked-in ledger schemas equal the rendered definitions. For a corpus of valid and invalid data per type, the pure validator and `jsonschema` agree, and an unknown property, a missing required field, a wrong scalar type, and an unknown type or version are rejected.
- `tests/test_ledger.py`:
  - **Aggregate:** accept onto an empty stream; each rejection code; re-acceptance with identical content is `policy.unchanged`; re-acceptance with a changed reason or decision is accepted; an unsupported past event is refused; the inputs are not mutated.
  - **Projection:** fold order; the latest acceptance wins; rules cite the right stream and version; foreign event types are ignored; invalid events produce findings; replay from empty is equal to replay from a prefix extended with the suffix; output is sorted and repeatable.
  - **End to end:** seed the three current rules through `decide_policy`, record them as `RecordedEvent`s, project them, and get exactly three rules equal to the seed rows.
- `tests/test_sans_io.py` runs the aggregate, projection, and validator with file, environment, network, process, and clock access patched to fail.
- `test_corpus_covers_every_public_behavioral_export` adds the new callables to its `POST_MIGRATION` allowlist. The corpus is not touched.

## Risks

- **Paseo vocabulary in the core.** `FIRST_SLICE_BINDINGS` names paseo-core actions inside `lasm_core`. That's accepted for the first slice, kept in one constant, and slated for replacement by binding records. A new paseo action needs a `lasm-core` release until then.
- **Optional `policy` on `decision.made`.** A write-forward decision with basis `rule` should always cite a policy. The schema can't enforce that because backfill needs the field to be optional. LogicalAssembly checks it, along with "every decision has an event", on its side.
- **Git dependency access.** LogicalAssembly's image builds need read access to `rdelgd/auto-bench`, supplied at build time and never baked into an image. LogicalAssembly owns that in its own change.
- **Shared checker refactor.** Moving `_check` out of `interchange.py` could disturb interchange behavior. The interchange and parity suites must pass unchanged before ledger code uses the checker.
- **Schema evolution.** When `policy.accepted` version 2 arrives, `project_decision_rules` and `decide_policy` will have to read both versions. That's why both already refuse versions they don't know rather than guessing.

## Resolved Questions

LogicalAssembly accepted the design in `lasm-reply-to-auto-bench-ledger-events.md` and corrected three fields: `resource` is an object, `decision.made` has no `bypassed` field, and removal provenance is optional. They also added `basis` and `traceId`. They answered this design's open questions:

1. **Require `policy` whenever `decision` is `allow`?** No. A backfilled allow was decided by the rule as it was then, so `policy` stays optional, and `basis` lets LogicalAssembly check the write-forward invariant.
2. **Make `FIRST_SLICE_BINDINGS` a parameter?** No. LogicalAssembly's `DecisionAction` choices hard-code the same three actions, so a new action already needs code on both sides. One source of valid actions is better than two that can disagree.
3. **Add `globalPosition` to `RecordedEvent`?** No. LogicalAssembly tracks the position itself and writes it into `projectionPosition`.

## Open Questions

None.
