# Change: Rename SArB Core to Nuveris

## Why
The completed Sans I/O core is currently presented as `@servco/sarb` and described as the SArB core. That naming conflates two distinct things established during subsequent ideation:

- **Nuveris** is the agentic control plane and the reusable core that models its primitives, traces, validation, and evaluation.
- **SArB** is the Servco Automotive Reality Benchmark that uses Nuveris to evaluate agentic systems inside automotive business reality.

Keeping the core under the SArB identity makes a general control-plane model appear inseparable from its first benchmark. The naming should reflect the boundary before more packages, adapters, or benchmark suites depend on it.

## What Changes
- Rename the private TypeScript package identity from `@servco/sarb` to `@nuveris/core`.
- Present the Sans I/O implementation and public documentation as **Nuveris Core**.
- Describe SArB as the automotive reference benchmark and fixture set built with Nuveris, rather than as the name of the core itself.
- Update ReffySpec project context to preserve the Nuveris/SArB distinction for future work.
- Preserve the existing Sans I/O architecture, domain APIs, validation, normalization, evaluation behavior, tests, and automotive fixture.

## Impact
- Affected specs: `establish-sarb-sans-io-core` (public identity and scenario terminology)
- Affected code: `package.json`, `package-lock.json`, root documentation, package metadata, and naming assertions or examples
- Affected planning context: `.reffy/reffyspec/project.md`
- Breaking surface: consumers importing the package by name must change from `@servco/sarb` to `@nuveris/core`

## Supersedes
- `establish-sarb-sans-io-core`

## Reffy References
- `agentic-control-primitives-for-sarb.md` - establishes Nuveris as the name for the agentic control plane modeled by the core.
- `naming-the-agentic-control-layer.md` - records the selected name and distinguishes Nuveris, agentic control primitives, and SArB.
