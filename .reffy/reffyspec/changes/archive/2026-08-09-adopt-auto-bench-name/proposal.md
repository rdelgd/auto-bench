# Change: Adopt Auto Bench Name

## Why
The automotive reference benchmark is currently named SArB (Servco Automotive Reality Benchmark). The project should use the clearer, more approachable name **Auto Bench** everywhere the current benchmark identity appears, while leaving Nuveris Core and its package identity unchanged.

## What Changes
- Rename the current benchmark identity from `SArB` to `Auto Bench` in documentation, Reffy artifacts, project context, and canonical specifications.
- Rename current artifact and specification paths from `sarb` identifiers to `auto-bench` identifiers.
- Update Reffy project and artifact metadata to use `auto-bench`.
- Preserve archived ReffySpec changes as historical records of the former name.
- Keep Nuveris Core and `@nuveris/core` unchanged.

## Impact
- Affected specs: `establish-sarb-sans-io-core` (renamed in current truth to `establish-auto-bench-sans-io-core`)
- Affected code: README and repository-local Reffy/ReffySpec content and metadata; runtime behavior is unchanged

## Supersedes
- `establish-sarb-sans-io-core`
- `rename-sarb-core-to-nuveris`

This change supersedes only those changes' current naming decisions. Their archived records remain unchanged.

## Reffy References
- `agentic-control-primitives-for-auto-bench.md` - defines the benchmark role whose name changes to Auto Bench
- `hle-template-for-a-generalized-reality-benchmark.md` - uses the former benchmark name throughout the generalized benchmark analysis
- `naming-the-agentic-control-layer.md` - records the former SArB/Nuveris naming boundary that this change updates
