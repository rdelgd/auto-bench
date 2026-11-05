# Reply: Agreed to All Five Adjustments

For auto-bench (`lasm-core`) developers and their agents, copied to
LogicalAssembly and Rastro. This answers
`lasm-core-reply-on-findings-event-data.md` (project `auto-bench`).

Date: 2026-11-04. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-reply-agreeing-to-findings-adjustments.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Summary
1. **Agreed to all five adjustments.** Please go ahead with
   `add-findings-evidence-v2`.
2. **One clarification on `served`,** which we'll define on our side.

## The Five
1. **Full commit hashes.** Agreed, and the short hash was our slip against
   the October agreement. The two-step finding's commit is
   `ec8e708727c6760577e8ae1cceed0adce450528a`. Our event builder will write
   the full hash in `patchrigCommit` and, unprefixed, in `scorerVersion`.
2. **`cites` as an event reference** (`streamId`, `streamVersion`), with the
   run id in the verdict's own `runId`. Agreed.
3. **`predicted` as a list of verdict values.** Agreed. The four verdicts
   carry `["holds"]`, `["holds"]`, `["inconclusive", "fails"]` and
   `["fails"]`.
4. **The scorer's numbers in `statistics`,** with `claim`, `claimId` and
   `tunedThreshold` staying named. Agreed.
5. **Adapter scopes by equality,** one entry per served date. Agreed.

We'll also write `preregistration` from the single constant our scorer uses,
so the em dash is identical on every verdict.

## A Clarification: `served`
Our draft used `served`, but patchrig doesn't record it yet: today's adapter
identity holds kind, model and host. We'll define it in `observer/1`, a
ReffySpec change now in progress (`define-observer-contract-version-1`):
- **`served` is the UTC date the run started,** written `YYYY-MM-DD`.
- **A run that crosses midnight carries one date,** its start, so every event
  from one run matches the same scope entry.
- **For the two-step finding,** both runs started on 2026-11-04 UTC, so
  `served` is `2026-11-04` for both, as drafted.

## Next
- **auto-bench:** implement and release `v0.6.0`.
- **patchrig:** finish `observer/1`, write the event builder against the
  version 2 schemas, generate the `patchrig-witness` token, and send Rastro
  only its hash before the first append.
