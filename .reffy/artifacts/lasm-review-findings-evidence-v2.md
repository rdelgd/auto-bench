# Review: `add-findings-evidence-v2` (`lasm-core` 0.6.0)

For auto-bench (`lasm-core`) developers and their agents, copied to
in-vitro-patching (patchrig) and rastro. This is LogicalAssembly's review of
`add-findings-evidence-v2` (project `auto-bench`), requested in
`lasm-core-note-on-0.6.0-ready-for-review.md`.

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-review-findings-evidence-v2.md \
  --workspace-id nuveris-v1 --project-id nuveris
```

## Summary
1. **Accepted. Please tag `v0.6.0`.** Nothing in this review blocks it.
2. **One optional suggestion:** if your schema checker supports `minLength` and
   `maxLength`, use them to catch short commit hashes and misspelled `served`
   dates.
3. **Our evidence contract is updated** with a version 2 section, and our gate
   extends to `runs`.

## What's Right
- **`runs` beside `cells`.** Version 1 and version 2 groups have different
  identities and never meet, and our 0.5.0-era types keep checking.
- **Grouping per (run, attempt, claim, pre-registration).** One run with
  several claims now projects as one group per claim. That's the problem we
  missed in our last note, and you caught it. The two-step finding projects as
  four `current` groups with no findings.
- **Version-aware scope lists.** A list matches only measurements that carry
  its field:
  - a larql invalidation can't reach a hosted finding;
  - an adapter invalidation can't reach a LARQL cell;
  - commit and scorer lists reach both.

  An invalidation naming one model through one gateway leaves the same model
  through another gateway untouched. That's the two-adapters decision working
  as intended.
- **Equality, not date ranges, for `served`.** It keeps the projection free of
  date ordering. The reasoning holds: an invalidation is written after the fact,
  when the affected dates are known.
- **Citations across versions are reported, not followed**
  (`verdict.measurement_version_mismatch`).
- **`predicted` as a list of verdict values.** A reader can compare prediction
  and outcome without parsing text, and writing the prediction down first is
  what made the two-step result a finding.
- **Free-form objects by design,** with the remedy stated: name a key in a
  later version once a reader depends on it.
- **Full commit hashes.** Spotting that the draft's 12-character hashes would
  make exact-match invalidations silently miss was a good catch.

## One Optional Suggestion: Length Instead of Pattern
You note that the checker has no `pattern` support, so 40-character hashes
are a writer-side rule. Two of your listed risks are about strings of an exact
length:
- **a short hash** in `patchrigCommit` or `scorerVersion` (40 characters);
- **a misspelled `served`,** such as `2026-11-4` (10 characters).

If the checker supports `minLength` and `maxLength`, setting both to 40 for
the commits and to 10 for `served` would turn the two likeliest mistakes into
rejected events, rather than invalidations that silently miss. It isn't full
validation, and `jsonschema` agrees on both keywords. If the checker doesn't
support them either, the writer-side rule is enough. It isn't worth growing
the checker for this alone.

## On Our Side
- **Our gate covers `runs`:** LogicalAssembly acts only on `current` groups
  with no finding addressed to their events, never on `conflicting`,
  `unresolved`, or `invalidated` groups, in either list.
- **Our evidence contract has a version 2 section,** in
  `lasm-paseo-assembly-source-of-truth.md` (project `nuveris`). It compares the
  two versions side by side, and covers adapter identity and `served`, claims,
  `predicted`, `statistics`, the `adapters` scope list, and cross-version
  matching.
- **One wording narrowed.** Our contract said the manipulation check is
  recorded "before any verdict counts". It now applies to measurements of an
  edit only, since a hosted-adapter run makes none, and version 2 rightly
  drops the field.
- **No pin yet.** LogicalAssembly still runs `lasm-core` 0.4.0 for governance.
  We'll move to 0.6.0 when we start projecting verdicts. The release keeps the
  governance API unchanged, so that move won't touch it.
