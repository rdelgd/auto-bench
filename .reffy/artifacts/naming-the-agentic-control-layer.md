# Lasm: One Name for the Semantic and Agentic Control Layer

Status: adopted
Date: 2026-08-17
Authors: Roberto Delgado, Codex

## Prompt

The project currently assigns three names to three layers:

- **LogicalAssembly (Lasm)** for the domain and semantic model;
- **Nuveris** for the agentic control layer and reusable Sans I/O library;
- **Auto Bench** for the automotive conformance workbench.

This artifact explores removing the Nuveris name completely. The proposed collapse is to let **Lasm** name both the thesis and the reusable implementation grounded in that thesis. Auto Bench then evaluates the Lasm.

## Adopted Thesis

> Lasm makes an organization's operational meaning executable across agent-facing context, capability, authority, action, and evidence. Auto Bench evaluates whether that Lasm remains faithful to reality and produces conformant outcomes.

A LogicalAssembly is not merely an ontology placed beneath a separate control plane. Its concepts, relations, constraints, events, policies, and evaluations become operational through projections into harness context, skills, MCP surfaces, permissions, approvals, and other agent-facing interfaces. Those surfaces are how an assembly participates in action.

Under this thesis, the former Nuveris layer is not an independent thing that needs its own proper name. It is the projected, enforced, and observable expression of a Lasm.

## Why Collapse the Names

The Nuveris distinction helped separate the reusable core from Auto Bench, but it now creates an artificial boundary inside the reusable system:

- A semantic model without projections and enforcement risks becoming descriptive documentation.
- Agentic control surfaces without maintained organizational meaning can govern the wrong behavior efficiently.
- Evidence and attribution need to connect actions back to the exact assembly entries and projections that shaped them.
- The active implementation direction already places LogicalAssembly slices, operational state, control-surface projections, runtime evaluations, and evidence in the same deterministic core.

Calling one half Lasm and the other half Nuveris makes users learn two identities for one dependency chain. Calling the whole thesis **Lasm** says that organizational meaning is the organizing abstraction, while agentic control is how that meaning becomes load-bearing.

## The Simplified Stack

| Layer | Responsibility |
| --- | --- |
| **Operational reality** | Supplies the living sources, practices, state, commitments, and accountable human judgment from which a Lasm is compiled and against which it must remain valid |
| **Lasm** | Represents load-bearing meaning; projects it into agent-facing context and capabilities; constrains consequential action; records state, runtime evaluation, and attributable evidence |
| **Agentic proxy** | Perceives, reasons, acts, clarifies, abstains, escalates, and hands off through the Lasm's projections and authority boundaries |
| **Auto Bench** | Exercises and evaluates the Lasm across realistic automotive episodes, locating divergence among reality, representation, projection, conduct, transition, and outcome |

The headline relationship becomes:

> **Auto Bench evaluates the Lasm.**

Auto Bench may evaluate a Lasm with or without a live agent execution. It can inspect materialized assemblies, projections, evidence, transitions, and outcomes deterministically, while adapters supply any live runtime or external-system behavior.

## What “Lasm” Names

The same name can operate at three related levels:

- **Lasm, the thesis:** operational meaning should be sourced, versioned, contestable, projected into the surfaces through which agents act, and continuously tested through evidence and evaluation.
- **LogicalAssembly, the domain model:** the explicit concepts, relations, constraints, events, policies, evaluations, provenance, version, and relevant operational-state contracts for a scoped reality.
- **Lasm, the library:** the reusable Sans I/O TypeScript implementation for materialized assemblies, projections, validation, evidence normalization, runtime-evaluation records, state transitions, and structured findings.

This is deliberate alignment rather than accidental overloading. The full term **LogicalAssembly** remains useful for the concrete domain object. **Lasm** names the broader thesis and software built around making that object operational.

## Agentic Control Still Exists as a Description

Removing Nuveris does not remove the agentic control-plane idea. “Agentic control plane” and “agentic control primitives” can remain descriptive vocabulary:

- harness context frames perception and interaction;
- skills project procedural meaning;
- MCP tools and resources project system-facing capability and context;
- policies, permissions, approvals, and handoffs constrain authority;
- traces and evidence reveal how intent and represented meaning became action and outcome.

These are **Lasm projections and control surfaces**, not a separately branded Nuveris layer.

## Library Identity

The npm library that replaces the former core uses the Lasm identity:

