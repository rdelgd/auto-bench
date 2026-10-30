# Lasm Is the Collective Mind: The Sellable Control Plane

Status: exploratory
Date: 2026-10-07
Revised: 2026-10-12 (mind generalized from paseo's fifth primitive to a layer every agent stack has)
Authors: Roberto Delgado, Claude

## Prompt

The in-vitro-patching project (workspace `lasm-v1`) added **mind** as the fifth primitive of the paseo micro-agent stack: identity, world, behavior, memory, mind. Working across the projects in that workspace, a pattern has become visible: the Lasm itself is the sellable control plane, and the "collective mind" the fleet shares is the Lasm. Write that down, test it against what the other artifacts have already settled, and say what it changes.

**Revision, 2026-10-12.** Mind was first identified as paseo's fifth primitive, but it is not specific to paseo. Every agent stack already has a mind: the shared knowledge its agents act from. paseo names it as a primitive of the micro-agent; it does not write to weights. Writing a mind into owned weights is one substrate being explored in the in-vitro-patching project. The claim below is restated for any stack and any substrate.

## Source Snapshot

Read on 2026-10-07. Remote artifacts were read with `reffy remote cat` from the `lasm-v1` workspace.

- `in-vitro-patching/.reffy/artifacts/paseo-micro-agent-summary.md`: paseo's telos is the durable micro-agent (identity, world, behavior, memory) reachable over a pipe. Operating rule: new capability arrives as a capability family, not a new actor type. reffy is a peer application on the same substrate.
- `in-vitro-patching/.reffy/artifacts/mind-as-capability-notes.md` (2026-09-06): adds **mind** as the fifth primitive. "Every agent gets a mind, not just a call to a rented external brain with frozen weights, but its own collective consciousness." Graduation ladder: capabilities, skills (behavior), tools (world), knowledge (memory and mind).
- `in-vitro-patching/.reffy/artifacts/mind-primitive-preconditions.md`: three decisions recorded. A mind is **shared across a fleet**, not one per agent. Writes inside the fleet are trusted ("intracranial trust"), which moves the governing question to **ingestion provenance at the fleet edge**. Memory and mind stay separate in the machine representation.
- `in-vitro-patching/.reffy/artifacts/three-controls-unified-architecture.md`: prevention is available where the artifact is symbolic; correction is the only option where it is sub-symbolic. "You can gate what enters the fleet. You cannot gate what the weights become." Mind in the day job is "the 4,000-token system prompt of column glossaries and business definitions."
- `in-vitro-patching/.reffy/artifacts/unity-catalog-patch-pipeline.md`: "govern the patch supply chain, never ask the weights to carry governance."
- `in-vitro-patching/.reffy/artifacts/knowledge-patch-as-data-asset.md`: an asset is defined by its circulation (address, owner, reference, transfer), not by its computation.
- `in-vitro-patching/.reffy/artifacts/lasm-orientation-layer-for-nuveris.md`: the six Lasm components mapped onto what Holocron's Nuveris needs a human for before training. The LogicalAssembly supplies row identity, the supersession graph, registry invariants, retraining triggers, and abstention policy.
- Local: `naming-the-agentic-control-layer.md` (adopted thesis), `lasm-as-sovereign-mapping-plugin.md`, `lasm-binding-record-as-the-sovereign-unit.md`, and `src/lasm_core/` at `a78e312`.

## Mind Is Not a paseo Primitive

paseo made the mind visible by naming it as a primitive of the micro-agent. The in-vitro-patching project is exploring one substrate for it: compiled knowledge patches in owned weights, shared across a fleet. The thing named was already present everywhere else, under other substrates:

| Stack | Where its mind lives today |
| --- | --- |
| paseo micro-agents | named as a primitive; the substrate is open, and owned weights are under exploration in in-vitro-patching |
| in-vitro-patching rig | compiled knowledge patches in owned weights (exploratory) |
| Claude, Codex, and other harnesses | system prompts, skill files, harness context, plugin instructions |
| Databricks Genie One | Metric Views, Domains and Pages, certified definitions, inferred snippets ranked by OntoRank |
| MCP-connected agents | resource contents, tool descriptions, and prompt templates |
| Nuveris and other trained trunks | the training set and the registry rows that decide what the trunk learns |

The three-controls note already said as much without generalizing it: mind in the day job is "the 4,000-token system prompt of column glossaries and business definitions." That prompt is a mind on a context substrate. A weight patch is the same mind on a weight substrate.

This sharpens the claim rather than replacing it:

- **Mind is substrate-independent; its substrate decides the controls.** A context mind can be gated before use because it is symbolic. A weight mind can only be gated at compilation and corrected afterward. The three-controls wall runs between substrates, not between stacks.
- **`lasm_core`'s projection surfaces are the substrates of mind.** Harness context, skills, MCP surfaces, and now weight patches are each a place a mind can be written. The weight-patch surface is not a paseo or in-vitro-patching integration. It adds weights to the substrates the core can see.
- **The fleet edge becomes the ingestion edge of any substrate.** For a weight mind it is compilation. For a context mind it is publishing a skill or a prompt. For Genie One it is certification. The governing question in the preconditions note, what may enter, applies to all of them, and the Lasm's provenance and authority regime is the answer for all of them.
- **One business can have many minds and one Lasm.** A company running Genie One, Claude skills, and a weight-patched model has three minds on three substrates. Without a Lasm they drift independently. With one, they are three projections of the same accountable account, and Auto Bench can tell which one lost meaning.

## The Claim

> The Lasm is the collective mind of a business's agents, in any stack and on any substrate, stated in a form the business owns. It is the control plane. Everything else in the stack, including the weights a mind is written into, is a data plane that executes it.

Three ideas that the workspace has been treating separately turn out to be one object seen from three sides:

| Seen from | The object is called | What it does |
| --- | --- | --- |
| any agent stack (runtime) | **mind** | the knowledge its agents share, on whatever substrate the stack provides: context, governed semantics, or weights |
| auto-bench (thesis) | the **Lasm** | an organization's operational meaning, made executable across agent-facing surfaces |
| the market (product) | the **control plane** | the thing a business pays to own, revise, and carry between runtimes |

The mind notes already say the mind is collective and the preconditions note already says it is shared fleet-wide. Every other stack shares its mind the same way: one prompt, one skill set, or one semantic layer serves all of its agents. The naming artifact already says the Lasm is what makes organizational meaning load-bearing for agents. The sovereignty artifacts already say the Lasm must be exportable with its provenance, authority, and evidence intact. Put together: every stack's shared mind is a projection of the Lasm, and the business owns the Lasm, so the business owns its minds wherever they run. That is the control-plane relationship exactly.

## Why "Control Plane" Is the Right Word

A control plane decides; a data plane carries. The division matches the stack cleanly:

| Control plane (Lasm) | Data plane (executes the Lasm) |
| --- | --- |
| Concepts, relations, constraints, events, policies, evaluations | Tables, Metric Views, workflows, Genie configuration |
| Bindings from entries to native implementations | paseo actors, Claude and Codex harnesses, Genie One, MCP capability families |
| Provenance, owner, dispute status, effective period | Skill files, harness context, plugin manifests |
| Conformance expectations and evidence requirements | Weight patches, vindexes, compiled models |
| Accountable human acceptance | Platform benchmark runners, optimizers, Auto Bench execution |

Two consequences follow:

1. **The weights become a projection target.** `LasmProjectionReferences` today sit on harness, skill, and MCP descriptors. A compiled knowledge patch is the same kind of thing: a surface that claims to realize certain entries. The binding record proposed in `lasm-binding-record-as-the-sovereign-unit.md` already has a slot for it. A `BindingEntry` with target kind `weight-patch`, a patch digest, and `fidelity` asserted by the probe results is how a mind becomes inspectable from the control plane.
2. **The fleet edge the preconditions note left open is the Lasm.** That note moved governance from "who may write into the mind" to "what gets into the fleet." The three-controls note said prevention belongs where the artifact is symbolic. The Lasm is the symbolic, governed, contestable statement of what the fleet holds to be true. An entry with `status: accepted` and a named accepter is what may be asserted into a mind. A `candidate` entry may not. Ingestion provenance is not a new mechanism. It is the Lasm's existing provenance and authority regime, applied at the moment of compilation into weights.

## Why "Sellable"

The question is what a customer is buying when they buy this stack, given that every other layer is either rented or converging toward commodity:

- The runtime is paseo, and paseo's own pivot note says the runtime is substrate, not product.
- The platform is Databricks or its peer, which is internalizing the agent lifecycle around its own assets (`lasm-as-sovereign-mapping-plugin.md`).
- The model is open weights, and the three-controls note shows the mind thesis is incompatible with a closed hosted model anyway.
- The agent clients are Claude, Codex, and their successors, each of which decides what a plugin may do.

None of those is defensible. What is left is the thing none of them can infer from telemetry: the maintained, owned, contestable account of what this business means by its words, who is accountable for each meaning, which native objects implement it, and the evidence that agents preserved it. That is the Lasm. It is sellable because:

- **It is the asset, in the circulation sense.** The data-asset note defines an asset by address, owner, reference, and transfer. A Lasm has all four. A weight patch has the first three and is missing transfer, which that note names as its gap. The Lasm is the transfer story for the mind: export the assembly with bindings and evidence, recompile the patch on the other side.
- **It survives platform migration.** The scope test in the binding-record artifact (survives migration, needs an accountable person, needed for attribution) is a test for control-plane membership. Everything that passes is sellable. Everything that fails is an adapter the platform will eventually offer for free.
- **It is where the value of the mind accumulates.** The mind notes want load-bearing knowledge moved out of the harness into the weights. If stacking degrades at scale, the weights are rebuilt from the Lasm. If it does not, the Lasm is still the only record of *why* each fact is in there and who can retire it. Either way the durable value sits in the control plane, and the weights are a cache.

The unit of sale is then a governed assembly for a bounded business context, plus the conformance evidence that the fleet using it stays faithful. Not seats, not tokens, not a workbench.

## The Graduation Ladder, Completed

The mind notes' ladder was: capabilities, then skills (behavior), then tools (world), then knowledge (memory and mind). It was written for paseo, but the rungs are generic; every agent stack climbs some version of them. The preconditions note observed the top rung may not be compositional because writes into shared weights can degrade prior writes; that is a property of the weight substrate, and context substrates degrade differently, through prompt length and instruction conflict. The control-plane reading adds the rung above knowledge for any stack:

```
capability family  →  skill (behavior)  →  tool (world)  →  memory  →  mind  →  Lasm
                                                                              ▲
                                            the symbolic, owned, contestable account
                                            the mind is compiled from and corrected against
```

This is why memory and mind staying separate (the preconditions note's third decision) matters more than it first looked. Memory supplies salience, which decides what the mind keeps. The Lasm supplies authority, which decides what the mind may hold at all. A fact can be rehearsed constantly and still be `disputed`. A fact can be `accepted` and never read. Three different signals, three different records.

## What This Changes

- **`lasm_core` gets a weight-patch projection surface, not a new kind of thing.** A `WeightPatchDescriptor` alongside harness, skill, and MCP descriptors, carrying `LasmProjectionReferences` and a digest. Conforms to paseo's stop rule, a capability family rather than an actor type, but the reason it belongs in the core is broader: it lets the core see weights as a substrate of mind. Implemented in commit `7f6d048`.
- **Auto Bench gets a new attribution target.** `DivergenceSource` can already say `projection`. With a patch binding it can say which patch carried the wrong meaning, and the in-vitro-patching probes (neighbour versus far-field, canonical versus paraphrase, remove-patch exactness) become conformance evidence attached to that binding.
- **The in-vitro-patching rig has a customer for its null result.** If the mind cannot accumulate at n=1000, the control plane does not lose its value. The Lasm still projects into skills, MCP, and harness context. Only the cheapest projection target is lost.
- **The Holocron Nuveris mapping sharpens.** The orientation-layer note already shows the Lasm supplying what Nuveris needs a human for before training. In control-plane terms, Nuveris is a data plane that compiles a Lasm into a trunk, and the registry rows it needs are Lasm entries with bindings.

## Tensions

- **"Mind" and "Lasm" are not the same substance.** A mind is sub-symbolic; a Lasm is symbolic. The claim is that the Lasm is the mind's *constitution*, not its contents. The three-controls note's wall between what can be named and what can only be addressed sits directly under this, and the metaphor should not be allowed to paper over it.
- **Collective means shared interference.** A fleet-wide mind spends one budget. The Lasm can say what may enter; it cannot say what the entry will displace. Correction remains the only option on the weight side, and `REMOVE PATCH` exactness remains load-bearing.
- **The platform will sell a semantic layer too.** Genie's ontology, Metric Views, and OntoRank are a native control plane for Genie Agents. The Lasm's answer has to be cross-platform, cross-client, human-accountable, and exportable, or the platform's version wins on convenience. The falsification condition in the binding-record artifact applies here unchanged.
- **Who is the buyer?** A control plane is bought by whoever is accountable for the meaning. That is a domain owner, not a platform team and not an agent developer. The plugin is how the developer consumes it; it is not what is sold.
- **"Sellable" and "sovereign" can pull apart.** Sovereignty wants export to be trivial. A business model wants something to be hard to leave. The honest resolution is that what is sold is the maintenance and the evidence, not the lock-in.

## Open Questions

1. Does a weight-patch binding need a different `fidelity` vocabulary than a skill binding? A skill's fidelity is asserted; a patch's can be measured by the rig's probes.
2. Should the Lasm's `accepted` status be a precondition for compilation into a patch, or only a flag the patch pipeline reads? The former makes the fleet edge a hard gate, which the three-controls note argues is available because the entry is symbolic.
3. Is "collective mind" the external name, or an internal metaphor that should recede behind "Lasm" the way "agentic control plane" was told to recede in the naming artifact?
4. What is the smallest sellable unit? One assembly for one bounded context with one accepted binding and one conformance case, or does a customer need the probe results before the claim is credible?
5. Does any runtime, paseo's `microAgentManager` included, need to know about the Lasm at all, or does each see only its own substrate (skills, MCP capability families, a patch, a semantic layer), with the Lasm consulted by the pipeline that produced them?
6. When one business runs minds on several substrates, should Auto Bench compare them directly, for example the same question answered through a skill and through a patch, to detect drift between minds before either diverges from the Lasm?

## Working Hypothesis

paseo's fifth primitive made the mind visible, but every agent stack already has one. A mind is what a business's agents know, on whatever substrate their stack provides. A Lasm is the business's owned, versioned, contestable statement of what any of those minds is permitted to know and how to tell whether it still does. That statement is the control plane. It is sellable because every other layer is being absorbed by a platform, a runtime, or a model vendor, none of them can author it, and none of them spans the others. The next concrete step is small: give `lasm_core` a weight-patch projection surface and a binding to it, so the first in-vitro-patching probe can be attributed from the control plane rather than argued about beside it.
