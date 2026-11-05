# Reply: The Pivots, the First Finding, and What Findings Need From `lasm_core`

For in-vitro-patching (patchrig) developers and their agents, copied to
auto-bench (`lasm-core`) and rastro. This answers
`in-vitro-patching-update-two-pivots-and-a-first-finding.md` (project
`in-vitro-patching`). Auto-bench is copied because one point needs a
`lasm_core` change before the first finding can be appended.

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-reply-to-patchrig-pivots-and-first-finding.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

## Summary
1. **We support both pivots.** Building on a contract rather than a mechanism
   is the bet LogicalAssembly's design rests on.
2. **No adapter of ours is ready to check yet.** The applicability readout
   hasn't been started.
3. **To auto-bench: findings can't be appended under `lasm-core` 0.5.0.** The
   `evidence.recorded` v1 schema requires weight-rig fields that a hosted
   adapter doesn't have. A version 2 with a generic identity is needed first.
4. **Receipts:** a new event type goes through the vocabulary process, not
   rastro alone. Our view on the substance is below.
5. **Agreed:** checks never enter the ledger; findings do.

## For patchrig

### The pivots
Moving from "can weights carry propositions?" to "what does an observer owe
the stack?" is the same move as the commoditization bet in
`lasm-sans-io-mind.md`: mechanisms change; contracts last. It also confirms
the hedge in our design. The baseline projectors (an exact index, and facts
provided in context) were meant to carry the mind even if weight editing
never earned its place. Your first finding is about that baseline: how a
model reads a catalogue in context, and when it should abstain. The weight
projector waits, which is how the design always meant it to work.

Shelving the LARQL rig with its tests still running, and pausing Tier 1 with
the October agreements kept as written, leaves the door open without paying
to keep it open.

### The first finding
It's a model of how evidence should look:
- pre-registered, with predictions written down first;
- confirmed on 40 unseen catalogues;
- reported with all four outcomes, including `inconclusive` and `fails`;
- scoped plainly: these models, as served on 2026-11-03, on fictional
  catalogues.

The four-value vocabulary did its job in its first real use. That the
thresholds don't transfer between models is a useful result in its own
right: a receipt has to carry its adapter's tuned threshold for anyone to
read it.

### Your question: which adapter to check first
None yet. The applicability readout hasn't been started, and nothing in
LogicalAssembly exposes a decision-style interface today. When one exists,
`observer/1` and `patchrig check` are the natural first test for it, and
we'll say so here.

## For auto-bench: findings need `evidence.recorded` version 2
Patchrig proposes appending each confirmed finding as `evidence.recorded`
for its confirmation run, plus one `verdict.recorded` per claim. That's
right in principle, but the data won't validate against `lasm-core` 0.5.0:

| Required in `evidence.recorded` v1 | A hosted-adapter finding has |
| --- | --- |
| `larqlVersion`, `larqlBinarySha256` | no larql |
| `vindexPin`, `patchDigest` | no vindex, no patch |
| `cellId`, `attempt` | a confirmation run, not a cell |

Your release note anticipated this: "the next measuring witness will need a
version 2 of `evidence.recorded` with a generic pin map." The next witness
turned out to be patchrig itself, after its pivot.

**What we'd ask for:**
- **`evidence.recorded` version 2,** with:
  - a generic run identity in place of `cellId`;
  - an **adapter identity** in place of the larql and vindex fields. Patchrig
    proposes kind, model, endpoint host, and the date the model was served,
    alongside `patchrigCommit`.
- **Version 1 stays readable,** for anything the shelved LARQL rig may yet
  write. `LEDGER_EVENT_SCHEMA_VERSIONS` already lets a type carry two versions.
- **Invalidation scopes need a matching list,** for example a list of adapter
  identities or served models. Otherwise an invalidation can't reach findings
  measured through a flawed adapter. Today's scope lists match only larql
  versions, vindex pins, and commits.
- **`project_verdicts` reads both versions,** grouping a run's verdicts the way
  it groups a cell's.

None of this is urgent until patchrig's first finding is ready to append. It
does need to land before then, or the first append fails validation.

## Receipts as Ledger Events
Patchrig asked rastro whether receipts should become `receipt.recorded`.
Rastro will authorize whatever the vocabulary defines, but defining an event
type is `lasm_core`'s job, in the order we agreed: patchrig proposes,
auto-bench defines, LogicalAssembly agrees, and rastro authorizes. Rastro is
replying too; this is LogicalAssembly's view of the substance, for
auto-bench:
- **A receipt is a fact about what an observer did.** That makes a production
  observer an **emitter**, not a witness. Its receipts belong to the ledger of
  the land where it runs (`lasm-an-order-of-sovereign-lands.md`), not to a
  central record.
- **Volume is evidence-ingest scale.** One receipt for every answer, from
  observers in production, looks like paseo-core's episode streams, not like
  write-once judgement streams. It probably wants an ingest path, with
  sampling recorded as rastro already does for episodes, rather than the
  command endpoint.
- **Receipts are records, not verdicts.** A receipt says what an observer
  answered, with its coverage probability and threshold under `observer/1`.
  Whether that answer was right is a separate judgement, made by a check, a
  finding, or a person contesting it.

We'd welcome a proposal from patchrig once `observer/1` settles, through the
usual process.

## Agreed as Proposed
- **Checks never enter the ledger.** They're prototype checks by contract,
  and "evidence, not verdicts" applies to the rig's own output too.
- **Findings do,** as pre-registered confirmations, once the schema can carry
  them.
- **The witness token waits** until the first finding is ready, and only its
  hash goes to rastro.
