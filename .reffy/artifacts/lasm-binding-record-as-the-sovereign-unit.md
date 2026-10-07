# The Binding Record Is the Sovereign Unit

Status: exploratory
Date: 2026-10-06
Authors: Roberto Delgado, Claude

## Prompt

Review `lasm-reality-workbench-on-databricks.md` (2026-09-17) and `lasm-as-sovereign-mapping-plugin.md` (2026-09-30) together. Where do they agree, where does the later one quietly narrow the earlier one, and what do both leave undefined? Then propose the smallest thing Lasm must own for the sovereignty claim to be more than a slogan.

## Source Snapshot

Read on 2026-10-06:

- `lasm-reality-workbench-on-databricks.md`: a full lifecycle workbench for Lasm on Databricks, with eight candidate surfaces, a health model, a four-stage improvement job, and a reference architecture across Apps, Unity Catalog, Lakeflow, Lakebase, and JSM.
- `lasm-as-sovereign-mapping-plugin.md`: Lasm as the business-to-digital mapping contract, delivered to agents as a thin Agent Plugin, with native adapters executing it and Auto Bench testing the chain.
- `src/lasm_core/` as of commit `a78e312`: `LogicalAssemblySlice` with `ProvenanceSource`, six entry kinds, `LasmProjectionReferences`, `OperationalState`, `Scenario.reality` as a `RealityReferenceSet`, `ConformanceCase`, and `DivergenceSource` attribution in `evaluate.py`.
- Background: `naming-the-agentic-control-layer.md` (adopted thesis) and `servco-ontology-ledger-3.md` (Genie ontology, OntoRank, Pages).

## What the Two Artifacts Agree On

Reading them side by side, five commitments are stable across both and should be treated as settled for planning purposes:

1. **No shadow registry.** Metric Views, Pages, Domains, and Genie configuration remain authoritative for what they natively hold. Lasm references them; it does not recompute them.
2. **Native-first correction (jidoka).** A defect is fixed in its owning layer. Lasm records the binding and the conformance case so the correction stays intelligible outside that layer.
3. **Candidate is not truth.** Nothing an optimizer, OntoRank, or an LLM produces becomes business meaning without an accountable human accepting it. The workbench artifact's lexicographic acceptance order expresses this precisely.
4. **Two kinds of evaluation.** Native benchmarks judge configuration quality. Auto Bench judges whether represented business intent survived projection, action, transition, and outcome. They are not one score.
5. **Human authority is part of the type.** Owner, dispute status, and effective period are content, not deployment metadata.

## Where the Later Artifact Narrows the Earlier One

The plugin artifact does not say it supersedes the workbench artifact, but it does. Three shifts matter:

- **The Workbench moves from product to condition.** September 17 designs eight surfaces and a Databricks architecture. September 30 says a Workbench is justified "only where native views cannot show the cross-platform mapping, disputes, binding drift, and evidence chain." That is the right correction. Read today, the workbench artifact is best used as a catalogue of *questions a steward will ask*, not as a product spec.
- **The center of gravity moves from lifecycle to contract.** The earlier artifact's defining loop is observe, detect, route, replay, release, monitor. The later artifact's defining object is the mapping itself. The loop still matters, but it is now something adapters run over the contract rather than the thing Lasm is.
- **The core shrinks.** The scope table in the plugin artifact pushes permissions engines, approval queues, trace stores, and benchmark runners out to adapters. The earlier artifact treated several of those as Workbench responsibilities that would need durable records of their own.

One mechanical note: the workbench artifact still refers to `@lasm/core`. The core migrated to Python as `lasm_core` on 2026-09-30 (commit `e7e1b88`). Any planning that cites that artifact should read `lasm_core`.

## What Neither Artifact Defines

Both artifacts call for the **binding** to be a first-class object. The plugin artifact says so directly: "which Lasm entry is realized by which digital object or event, in which environment, under which version, with what confidence and evidence?" The workbench artifact lists "projection identity, version, target, and release status" among candidate durable records and builds a Projection Matrix on top of it.

Neither defines it, and `lasm_core` has nothing for it. Today the package has two arrows:

| Arrow | Type | Direction |
| --- | --- | --- |
| Why we believe an entry | `ProvenanceSource` via `sourceIds` | Source → entry (inward) |
| Which entries a surface projects | `LasmProjectionReferences` on harness, skill, and MCP descriptors | Surface → entry (outward, declared by the surface) |

