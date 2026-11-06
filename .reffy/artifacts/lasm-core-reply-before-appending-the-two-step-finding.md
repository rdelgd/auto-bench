# Reply: Yes to All Three. Go Ahead and Append

For in-vitro-patching (patchrig) developers and their agents, copied to
LogicalAssembly and Rastro. This answers
`in-vitro-patching-note-before-appending-the-two-step-finding.md` (project
`in-vitro-patching`).

Date: 2026-11-05. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-before-appending-the-two-step-finding.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **Yes to all three points.** Append when you're ready, evidence first.
2. **Two small suggestions,** neither blocking.
3. **Nothing changes in `lasm-core`.** 0.6.0 accepts the six events as you
   describe them.

## The Three Points

### 1. `["inconclusive", "fails"]` for Jev's combined cell: yes
`predicted` means what was written before the run, so the pre-registration
is its only source. A prediction narrowed afterwards, even correctly, isn't a
prediction. Taking it from the pre-registration rather than from the tidier
table is the discipline that made this a finding.

Our archived design records `["fails"]` from your earlier note. That stays as
history; the events are what count.

### 2. No `route` on Jev's adapter: yes
`route` is optional so that a value nobody recorded can be left out instead
of guessed. A guessed route would be worse than a missing one: an adapter
invalidation naming a route would then match or miss for a false reason.

### 3. Full precision: yes
`lasm-core` never interprets `measurements` or `statistics`. The only numeric
limits are finite numbers, and integer-valued numbers within the safe range;
values like `0.24270833333333336` pass both. Numbers that recompute exactly
from the records are better evidence than rounded ones.

## The Builder's Other Choices
All fit what was agreed:
- deterministic event ids, so a re-send is a replay;
- the bare 40-character `scorerVersion`;
- `tier: hosted`, and the `fixture` object;
- stream names that nothing parses.

## Two Small Suggestions

### Put the attempt in the judgement stream id now
You'd add it when a second attempt happens. Adding it from the first event,
for example `judgement:<claim id>@<attempt>@2026-11-03@<commit>`, keeps one
naming scheme across all your judgement streams. A collision would be caught
either way, since Rastro rejects a second write to a stream, so this is
about tidiness, not safety. If the first six go out as they are, that's
fine.

### Keep one rule for `served`
"The date the confirmation check started" is a sound reading of "the UTC date
the run started", since the confirmation is when the model answered.
Receipts share `AdapterIdentity` with findings. When they come, they should
use the same rule, so an adapter scope entry with a `served` date means the
same thing for both.

## Next
- **Patchrig:** append the two `evidence.recorded` events, then the four
  `verdict.recorded` events.
- **LogicalAssembly:** projecting the local Rastro's log through
  `project_verdicts` (0.6.0) should give four `current` runs with no findings.
  If it doesn't, tell us what it gives.
