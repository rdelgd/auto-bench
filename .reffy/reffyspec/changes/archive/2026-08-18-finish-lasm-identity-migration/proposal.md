# Change: Finish the Lasm Identity Migration

## Why
Archiving `center-reality-validation-stack` correctly made Lasm and `@lasm/core` canonical for the package, scenario, evidence, evaluation, and new reality-validation models. Three unchanged legacy requirements still describe harnesses, skills, and MCP surfaces using the retired middle-layer identity, and the capability purpose retains the former package name.

The implementation, README, project context, package metadata, and tests already use Lasm. Canonical truth should describe those shipped surfaces consistently.

## What Changes
- Describe harnesses, skills, MCP servers, tools, resources, and prompts as Lasm projections or control surfaces.
- Replace the remaining active legacy identity in those requirements and scenarios with Lasm and `@lasm/core`.
- Update the canonical capability purpose to say that Auto Bench evaluates Lasm.
- Preserve archived planning records unchanged.

## Impact
- Affected specs: `establish-auto-bench-sans-io-core`
- Affected code: none; this change reconciles canonical specification language with the shipped implementation
- Compatibility: none

## Builds On
- `center-reality-validation-stack` - implemented and archived the Lasm model, library identity, projection references, operational state, evidence, and Auto Bench evaluation

## Reffy References
- `naming-the-agentic-control-layer.md` - establishes Lasm as the thesis and library and removes the separately named middle layer
