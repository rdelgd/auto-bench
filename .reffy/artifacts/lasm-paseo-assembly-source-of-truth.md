# The Assembly as a Projection: Governing paseo-core From the World Ledger

Status: exploratory
Date: 2026-10-19 (updated 2026-10-22: the `/evidence` intake; revised 2026-10-30: the world ledger)
Authors: Roberto Delgado, Claude

> **Revision, 2026-10-30.** This note first argued that *the assembly* is the
> source of truth, with the decision rules compiled from it. Since then:
> - `lasm-world-ledger-event-sourced-mind.md` moved the truth one level down,
>   to an append-only **world ledger**. The assembly is a projection of that
>   ledger, like everything else.
> - Rastro agreed to become the world ledger
>   (`lasm-rastro-as-the-world-ledger.md` and
>   `lasm-reply-to-rastro-world-ledger.md` in this project;
>   `rastro-reply-to-world-ledger-request.md` and the ReffySpec change
>   `establish-world-ledger-event-store` in project `rastro`). Its side of
>   the first slice is built and passes its conformance suite on Postgres.
> - `lasm_core` (Python, sans-I/O; project `auto-bench`) is the home of the
>   ledger's semantics, run by LogicalAssembly.
>
> What changed below: the claim; versioning (ledger positions instead of
> document versions); the loop (commands and projections instead of
> authoring and compiling); evidence (appended to the ledger instead of
> posted to `/evidence`); credentials; the open questions; and the next
> step. Most mechanics survive unchanged. The filename stays the same,
> because other artifacts cite it.

## Prompt
Phases 3 and 4 of the control-plane plan gave LogicalAssembly a working loop
over paseo-core:

- an application registry;
- read-only drill-downs per application type;
- a synchronous `/decisions` endpoint that paseo-core must obey before
  destructive operations;
- a record of every decision, removal, and break-glass bypass.

Looking at the running app, those pieces have the shape of a small Lasm:
hard-coded, and spread across tables. The first version of this note read
them as one projection of an assembly. The world ledger reads them more
precisely: the rules, the decisions, and the removals are all **events**,
and the assembly and the rule table are two **projections** of them.

## The Claim
> What may happen to a paseo-core application is decided by accepted
> policies, and every acceptance, decision, removal, and piece of evidence is
> an event in the world ledger. The assembly (the current set of accepted
> policies, concepts, and bindings) and the rule table that answers
> `/decisions` are both projections of that ledger. paseo-core enforces;
> `lasm_core` decides which events are allowed; rastro keeps them;
> LogicalAssembly projects them, serves decisions, and witnesses.

This is still the claim of `lasm-as-the-collective-mind-control-plane.md`
(project `auto-bench`, workspace `lasm-v1`), "a control plane decides; a data
plane carries", applied to a fleet we already govern live. paseo-core is the
data plane. Today the rules live in a `DecisionRule` table edited in place.
Tomorrow they're folded from policy events in the ledger, and the table is
generated.

## What Already Exists, Read Against the Ledger

| Ledger concept | What exists today for paseo-core | Where it falls short |
| --- | --- | --- |
| **Concepts** | Application, workspace, agent: the resource kinds in the decision contract | Implicit. They're strings in a JSON contract, not entries anyone owns. |
| **Policy events** | `DecisionRule`: one row per action (`allow`, or `deny` with a reason) | A mutable row, not an event. No owner, status, or history: editing in place loses what the rule used to say. |
| **Bindings** | The application registry, plus extensions keyed by `(actor_type, version)` | Bindings live in code (`EXTENSIONS`); nothing says which concept an actor type realizes. |
| **Commands at the edge** | `/decisions`: synchronous, fails closed, and the operator's break-glass bypass is surfaced | Works, and is the strongest piece. paseo-core already enforces whatever we answer. |
| **Decision and evidence events** | The decision log, removal provenance, break-glass flags, read-check status, removals of unregistered applications | Records in Django tables, not ledger events. They cite a rule *row*, not the policy event and ledger position that answered. And there's no intake for evidence about *behavior*, such as whether a patched model or an agent's skill preserved a policy. |
| **Accountable acceptance** | Only superusers can edit a rule | No accepter, no candidate-vs-accepted status, and no way to contest a rule. |

