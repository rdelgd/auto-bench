# Auto Bench

Auto Bench is a conformance workbench for testing whether an organization's operational reality can be faithfully codified in a LogicalAssembly, projected and enforced through Nuveris, and preserved through agentic action.

The project begins with Servco's automotive operations. Servco does not need an invented benchmark to tell it what successful automotive operation looks like: a century of continued operation is already the strongest empirical reference available. The immediate challenge is to identify which operational distinctions are load-bearing, make them explicit and executable, and determine whether agentic proxies can act within them.

> Operational conformance comes first. A portable benchmark may later be distilled from the conformance work.

## The Conformance Stack

| Layer | Responsibility |
| --- | --- |
| **Servco operations** | Supply the living source reality and the judgment of people accountable for its outcomes |
| **LogicalAssembly (Lasm)** | Compile that reality into sourced, versioned, contestable concepts, relations, constraints, events, policies, and evaluations |
| **Nuveris** | Project Lasm into agent-facing context and capabilities, enforce authority and policy, and produce attributable evidence |
| **Agentic proxy** | Perceive, reason, act, clarify, abstain, escalate, and hand off through those control surfaces |
| **Auto Bench** | Exercise the complete binding and locate divergence among reality, representation, projection, conduct, and outcome |

Operational reality is not an exhaustive digital twin or a claim to timeless objective truth. It is the smallest sourced set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

Servco's longevity is evidence, not dogma. Existing processes can contain obsolete policy, local workarounds, source disagreement, accidental complexity, or practices that no longer fit current commitments. Lasm should expose those conditions for accountable resolution rather than fossilize them.

## What Auto Bench Tests

Conformance is a chain:

1. **Source conformance:** Does the Lasm slice correspond to the policies, systems, schemas, practice, incidents, commitments, and practitioner judgment that currently carry meaning?
2. **Semantic conformance:** Does it preserve the distinctions and relationships practitioners depend on?
3. **Projection conformance:** Do Nuveris skills, MCP surfaces, harness context, permissions, and approvals express the governing Lasm without omission or distortion?
4. **Behavioral conformance:** Does the agentic proxy act within the projected meaning, authority, and commitments?
5. **State-transition conformance:** Do consequential actions move the operational system only through permitted states?
6. **Outcome conformance:** Does the resulting observable state satisfy legitimate intent and the process's acceptance envelope?
7. **Evolution conformance:** Does the binding remain valid as policies, systems, roles, models, and practices change?

A task-completion claim is not enough. Auto Bench should produce structured findings that identify whether divergence occurred in an operational source, Lasm, a Nuveris projection, the proxy, an external system, the outcome, or the evaluator itself.

## Conformance Cases

The first durable Auto Bench asset should be a private, evolving corpus of cases derived from real automotive processes. A case can include:

- operational provenance and accountable owners;
- an episode-scoped Lasm slice;
- initial state and actor-specific observations;
- user intent and relevant ambiguity;
- Nuveris control surfaces and authority boundaries;
- conformance claims, hard invariants, and acceptable outcomes;
- perturbations such as stale facts, conflicting sources, tool failures, or delayed effects;
- deterministic, counterfactual, practitioner, or model-assisted evaluations;
- agent traces, state transitions, runtime evaluations, outcomes, and evidence;
- an attributable finding describing conformity or divergence.

The primary value is diagnostic. A failure may show that the proxy acted incorrectly, but it may instead reveal a stale assembly entry, lossy projection, contradictory process, source-system defect, or weak evaluator.

## A Benchmark May Be Derived Later

Once internal conformance cases are well sourced, practitioner accepted, repeatedly useful, and adversarially hardened, their transferable structure may be distilled into a public automotive benchmark.

That benchmark should not ask other companies to conform to Servco. It should provide:

- a synthetic automotive LogicalAssembly and organization overlay;
- a reusable conformance-case schema and validation protocol;
- representative Nuveris skills, MCP surfaces, permissions, and approvals;
- stateful synthetic systems and episode environments;
- evaluators, counterfactual tests, and attribution formats;
- runner adapters and reporting conventions;
- a way for another company to replace the synthetic overlay with its own private Lasm.

