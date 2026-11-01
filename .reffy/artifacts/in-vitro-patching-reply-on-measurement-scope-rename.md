# Reply: Rename the Measurement's `scope` to `claimScope`

For auto-bench (`lasm-core`) developers and their agents, copied to
LogicalAssembly. This answers `lasm-core-note-on-measurement-scope-rename.md`
(project `auto-bench`, workspace `nuveris-v1`).

Date: 2026-11-01. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/in-vitro-patching-reply-on-measurement-scope-rename.md \
  --workspace-id nuveris-v1 --project-id in-vitro-patching
```

## Answer
**Rename it to `claimScope`,** on `evidence.recorded`, before `v0.5.0` is
tagged. The invalidation's `scope` keeps its name.

## Why
- **One word, one meaning.** It's the rule we just applied to verdicts,
  where `holds_weakly` had come to mean three things. The projection never
  confuses the two fields, but people reading events, schemas and these notes
  do, and "scope" is now a matching condition in one place and a description
  in the other.
- **The name says what the field is.** It comes from our `FINDINGS.md` rule
  that every finding states its tier and "its **scope and limits**" before its
  number: what the measurement can be claimed to be about, and no further.
  `claimScope` says that. A bare `scope` doesn't.
- **Now it costs one line; after the tag, a version 2.**

## What goes in it
A short human-readable statement of what the measurement covers, for
example:

```text
Tier 1, Gemma 3 1B (fruitfly), larql MODE COMPOSE, N=10, toy scale
```

It's descriptive, like `instrument` and `detail`: projections report it and
never parse it. Anything a reader must *match* on already has its own field
(`vindexPin`, `patchrigCommit`, `larqlVersion`, and so on).

## On our side
Our earlier notes list the measurement's field as `scope`, for example the
data table in `in-vitro-patching-reply-to-lasm-core-on-event-shape.md`. Read
those as `claimScope`. Our event builder isn't written yet, so it will use
`claimScope` from the start.

Go ahead and tag `v0.5.0`.
