# Change: Center the Reality Validation Stack

## Why
The current core models harnesses, skills, MCP surfaces, agentic traces, and structured evaluation, but it stops short of modeling the operational reality against which agent conduct should be validated. It can describe how an agent moved through control surfaces without determining whether the governing meaning was current, the initial state was perceived correctly, actions produced permitted transitions, or the resulting business state was acceptable.

The earlier architecture placed Nuveris between LogicalAssembly and Auto Bench. That middle layer is no longer useful. Agent-facing context, skills, MCP surfaces, permissions, approvals, handoffs, runtime checks, and evidence are the projections and operational expression of a Lasm, not a separately named system.

The converged thesis has two named responsibilities:

- **Lasm** is the thesis, semantic/domain model, and reusable Sans I/O library. A LogicalAssembly represents load-bearing operational meaning; its projections expose and enforce that meaning through agent-facing surfaces.
- **Auto Bench** exercises and evaluates the Lasm across realistic automotive episodes, locating conformance or divergence among operational reality, representation, projection, conduct, state transition, and outcome.

Generic agent analytics are not the product thesis. Telemetry is evidence only when it supports a validation or attribution decision.

## What Changes
- Replace Nuveris Core and `@nuveris/core` with the Lasm library and package identity `@lasm/core`; do not provide a compatibility alias for the private pre-release package.
- Model a serializable LogicalAssembly slice containing concepts, relations, constraints, events, policies, runtime evaluation descriptors, provenance, and version identity.
- Treat harnesses, skills, MCP surfaces, prompts, permissions, approvals, and handoffs as Lasm projections or control surfaces that reference the assembly meaning they expose or enforce.
- Extend Auto Bench episodes with explicit operational state, permitted or prohibited transitions, acceptable or prohibited outcomes, and references to the assembly entries exercised by the episode.
- Expand normalized evidence to cover assembly selection and consultation, projections, state observation and transition, runtime evaluation, outcome observation and validation, evidence linking, and failure attribution.
- Evaluate the Lasm through dimensions for intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance.
- Keep Lasm runtime evaluations distinct from Auto Bench evaluation while allowing runtime results to serve as evidence about the Lasm.
- Remove Nuveris from active package, source, specification, workspace, and documentation identities while preserving archived ReffySpec files as historical records.
- Keep the package Sans I/O and exclude general-purpose analytics, universal telemetry, source ingestion, dashboards, and digital-twin scope.

## Impact
- Affected specs: `establish-auto-bench-sans-io-core`
- Affected planning/context: active ReffySpec change, project context, README, Reffy workspace metadata, and current canonical spec when the change is archived
- Affected code: `package.json`, lockfile, `src/scenario.ts`, `src/trace.ts`, `src/evaluate.ts`, `src/validate.ts`, exports, fixtures, and tests; likely new LogicalAssembly and operational-state modules
- Compatibility: the import specifier changes from `@nuveris/core` to `@lasm/core`, and conformance cases must supply the new materialized reality and state inputs; the package is private and pre-release, so no compatibility layer is planned

## Supersedes
- `establish-sarb-sans-io-core`
- `rename-sarb-core-to-nuveris`

This change supersedes the earlier control-plane-only modeling boundary and reverses the decision to give that boundary a separate Nuveris identity. It preserves the TypeScript Sans I/O architecture and deterministic evaluation principles while centering the system on Lasm.

## Builds On
- `adopt-conformance-api` - establishes `ConformanceCase`, `ConformanceEvaluation`, and `evaluateConformance` as the public API vocabulary

## Reffy References
- `naming-the-agentic-control-layer.md` - decides to retire Nuveris, use Lasm for the thesis and reusable library, and define Auto Bench as the evaluator of the Lasm
- `agentic-control-primitives-for-auto-bench.md` - defines reality validation, the required semantic substrate, evidence model, and evaluation dimensions