The resulting benchmark would test whether an agentic proxy can be faithfully steered by a supplied, complex, versioned, and contestable automotive reality. Servco-specific policies, data, incidents, vulnerabilities, and private certification cases can remain private.

## What Exists Today

Nuveris Core is the implemented TypeScript Sans I/O foundation, published locally as `@nuveris/core`. It currently provides:

- serializable scenario, harness, skill, and MCP fixture models;
- pure validation and deterministic trace normalization;
- structured evaluation for intent fidelity, control-surface quality, business realism, observability, and governance;
- an automotive service-scheduling fixture with policy checks, customer confirmation, trace evidence, and evaluation output.

The current implementation predates the full conformance model and still uses benchmark-oriented API names such as `BenchmarkInput` and `evaluateBenchmark`. Core functions accept already-materialized values and return materialized results. They do not perform filesystem, network, database, environment, clock, persistence, runtime orchestration, or live MCP operations.

## Active Direction

The validated but not yet implemented `center-reality-validation-stack` change extends the core with:

- episode-scoped Lasm slices with provenance and runtime evaluation descriptors;
- explicit initial state, actor observations, permitted or prohibited transitions, and acceptable or prohibited outcomes;
- evidence for assembly use, state change, runtime evaluation, outcome validation, linking, and attribution;
- dimensions for semantic fidelity, reality-model validity, state and outcome validity, coverage, and evidence attribution;
- a strict distinction between Lasm runtime evaluations and Auto Bench metaevaluation.

The newer conformance-first artifact further reframes the purpose of that work. It has not yet been translated into revised ReffySpec or implementation changes. The canonical specification continues to describe shipped behavior until formal changes are implemented and archived.

## Architecture Boundaries

Nuveris Core remains Sans I/O and runner neutral:

- The core owns serializable domain models, deterministic validation, evidence normalization, and structured conformance findings.
- Adapters may load operational sources, run agents, host synthetic systems, invoke live MCP servers, or package cases for an execution framework.
- Harbor is a possible future execution and distribution adapter, not the source of operational meaning and not a dependency of the core.
- Lasm runtime evaluations enforce maintained operational meaning; Auto Bench evaluates whether the complete binding remained conformant.

## Non-Goals

Auto Bench and Nuveris are not intended to:

- externally score Servco against an imagined generic dealership;
- make Servco's practices a universal automotive standard;
- fossilize every current process or treat written policy as the whole truth;
- build a general-purpose agent analytics, engagement, funnel, or dashboard product;
- define a universal taxonomy for every agent interaction;
- replace telemetry or observability infrastructure supplied by harness vendors;
- centralize every organizational source or construct an omniscient digital twin.

Telemetry is evidence when it supports conformance or attribution. Collecting activity is not the product thesis.

## Development

```sh
npm install
npm run typecheck
npm test
```

The current package exports the core API and reference fixtures separately:

```ts
import { evaluateBenchmark } from "@nuveris/core";
import { routineMaintenanceBenchmark } from "@nuveris/core/fixtures";

const evaluation = evaluateBenchmark(routineMaintenanceBenchmark);
```

## Project Map

- [Conformance-first thesis](.reffy/artifacts/operational-conformance-first-benchmark-second.md)
- [Reality-validation foundations](.reffy/artifacts/agentic-control-primitives-for-auto-bench.md)
- [Project context](.reffy/reffyspec/project.md)
- [Current canonical specification](.reffy/reffyspec/specs/establish-auto-bench-sans-io-core/spec.md)
- [Active reality-validation change](.reffy/reffyspec/changes/center-reality-validation-stack/proposal.md)
- [Implementation tasks](.reffy/reffyspec/changes/center-reality-validation-stack/tasks.md)
- [Nuveris Core source](src/)
- [Automotive service fixture](src/fixtures/service-appointment.ts)
