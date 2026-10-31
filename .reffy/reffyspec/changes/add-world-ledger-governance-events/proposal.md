# Change: Add World-Ledger Governance Events to lasm_core

## Why

LogicalAssembly is moving paseo-core's governance onto a world ledger. Rastro has built the ledger as an event store that keeps order, durability, idempotency, and attribution, and deliberately treats an event's `type`, `schema_version`, and `data` as opaque. Someone has to own what those events mean: their schemas, which commands may produce them, and how they fold into state. That is domain meaning, which is what `lasm_core` owns. If LogicalAssembly implemented it alone, every later projector (the assembly, a retrieval index, weight patches) would need its own copy.

The LogicalAssembly developers asked for the smallest addition that runs their first slice: paseo-core's three decision rules and their decision history moved onto the ledger with no behavior change. This change delivers that slice: three event types, one aggregate, and one projection, all Sans I/O.

## What Changes

- Add a `lasm_core.ledger` module that holds ledger semantics. It is separate from the interchange module because ledger events are not interchange documents.
- Add three event types, each with a `TypedDict` for its `data` keyed by camelCase wire names:
  - `policy.accepted`, on stream `policy:<policyId>`;
  - `decision.made`, on stream `application:<applicationId>`;
  - `application.removed`, on stream `application:<applicationId>`.
- Add a `RecordedEvent` input view: the stream id, stream version, type, schema version, and data of an event read back from the ledger. Rastro's other envelope fields stay with the adapter.
- Add the `decide_policy(past_events, command)` aggregate. It takes an `AcceptPolicy` command and returns either one `policy.accepted` event to append, or rejection findings: invalid binding, invalid action, a policy id that doesn't match the binding and action, a `deny` without a reason, or content identical to the currently accepted content.
- Add the `project_decision_rules(events)` projection. It folds `policy.accepted` events into one rule per (binding, action), keeps the latest acceptance, and cites the policy event each rule came from. Other event types are ignored.
- Add `validate_ledger_event_data(type, schema_version, data)`, a pure structural check against the event schemas, using the same JSON Schema interpreter as the interchange decoder.
- Render per-event JSON Schemas into `src/lasm_core/schemas/ledger/`, on a version line separate from interchange version 1. Each event type is versioned on its own, matching rastro's per-event `schema_version`.
- Bump the package to `0.4.0`. LogicalAssembly depends on it as a git dependency pinned to a release tag.

## Impact

- Affected capability: `world-ledger-governance-events` (new). `establish-auto-bench-sans-io-core` is unchanged. The new module follows its Sans I/O, typing, and packaging requirements.
- Affected implementation: `src/lasm_core/ledger.py` (new), `src/lasm_core/_schema_ledger.py` (new), `src/lasm_core/interchange.py` (internal reuse of the schema checker only), `__init__.py`, `scripts/write_schemas.py`, rendered schemas under `src/lasm_core/schemas/ledger/`, `tests/`, `docs/api-inventory.md`, `README.md`, `.reffy/reffyspec/project.md`, `pyproject.toml`.
- Compatibility: additive. Interchange version 1 documents, the recorded corpus, fixtures, and evaluations are unchanged. No parity deviation is needed.
- Consumers: LogicalAssembly gains a dependency on `lasm-core`. This is the first time the Django app imports it.
- Out of scope:
  - `policy.proposed`, `policy.contested`, and `policy.superseded`;
  - concept-based policies and bindings, which arrive later as `policy.accepted` schema version 2;
  - moving rule evaluation (the `/decisions` answer) into `lasm_core`;
  - aggregates for decisions or removals;
  - any rastro client, polling, event-id derivation, or `DecisionRule` table handling, which remain LogicalAssembly adapter concerns;
  - a new `LogicalAssemblySlice` entry kind for policies.

## Supersedes

None

## Reffy References

- `lasm-core-ledger-events-request.md` - the LogicalAssembly request: the three event types and their fields, the aggregate and its rejections, the projection, the test expectations, the seed/backfill/project/write-forward plan, and the four questions answered in `design.md`
- `lasm-reply-to-auto-bench-ledger-events.md` - LogicalAssembly's acceptance of the design: `resource` corrected to an object, `bypassed` dropped from `decision.made`, removal provenance made optional, `basis` and `traceId` added, and answers to the design's three open questions
- `lasm-reply-on-trace-ids-and-verdict-projection.md` - LogicalAssembly's correction: `decision.made.traceId` is paseo-core's per-request correlation id, not a link to an episode; no schema change
