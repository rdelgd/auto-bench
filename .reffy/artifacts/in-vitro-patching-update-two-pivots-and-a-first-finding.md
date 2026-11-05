# Update: patchrig Changed Course Twice, and Has a First Finding

For LogicalAssembly, Rastro and paseo-core developers and their agents. It
updates what in-vitro-patching (`patchrig`) agreed with each of you in
October. Each project has a section below; read yours, and the summary.

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-update-two-pivots-and-a-first-finding.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **patchrig no longer tests weight editing first.** Since 2026-11-03 it is
   a **conformance kit**. It checks any model or adapter against the
   **observer contract**, on planted fictional catalogues, in seconds to
   minutes. The LARQL rig is shelved: still built and tested, not run.
2. **There are two kinds of result.**
   - **Checks** are fast, labelled "prototype check, not evidence", and never
     findings.
   - **Findings** are pre-registered and confirmed on unseen fixtures.
3. **The first finding.** On a catalogue in context, asking "Does any entry
   cover this?" first, and abstaining below a tuned threshold, lifts
   balanced accuracy by about 0.2 for `gpt-6-luna` and TypeSafe's Jev. Both
   claims held on 40 catalogues nobody had seen.
4. **What changes for you:**
   - **LogicalAssembly:** the Tier 1-on-Modal plan is paused, and nothing is
     needed from you now.
   - **Rastro:** we have a proposal for what enters the ledger, and one
     question.
   - **paseo-core:** for information only.

## What changed, and why

### First: language games, not weights
`FINDINGS.md` 2026-11-03. The question moved from whether LARQL patches
scale, to whether a model can be *trained* in the practice at the point of
use, as well as or better than having propositions written into its
weights. The comparison was built and pre-registered, then parked before it
ran, for the reason below.

### Then: the contract, not the mechanism
`FINDINGS.md` 2026-11-03, "patchrig becomes a conformance kit";
`patchrig-as-a-conformance-kit.md`.

The mechanisms that carry propositions into a model are likely to go native
soon: weight edits, in-context regimens, and monitoring streams like
Nuveris's own. Building around them is scaffolding that goes stale, as
2023's did around early reasoning models. What lasts is what an observer
owes the stack:
- classify a span against numbered propositions;
- abstain when nothing applies;
- respect editions (current, and as of a date);
- emit a **receipt** for every answer.

The kit is:
- **the contract,** `observer/0`;
- **fixtures:** a fictional catalogue generator, with numbered entries in
  editions and abstention traps;
- **adapters:** OpenAI's Decisions API, the Vercel AI Gateway (Jev),
  OpenAI-compatible chat endpoints, and scripted fakes;
- **`patchrig check`:** a scorecard in seconds.

A ten-seed check on two decision models takes well under a minute and costs
fractions of a cent. The shelved Tier 1 campaign had estimated 12 hours on
the M5 for one small model.

### The first finding
`FINDINGS.md`, "result: the two-step observer". Exploratory checks found
that, with only a catalogue in context, every model tested mostly answers
an abstention item with an entry, usually the one sharing the stranger's
place. The same model, asked the yes/no question "Does any catalogue entry
cover this?", mostly says no. So we pre-registered a two-step rule:
1. ask the yes/no question;
2. abstain below a threshold tuned on fresh seeds;
3. otherwise pick an entry.

On 40 unseen catalogues:

| Claim | Gain in balanced accuracy [95%] | Verdict |
|---|---|---|
| `gpt-6-luna`, catalogue only | +0.243 [+0.215, +0.271] | Holds |
| `typesafe-ai/jev`, catalogue only | +0.208 [+0.181, +0.235] | Holds |
| Luna, rules and drills already in context | +0.067 [+0.033, +0.100] | Inconclusive |
| Jev, rules and drills already in context | +0.031 [+0.015, +0.049] | Fails |

All four came out as predicted in advance. The thresholds do not transfer
between models (0.02 for Luna, 0.30 for Jev), so each adapter is tuned. The
result covers these models as served on 2026-11-03, on fictional
catalogues. It says nothing yet about real codified material.

**Consequence:** the contract's next version, `observer/1`, makes the move
explicit. A receipt says *whether anything applies*, with its probability
and the adapter's tuned threshold, before it says *which entry*.

## For LogicalAssembly
- **The Tier 1-on-Modal plan is paused, not cancelled.** That covers cells
  as the unit, shards, the controls-gate ordering in the jobs application,
  and the f16 extract for the S3 prefix. We won't ask for jobs or upload the
  extract while the weight-level rig is shelved. If it returns, the October
  agreements (controls gating other units, the preregistration field, a
  shard running all its phases) still stand as written.
- **What we can offer instead.** The observer contract and `patchrig check`
  can check any adapter you have, including anything built on the Nuveris
  applicability readout, against the same fixtures in minutes. If an adapter
  exposes a decision-style interface (a choice over options, plus a yes/no
  coverage question), it plugs in directly.
- **A question for you:** is there an adapter of yours you'd want checked
  first?

## For Rastro
- **What we agreed** (October): `evidence.recorded` on `experiment:<cell-id>`
  streams, and `verdict.recorded`, `verdict.invalidated` and
  `invalidation.retracted` on `judgement:` streams, through
  `patchrig-witness`. We have not generated its token, so nothing has been
  written.
- **What we propose now:**
  - **Checks never enter the ledger.** They are prototype checks by
    contract.
  - **Findings do.** A pre-registered confirmation like the two-step result
    becomes `evidence.recorded` for its confirmation run and one
    `verdict.recorded` per claim, on the streams already authorised. The
    stream naming would follow the confirmation run instead of a cell.
  - **Identity fields.** `larqlVersion` and `larqlBinarySha256` don't apply
    to hosted adapters. We'd carry an adapter identity instead — kind,
    model, endpoint host, and the date the model was served — alongside
    `patchrigCommit`.
- **One question:** should *receipts* become ledger events in their own right
  (`receipt.recorded`?), written by an observer in production, rather than
  by patchrig? `observer/0` receipts already use your conventions (camelCase
  keys, kebab-case values) and carry no credential, and `observer/1` adds
  the two-step move. We'd like your view before fixing its shape.
- We'll generate the witness token, and send only its hash, when the first
  finding is ready to append.

## For paseo-core
For information only; nothing is asked. The "mind" primitive, as patchrig
first imagined it, meant domain knowledge written into a model's weights.
It is now framed as a **contract**: the observer's moves and receipts,
checked against any carrier. Its scripted fake adapter is the sans-I/O mind
from the earlier exchange with LogicalAssembly, the same contract with no
model behind it.

## Where to read more
All in project `in-vitro-patching`:
- the argument: `language-games-instead-of-weights.md` and
  `patchrig-as-a-conformance-kit.md`;
- the exploratory checks, labelled as such: `first-conformance-checks.md`;
- the current specs: `observer-contract`, `adapters` and `checks`;
- `FINDINGS.md`, in the repository: the dated entries.
