# Reply to auto-bench: Ledger Governance Events

For auto-bench developers and their agents. This answers the ReffySpec change
`add-world-ledger-governance-events` (project `auto-bench`, workspace
`nuveris-v1`), which responds to `lasm-core-ledger-events-request.md`.

Date: 2026-10-30. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-reply-to-auto-bench-ledger-events.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

## Summary
1. **We accept the design,** including all four answers: a separate
   `lasm_core.ledger` module, one schema version line per event type, a
   governance record rather than a `PolicyEntry` for v1, and a git dependency
   pinned to `v0.4.0`.
2. **Three field corrections,** found by checking the design against
   LogicalAssembly's models. One of them is our mistake in the request.
3. **Two additions:** a required `basis` on `decision.made`, which keeps why
   each decision was made, and an optional `traceId`.
4. **Answers to your three open questions:** keep `policy` optional, keep
   `FIRST_SLICE_BINDINGS` a constant, and no `globalPosition` on
   `RecordedEvent`.

## What We Especially Like
- `decide_policy` reports every rejection, and refuses to decide over history
  it can't read.
- Enforcing `policyId == <binding>.<action>`, so two policies can't race for
  one action, and "latest acceptance" equals "the rule for this action".
- `project_decision_rules` folds the whole global feed, and LogicalAssembly
  must not rewrite `DecisionRule` while findings are non-empty. A malformed
  event can't silently drop a governance rule.
- Keeping `binding` and `action` separate in v1, so v2's move to `appliesTo`
  stays mechanical.

## Field Corrections
These come from LogicalAssembly's `apps/control_plane/models.py`, which is
the history the backfill reads.

### 1. `decision.made.resource` is an object, not a string
`ApplicationDecision.resource` is a JSON object, the `resource` paseo-core
sends with the decision request. Please type it as an object (`JsonValue`,
or a mapping) rather than `str`. Our request didn't give its type, so this
one is on us.

### 2. Drop `decision.made.bypassed`
This was our mistake in the request. Decisions have no bypass concept in
LogicalAssembly. A break-glass bypass belongs to a *removal*: the operator
removes an application without asking, and the removal reports
`approval.bypassed`. `application.removed` already carries that. On
`decision.made`, the field would always be false.

### 3. Removal provenance must be optional
Removal provenance (`removed_by` and `approval`) was added in Phase 4, and
paseo-core's removal fields are parsed leniently. So a removal record can
have an empty `removed_by` and an empty `approval` (`{}`). As drafted,
`ApplicationRemovedData` requires `removedBy` and `approval`, with `bypassed`
and `required` inside it. The backfill would then have to invent values,
which defeats the purpose of a ledger. Please make `removedBy` and `approval`
optional (`NotRequired`), and `bypassed` and `required` optional within
`approval`. "Omitted" then honestly means "not reported".

## Additions

### `basis` on `decision.made` (required)
LogicalAssembly records why each decision was made, in
`ApplicationDecision.rule`. There are four kinds:

| `rule` today | Meaning |
| --- | --- |
| `rule:<action>` | answered by the decision rule for that action |
| `unknown-action` | fail-closed: paseo-core asked about an action we don't know |
| `unknown-application` | fail-closed: the application isn't registered |
| `no-rule` | fail-closed: the action is known, but its rule was deleted |

Without this field, a backfilled fail-closed denial looks the same as a
rule's denial, and the ledger loses the explanation the Django record keeps.
We propose:

```python
DecisionBasis = Literal["rule", "unknown-action", "unknown-application", "no-rule"]

class DecisionMadeData(TypedDict):
    ...
    basis: DecisionBasis
```

With `basis`, LogicalAssembly can check "every write-forward decision with
basis `rule` cites a policy event" on its side.

### `traceId` on `decision.made` (optional)
`ApplicationDecision.trace_id` holds paseo-core's trace id when it's sent.
paseo-core has since told us that its episode ids will be built from the
`trace_id` (`lasm_rastro_evidence_reply.md`, project `paseo-core`). Keeping
it on the decision lets a later projection link a decision to the
invocation's evidence. It's optional, since older decisions may not have it.

## Answers to Your Open Questions

### 1. Require `policy` whenever `decision` is `allow`?
**No, keep it optional.** Only rules ever allow, but a backfilled allow was
decided by the rule *as it was then*, and a superuser may have edited it
since. Citing the seeded policy event would credit the decision to content
that didn't make it. With `basis` added, LogicalAssembly checks the
write-forward invariant itself.

### 2. `FIRST_SLICE_BINDINGS` as a parameter?
**Keep it a constant.** LogicalAssembly's `DecisionAction` choices hard-code
the same three actions, so a new paseo action already needs a code change on
our side. One source of valid actions in `lasm_core` is better than two that
can disagree. Binding records in the concept-based change are the real fix.

### 3. `globalPosition` on `RecordedEvent`?
**Not needed.** LogicalAssembly tracks the position its projection reflects,
and writes it into `decision.made.projectionPosition`. Leave it out, as you
proposed.

## On Our Side
- **Build access for the git dependency.** `lasm-core @ git+ssh://…@v0.4.0`
  means LogicalAssembly's image builds (local and deployed) need read access
  to `rdelgd/auto-bench`, through a deploy key or token passed in at build
  time and never baked into the image. That goes into our ReffySpec change.
- **The Django side of the slice** becomes a ReffySpec change in this project
  once you tag `v0.4.0`: the seed, the backfill (validated with
  `validate_ledger_event_data` before appending), projection catch-up,
  write-forward decisions, and the joint acceptance test with rastro.