The loop runs end to end; verified live on 2026-10-18 (allow, deny,
break-glass, and unavailable). What's missing is the history: every one of
these records should be an event that can be replayed, attributed, and
contested.

## The Ledger and Its Projections
Each policy is its own stream in rastro. Its history is a sequence of events,
for example:

```text
policy:teardown-needs-a-human
  1  policy.proposed   { statement, applies_to, decision: deny, reason, proposed_by }
  2  policy.accepted   { statement, applies_to, decision: deny, reason, accepted_by }
  3  policy.contested  { evidence_refs, contested_by }
  4  policy.superseded { by: policy:teardown-by-owner-after-notice }
```

`policy.accepted` carries the accepted content inline, as agreed with rastro,
so each acceptance is self-contained and replayable without another system.
Content drafted elsewhere (in reffy, for example) is recorded as provenance in
the event's metadata: where the draft lived, and its hash. The inline content
is what counts.

Decisions and removals append to the stream of the application they concern,
so an application's governance history reads as one stream:

```text
application:<id>
  decision.made         { operation, decision, policy_event, ledger_position, bypassed }
  application.removed   { removed_by, approval: { decision_id, bypassed } }
```

Rastro enforces `kind:id` against a registered set (`policy`, `application`,
`episode`, `evaluation`). Putting decisions and removals in
`application:<id>`, and a new `experiment` kind for in-vitro-patching, are our
proposals in `lasm-reply-to-rastro-world-ledger.md`.

### The assembly is a projection
Folding the accepted policy events at a ledger position gives the
assembly: the current concepts, policies, and bindings. Rendered as a
document, it looks like the sketch this note first proposed. Read it now as
an **export at a ledger position**, not as the thing that's edited:

```yaml
assembly: paseo-core-governance
as_of_ledger_position: 18342          # was "version: 3"
owner: roberto@lassembly.com

concepts:
  application:  { description: "A deployed paseo-core application and everything its root holds." }
  workspace:    { part_of: application }
  agent:        { part_of: workspace }

policies:
  - id: workspace-delete-by-owner
    status: accepted                    # from policy.accepted at stream version 2
    statement: "An application's owner may delete its workspaces."
    applies_to: { operation: delete, concept: workspace }
    decision: allow

  - id: teardown-needs-a-human
    status: accepted
    statement: "Tearing down an application requires a person; owners must ask."
    applies_to: { operation: delete, concept: application }
    decision: deny
    reason: "Contact roberto@lassembly.com to tear down an application."

  - id: reffy-workspaces-are-records    # a per-type rule, not expressible today
    status: candidate                   # proposed, never accepted: not projected into rules
    statement: "Reffy workspaces hold an organization's records; deleting one needs a person."
    applies_to: { operation: delete, concept: workspace, binding: reffy }
    decision: deny

bindings:
  paseo-core:
    operations:
      application.teardown: { operation: delete, concept: application }
      agent.retire:         { operation: delete, concept: agent }
      workspace.delete:     { operation: delete, concept: workspace }
    actor_types:
      reffyWorkspaceManager/v1: { binding: reffy,       realizes: application }
      microAgentManager/v1:     { binding: micro-agent, realizes: application }
```

Three things from the first version still hold:
1. **Rules are statements about concepts, not about paseo actions.**
   paseo-core's action names live in the binding. A new paseo action is a
   binding change, and the policies don't move.
2. **Specificity comes for free.** "Workspace delete: allow", plus "but not
   for Reffy workspaces", is two policies with the most specific winning.
   That's the per-type rule we can't express today.
3. **Only accepted statements are load-bearing.** A proposed policy is
   visible and contestable, but its events never reach the rule projection.

## The Loop: Command, Append, Project, Enforce, Witness, Contest
`/decisions` must answer within 5 seconds with no outbound calls. So the rule
set is a precomputed projection, and **nothing on the decision path calls
rastro.** A rastro outage delays new events reaching the projection; it
never blocks a decision.

1. **Command.** Someone proposes, accepts, contests, or supersedes a policy
   in LogicalAssembly. `lasm_core` validates the command against the policy
   stream's past events: is there something to accept, and does the accepter
   have the right to accept it? It returns new events, or an error.
