# Step 1: The First `MODE COMPOSE` Check, on fruitfly 1B

For LogicalAssembly, auto-bench (`lasm-core`) and Rastro developers and their
agents. This is the step 1 note promised in
`in-vitro-patching-reply-to-lasm-core-on-event-shape.md` and
`in-vitro-patching-reply-on-cannot-tell-reasons.md`.

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-step-1-fruitfly-compose-check.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

**Status of everything below: exploratory observations.** One insert, one
session, larql's default settings, and no run directory or test pinning it. By
our own rules none of it is a finding yet, and none of it should be quoted as
one.

## Summary
1. **`MODE COMPOSE` edits weights on Gemma 3 1B.** larql installed a
   constellation in the feed-forward weights, with no retrieval sidecar.
2. **At larql's default settings, one insert took over the whole model.** It
   wasn't targeted: every prompt we tried, related or not, now answers with
   the inserted token.
3. **larql holds about 6 GB per billion parameters** for this path. That
   explains the 4B result, and sizes a Mac Studio.
4. **The 1B is fast:** about 200 ms per probe, and 18 s for a whole session.
5. **It exposed two problems in patchrig itself,** both to fix before any
   cell runs. No date for our first verified cell yet.
6. **auto-bench can start the verdict schemas now.** Nothing here changes
   the event shapes we agreed.

## What was done
- **Model:** `google/gemma-3-1b-it` at revision `dcc83ea8…`, 999,885,952
  parameters. Weights verified against their published SHA-256 (`3d4ef8d7…`).
- **Extract:** larql 0.2.0, `--level all`, f16, unquantized, in 311 s with a
  3.8 GB peak. All 340 tensors recognised and none dropped. That supports the
  reading that the 439 tensors dropped from the 4B were its vision side; the
  1B is text-only.
- **Pin:** `595253292fbddf0d1a5a6d75eff6c74e19d37722387e39a208a7e75d48558890`,
  13 files, 1.91 GiB.
- **Larql's support for the small models' `gemma3_text` architecture:**
  confirmed.
- **The check:** in one larql session, probe, then `INSERT INTO EDGES
  ("Atlantis", "capital-of", "Poseidon") MODE COMPOSE` with no other
  settings, then probe again. This is `compile_demo`'s fact; on the 4B, LARQL
  published Atlantis → "Pose" 56.91% and France → Paris 97.91% → 67.34%. A
  watchdog was ready to stop larql before it reached swap, as the 4B had.

## What happened

larql reported: `Inserted: Atlantis —[capital-of]→ Poseidon at L18`, `mode:
constellation (trace-guided gate + up + down, gate_scale=30,
install_compiled_slot, balanced)`. Layer 18 is inside the 1B's knowledge
band (layers 10–19).

| Prompt | Before the insert | After one insert |
|---|---|---|
| The capital of Atlantis is | said 29.2% | **Pose 99.99%** |
| The capital of France is | Paris 90.6% | **Pose 99.98%** (Paris 0.01%) |
| The capital of Japan is | Tokyo 96.3% | **Pose 99.82%** |
| The capital of Germany is | Berlin 94.8% | **Pose 94.85%** |
| The largest planet is | Jupiter 75.0% | **Pose 100.00%** |
| Poseidon is the god of the | sea 99.4% | **Pose 100.00%** |
| The capital of Atlantis is Pose | **idon 91.9%** | **Pose 99.99%** |

**What it shows:**
- **It is a weight edit.** No `knn_override` source appears anywhere. The
  path patchrig exists to study is reachable on the M5.
- **At default settings it isn't targeted.** The edit fires on near
  neighbours, on unrelated prompts ("The largest planet is"), and even on the
  prompt that should continue "Poseidon". On the 4B, LARQL published France →
  Paris falling to 67.34% after one insert. Here it falls to 0.01%, and far
  fields go too.
- **It may be a matter of settings.** We used none of the knobs (`AT LAYER`,
  `CONFIDENCE`, `ALPHA`), and larql's defaults (`gate_scale=30`) may be tuned
  for larger models. Whether a targeted insert exists on the 1B is the next
  experiment, and it will be declared before it runs. Tuning settings until
  the numbers look good is what pre-registration exists to prevent.

## Memory, and sizing a Mac Studio
The 1B session peaked at a **6.1 GB** footprint: about **6 GB per billion
parameters** on the unquantized `MODE COMPOSE` path. That fits the 4B's 22 GB
peak before we stopped it. Rough sizing for one session at a time:

| Model | Peak, estimated | Machine |
|---|---|---|
| 1B | 6 GB (measured) | the M5 |
| 4B | ~24 GB | 48–64 GB Studio; 32 GB is borderline |
| 12B | ~72 GB | 96 GB or more |
| 27B | ~160 GB | 192 GB |

Running several cells at once multiplies these.

## Two problems this exposed in patchrig
Both are ours, and both get fixed before any cell runs.

1. **Our scoring couldn't credit a multi-token target.** One `INFER` predicts
   one token, and " Poseidon" is " Pose" + "idon": before the insert, the
   model continued "Pose" with "idon" at 91.9%. "Pose" is the correct first
   token. Patchrig's rule that a token fragment never counts as an exact hit
   would make exact retrieval impossible for any multi-token target, and
   every invented name we plant is almost certainly multi-token. The fix is to
   score the whole token sequence, prompting with each correct token in turn.
   It changes a scoring rule, so it goes through a ReffySpec change and a
   dated amendment.

   **A correction we owe:** our notes have called LARQL's published "Pose
   56.91%" a fragment that barely made a majority. Part of that was this
   artifact. "Pose" is the right first token; the open question is whether
   the continuation completes, and how strongly.

2. **The positive controls don't transfer to the 1B.** LARQL's published
   numbers are from the 4B, so on the 1B there is nothing published to
   reproduce. fruitfly needs its own control definition, at least that an
   insert retrieves and that a manipulation check shows the edit changed
   something, before any failure on it can be interpreted.

## What this means for each project
- **auto-bench:** you can open the `lasm-core` change for
  `evidence.recorded`, `verdict.recorded`, `verdict.invalidated` and
  `invalidation.retracted` now, as you planned. Nothing here changes the event
  shapes, the four verdict values, or the five cannot-tell reasons.
- **LogicalAssembly:** the weight projector is now testable on hardware we
  have, at fruitfly scale. The first observation is a warning, not a
  verdict: an untargeted insert would fail interference badly. That is
  exactly the guarantee your conformance table puts between a weight projector
  and being enabled.
- **Rastro:** nothing yet. The first verified cell is still some steps away.

## Next, in order
1. Fix the multi-token scoring rule: a ReffySpec change and a dated
   amendment.
2. Define fruitfly's positive controls.
3. Pre-register a small exploration of `AT LAYER`, `CONFIDENCE` and `ALPHA`,
   starting from the settings larql's README gives for this very fact as its
   "validated regime" (`AT LAYER 24 CONFIDENCE 0.95 ALPHA 0.30`, on the 4B's 34
   layers), adapted to the 1B's 26.
4. Then `LarqlEngine`, `patchrig cell` and `patchrig verify`, toward the
   first verified cell.

No date for the first verified cell yet. We'll post again after step 3.
