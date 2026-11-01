# Review: `add-evidence-and-verdict-events`

For auto-bench (`lasm-core`) developers and their agents, copied to
in-vitro-patching (patchrig). This is LogicalAssembly's review of the draft
change `add-evidence-and-verdict-events` (project `auto-bench`), requested in
`lasm-core-note-on-invalidation-scope-fields.md`.

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-review-evidence-and-verdict-events.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

## Summary
1. **We accept the design,** with one gap to close: a (cell,
   pre-registration) group can end up with no status.
2. **Your decisions made without us are all fine for LogicalAssembly.**
3. **On your questions to patchrig:** matching a scope commit against either
   commit, and a conflict for an unsuperseded re-run, are both safe from our
   side. Patchrig decides.
4. **Our contract now matches your draft:** `supersedes` omitted rather than
   null, `policyEvent` as an event reference, `detail` on any verdict, and the
   two new measurement fields, pending patchrig.

## What We Like
- **It extends 0.4.0** (the per-type schema line, the validator, the shared
  checker) instead of adding a second mechanism.
- **The projection keeps every agreement:**
  - it folds per (cell, pre-registration);
  - `supersedes` orders re-scores;
  - an invalidation's condition reaches later verdicts;
  - a retraction makes its invalidation inert;
  - an empty scope never matches everything;
  - conflicts are reported, not resolved;
  - it never parses a stream id.
- **`manipulationCheck` is copied onto each projected verdict and never
  acted on.** Whether a verdict counts with a failed manipulation check is
  ours to judge, and that's the right split.
- **"LogicalAssembly must not act on a group with a finding addressed to its
  events."** We'll build our gate exactly that way. It's the same stance our
  rule projection takes, when it refuses to rewrite `DecisionRule` while
  findings are reported.
- **Addressed findings for the reason rule** (`verdict.reason_required`,
  `verdict.reason_not_allowed`), rather than a generic finding at `data`.

## The Gap: a Group With No Status
The design defines three statuses:
- **`current`:** exactly one candidate;
- **`invalidated`:** no candidates, and at least one removed by an
  invalidation;
- **`conflicting`:** more than one candidate.

Two cases leave **no candidates without any invalidation**, and fall outside
all three:
1. **A supersession cycle.** If A's `supersedes` names B and B's names A, each
   removes the other.
2. **Only unverifiable verdicts.** If every verdict in a group cites a
   measurement absent from the log, none is a candidate. Each is reported as
   `verdict.unknown_measurement`, but the group itself has no status.

**We'd ask:**
- **Report a supersession cycle as a finding** (for example
  `verdict.supersedes_cycle`), addressed to the verdicts in it.
- **Give a group with no candidates and no invalidation a defined outcome:**
  either a fourth status (for example `unresolved`) or no group at all, plus
  the findings that explain why. The second is enough for us, provided it's
  written down.
- **State the superseded-then-invalidated case.** If B supersedes A, and B is
  later invalidated, does A come back, or is the group `invalidated`? Either
  is defensible. The safe reading for us is `invalidated`, with no current
  verdict: a re-score that replaced A was itself found flawed, and A was
  already judged worth replacing. Whichever you choose, please put it in a
  scenario.

## Your Questions to Patchrig, From Our Side
Patchrig decides both. Here's how each lands for LogicalAssembly:
- **Matching a scope commit against either commit.** It over-invalidates
  rather than under-invalidates. For us that means a weight projector stays
  off more often than strictly needed, which is the safe direction. A
  separate `scorerVersions` list later would add precision without changing
  that default.
- **A re-run attempt in the same group.** A conflict blocks us from acting
  until someone supersedes, which is also safe. Patchrig said two attempts
  are different evidence, so whether a re-run should replace the earlier
  verdict, or sit beside it, is theirs to state.

## Your Decisions Without Us: Fine
- **`instrument` is descriptive only.** Agreed. Narrowing by instrument can
  wait until measurements list their instruments.
- **Every present scope list must match.** Agreed.
- **An invalidation with an empty scope matches by citation only, and is
  reported.** Agreed.
- **A cited verdict outside the scope is still removed, and reported.**
  Agreed.
- **`detail` on any verdict.** Agreed. Our contract had it beside the reason
  only, and now allows it on any verdict.
- **Stream kinds aren't checked by the projection.** Agreed. Rastro enforces
  them.
- **`policyEvent` as a `LedgerEventRef`,** matching `decision.made.policy`.
  Agreed. Our contract showed a string, and now shows an event reference.

## Two Small Points
1. **Two fields named `scope` mean different things.** On `evidence.recorded`
   it's a label ("Gemma 3 1B, N=10"). On `verdict.invalidated` it's a matching
   condition (commits, pins, versions). The projection never confuses them,
   but a reader will. Renaming the measurement's field, for example
   `claimScope`, would help. That's patchrig's vocabulary, so it's only a
   suggestion for them.
2. **Patchrig-specific fields in the core.** We agree with your risk note:
   `patchrigCommit` and `larqlVersion` are right for the first witness, and a
   second measuring witness should bring a version 2 with a generic pin map.

## On Our Side
- **The contract is aligned.** The evidence section of
  `lasm-paseo-assembly-source-of-truth.md` (project `nuveris`) now:
  - omits `supersedes` on a first score;
  - shows `policyEvent` as an event reference;
  - allows `detail` on any verdict;
  - carries `patchrigCommit` and `larqlVersion` on measurements, pending
    patchrig's names.
- **We'll pin `v0.5.0`** when we start projecting verdicts, and gate on
  findings as described.
