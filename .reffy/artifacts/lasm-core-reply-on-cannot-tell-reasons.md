# Reply: Five Cannot-Tell Reasons, Settled

For in-vitro-patching (patchrig) and LogicalAssembly developers and their
agents. This answers `in-vitro-patching-reply-on-cannot-tell-reasons.md`
(project `in-vitro-patching`).

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-cannot-tell-reasons.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **We adopt `no-eligible-chains`.** The starting set is five codes.
2. **We adopt both exclusions:** "no threshold yet" and engine or parse
   errors are not codes, and produce no verdict event.
3. **The rest is settled as agreed:**
   - a closed set, kebab-case on the wire;
   - required with `cannot-tell`, and forbidden with any other verdict;
   - an optional free-text `detail`;
   - the order for adding a code.
4. **Nothing changes in `lasm-core` yet.** The verdict schemas are written
   when your step 1 artifact arrives.

## 1. The Five Codes

| Code | When |
| --- | --- |
| `no-probes` | nothing was measured |
| `too-few-values` | fewer than two values, so no interval |
| `degenerate-stratum` | the stratum can't discriminate: no correct, or no incorrect, answers |
| `instrument-gate-failed` | an instrument or control check failed; `detail` names which |
| `no-eligible-chains` | probes were measured, but no chain had both hops retrieve, so there's no denominator |

**Why `no-eligible-chains` earns its own code.** It's a different case from
`no-probes`:
- **`no-probes`** means nothing was measured.
- **`no-eligible-chains`** means the measurement happened, and the insertion
  failed so badly that none of it could count.

A projection that groups reasons should show that difference. Adding the
code before the schema exists costs nothing, while adding it later would
cost a release. Keep it in the rig.

## 2. What Is Not a Code
Both exclusions are right, and the verdict schema's design will record them,
so that nobody later adds a code for either:
- **No threshold yet:** no verdict event at all. A judgement that was never
  attempted shouldn't look like one that was. A remove-exactness measurement
  before its pre-registration, or the deliberately unthresholded
  planted-into-native stratum, is a measurement on its own.
- **Engine or parse errors:** no event at all. The cell stops, and an
  unverified cell sends nothing. A `cannot-tell` here would quietly turn a
  failure into a judgement, which is what your rule 8 exists to prevent.

## 3. Thank You
We're glad the rig now enforces reasons where the spec already required
them. A `cannot_tell` without a reason, or a reason on another verdict,
can't even be constructed. The schema will hold events to the same rule, so
the rig and the ledger reject the same mistakes.

## 4. Next
- **Patchrig:** post when the fruitfly 1B `MODE COMPOSE` check is done.
- **auto-bench:** then open the `lasm-core` change for `evidence.recorded`,
  `verdict.recorded`, `verdict.invalidated`, and `invalidation.retracted`:
  - the four verdict values;
  - `cannotTellReason` from these five codes, with the conditional
    requirement both ways;
  - an optional `detail`;
  - the two exclusions recorded in its design.
