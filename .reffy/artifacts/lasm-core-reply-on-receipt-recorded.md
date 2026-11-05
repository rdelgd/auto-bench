# Reply: `receipt.recorded`, Answered Now and Defined When It Has a Writer

For in-vitro-patching (patchrig) developers and their agents, copied to
LogicalAssembly and Rastro. This answers
`in-vitro-patching-proposal-receipt-recorded.md` (project
`in-vitro-patching`).

Date: 2026-11-05. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-receipt-recorded.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **The receipt is well shaped.** It's a record, not a verdict, with no
   span text, and the two-step move is explicit.
2. **We'll define `receipt.recorded` when it has a writer,** not before.
   Nothing would emit it yet.
3. **Our answers to your three questions:**
   - options stay as text for now;
   - `sequence` goes in the envelope, and `episode` stays in data;
   - `adapter` is shared with `evidence.recorded` v2.
4. **One field to define before the schema:** what "off-game" means for
   `answer`.

## Why Not Define It Yet
Every event type in `lasm-core` so far was written for a writer that existed,
and fitted to its real data. The version 2 findings are the clearest case:
your draft events showed the grouping gap and the short hashes, and no field
list would have.

For receipts, there's no writer yet:
- **Patchrig's receipts stay inside check records,** which never leave the
  rig, by your own rule.
- **No production observer exists.** LogicalAssembly's applicability readout
  hasn't started.
- **Whether receipts belong in the ledger at all** is still LogicalAssembly's
  call. Their view is that receipts belong to each land's ledger, at episode
  ingest volume, emitted by an observer's own principal.

So we'll define `receipt.recorded` v1 when the first emitter is being built.
It will be fitted to that emitter's real receipts, as we did with your
findings. Your two receipts and the field table are the starting draft. The
answers below are settled now, so `observer/1` can rely on them.

## Answers to Your Three Questions

### 1. Option texts: by reference?
**Not for now.**
- In a `classify` receipt, the options are already references: entry numbers
  like `XT.1-500`.
- `retrieve` targets are the catalogue's own words, not user text. They're
  held by the same land that holds the receipts.

A second form, references plus hashes resolved from the assembly, is only
worth defining when a land with a sensitive catalogue exists. That land's
needs should decide it. We'll record it as an open question in the change,
rather than build both forms now.

### 2. `episode` and `sequence`: data or envelope?
**Split them:**
- **`sequence` goes in the envelope.** It exists for Rastro's retry handling,
  so it belongs where Rastro reads it, and out of `data`, by your own rule of
  nothing the envelope carries.
- **`episode` stays in `data`.** It identifies what the receipt belongs to,
  and our rule is that anything a stream name encodes also appears in data,
  because projections never parse stream ids.

**Rastro:** please confirm the envelope's ingest field for the per-episode
sequence, so we can name it the same way.

### 3. Share `adapter` with `evidence.recorded` v2?
**Yes.** `lasm-core` 0.6.0 already defines `AdapterIdentity` (`kind`, `model`,
`host`, `served`, and optional `route`, with exact-length `served`), and
`receipt.recorded` will reuse that same definition. Adapters are then
identified one way everywhere.

**One correction to the reasoning:** sharing the shape doesn't let an
invalidation reach receipts. An invalidation removes **verdicts**, and a
receipt isn't a verdict, by design. The verdict projection never reads
receipts, so there is nothing for it to remove.

If someone later needs to find "every receipt made through a flawed adapter",
that's a separate receipt projection. It would match the same
`AdapterIdentity`, which sharing the definition makes simple.

## One Field to Define: "Off-Game"
`answer` is required "unless off-game", but the proposal doesn't say what
off-game is. Before the schema, we'll need:
- what makes a move off-game, in `observer/1`'s terms;
- how a receipt shows it, for example a `move` value or a flag, so that a
  missing `answer` is never ambiguous between "off-game" and "malformed".

## Next
- **Patchrig:** define off-game in `observer/1`. Nothing else is needed now.
- **Rastro:** confirm the envelope's sequence field.
- **LogicalAssembly:** decide whether receipts enter the ledger, and tell us
  when the first emitter is being built. That's when we open the
  `receipt.recorded` change.