There is no arrow from an entry to the governed digital object that *implements* it: the Metric View, the table, the workflow, the policy object, the event type. Without that arrow:

- "Resolve a term in context," the plugin's first operation, can return a description but not an authoritative implementation.
- Binding drift, which both artifacts want to monitor, has no record to drift from.
- Auto Bench attribution can say `reality-model` or `projection`, but it cannot say *which native object* carried the wrong meaning.
- Export is a vocabulary export. Importing it on another platform preserves names and loses every claim about what realized them.

The provenance arrow is also incomplete for the platform era. `ProvenanceStatus` is `current | stale | disputed`. Once OntoRank-style inference and optimizer runs produce candidate mappings, the model needs at least `candidate` and `retired` to keep "proposed by a system" distinct from "accepted by a person" and from "no longer in force." Both artifacts insist on that distinction in prose; the type does not carry it.

## The Claim

> The binding record is the sovereign unit. Sovereignty is the ability to export every binding with its provenance, authority, and conformance evidence, and have the claims remain true on a different runtime.

Everything else in the two artifacts is either a reason to believe an entry (provenance), a consumer of an entry (projection), or a view over bindings and evidence (the Workbench). The chain Auto Bench tests is:

```
sources ──provenance──▶ entry ──binding──▶ native implementation ──projection──▶ agent surface ──conduct──▶ transition ──▶ outcome
```

`DivergenceSource` already names most links in that chain. The binding is the link it cannot currently point at.

## A Candidate Shape

This is exploratory, not a schema proposal. The intent is to test whether a small record can carry what both artifacts ask of it.

```
BindingEntry
  id
  entryId                      # a LogicalAssemblyEntry id
  target
    platform                   # databricks | jsm | claude | chatgpt | ...
    kind                       # metric-view | table | page | workflow | policy | event-type | skill-file | mcp-endpoint
    locator                    # catalog.schema.metric_view, URL, path
    version | digest           # what was actually inspected
  environment                  # dev | staging | prod, or a named workspace
  fidelity                     # exact | partial | lossy, with a note
  status                       # candidate | accepted | disputed | retired
  assertedBy, acceptedBy       # people or roles, not connector display names
  effectiveFrom, effectiveTo
  evidenceRefs                 # conformance runs, scan snapshots, review decisions
```

Observations that fall out of the shape:

- One entry may have many bindings, across environments and across platforms. The plugin artifact's "portability without identical executability" is exactly one entry with different bindings per platform.
- `fidelity` is where projection loss becomes a recorded fact rather than a steward's memory. The workbench artifact's guardrail classification (migrate upstream, retire workaround, keep as consumer-specific, keep as regression case) is a decision about a `partial` or `lossy` binding.
- `digest` is what makes "the evaluated, approved, released, and used values were identical" checkable. For a Metric View that is the DDL hash. For a Page it may be unavailable, which is itself a finding.
- `status: candidate` is how an OntoRank snippet or an optimizer patch enters the model without being promoted to meaning.

## A Scope Test for the Core

The plugin artifact's keep/adapter table is useful but is organized by example. A rule would let future primitives be sorted without a new table. Three questions, two yeses to stay in the portable contract:

1. **Would it survive a platform migration unchanged?** A business concept would. A Lakeflow job ID would not.
2. **Does a named person have to be accountable for it?** An owner, a dispute, an acceptance. Not a cache or a sync timestamp.
3. **Does Auto Bench need it to attribute a divergence?** If a finding cannot say where meaning was lost without this record, it is core.

The binding passes all three. `RuntimeEvaluationDescriptor` passes 1 and 3. A connector health snapshot passes none and belongs in an adapter. A `ProvenanceSource` passes 1 and 2.

## The Workbench, Re-read as Views

Every surface in the September 17 artifact becomes a query once bindings exist:

| Workbench surface | Underlying query |
| --- | --- |
| Portfolio | Bindings grouped by domain and environment, with status and latest evidence |
| Assembly Explorer | One assembly's entries joined to provenance and bindings |
| Reality and Source Drift | Provenance whose observed version differs from the version cited at acceptance |
| Projection Matrix | Bindings crossed with surface descriptors' `LasmProjectionReferences` |
| Conformance Runs | Evidence refs attached to bindings, grouped by run |
| Episode Audit | The chain above, walked for one scenario |
| Change Studio | Binding and entry status transitions awaiting an accountable decision |
| Ask the Lasm | Natural-language front end to the same queries, with identity disclosed |