| Former | Selected |
| --- | --- |
| Nuveris Core | Lasm |
| `@nuveris/core` | `@lasm/core` |
| Nuveris fixture/model | Lasm fixture/model or the more precise domain term |
| Nuveris projection | Lasm projection |
| Lasm–Nuveris–Auto Bench stack | Lasm–Auto Bench stack |

The selected private package identity is `@lasm/core`. Registry availability and ownership should still be checked before any external publication, but those concerns do not change the Lasm identity.

The public API should continue to favor domain-driven names such as `LogicalAssembly`, `ConformanceCase`, `OperationalState`, `EvidenceEvent`, and `evaluateConformance`. Replacing Nuveris does not justify adding `Lasm` prefixes to every exported type.

## Evaluation Boundary

The name collapse must not collapse two different evaluation loops:

- **Lasm runtime evaluations** check or gate behavior against maintained concepts, constraints, policies, and state contracts during operation.
- **Auto Bench evaluation** judges the Lasm as a whole: whether its source model was fit, its projections preserved meaning, its runtime checks were adequate, the proxy acted conformantly, and the resulting state was acceptable.

A Lasm runtime check can pass against stale or incomplete meaning. Auto Bench therefore treats runtime results as evidence, not as proof that the Lasm conformed.

## Consequences for the Current Project

If this direction is adopted in planning, it implies more than an npm rename:

- remove Nuveris as a thesis, product, layer, package, and documentation identity;
- replace `@nuveris/core` with the selected Lasm package identity;
- replace active infrastructure labels such as the `nuveris-v1` Reffy workspace identity;
- revise the active reality-validation change from a three-layer Lasm–Nuveris–Auto Bench model to a Lasm–Auto Bench model;
- describe harnesses, skills, MCP surfaces, permissions, approvals, handoffs, and evidence as Lasm projections, control surfaces, or evaluation inputs;
- retain archived ReffySpec changes as historical records rather than rewriting them;
- update current specs, project context, README, source metadata, fixtures, tests, and examples through a new superseding ReffySpec change.

This artifact records the naming and conceptual direction only. It does not itself authorize or specify the migration.

“Completely” should mean no Nuveris identity remains in current product, package, specification, workspace, or documentation surfaces. Archived ReffySpec changes should retain the word where it records what actually happened; those references are historical provenance, not an active identity.

## Risks and Tensions

### Lasm may sound narrower than the implementation

Readers may interpret LogicalAssembly as only the six semantic entry kinds and wonder why the library also models projections, operational state, evidence, and conformance inputs. The thesis must consistently explain that projections and evaluations are what make an assembly operational; they are not unrelated platform features attached to it.

### One name can blur object, system, and package

The project should use precise grammar:

- “a LogicalAssembly” or “an assembly” for a materialized domain object;
- “Lasm” for the thesis, ecosystem, or library identity;
- a code-formatted package specifier for the npm package;
- “Auto Bench” for the evaluator and automotive conformance workbench.

### Auto Bench must not absorb Lasm responsibilities

Auto Bench evaluates the Lasm but should not become the source of organizational meaning, the production enforcement runtime, or the universal owner of every Lasm evaluation. It consumes materialized evidence and may provide fixtures and adapters for exercising the system.

### Package availability remains external

The desired npm name or scope may be unavailable or unsuitable. That can change the import specifier without reviving the Nuveris concept.

## Open Questions

- Should the repository eventually separate the reusable Lasm library from the Auto Bench evaluator, or can package exports preserve that boundary initially?
- Which current “conformance” models belong generically to Lasm, and which are specifically Auto Bench evaluation models?
- Should “agentic control plane” remain prominent explanatory vocabulary or recede behind “Lasm projections”?
- Does the name need a formal expansion everywhere, or is defining **Lasm = LogicalAssembly** once per major surface sufficient?

## Adopted Direction

Retire **Nuveris** completely.

Use **Lasm** for the thesis and reusable library, **LogicalAssembly** for the concrete semantic/domain object, and **Auto Bench** for the automotive workbench that evaluates the Lasm. Treat harnesses, skills, MCP surfaces, permissions, approvals, handoffs, traces, and runtime evaluations as the projections, controls, and evidence through which a Lasm becomes operational.

The resulting formulation is simpler and more faithful to the architecture:

> Lasm makes operational meaning executable. Auto Bench evaluates the Lasm.
