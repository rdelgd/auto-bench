# Auto Bench

Auto Bench is a conformance workbench for evaluating whether an organization's operational reality can be faithfully codified and made executable as a Lasm, then preserved through agentic action.

> Lasm makes operational meaning executable. Auto Bench evaluates the Lasm.

The project begins with Servco's automotive operations. Servco does not need an invented benchmark to define successful automotive operation: its lived operations supply the initial source reality and accountable judgment. Auto Bench helps identify which distinctions are load-bearing, make them explicit and executable, and determine whether agentic proxies can act within them.

## The Conformance Stack

| Layer | Responsibility |
| --- | --- |
| **Servco operations** | Supply living source reality and the judgment of people accountable for its outcomes |
| **Lasm** | Compile that reality into sourced, versioned, contestable concepts, relations, constraints, events, policies, and evaluations; project it into agent-facing context and capabilities |
| **Agentic proxy** | Perceive, reason, act, clarify, abstain, escalate, and hand off through Lasm projections and authority boundaries |
| **Auto Bench** | Exercise and evaluate the Lasm, locating divergence among reality, representation, projection, conduct, state transition, and outcome |

Operational reality is not an exhaustive digital twin or timeless objective truth. It is the smallest sourced set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

## What Lasm Means

The name operates at three related levels:

- **Lasm, the thesis:** operational meaning should be sourced, versioned, contestable, projected into agent-facing surfaces, and continuously tested.
- **LogicalAssembly, the domain model:** a materialized slice containing concepts, relations, constraints, events, policies, runtime evaluations, provenance, and version identity.
- **`lasm-core`, the library:** the deterministic Sans I/O Python implementation for assemblies, projections, operational state, evidence, validation, and evaluation mechanics, imported as `lasm_core`.

Harness context, skills, MCP surfaces, permissions, approvals, and handoffs are modeled as Lasm projections or control surfaces. They can reference the assembly entries and operational-state fields they expose or enforce.

## What Auto Bench Evaluates

Auto Bench evaluates a Lasm across eight dimensions:

1. Intent fidelity
2. Semantic fidelity
3. Reality-model validity
4. State and outcome validity
5. Control-surface quality
6. Reality coverage
7. Evidence and attribution
8. Governance

A task-completion claim is insufficient. A complete conformance case includes an episode-scoped LogicalAssembly, initial operational state, actor observations, permitted and prohibited transitions, acceptable and prohibited outcomes, agent-facing projections, and normalized evidence.

Lasm runtime evaluations and Auto Bench evaluation remain distinct. Runtime evaluations gate or check behavior against maintained meaning. Auto Bench evaluates the Lasm as a whole, including whether its sources were fit, its projections preserved meaning, its runtime gates were adequate, and the resulting state was acceptable.

## What Exists Today

`lasm-core` provides:

- explicit LogicalAssembly entry and provenance models;
- materialized operational state, actor observation, transition, and outcome contracts;
- harness, skill, MCP, permission, approval, and handoff projection references;
- pure cross-reference validation and deterministic evidence normalization;
- structured findings with assembly-entry, transition, outcome, evidence, and attribution references;
- an automotive service-scheduling fixture covering a complete Lasm evaluation episode;
- versioned JSON interchange documents and JSON Schemas for assemblies, cases, traces, and results.

The package accepts materialized values and returns materialized results. It has no runtime dependencies and does not perform filesystem, network, database, environment, process, clock, persistence, runtime orchestration, or live MCP operations.

## Architecture Boundaries

- `lasm_core` owns serializable domain models, deterministic validation, evidence normalization, pure evaluation mechanics, and the versioned JSON interchange contract.
- Auto Bench owns automotive conformance cases, expectations, fixtures, perturbations, and the evaluation of a Lasm.
- Adapters may load operational sources, run agents, host synthetic systems, invoke live MCP servers, persist results, or expose Lasm to other languages through JSON documents.
- Telemetry is evidence when it supports conformance or attribution; generic analytics are not the product thesis.
- Archived ReffySpec changes retain earlier naming decisions as historical provenance.

## Development

Requires Python 3.11 or later and [uv](https://docs.astral.sh/uv/). Node.js is not required.

```sh
uv sync                                        # create the environment with development tools
uv run pytest                                  # behavior, parity, interchange, and Sans I/O tests
uv run mypy                                    # strict static typing
uv run python scripts/write_schemas.py --check # verify the checked-in JSON Schemas are current
uv build                                       # build the wheel and source distribution into dist/
```

The package exposes the core API and the automotive reference fixtures separately:

```python
from lasm_core import evaluate_conformance
from lasm_core.fixtures import routine_maintenance_conformance_case

evaluation = evaluate_conformance(routine_maintenance_conformance_case)
print(evaluation["conformant"])
```

Records are plain dictionaries with the same camelCase keys as the JSON contract. Other languages exchange version 1 documents (`{"schemaVersion": 1, "kind": ..., "value": ...}`) through an adapter; `decode_document` and `encode_document` validate them without I/O.

`lasm-core` replaced the private npm package `@lasm/core` without a compatibility wrapper. See the [migration guide](docs/migrating-from-npm.md) and the [API inventory](docs/api-inventory.md). The TypeScript implementation is retained in version control history, and its recorded outputs remain the [regression corpus](tests/corpus/PROVENANCE.md).

## Project Map

- [Naming thesis](.reffy/artifacts/naming-the-agentic-control-layer.md)
- [Conformance-first thesis](.reffy/artifacts/operational-conformance-first-benchmark-second.md)
- [Project context](.reffy/reffyspec/project.md)
- [Current specification](.reffy/reffyspec/specs/establish-auto-bench-sans-io-core/spec.md)
- [Lasm source](src/lasm_core/)
- [Automotive service fixture](src/lasm_core/fixtures/service_appointment.py)
- [Interchange schemas](src/lasm_core/schemas/v1/)
- [Migration guide](docs/migrating-from-npm.md)
