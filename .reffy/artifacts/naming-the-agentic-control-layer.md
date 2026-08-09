# Nuveris: Naming the Agentic Control Layer

Status: name selected
Date: 2026-07-15
Authors: Roberto Delgado, Codex

## Scope Clarification

The idea that needs a standalone name is the thesis in `agentic-control-primitives-for-auto-bench.md`, not Auto Bench or the generalized reality-benchmark system.

`Auto Bench` is Servco's automotive reference benchmark. Auto Bench can model and evaluate the idea, but the idea exists independently of that benchmark and should not be named “for Auto Bench.”

The concept is the inspectable layer around an agent through which human intent is framed, procedural behavior is supplied, capabilities and context are exposed, authority is constrained, work is handed off, and resulting behavior is observed.

Its major elements are:

- harnesses that frame the interaction loop, context, workspace, permissions, and approvals;
- skills that encode discoverable procedural knowledge and workflow constraints;
- MCP tools, resources, and prompts that expose system-facing capabilities and context;
- policies, human confirmations, and handoffs that constrain or redirect action;
- traces and analytics that reveal how intent became action and outcome.

## Selected Name: Nuveris

**Nuveris** is the selected proper name for this idea.

Nuveris does not replace the underlying descriptive vocabulary. It gives the thesis and potential system a distinct identity:

- **Nuveris** — the proper name.
- **Agentic control plane** — the descriptive category.
- **Agentic control primitives** — the composable harness, skill, MCP, governance, handoff, and trace elements.

A concise formulation:

> Nuveris is the agentic control plane through which intent becomes governed capability, action, and evidence.

This keeps the name portable while preserving language that explains what it is.

## Descriptive Category: Agentic Control Plane

In infrastructure, a control plane configures, constrains, and observes how work is carried out without being identical to the work itself. The analogy fits here: the model or agent performs reasoning and action, while harnesses, skills, MCP surfaces, permissions, policies, approvals, and trace semantics shape what agency is possible and legible.

A concise definition:

> The agentic control plane is the externalized, inspectable layer through which intent is translated into governed agent capability, action, and evidence.

The term supports useful distinctions:

- **Agent:** the reasoning and acting locus.
- **Agentic control plane:** the surfaces that configure, enable, constrain, and observe that agency.
- **Business environment:** the people, systems, policies, state, and consequences on which the agent acts.
- **Benchmark:** the system that evaluates the agent and its control plane inside a modeled reality.

Under this vocabulary, Auto Bench is a benchmark of Nuveris—the agentic control plane—operating inside Servco automotive reality.

## Alternative Names

### Intent Mediation Layer

Emphasizes the path from submitted intent through inference, controls, tools, handoffs, and outcomes.

Strength: closest to the original thesis that agentic systems increasingly mediate human intent.

Risk: understates capability exposure, runtime configuration, and governance; “layer” may imply a clean technical boundary that does not exist.

### Agency Stack

Treats harnesses, skills, MCP, policy, and observability as a composable stack that produces practical agency.

Strength: short, accessible, and broader than a single agent runtime.

Risk: “stack” suggests a fixed vertical architecture, while these control surfaces may be distributed across products and organizations.

### Agentic Interface Plane

Emphasizes that these primitives form the interfaces between human intent, agents, and external systems.

Strength: highlights the analogy to HTML, JavaScript, and other inspectable platform surfaces.

Risk: “interface” can sound limited to UI or API concerns and may not communicate governance strongly enough.

### Agentic Mediation Infrastructure

Names the complete infrastructure through which agents represent people, use systems, and coordinate work.

Strength: captures the sociotechnical and organizational breadth of the thesis.

Risk: long, abstract, and difficult to use as a crisp category or project name.

### Intent Control Plane

Centers the thing being preserved and governed rather than the agent.

Strength: foregrounds intent fidelity and remains relevant if agents change form.

Risk: may imply control over human intent rather than control over its automated mediation.

## Why “Agentic Control Primitives” Is Not Quite the Name

“Agentic control primitives” remains useful for the individual elements: a harness permission gate, a skill activation rule, an MCP resource boundary, or a human-confirmation event can each be a primitive.

The larger idea is about how those primitives compose into an operational and observable system. **Nuveris** names that whole, **agentic control plane** describes its category, and **agentic control primitives** names its constituent parts.

## Relationship to Auto Bench

Auto Bench should use the concept without owning its name:

> Auto Bench evaluates whether Nuveris preserves intent and produces acceptable outcomes inside realistic automotive business processes.

This preserves a clean hierarchy:

- Nuveris — the named idea and potential system.
- Agentic control plane — its general category.
- Agentic control primitives — harness, skill, MCP, policy, approval, handoff, and trace surfaces.
- Auto Bench — Servco's automotive reference benchmark that evaluates them in context.
- A generalized reality-benchmark method — a separate, still-unnamed system that could support Auto Bench and other benchmarks.

## Remaining Questions

- Is this primarily a conceptual category, a reference architecture, or a product identity?
- Should observability be understood as part of the control plane or as a separate data plane derived from it?
- What visual identity or expansion, if any, should accompany the name Nuveris?
- Should availability and collision research happen before Nuveris appears in package or repository names?

## Working Hypothesis

Use **Nuveris** as the name for the overall idea, **agentic control plane** as its descriptive category, and **agentic control primitives** for its composable elements. Reserve Auto Bench for the benchmark that evaluates Nuveris inside automotive reality.
