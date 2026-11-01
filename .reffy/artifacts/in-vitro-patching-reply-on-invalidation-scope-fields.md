# Reply: Invalidation Scope Fields, and Three Answers

For auto-bench (`lasm-core`) and LogicalAssembly developers and their agents.
This answers `lasm-core-note-on-invalidation-scope-fields.md` (project
`auto-bench`, workspace `nuveris-v1`), for the draft change
`add-evidence-and-verdict-events`.

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-reply-on-invalidation-scope-fields.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **Yes to `patchrigCommit` and `larqlVersion`** on `evidence.recorded`,
   plus one descriptive field, `larqlBinarySha256`. Patchrig doesn't record
   any of them today; we'll add them with the cell tooling.
2. **Q1: separate the two commits.** Matching a scope commit against "either"
   would invalidate *corrected* verdicts. Use `patchrigCommits` for the
   measuring commit and a new `scorerVersions` for the scoring commit.
3. **Q2: attempts are separate groups.** Fold per (`cellId`, `attempt`,
   `preregistration`). A re-run is a replication, not a revision.
4. **Q3: omit, not `null`. Agreed.**
5. **All six of your decisions in section 3 are right for the rig.**

## Changes for `add-evidence-and-verdict-events`

| Where | Change |
|---|---|
| `evidence.recorded` | add required `patchrigCommit` (string, full git commit hash) |
| `evidence.recorded` | add required `larqlVersion` (string, for example `0.2.0`) |
| `evidence.recorded` | add required `larqlBinarySha256` (string). Descriptive, not a scope list (see below) |
| `verdict.invalidated` `scope` | add optional `scorerVersions` (list of strings) |
| `verdict.invalidated` `scope` | `patchrigCommits` matches only the measurement's `patchrigCommit`, not `scorerVersion` |
| verdict projection | group key is (`cellId`, `attempt`, `preregistration`), not (`cellId`, `preregistration`) |
| event data | `cellId` excludes the attempt; `attempt` is its own field. Stream names still include both |

Each is argued below.

## 1. The two scope fields, and a third
**Confirmed:** `patchrigCommit` and `larqlVersion`, required on
`evidence.recorded`.

**Neither is recorded today.** Patchrig's run-directory manifest has `seed`,
`engine`, `corpus`, `protocol`, `thresholds` and `files`. There's no git
commit at all, and the larql version would only sit inside the free-form
`engine` object, which isn't built yet. We'll add both with the cell tooling,
before any cell is sent. Nothing in our step 2 to 4 order changes.

**A clean tree, or no cell.** A commit hash identifies the code only if the
working tree was clean. Patchrig will refuse to produce a reportable cell from
uncommitted changes, so `patchrigCommit` always means exactly the code that
ran. Your schema needs nothing extra for this; we're telling you so you can
rely on it.

**Add `larqlBinarySha256` as well, as a descriptive field.** One version
number can mean different builds. LogicalAssembly's Graviton build of larql
0.2.0 needed `-C target-feature=+dotprod`, while the release binaries didn't.
A flaw in one build can then be traced later. We aren't asking for a
`larqlBinaries` scope list yet. Measurements carrying the digest from the
first cell is what keeps that option open without a backfill.

## 2. Q1: separate the measuring commit from the scoring commit
Matching a scope commit against either one doesn't err in the safe
direction. Here's the failure:
1. The scorer at commit `X` has a bug. Verdicts scored at `X` are wrong.
2. We fix it at commit `Y`, and re-score the old measurements. The new
   verdicts carry `scorerVersion: Y` and `supersedes` the old ones. Their
   measurements still carry `patchrigCommit: X`, because that's when they
   were taken, and the measuring code was fine.
3. An invalidation naming `X` under "either" matches those measurements, and
   wipes out the corrected verdicts too.

So the scope needs two lists, each matching one field:

| Scope list | Matches | Use it when |
|---|---|---|
| `patchrigCommits` | the measurement's `patchrigCommit` | the code that *measured* was wrong |
| `scorerVersions` | the verdict's `scorerVersion` | the code that *scored* was wrong |

Your rule that every present list must match still applies. An invalidation
that really does cover both names both.

## 3. Q2: a re-run attempt is not the same verdict group
Two attempts are two independent measurements of one cell: a replication,
not a revision. If they shared a group, attempt 2 would have to claim
`supersedes` over attempt 1, which would be false, or the projection would
report a conflict that isn't one.

So:
- **In event data,** `cellId` names the cell without the attempt, and
  `attempt` is its own field, as in our event-shape reply.
- **The fold runs per (`cellId`, `attempt`, `preregistration`).**
  `supersedes` only ever links re-scores of the same attempt.
- **Combining attempts is a separate analysis,** like pooling repetitions.
  The verdict projection shouldn't do it.

Stream names still include the attempt, as agreed, so each attempt's streams
are written once.

## 4. Q3: omit, don't send `null`
Agreed. A first verdict leaves `supersedes` out. Our verdict serialization
already omits absent fields: a given verdict writes no `cannot_tell_reason`
at all.

## 5. Your section 3 decisions
All six suit the rig:
- **`instrument` as descriptive only:** agreed. Measurements don't list their
  instruments.
- **Every present scope list must match:** agreed, and it now includes
  `scorerVersions`.
- **An empty scope matches only the verdicts it cites, and is reported:**
  agreed. An empty condition must never match everything.
- **A cited verdict outside the scope is still removed, and reported:**
  agreed.
- **`detail` on any verdict:** agreed.
- **No stream-kind checks in the projection:** agreed. Rastro's
  authorization already enforces them.

## Our side
With the cell tooling (our step 4), patchrig will record
`patchrigCommit` (refusing a dirty tree), `larqlVersion` and
`larqlBinarySha256` in every run directory, and the event builder will emit
them. Steps 1 to 3 (the multi-token scoring fix, fruitfly's controls, and the
knob exploration) are unaffected.
