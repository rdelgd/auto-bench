# Note: Two Fields an Invalidation Needs, and Three Questions

For in-vitro-patching (patchrig) and LogicalAssembly developers and their
agents. This follows `in-vitro-patching-step-1-fruitfly-compose-check.md`
(project `in-vitro-patching`), which cleared auto-bench to start the verdict
schemas.

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-note-on-invalidation-scope-fields.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **We've drafted the change:** `add-evidence-and-verdict-events`, in
   project `auto-bench`. It covers the four event types, the four verdict
   values, the five reason codes, and the verdict projection.
2. **One gap:** an invalidation's scope can't be matched against verdicts
   yet. Measurements don't record the patchrig commit or the larql version.
   We propose adding `patchrigCommit` and `larqlVersion` to
   `evidence.recorded`.
3. **Three questions,** on which commit a scope means, how re-run attempts
   relate, and `null`.
4. **Thanks for step 1.** An untargeted insert failing every far-field
   prompt is exactly what the interference check is for. Thanks too for the
   correction on "Pose 56.91%".

Read the draft with:

```bash
reffy remote cat .reffy/reffyspec/changes/add-evidence-and-verdict-events/design.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## 1. The Gap
An invalidation states its flaw as a condition:

```json
"scope": { "patchrigCommits": ["…"], "vindexPins": ["…"], "larqlVersions": ["…"] }
```

The condition applies to every verdict it matches, including verdicts written
after the flaw was found. To match, the projection follows a verdict's
`cites` to its measurement, and compares the measurement's pins with the
scope. The agreed `evidence.recorded` carries `vindexPin`, but neither of the
other two:

| Scope list | Measurement field | Today |
| --- | --- | --- |
| `vindexPins` | `vindexPin` | present |
| `patchrigCommits` | none | **missing** |
| `larqlVersions` | none | **missing** |

So an invalidation naming a larql version or a patchrig commit could only
reach the verdicts it explicitly cites, and never the later ones. That's the
case the condition exists for.

**What we propose:** two required fields on `evidence.recorded`:
- **`patchrigCommit`:** the patchrig commit that ran the cell;
- **`larqlVersion`:** the larql version used, for example `0.2.0`.

Your run directory probably records both already. Please confirm the names,
or send yours, and tell us if either isn't recorded today.

## 2. Three Questions

**Q1. Which commit does `patchrigCommits` mean?**
A flaw can be in the code that measured, or in the code that scored. A verdict
carries `scorerVersion`, its scoring commit, and the measurement would carry
`patchrigCommit`. Our draft matches a scope commit against **either**, so an
ambiguous invalidation reaches too many verdicts rather than too few. If you'd
rather separate them, for example `scorerVersions` beside `patchrigCommits`,
now is the time.

**Q2. Is a re-run attempt the same verdict group?**
The projection folds per (cell, pre-registration), as agreed. A re-run is a
new attempt with its own measurement stream. If attempt 2's verdict shares
attempt 1's `cellId`, it's in the same group, so it must name attempt 1's
verdict in `supersedes`. Otherwise the two conflict, and the projection
reports a finding. Is that what you intend? Or does `cellId` differ per
attempt, so they never meet?

**Q3. `supersedes` is omitted, not `null`.**
The contract's example says "or null". `lasm-core` omits absent optional
fields, and the schema rejects `null`. A first score just leaves `supersedes`
out. This is a convention, not a question, but your event builder should know
before the first cell.

## 3. What We Decided Without You
These are in the draft. Tell us if any of them is wrong for the rig:
- **`instrument` is descriptive.** It doesn't narrow the match, because
  measurements don't record which instruments they used. Narrowing by
  instrument would need measurements to list their instruments, which we'd
  leave for a later version.
- **Every present scope list must match.** For example, larql `0.2.0` *and*
  vindex pin `X` matches only measurements with both.
- **An invalidation with no scope lists matches only the verdicts it cites,**
  and is reported. An empty condition never matches everything.
- **A cited verdict outside the scope is still removed,** and is reported, so
  the inconsistency is visible.
- **`detail` is allowed on any verdict,** not only `cannot-tell`.
- **Stream kinds aren't checked by the projection.** Rastro's authorization
  already enforces them, and checking prefixes would mean parsing stream ids.

## 4. Next
- **Patchrig:** answer section 1 and Q1–Q2. Implementation starts once the
  field names are settled. Nothing in your step 2 to 4 order needs to change.
- **LogicalAssembly:** review the draft, as you did the governance events.
  You'll pin `v0.5.0` when you start projecting verdicts.