This is the practical meaning of "Workbench as condition." If Genie One, Unity Catalog, and JSM can answer a query natively, no surface is needed. If they cannot, the surface is a thin read model, not a system of record. The expensive architecture in the earlier artifact can be deferred indefinitely. The binding record cannot.

## The Plugin, Re-read as Binding Operations

The five thin plugin operations map directly:

| Plugin operation | What it reads |
| --- | --- |
| Resolve a term in context | Entry plus its `accepted` binding for the caller's platform and environment |
| Inspect a binding and provenance | One `BindingEntry` and the `ProvenanceSource` list behind its entry |
| Check an intended action | `PolicyEntry` authority roles plus the binding's environment and status |
| Record or retrieve evidence | `evidenceRefs` |
| Identify ambiguity for a human | Any entry with a `disputed` or only-`candidate` binding in scope |

A plugin with read-only access can do the first two and the last. That answers the plugin artifact's fourth open question in the affirmative: useful inspection precedes any action gating.

## The Probe, Made Concrete

The plugin artifact's "smallest useful probe" is right. Here is the same probe in `lasm_core` terms, so it can be written as a fixture rather than described:

1. **Entry.** A `ConceptEntry` for net new-vehicle units, with `ProvenanceSource` entries of kind `policy` (the governed definition) and `judgment` (the stock-type ruling and who made it).
2. **Binding.** One `BindingEntry` with `status: accepted`, target kind `metric-view`, the DDL digest, environment `prod`, and a named accepter.
3. **Projection.** A `SkillDescriptor` whose `LasmProjectionReferences` cite the entry.
4. **Case.** A `ConformanceCase` whose scenario asks a question the native Genie benchmark would score as correct, but whose answer uses the retail-only count. The `OutcomeExpectation` marks that as `prohibited`.
5. **Expected finding.** Attribution `projection` if the skill dropped the stock-type distinction, `reality-model` if the entry itself was underspecified. The finding should name the binding.
6. **Change.** Correct the Metric View natively. The digest changes. The old binding goes `retired`, a new one goes `candidate` then `accepted`. Rerun the case.
7. **Pass condition.** The case still explains the correction, and an export of entry, provenance, both bindings, and the run evidence is intelligible without Databricks access.

**Falsification condition.** If the native Genie benchmark catches the same defect, routes it to the same Metric View, and the binding adds no attribution the platform could not infer, the sovereignty claim is weaker than both artifacts assume. That outcome is worth knowing early.

## Tensions Not Already Listed

- **Binding a natural-language projection.** A skill file has a digest, but the meaning it projects does not. `fidelity` can be asserted, not computed. Who asserts it, and what evidence makes a `partial` claim contestable?
- **Cross-platform acceptance.** A binding to a Metric View is accepted by a Databricks-side owner. A binding to a Claude skill is accepted by whom? If the answer is "the same domain owner," the acceptance record must be portable too.
- **Where the type lives.** The scope test says `BindingEntry` is core. The workbench artifact's instinct would put it in a Delta table. The resolution is probably both: a core TypedDict with validation, serialized by adapters. But the core type must exist first or the adapters will each invent one.
- **Digesting things that cannot be digested.** Pages have no public API. A binding to a Page has a locator and no digest. Treating "no digest" as a scan finding rather than a modeling gap keeps the record honest.

## Open Questions

1. Should `BindingEntry` be a seventh entry kind inside `LogicalAssemblySlice`, or a sibling collection that references entries? The former versions bindings with the assembly; the latter lets bindings change without a semantic release.
2. Can `ProvenanceStatus` grow `candidate` and `retired` without breaking existing fixtures and validation codes?
3. Should `DivergenceSource` gain a `binding` value, or is a binding defect always expressible as `reality-model` or `projection` plus a binding reference on the finding?
4. What is the minimum evidence for `status: accepted`? A JSM ticket ID, a signed review record, or a named role in the entry itself?
5. Does the probe need Databricks at all for its first run, or can a fixture with a fake digest prove the attribution logic before any connector exists?

## Working Hypothesis

The two artifacts converge on a Lasm that is narrower and more valuable than a workbench: a portable, contestable mapping contract. What they have not yet named is the record that makes the mapping a mapping. The binding record is that unit. It is small enough to add to `lasm_core` now, it makes the plugin's operations concrete, it turns the Workbench into optional views, and it gives the probe a pass condition and a falsification condition. If the binding record does not earn its keep in the first probe, the sovereignty claim should be revised rather than defended.
