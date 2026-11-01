# Note: Rename the Measurement's `scope` Before 0.5.0 Is Tagged?

For in-vitro-patching (patchrig) developers and their agents, copied to
LogicalAssembly. One question, before `lasm-core` 0.5.0 is released.

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-note-on-measurement-scope-rename.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Where Things Stand
`add-evidence-and-verdict-events` is implemented, with your answers folded in:
- **Measurements:** require `patchrigCommit`, `larqlVersion`, and
  `larqlBinarySha256`.
- **Invalidations:** their scope has four lists: `patchrigCommits`,
  `scorerVersions`, `vindexPins`, and `larqlVersions`.
- **The projection:** folds per (`cellId`, `attempt`, `preregistration`).

All tests pass. We're holding the `v0.5.0` tag for one answer from you.

## The Question
Two fields named `scope` mean different things:
- **On `evidence.recorded`:** a label, for example `"Gemma 3 1B, N=10"`.
- **On `verdict.invalidated`:** a matching condition (commits, pins,
  versions).

LogicalAssembly suggested in `lasm-review-evidence-and-verdict-events.md`
that the measurement's field be renamed, for example to `claimScope`. It's
your vocabulary, so it's your call.

**Why now:** before the tag, a rename is a one-line change. After the tag,
it's a version 2 of `evidence.recorded`, and every reader then has to handle
both versions.

**Please reply with one of these:**
- **a new name,** `claimScope` or your own; or
- **keep `scope`.** That works too. The two fields sit on different event
  types, so the projection never confuses them.

We tag `v0.5.0` as soon as you answer.
