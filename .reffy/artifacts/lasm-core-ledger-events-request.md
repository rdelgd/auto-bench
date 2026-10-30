# Ledger Events in `lasm_core`: A Request for the Governance First Slice

For auto-bench developers and their agents, who maintain `lasm_core`.
LogicalAssembly asks `lasm_core` to become the home of the **world ledger's
semantics**: event types, the aggregates that decide which events are
allowed, and the projections folded from them. Rastro has built the ledger
itself, an event store with no semantics. This note asks for the smallest
`lasm_core` addition that lets LogicalAssembly run the first slice.

Date: 2026-10-30. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-ledger-events-request.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

Background:
- in project `nuveris`:
  - `lasm-world-ledger-event-sourced-mind.md`: the design;
  - `lasm-paseo-assembly-source-of-truth.md`: governance as a ledger
    projection;
  - `lasm-rastro-as-the-world-ledger.md` and
    `lasm-reply-to-rastro-world-ledger.md`: the agreement with rastro;
- in project `rastro`: the ReffySpec change
  `establish-world-ledger-event-store`, which defines the envelope and the
  guarantees.

## Summary
1. **Where the semantics live:**
   - **rastro** keeps events: order, durability, idempotency, and
     attribution. It treats `type`, `schema_version`, and `data` as opaque.
   - **`lasm_core`** decides what the events mean: their schemas, which
     commands may produce them, and how they fold into state.
   - **LogicalAssembly** runs `lasm_core` and does the I/O.
2. **The first slice needs three event types, one aggregate, and one
   projection.** It moves paseo-core's three decision rules and their
   decision history onto the ledger with no behavior change.
3. **Everything stays Sans I/O,** in `lasm_core`'s existing conventions:
   `TypedDict` records keyed by camelCase wire names, versioned JSON Schemas,
   pure functions, and no runtime dependencies.
4. **LogicalAssembly will depend on `lasm-core`.** That's new: today the
   Django app doesn't import it.

## Why `lasm_core`
An event-sourced system keeps its rules in pure functions: given past
events, when a command arrives, then new events or an error. Those rules are
domain meaning, which is exactly what `lasm_core` owns. Rastro deliberately
implements none of it, and LogicalAssembly shouldn't implement it alone,
because the same meaning will be needed by other projectors: the assembly, a
retrieval index, and eventually weight patches. Putting the ledger's
semantics in `lasm_core` keeps one implementation of them.

## What the First Slice Needs

### 1. Event types and schemas
The `data` of each event, as `TypedDict`s with JSON Schemas rendered beside
the existing v1 interchange schemas. Rastro's envelope fields (`event_id`,
`stream_id`, `stream_version`, `global_position`, `metadata`) stay outside
`lasm_core`'s records.

| Event type | Stream | `data` (camelCase, per your conventions) |
| --- | --- | --- |
| `policy.accepted` | `policy:<policyId>` | `policyId`, `binding` (`paseo-core`), `action` (e.g. `application.teardown`), `decision` (`allow` or `deny`), `reason` (required for `deny`), `acceptedBy` |
| `decision.made` | `application:<applicationId>` | `decisionId`, `applicationId`, `action`, `resource`, `requestedBy`, `requestedAt`, `decision`, `reason`, `policy` (the policy event it came from: stream id and version), `projectionPosition` (the ledger position the rules reflected; absent for backfilled decisions), `bypassed` |
| `application.removed` | `application:<applicationId>` | `applicationId`, `removedAt`, `removedBy`, `approval` (`decisionId`, `bypassed`, `required`), `registered` (false for removals of unregistered applications) |

Notes:
- **The first slice keys policies by paseo action.** It does that because
  today's rules are keyed that way, and "no behavior change" is the
  acceptance criterion. The richer model (policies about concepts, with
  paseo actions in bindings) is the next step, and should be a later schema
  version, not a different event type.
- **`policy.proposed`, `policy.contested`, and `policy.superseded`** come in
  that next step. The first slice seeds accepted policies only.
- **Timestamps of when something happened** live in `data` (`requestedAt`,
  `removedAt`), never in ledger order. Backfilled events are appended long
  after they happened.

### 2. One aggregate: accepting a policy
`decide_policy(past_events, command) -> events | rejection`, pure:
- **Command:** `AcceptPolicy`, with the policy content and the accepter.
- **Rejections:**
  - an invalid binding or action;
  - a `deny` without a reason;
  - accepting a policy whose current accepted content is identical (a no-op,
    rejected, so replays don't append duplicates).
- **Output:** a `policy.accepted` event's `data`.

LogicalAssembly then appends the event to rastro at the stream version it
read. A conflict means another writer got there first, so LogicalAssembly
re-reads and decides again.

Recording decisions and removals needs no aggregate in the first slice: they
are facts about something that already happened, appended as such.

### 3. One projection: the decision rules
`project_decision_rules(events) -> rules`, pure: fold `policy.accepted`
events into the current rule per (binding, action). The latest acceptance
for a policy wins, and each rule cites the policy event it came from.
LogicalAssembly writes the result into its `DecisionRule` table, which then
becomes generated output. `/decisions` keeps evaluating that table locally,
exactly as today.

Moving rule *evaluation* (the decision itself) into `lasm_core` is a natural
later step. It isn't needed for "no behavior change".

### 4. Tests, in your style
- Fixture tests for the three event types and their schemas, including
  checks that schemas, decoder, and `jsonschema` agree.
- Aggregate tests: accept, each rejection, and idempotent re-acceptance.
- Projection tests: fold order, latest acceptance wins, and replay from
  empty gives the same rules.
- Sans I/O tests with file, environment, network, process, and clock access
  patched to fail.

## How LogicalAssembly Will Use It
1. **Seed.** For each current `DecisionRule` row, as it is in the database
   today and not the original migration defaults (a superuser may have edited
   them): call `decide_policy` with `AcceptPolicy`, and append the result to
   `policy:paseo-core.<action>`.
2. **Backfill.** Append each `ApplicationDecision` and removal record as
   `decision.made` or `application.removed`, with event ids derived from the
   Django record, in original order.
3. **Project.** Poll rastro from the last global position, fold through
   `project_decision_rules`, and rewrite `DecisionRule`.
4. **Write forward.** Append each new decision, citing the policy event and
   projection position.
5. **Accept,** with rastro: the rebuilt table equals today's, every decision
   has an event, and a replay from position 0 rebuilds the same rules.

LogicalAssembly will pin `lasm-core` by version or commit. How we get it
(a package index, or a git dependency) is your call.

## Questions for You
1. **Module placement:** a new `lasm_core.ledger` module, or alongside the
   existing interchange types?
2. **Schema versioning:** do ledger event schemas join the existing v1
   interchange set, or get their own version line?
3. **Policy entries:** the source-of-truth artifact's open question was
   whether policies need a new entry kind in `lasm_core`. Should the
   first-slice `policy.accepted` already be shaped as a LogicalAssembly
   policy entry, or stay a governance record until the concept-based model
   arrives?
4. **Distribution:** how should LogicalAssembly depend on `lasm-core`?
