# Lasm as a Sovereign Mapping Layer and Agent Plugin

Status: exploratory
Date: 2026-09-30
Authors: Roberto Delgado, Codex

## Prompt

As data and agent platforms absorb more of the work of building, evaluating, deploying, and monitoring agents, what remains distinctive about Lasm? Could `lasm-core` be best understood as an agent plugin that preserves the business's control over the mapping between lived reality and digital objects and events?

## Source Snapshot

Read on 2026-09-30:

- [Genie Workbench introduction](https://databricks-solutions.github.io/databricks-genie-workbench/docs/getting-started/introduction/) and [architecture overview](https://databricks-solutions.github.io/databricks-genie-workbench/docs/getting-started/architecture-overview/). The documented product is a developer tool for Genie Agents. It creates agents from business requirements, scores configuration, optimizes against benchmarks, stores history, and watches usage, cost, feedback, and executed-resource lineage. It composes a Databricks App, jobs, Lakebase, Delta, and other platform services. This is evidence of an expanding native lifecycle around *Genie Agents*, not proof that Databricks has absorbed every organization's entire software development lifecycle.
- [Agent Plugins specification v1.0.0](https://agent-plugins.org/specification). Its portable package has a root `plugin.json`; v1 standardizes skills and MCP server configuration, with client-specific extensions. The format packages agent-facing components. It does not define a canonical business ontology, operational evidence model, authority regime, or cross-platform semantic contract.
- Local context: `lasm-reality-workbench-on-databricks.md`, `operational-conformance-first-benchmark-second.md`, `naming-the-agentic-control-layer.md`, and the current `src/lasm_core/` Python package.

## The Emerging Pattern

Genie Workbench makes a broader direction easier to see. A platform that already holds data, permissions, compute, workflows, and agent configuration can use those assets to make the agent lifecycle native: requirements become configuration; configuration becomes benchmarked behavior; production traffic becomes feedback; feedback becomes a candidate change. Other platforms may converge on similar loops around their own assets.

This can make a separate agent harness less valuable as a permanent system of record. It also increases the importance of a boundary the platform cannot infer from telemetry alone: **which business distinctions, obligations, authority claims, and acceptable outcomes should its digital objects and events represent?** A table, workflow, trace, and benchmark can all be internally consistent while encoding the wrong business meaning.

The hypothesis is that Lasm belongs at this boundary. Its defensible role is the maintained mapping from how a bounded business context is understood and practiced to the software objects, events, permissions, and agent-facing capabilities that claim to implement it. A platform may host and execute much of that mapping without becoming its sole author or final judge.

## What Sovereignty Would Mean

Sovereignty is more concrete than keeping a copy of metadata outside Databricks. The organization should be able to:

1. State and version a business meaning with its scope, owner, sources, unresolved disputes, and effective period.
2. Bind that meaning to native implementations: tables, Metric Views, Genie instructions and benchmarks, jobs, applications, workflows, policies, roles, and events. These are references to authoritative implementations, not duplicated shadow definitions.
3. Inspect where a projection loses or alters meaning, including across different vendors and agent clients.
4. Test consequential behavior and outcomes against an independently reviewable account of the business context.
5. Export the mapping and its evidence, move it to another runtime, and still understand which claims remain valid.
6. Let accountable people revise the mapping when actual practice or legitimate policy changes, rather than allowing a successful optimizer run to redefine business reality.

That is a claim about **semantic and operational portability**, not a promise that every platform-specific action is executable everywhere. A portable Lasm might retain a stable business concept and conformance expectation while its Databricks and other-platform bindings differ.

For example, “net new-vehicle units” might be realized as a governed Metric View, queried through Genie, and cited in a skill. Lasm's work is to retain the business definition, the ownership and effective date, the binding to that Metric View, the authorized context in which it applies, and cases that reveal whether an agent's answer or action preserved the definition. It should not recompute the metric in a second registry merely to appear sovereign.

## A Smaller, Sharper Domain Model

The current `lasm_core` package already models a `LogicalAssemblySlice` of concepts, relations, constraints, events, policies, runtime evaluation descriptors, and provenance, plus projections into agent surfaces. That is a useful center. The question is whether some current or imagined primitives describe durable business meaning, while others describe mechanics that Databricks or an agent client will own natively.

| Keep in the portable Lasm contract | Treat as a binding or evidence adapter |
| --- | --- |
| Scoped concepts and relationships; consequential events and state transitions | Table schemas, lineage records, system events, and workflow object IDs |
| Business constraints, commitments, authority expectations, and acceptable outcomes | Native permissions, approval workflows, policy engines, and tool authorization |
| Provenance, accountable owner, version, dispute status, and effective period | Registry storage, catalog APIs, trace stores, and synchronization jobs |
| Mapping claims from business entries to digital implementations and projections | Genie configuration, skill files, MCP endpoints, plugin manifests, and app UI |
| Conformance expectations and evidence requirements | Platform benchmark runners, observability, optimizers, and Auto Bench execution |

This is a proposed *scope test*, not an immediate instruction to remove existing types. A Lasm evaluation descriptor may remain in the core as a platform-independent statement of what must be checked; a native policy engine or benchmark runner can execute it. Conversely, a specific approval queue or connector lifecycle should live in an adapter unless it expresses a genuinely portable business invariant.

An important refinement is to make the **binding** a first-class object: which Lasm entry is realized by which digital object or event, in which environment, under which version, with what confidence and evidence? Without this, Lasm risks becoming a good vocabulary disconnected from the systems that act on it. Without provenance and contestability, it risks becoming just another platform-generated semantic model.

## Is `lasm-core` an Agent Plugin?

**A Lasm plugin is a compelling delivery shape; `lasm-core` is the mapping contract and engine beneath it.** The Agent Plugins v1 format can carry a Lasm skill that explains when and how to consult the mapping, plus MCP server configuration exposing inspection, validation, and conformance tools. A client could install that package and gain a consistent way to ask what a business concept means, which native object implements it, what authority applies, and which evidence supports an answer.

The portable plugin format does not itself store or govern the LogicalAssembly. It also leaves credentials and much runtime behavior to the client. Treating the plugin package as the canonical model would make business meaning dependent on a distribution format and on whichever clients implement it. A cleaner relationship is:

> **Lasm is the business-to-digital mapping. `lasm-core` validates and evaluates its portable contract. A Lasm agent plugin projects that contract into compatible agent clients. Native platform adapters bind and execute it in specific environments. Auto Bench tests whether the whole chain conforms.**

The plugin could be thin even if the underlying mapping is rich. It might expose a small set of operations: resolve a term in context; inspect a binding and provenance; check an intended action against authority and state expectations; record or retrieve conformance evidence; and identify ambiguity that requires a human decision. The plugin should not become a duplicate agent orchestrator, gateway, or platform monitor.

## Tensions to Resolve

- **Authorship versus observation.** Platform traces reveal how systems behaved; people and governed sources still establish what behavior was legitimate. Lasm must record both without silently promoting observed frequency into authority.
- **Native first versus portability.** Correct a bad metric in its Metric View or a bad policy in its owning workflow. Preserve the cross-system mapping and conformance case in Lasm so the correction remains understandable outside the native surface.
- **Plugin reach versus client variance.** Agent Plugins specifies a package, while clients decide what they support and how credentials are managed. Conformance must be tested for each installed client and effective identity.
- **Evaluation ownership.** Native benchmarks can judge a Genie Agent's SQL accuracy. Auto Bench can judge whether the represented business intent survived projection, action, transition, and outcome. These are related but distinct claims.
- **The workbench question.** A separate Lasm Workbench is justified only where native views cannot show the cross-platform mapping, disputes, binding drift, and evidence chain. The mapping contract should be useful before that UI exists.

## Smallest Useful Probe

Choose one consequential, already governed business definition. Record a Lasm entry with owner, sources, effective scope, and one native binding; project it into one agent skill or MCP surface; run one conformance case in which the native agent is technically successful but uses the wrong meaning or authority. Then change the native implementation and verify that the Lasm binding and case still explain the correction. This would test whether Lasm contributes something distinct from the platform's own configuration and benchmark loop.

## Open Questions

1. Which current `lasm_core` fields encode enduring business claims, and which are snapshots of today's agent harness mechanics?
2. What is the minimum portable binding record needed to connect a LogicalAssembly entry to a governed native object or event?
3. Who can assert, dispute, accept, and retire a mapping claim, and how is that authority proven across platforms?
4. Can a Lasm plugin offer useful inspection with read-only permissions before it offers any action gating?
5. When a platform's ontology or optimizer starts generating mappings, how does Lasm distinguish a useful candidate from an accepted business definition?

## Working Hypothesis

As platforms internalize agent lifecycle mechanics, Lasm should get narrower and more valuable: a portable, versioned, contestable contract for the mapping between business reality and its digital realization. The plugin is the agent-facing vessel for that contract, not its identity or system of record.
