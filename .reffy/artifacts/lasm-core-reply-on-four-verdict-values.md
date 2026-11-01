# Reply: The Verdict Schemas Will Use Patchrig's Four Values

For in-vitro-patching (patchrig), LogicalAssembly, and Rastro developers and
their agents. This answers `in-vitro-patching-reply-on-cannot-tell.md`
(project `in-vitro-patching`) and `lasm-reply-on-four-verdict-values.md`
(project `nuveris`).

Date: 2026-10-31. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-four-verdict-values.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **The verdict schemas will use patchrig's four values:** `holds`,
   `inconclusive`, `fails`, and `cannot-tell`.
2. **Our earlier meaning of `inconclusive` is withdrawn.** That conflict was
   ours. `lasm-core-reply-on-enum-values.md` now carries a dated correction.
3. **`cannotTellReason` is a code from a closed set,** with an optional
   free-text `detail`.
4. **Patchrig confirms or replaces the four codes** before the schemas are
   written.

## 1. The Four Values
The schema's `verdict` enum uses the definitions in patchrig's change and in
`lasm-paseo-assembly-source-of-truth.md`:

| Value | Meaning |
| --- | --- |
| `holds` | the whole interval clears the bar |
| `inconclusive` | the interval straddles the bar; evidence exists but doesn't decide |
| `fails` | the whole interval is on the wrong side of the bar |
| `cannot-tell` | no verdict was possible. Never a pass |

Thank you, patchrig, for going past the marker we asked for. Removing the
unregistered 0.05 margin, rather than moving it into the thresholds, matters
more than any field name.

## 2. The Conflict, and Its Correction
`lasm-core-reply-on-enum-values.md` proposed `holds-weakly`, and used
`inconclusive` for "no usable evidence". Patchrig's change uses
`inconclusive` for "the interval straddles the bar", and `cannot-tell` for
what we meant. Two notes using one word for two meanings is how a ledger
ends up with verdicts nobody can read, so we've corrected ours. Its top now
carries a dated correction pointing here, and the original text is kept
below it. The rule that keys are camelCase and enum values kebab-case still
stands.

## 3. `cannotTellReason`: a Closed Set of Codes
- **Required when the verdict is `cannot-tell`,** and not allowed with any
  other verdict.
- **A kebab-case code from a closed set** in the `verdict.recorded` schema. A
  value outside the set is rejected, not passed through.
- **An optional `detail`,** free text, allowed beside `cannotTellReason` for
  anything the code doesn't say. Projections report it and never interpret
  it.

The starting set, from LogicalAssembly's reply:

| Code | When |
| --- | --- |
| `no-probes` | nothing was measured |
| `too-few-values` | fewer than two values, so no interval |
| `degenerate-stratum` | the stratum can't discriminate |
| `instrument-gate-failed` | an instrument or control check failed, for example the in-context gate |

**Why closed:**
- A projection can count and group reasons only if their spelling is
  guaranteed.
- A mismatch between the rig and the schema then shows up as a rejected
  event, not as a new, silent category.
- It's the same choice `lasm-core` 0.4.0 made for paseo-core actions in
  `FIRST_SLICE_BINDINGS`: one source of valid values.

**What it costs:** a new reason needs a `lasm-core` release before patchrig
emits it. The order is:
1. patchrig proposes the code;
2. `lasm-core` adds it to the `verdict.recorded` schema and releases;
3. LogicalAssembly updates its pin;
4. patchrig emits it.

Adding a code is additive and doesn't change the event's schema version.
Readers must be upgraded before writers use the new code. Patchrig changes
its reasons through dated amendments anyway, so we expect this to be rare.

## 4. What We Need From Patchrig
- **Confirm the four codes,** or send your own list. Your scorer produces the
  reasons, so the list is yours. We'll write whatever you confirm.
- **No date needed yet.** The `lasm-core` change for `evidence.recorded`,
  `verdict.recorded`, `verdict.invalidated`, and `invalidation.retracted`
  still starts when your step 1 artifact arrives.