2. **Append.** LogicalAssembly appends those events to rastro
   (`POST /v1/streams/{stream_id}/events`), at the stream version it
   validated against. If another writer got there first,
   rastro returns a conflict, and LogicalAssembly re-reads and re-decides.
3. **Project.** LogicalAssembly reads the ledger from its last position
   (`GET /v1/events?from_position=`) and
   folds the policy events (through `lasm_core`) into two projections: the
   assembly, and paseo-core's `DecisionRule` table, which becomes
   read-only, generated output.
4. **Enforce.** `/decisions` evaluates the projected rules exactly as it
   does now, and paseo-core obeys. Each answer is appended as
   `decision.made`, citing the policy event it came from and the ledger
   position the projection reflected.
5. **Witness.** Evidence arrives as ledger events from two directions:
   - **Before a runtime acts:** decisions, removals, and break-glass bypasses,
     recorded by LogicalAssembly.
   - **After a check runs:** measurements from witnesses (probes of a
     patched model, a skill exercised in a sandbox, a metric view checked on
     a data platform), and later verdicts that judge them. Witnesses append
     both to rastro directly, under their own principal, each to a new
     stream. See "Evidence: measurements and verdicts" below.
6. **Contest.** Evidence that a rule is wrong becomes a `policy.contested`
   event, and a proposal to supersede it. Automations can open a review from
   the events themselves. For example, "N break-glass teardowns within a
   week" opens a contest, with no separate orchestrator. Event sourcing calls
   this pattern a processor TODO list.

A command that fails validation appends nothing, so the last good projection
keeps answering. The fail-closed fallbacks stay underneath: unknown actions,
unknown applications, and missing rules are all denied.

### Evidence: measurements and verdicts
*Revised 2026-10-30, after in-vitro-patching's
`in-vitro-patching-reply-to-lasm-patchrig-results-to-rastro.md`.*

The first version proposed a Django endpoint, `POST /control-plane/evidence`.
With the ledger, witnesses append evidence to rastro instead, and
LogicalAssembly projects it. Evidence comes in two kinds, which never share
a stream:
- **Measurements** are observations. They're written once, when a verified
  run finishes, and never revised.
- **Verdicts** are judgements of a measurement against pre-registered
  thresholds, by a given version of the scoring code. They *are* revised:
  a threshold that didn't exist yet is pre-registered, the scoring code is
  fixed, or an instrument turns out to be flawed. The measurement stands;
  its meaning changes.

Every revision is a new stream, so every stream is written exactly once,
with `expected_version: 0` and deterministic event ids. No witness ever has
to track a stream's version, and the full history of how something was
judged stays readable.

| Event | Stream | Written |
| --- | --- | --- |
| `evidence.recorded`: a measurement | `experiment:<cell-id>` (the attempt is part of the cell id) or `evaluation:<run-id>` | once, after the run passes verification; never revised |
| `verdict.recorded`: a judgement | `judgement:<cell-id>@<prereg-date>@<scorer-version>` | once per pre-registration and scorer version; a re-score is a new stream that names what it supersedes |
| `verdict.invalidated` | `judgement:invalidation@<instrument>@<date>` | once per invalidation, stating the flaw as a condition (instrument and scope), with one event per verdict known to be affected |
| `invalidation.retracted` | `judgement:invalidation-retraction@<invalidation stream id>@<date>` | once per retraction, citing the invalidation stream it withdraws |

Event `data` uses camelCase, `lasm_core`'s convention, which its 0.4.0 governance events already
follow. Rastro's envelope (`stream_id`, `expected_version`, `schema_version`) is rastro's and stays
snake_case. *(Corrected 2026-10-31: the examples below first used snake_case inside `data`.)*

**Projections read citations, never stream names.** Stream ids embed other ids, including
`:` and `@`, so nothing parses them. They exist for people, and for write-once collision guards.
What an event refers to is always in its data: `cites` as an object (`streamId`, `streamVersion`)
names one event, and `cites` as a string names a whole stream.

Everything a stream name encodes also appears in the event data, since no reader parses stream
names (`in-vitro-patching-reply-to-lasm-core-on-event-shape.md`). Field names below follow patchrig's;
the schemas themselves will come from `lasm_core`.

A measurement:

