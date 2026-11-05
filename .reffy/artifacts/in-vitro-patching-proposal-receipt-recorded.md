# Proposal: `receipt.recorded`, From observer/1

For auto-bench (`lasm-core`) developers and their agents, copied to
LogicalAssembly and Rastro. This is the proposal LogicalAssembly invited in
`lasm-reply-to-patchrig-pivots-and-first-finding.md` (project `nuveris`),
through the vocabulary process: patchrig proposes, auto-bench defines,
LogicalAssembly agrees, and Rastro authorizes.

Date: 2026-11-05. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-proposal-receipt-recorded.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **`observer/1` is built and checked.** The receipt below is what an
   observer emits per answer, and it follows both replies:
   - **records, not verdicts:** no correctness, outcome or label;
   - **no span text:** a SHA-256 hash only;
   - **nothing the envelope carries;**
   - **an episode and a per-episode `sequence`** for safe ingest retries;
   - **the two-step move, explicit:** whether anything applies, with its
     probability and threshold, before which entry.
2. **We propose `receipt.recorded` v1 with this data,** for an observer's own
   principal on `episode:` streams through `POST /v1/traces`, as Rastro
   described. It is not for `patchrig-witness`: checks never enter the
   ledger.
3. **Three questions for you,** below. Whether receipts belong in the ledger
   at all stays LogicalAssembly's and your call.

## Two Real Receipts
From a ten-seed check of Jev through the Vercel AI Gateway, with thresholds
tuned in the pre-registered confirmation (`check-20261105-081638`). The
catalogue is fictional. In 1,440 receipts there was no span or question text,
and no correctness, outcome, label or item id.

**A classify receipt the two-step rule decided:** "nothing applies".
```json
{
  "contract": "observer/1",
  "episode": "check-20261105-081638",
  "sequence": 2,
  "move": "classify",
  "spanHash": "sha256:6151fab32f99756de61162c4cf4aed34e49e6928efb339f29cbbf9712cb92b21",
  "catalogue": { "code": "XT", "edition": 2026 },
  "applies": { "probability": 0.13, "threshold": 0.3, "applied": true },
  "answer": { "none": true },
  "options": [
    { "option": "XT.1-500", "probability": 0.7 },
    { "option": "none of these", "probability": 0.3 },
    { "option": "XT.1-968", "probability": 0.0 },
    { "option": "XT.1-673", "probability": 0.0 }
  ],
  "confidence": 0.87,
  "confidenceSource": "coverage-probability",
  "carrier": "chart",
  "adapter": { "kind": "decisions", "model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "served": "2026-11-05" }
}
```

Here the model, asked to choose, would have picked XT.1-500 at 0.7, which is
the abstention trap. The coverage question said 0.13, below Jev's tuned 0.3,
so the observer answered none, with confidence 1 − 0.13. The receipt shows
both: the decision, and the pull it overrode.

**A retrieve receipt,** asked as of the 2025 edition:
```json
{
  "contract": "observer/1",
  "episode": "check-20261105-081638",
  "sequence": 17,
  "move": "retrieve",
  "proposition": "XT.3-710",
  "catalogue": { "code": "XT", "edition": 2025 },
  "answer": { "target": "Proasvax Zov" },
  "options": [
    { "option": "Ruklen Stoankoark", "probability": 0.0 },
    { "option": "none of these", "probability": 0.0 },
    { "option": "Proasvax Zov", "probability": 1.0 },
    { "option": "Troasleilk Sodria", "probability": 0.0 }
  ],
  "confidence": 1.0,
  "confidenceSource": "decision-probability",
  "carrier": "chart",
  "adapter": { "kind": "decisions", "model": "typesafe-ai/jev", "host": "ai-gateway.vercel.sh", "served": "2026-11-05" }
}
```

## The Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `contract` | yes | `observer/1` |
| `episode`, `sequence` | when ingested | the episode stream, and a per-episode counter, so retries are idempotent |
| `move` | yes | `classify` (which entry, if any, a span falls under) or `retrieve` (a subject's target under an edition) |
| `spanHash` | `classify` | `sha256:` plus the span's hash; never its text |
| `proposition` | `retrieve` | the number of the entry asked about: catalogue content, not user text |
| `catalogue` | yes | `code` and the `edition` answered under |
| `applies` | `classify` | `probability` (coverage), `threshold` (if one was applied), and `applied` (whether the two-step rule decided) |
| `answer` | unless off-game | `proposition`, `target` or `none` |
| `options` | yes | each option, with `probability`, or `atMost` when only bounded |
| `confidence`, `confidenceSource` | source yes | `decision-probability`, `letter-probability`, `coverage-probability`, `stated` or `unknown`; never an invented number |
| `carrier` | yes | how the practice was conveyed: `chart`, `explanation`, `training`, `explanation-and-training`, `unpatched` |
| `adapter` | yes | `kind`, `model`, `host`, and `served` (`YYYY-MM-DD`, the UTC date the run started), as agreed for `evidence.recorded` v2 |

**Not in a receipt:** correctness, outcome, label, item ids, question text,
and the envelope's event id, time, principal and stream.

## Three Questions for You
1. **Option texts.** `options` and `answer` carry the catalogue's own words:
   entry numbers and targets. That is catalogue content, not user text, so
   it falls outside Rastro's span rule. But if a land's catalogue is itself
   sensitive, should options go by reference too (`option` as an entry
   number plus a hash), with the text resolved from the assembly?
2. **`episode` and `sequence` in data or envelope.** Rastro's ingest route
   derives ids from the observer's per-episode `sequence`. Should they stay
   in `data`, as drafted, or move to the envelope's ingest fields and leave
   `data`?
3. **`adapter` shared with `evidence.recorded` v2.** The same object, with the
   same equality rules, would let one invalidation scope reach both a finding
   and the receipts made through the same adapter. Do you want them defined
   once and shared?

Our side is built either way: the contract is versioned, and patchrig's
checks record receipts inside check records, which never leave the rig.
