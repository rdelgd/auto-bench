# Change: Center the Reality Validation Stack

## Why
The current Nuveris Core specification models harnesses, skills, MCP surfaces, agentic traces, and structured evaluation, but it stops short of modeling the operational reality against which agent conduct should be validated. It can describe how an agent moved through control surfaces without determining whether the governing meaning was current, the initial state was perceived correctly, actions produced permitted transitions, or the resulting business state was acceptable.

The converged thesis defines a three-layer reality-validation stack:

- A LogicalAssembly defines and continuously tests a scoped representation of load-bearing operational reality.
- Nuveris binds agent perception and action to that reality and produces attributable evidence.
- Auto Bench stress-tests whether that binding holds across realistic automotive episodes.

Generic agent analytics are not the product thesis. Telemetry is evidence only when it supports a validation or attribution decision.

## What Changes
- Extend Nuveris Core with a serializable LogicalAssembly slice containing concepts, relations, constraints, events, policies, runtime evaluation descriptors, provenance, and version identity.
- Extend Auto Bench scenarios with explicit operational state, permitted/prohibited transitions, acceptable/prohibited outcomes, and references to the assembly entries exercised by the episode.
- Expand normalized evidence events to cover assembly selection and consultation, state observation and transition, runtime evaluation, outcome observation/validation, evidence linking, and failure attribution.
- Replace the older evaluation dimensions with intent fidelity, semantic fidelity, reality-model validity, state and outcome validity, control-surface quality, reality coverage, evidence and attribution, and governance.
- Keep Lasm runtime evaluations distinct from Auto Bench metaevaluation while allowing runtime results to serve as benchmark evidence.
- Keep the package Sans I/O and explicitly exclude general-purpose analytics, universal telemetry, source ingestion, dashboards, and digital-twin scope.

## Impact
- Affected specs: `establish-auto-bench-sans-io-core`
- Affected code: `src/scenario.ts`, `src/trace.ts`, `src/evaluate.ts`, `src/validate.ts`, exports, fixtures, and tests; likely new LogicalAssembly and operational-state modules
- Compatibility: benchmark fixtures and consumers must supply the new materialized reality and state inputs; the package is private and pre-release, so no compatibility layer is planned

## Supersedes
- `establish-sarb-sans-io-core`

This change supersedes that change's control-plane-only modeling boundary while preserving its TypeScript Sans I/O architecture and deterministic evaluation principles.

## Reffy References
- `agentic-control-primitives-for-auto-bench.md` - defines reality validation as the stack's center, assigns responsibilities to Lasm/Nuveris/Auto Bench, and identifies the required evidence and evaluation dimensions