```json
{
  "type": "evidence.recorded",
  "stream_id": "experiment:<cell-id>",
  "data": {
    "cellId": "<cell id>",
    "attempt": 1,
    "shardIndex": "<optional, for a shard>",
    "shardCount": "<optional, for a shard>",
    "target": { "binding": "weight-patch", "ref": "<what was measured>" },
    "vindexPin": "<revision>",
    "patchDigest": "sha256:<digest>",
    "manipulationCheck": "<passed, failed, or not applicable>",
    "tier": "<e.g. Tier 1>",
    "scope": "<e.g. Gemma 3 1B, N=10>",
    "controlsState": "<controls state at the time>",
    "measurements": { "<free-form>": "…" },
    "recordsDigest": "sha256:<the verified records>",
    "environment": { "host": "<e.g. M5, Mac Studio>", "fingerprint": "…" },
    "ledgerPosition": "<optional: only when the subject is a projection of ledger events>"
  }
}
```

A verdict:

```json
{
  "type": "verdict.recorded",
  "stream_id": "judgement:<cell-id>@<prereg-date>@<scorer-version>",
  "data": {
    "cellId": "<cell id>",
    "attempt": 1,
    "cites": { "streamId": "experiment:<cell-id>", "streamVersion": 1 },
    "preregistration": "<date of the FINDINGS.md entry>",
    "scorerVersion": "<git commit of the scoring code>",
    "supersedes": "<the verdict stream this re-score replaces, or null>",
    "verdict": "holds | inconclusive | fails | cannot-tell",
    "cannotTellReason": "<required with cannot-tell, forbidden otherwise: a code from a closed set>",
    "detail": "<optional free text beside the reason, e.g. which instrument check failed>",
    "policyEvent": "<optional: the policy event judged, when there is one>"
  }
}
```

*(Revised 2026-10-31.)* A verdict carries the rig's verdict in the rig's own
vocabulary, as evidence in its own terms. How LogicalAssembly judges it (for
example, whether a policy holds) is a separate projection on our side.
Patchrig's four values (`in-vitro-patching-reply-on-cannot-tell.md`), in
`lasm_core`'s kebab-case for values:

| Value | Meaning |
| --- | --- |
| `holds` | the whole interval clears the bar |
| `inconclusive` | the interval straddles the bar; evidence exists but doesn't decide |
| `fails` | the whole interval is on the wrong side of the bar |
| `cannot-tell` | no verdict was possible: no probes, too few values for an interval, a degenerate stratum, or a failed instrument check. Never a pass |

`cannot-tell` always carries `cannotTellReason`, and no other verdict may. It's a
code from a closed set in `lasm_core`'s `verdict.recorded` schema, so a code
outside the set is rejected rather than passed through. An optional `detail`
explains further; projections report it and never interpret it
(`lasm-core-reply-on-four-verdict-values.md`,
`in-vitro-patching-reply-on-cannot-tell-reasons.md`):

| Code | When |
| --- | --- |
| `no-probes` | a criterion was scored over no probes |
| `too-few-values` | fewer than two values, so no interval |
| `degenerate-stratum` | a stratum with no correct, or no incorrect, answers, so it can't discriminate |
| `instrument-gate-failed` | an instrument or control check failed; `detail` names which |
| `no-eligible-chains` | *proposed by patchrig, pending `lasm_core`:* composites were measured, but no chain had both hops retrieve |

A new code reaches the ledger in a fixed order: patchrig proposes it, `lasm_core`
adds it and releases, LogicalAssembly updates its pin, and only then does
patchrig emit it.

**Two things are never `cannot-tell`.** A measurement with no pre-registered
threshold yet produces **no verdict event**: a `cannot-tell` would imply a
judgement was attempted. An engine or parse error stops the cell, and an
unverified cell sends nothing. A summary across criteria ranks `fails`, then
`cannot-tell`, then `inconclusive`, then `holds`: one unmeasured criterion blocks
a pass. The first version of this contract used `conforms | diverges |
inconclusive`, and patchrig's scorer once reported cannot-tell as
`holds_weakly`. Both are superseded: `holds_weakly` no longer exists.

An invalidation:

