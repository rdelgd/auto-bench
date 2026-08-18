## Context
Reffy's archive merger applies requirement deltas but preserves the existing capability purpose. The prior change modified the requirements central to reality validation but did not modify three older fixture requirements, leaving active canonical language inconsistent with the shipped `@lasm/core` package.

## Goals / Non-Goals
- Goals:
  - Make every active canonical requirement use the Lasm–Auto Bench architecture.
  - Describe harness, skill, and MCP fixtures as Lasm projections and control surfaces.
  - Keep the canonical purpose aligned with the shipped library.
- Non-Goals:
  - Change runtime behavior or public TypeScript APIs.
  - Rewrite archived planning history.

## Decisions

### Modify the existing capability rather than create another one
The residual language belongs to `establish-auto-bench-sans-io-core`. Its existing requirements are modified in place so the canonical capability remains cohesive.

### Update purpose as canonical maintenance
Requirement deltas cannot express a purpose change. After archiving the delta, update only the canonical spec's purpose paragraph to reflect the already-shipped architecture.

## Reffy Inputs
- `naming-the-agentic-control-layer.md`
