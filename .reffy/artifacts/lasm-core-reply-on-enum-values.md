# Reply: Enum Values Are Kebab-Case, and "Cannot Tell" Needs Its Own Value

For in-vitro-patching (patchrig), LogicalAssembly, and Rastro developers and
their agents. This answers `in-vitro-patching-reply-to-lasm-core-on-event-shape.md`
(project `in-vitro-patching`).

Date: 2026-10-31. Read it from any `nuveris-v1` project with:

```bash
reffy remote cat .reffy/artifacts/lasm-core-reply-on-enum-values.md \
  --workspace-id nuveris-v1 --project-id auto-bench
```

## Summary
1. **camelCase is for keys only.** Enum values in `lasm-core` are lowercase
   kebab-case: `holds-weakly`, `single-hop`.
2. **We suggest a separate `inconclusive` verdict.** "Cannot tell" and "holds
   weakly" mean different things to anything that acts on a verdict.
3. **Your identifying fields in `data` look right,** and so does keeping
   local records in snake_case and mapping at export.
4. **No date needed.** We'll start the verdict-projection change when your
   step 1 artifact arrives.

## 1. Enum Values
`lasm-core` already has a convention for values: lowercase words joined by
hyphens. Examples in the package today include `unknown-action`, `no-rule`,
`control-surface`, `reality-model-validity`, and `read-only`. So your values
map like this:

| Today | In event data |
| --- | --- |
| `holds`, `fails` | unchanged |
| `holds_weakly` | `holds-weakly` |
| `canonical`, `paraphrase`, `native` | unchanged |
| `single_hop` | `single-hop` |
| `composite_canonical`, `composite_paraphrase` | `composite-canonical`, `composite-paraphrase` |
| `in_context` | `in-context` |
| `planted_into_native` | `planted-into-native` |

Event type names are a separate case. They stay a dotted noun and verb
(`verdict.recorded`, `invalidation.retracted`). Like the key mapping, the
value mapping happens when events are built from a verified run directory.
`records.jsonl` and `metrics.json` don't change.

## 2. "Cannot Tell" Should Not Be `holds-weakly`
Today a degenerate stratum or a failed instrument gate is reported as
`holds_weakly`. That covers two different situations:
- **`holds-weakly`:** the instrument worked, and the evidence that the patch
  holds is weak.
- **Cannot tell:** the instrument didn't produce usable evidence, so there's
  no evidence either way.

Anything that acts on verdicts reads `holds-weakly` as a weak pass. Examples
are the verdict projection, a policy that gates a weight patch on its
verdicts, and a `policy.contested` automation that counts failures. A failed
gate would then count toward a patch being trusted. It also hides the case
that most needs attention: an instrument that isn't working.

We suggest four verdict values:

| Value | Meaning |
| --- | --- |
| `holds` | the instrument worked; the evidence meets the pre-registered margins |
| `holds-weakly` | the instrument worked; the evidence is in the direction claimed but short of the margins |
| `fails` | the instrument worked; the evidence contradicts the claim |
| `inconclusive` | the instrument did not produce usable evidence: a degenerate stratum, a failed instrument gate, or similar |

An `inconclusive` verdict could carry an optional `inconclusiveReason`, for
example `degenerate-stratum` or `instrument-gate-failed`. Then the projection
can report why without parsing free text.

This only changes the exported event. Your scorer can keep its three values
internally, as long as the run directory records *why* a cell came out
`holds_weakly`, so the export can tell the two cases apart. If it doesn't
record that today, that's the one place this touches your records.

The design document's earlier verdict sketch had a separate value for this
(`conforms | diverges | inconclusive`), so this restores a distinction rather
than adding one. If you see a reason the two cases should stay merged, tell
us before the schemas are written.

## 3. Identifying Fields and Local Records
We agree with both:
- **Everything a stream name encodes also goes in `data`.** That follows
  directly from never parsing stream names. Your table of identifying fields
  per event type is what the schemas will require.
- **Local records stay snake_case,** and the mapping happens at export. Event
  data is a view built for the ledger. Your records stay the source of truth
  for recomputing metrics.

## 4. Timing
Understood: there's no date for your first verified cell. We'll open the
`lasm-core` change for `evidence.recorded`, `verdict.recorded`,
`verdict.invalidated`, and `invalidation.retracted` when your step 1 artifact
arrives. If your answer on `inconclusive` comes before then, the change will
include it from the start.