```json
{
  "type": "verdict.invalidated",
  "stream_id": "judgement:invalidation@<instrument>@<date>",
  "data": {
    "instrument": "<the control or instrument found flawed, by id>",
    "scope": { "patchrigCommits": ["…"], "vindexPins": ["…"], "larqlVersions": ["…"] },
    "cites": { "streamId": "judgement:<cell-id>@<prereg-date>@<scorer-version>", "streamVersion": 1 },
    "reason": "<what was wrong>"
  }
}
```

The condition (the instrument and its scope) applies to *every* verdict, including verdicts written after
the flaw was found. The list of verdicts named in the stream's events records
what was known at the time. A writer checks each new verdict against
outstanding invalidations before writing it: recording a verdict an
invalidation already covers is a bug on the writer's side.

A retraction, when an invalidation itself turns out to be wrong
(`in-vitro-patching-reply-on-retracting-invalidations.md` and
`lasm-core-reply-on-retracting-invalidations.md`, accepted 2026-10-31):

```json
{
  "type": "invalidation.retracted",
  "stream_id": "judgement:invalidation-retraction@<invalidation stream id>@<date>",
  "data": {
    "cites": "judgement:invalidation@<instrument>@<date>",
    "reason": "<why the invalidation was wrong>"
  }
}
```

An invalidation applies only while no `invalidation.retracted` cites it. The
verdicts it covered then fall back to the projection's rules below. Two
things are deliberately left out:
- **Retracting a retraction:** a wrong retraction is recorded as a new
  invalidation, with its own condition and date.
- **Retracting a verdict:** a re-score naming it in `supersedes`, or an
  invalidation, already handles that.

What changed from the first version, and why:
- **Measurement and outcome are separated,** because they change at
  different rates. A single event holding both would have to be edited
  whenever a threshold or the scoring code changes, and a ledger can't edit.
- **Verdicts carry the pre-registration date and scorer version,** so each
  can be traced to the thresholds and code it was judged under.
- **Measurements carry their pins** (vindex revision and patch digest), so a
  number names the exact artifact it was taken against.
- **Only verified runs are reported.** A crashed or unverified run produces
  no event, and a re-run is a new attempt, so it gets a new stream.
- **Tier, scope, and controls state travel with every measurement,** as
  in-vitro-patching asked. Whether results mean "a policy holds" stays
  LogicalAssembly's judgement.
- **The manipulation check is recorded** before any verdict counts
  (`lasm-sans-io-mind.md`). Cannot-tell is its own verdict value, `cannot-tell`, never a
  weak positive.
- **The ledger position is optional.** Patchrig plants a synthetic corpus and
  projects no ledger events, so there's nothing to cite yet.
- **The policy event is optional on a verdict,** since experiments don't
  always judge a governance policy.

Verdicts about experiments use their own stream kind, `judgement`, which
rastro registered so that research verdicts never blur with `evaluation`
findings about operational episodes (`rastro-reply-on-measurements-and-verdicts.md`,
project `rastro`). The stream kind is the field rastro's authorization table
checks, so the separation doesn't rest on id conventions.

**A cell's current verdict exists only per pre-registration.** Each dated
pre-registration is its own claim: a later one adds a question, and never
overwrites an earlier answer. Scorer versions are git commits, which have no
order. So the verdict projection
(`in-vitro-patching-reply-on-judgements-and-invalidations.md`, project
`in-vitro-patching`) follows four rules:

| Rule | Why |
| --- | --- |
| Fold per (cell, pre-registration), never across pre-registrations. | Each pre-registration is its own claim. |
| Within one, a re-score names the verdict stream it replaces in `supersedes`. | Order comes from the events, not from comparing commit hashes. |
| The current verdict is the one nothing supersedes, minus any whose invalidation condition matches an unretracted invalidation. | Combines supersession, invalidation conditions, and retractions. |
| Two verdicts for one (cell, pre-registration) with neither superseding the other is a projection *finding*, not a tie to break. | The same stance as the rule projection, which refuses to rewrite while it reports findings. |

Rastro can't list streams, so the projection builds its own index by following
the global log: from each `judgement` event to the measurement it cites, and
from each invalidation's condition to every verdict it matches. That
projection belongs in `lasm_core` later.

### Credentials
The principle from the first version still holds, and rastro now implements
it. Each writer is a separate principal: paseo-core's evidence emitters,
LogicalAssembly's command writer, and each witness. Rastro authorizes on
(principal, stream kind, event type), so a witness can append to
`evaluation:*`, `experiment:*`, or `judgement:*`, but never to `policy:*`.
Witnesses should each have their own credential: patchrig has asked rastro for
one limited to `experiment` and `judgement` streams, so a faulty auto-bench
writer can't append to patchrig's streams, or the reverse. A compromised
witness can't accept a policy or record a decision. The decision bearer that
paseo-core uses for `/decisions` stays separate from all of them.

## Why This Is a General Pattern
paseo-core is the first binding target because it's the one we govern live.
The same shape (policy events, projections per binding, and evidence
events) carries over to other data planes:

- **A data platform:** the bindings point at tables and metric views, and
  the projection becomes grants and constraints.
- **Agent runtimes:** the bindings point at skills and MCP capability
  families, and the projection becomes skill content and capability
  allowlists.
- **Model weights:** the binding is a weight patch. The projection is
  enabled only for engines whose evidence (in particular integration and
  retraction) clears pre-registered thresholds
  (`lasm-world-ledger-event-sourced-mind.md`).

paseo-core proves the loop first: command, append, project, enforce,
witness, contest. It has a real enforcement point, a runtime that refuses to
act without our answer, and that's still rare.

## Tensions
- **Projection lag.** "Accepted in the ledger" and "enforced by
  `/decisions`" are different moments. The first version called this a
  rollout problem; it's now named and measurable. Every decision records the
  ledger position its projection reflected, so a decision made before a new
  policy reached the projection is attributable, not mysterious.
- **Who issues commands.** The positioning says the buyer is whoever is
  accountable for the meaning, a domain owner. Today the only editor is a
  superuser. Ownership per policy, and a real acceptance step, are needed
  before this is more than a renamed admin table. `lasm_core`'s aggregates
  are where those rules get enforced.
- **Identity of applications.** paseo-core mints application ids. Policies
  that name ids are brittle. They should select applications by binding,
  type, and eventually owner, which brings back the deferred `owner` format
  question (`kind:value`) from Phase 3. The `application:<id>` stream is
  keyed by id, which is fine: streams record history, while policies select
  targets.
- **Break-glass stays outside governance by contract.** The operator is
  never asked. The ledger records each bypass, but no policy can govern it.
  That makes contested-policy automation essential: a policy with many
  bypasses is a policy in dispute.

## Open Questions
1. **Event schemas in `lasm_core`.** The first schemas are `policy.proposed`,
   `policy.accepted`, `policy.contested`, `policy.superseded`,
   `decision.made`, `application.removed`, and `evidence.recorded`. What
   does auto-bench need to add to `lasm_core` for them: a policy entry kind,
   aggregates, and projections?
2. **Stream kinds.** Rastro registers `policy`, `application`, `episode`,
   and `evaluation`. Our proposals (decisions and removals in
   `application:<id>`, and an `experiment` kind) await rastro's answer.
3. **Backfill.** Existing decision and removal records become events with
   deterministic ids (so re-running is idempotent), original timestamps in
   the data, and the backfill recorded in metadata. Should Django keep
   writing both its own records and ledger events until the projection is
   trusted, or switch over at once?
4. **How is a policy contested in the app?** A staff action, an evidence
   threshold that opens a review, or both?
5. **Does paseo-core need to know?** Probably not. It sees only
   `/decisions`. If it ever asks *why*, a decision could return the policy
   event it came from, as a generic field, per the contract-leads rule.

## Working Hypothesis
The decision rules we shipped in Phase 4 are the first projection of a
ledger that doesn't exist yet. Making that ledger exist (rastro keeping the
events, `lasm_core` deciding which are allowed, and LogicalAssembly
projecting and enforcing them) turns LogicalAssembly from "a control plane
with a rule table" into "a control plane whose every rule, decision, and
piece of evidence has a history that can be replayed, attributed, and
contested." paseo-core is where that starts, because it's the one runtime
that already refuses to act without our answer.

**The next step is the first slice agreed with rastro**
(`lasm-rastro-as-the-world-ledger.md`), with no behavior change:
1. Seed today's three rules as `policy.accepted` events.
2. Backfill the existing decision and removal records.
3. Project `DecisionRule` from the ledger, through `lasm_core`.
4. Append every new decision as `decision.made`.
5. Accept when replaying from position 0 rebuilds the same table.
