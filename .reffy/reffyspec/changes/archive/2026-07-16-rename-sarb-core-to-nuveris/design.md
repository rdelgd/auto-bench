## Context
The initial implementation correctly established a pure TypeScript core, but it used SArB for both the reusable implementation and the automotive benchmark. The naming decision captured in Reffy now gives the reusable agentic control-plane idea its own identity: Nuveris.

This is a naming and boundary-clarification pivot, not an architectural rewrite. The implemented core remains useful, and SArB remains its first realistic automotive benchmark fixture.

## Goals / Non-Goals

Goals:

- Make Nuveris the public identity of the Sans I/O core.
- Reserve SArB for the Servco Automotive Reality Benchmark.
- Make the package-name migration explicit and testable.
- Preserve the prior change as historical lineage rather than rewriting it.
- Keep all current deterministic behavior and Sans I/O constraints intact.

Non-Goals:

- Do not generalize or remove the current automotive domain model in this change.
- Do not move SArB fixtures into a separate package yet.
- Do not rename the repository directory, Reffy project id, or historical change files.
- Do not add adapters, persistence, networking, live MCP integration, or runtime orchestration.
- Do not provide a compatibility package under `@servco/sarb`; the package is private and pre-release.

## Decisions

### Use Nuveris Core as the implementation identity

The package will be named `@nuveris/core`, and user-facing documentation will call it **Nuveris Core**. “Agentic control plane” remains the descriptive category and “agentic control primitives” remains the name for harness, skill, MCP, governance, handoff, and trace elements.

### Keep SArB as the benchmark identity

Automotive scenarios and fixtures remain in the repository as the SArB reference benchmark. Their automotive vocabulary is not renamed to Nuveris, because Nuveris supplies the core model while SArB supplies the benchmark reality.

### Preserve source-level domain names

Current exported names such as `Scenario`, `HarnessDescriptor`, `SkillDescriptor`, and `McpSurfaceDescriptor` are already neutral. They should not receive a `Nuveris` prefix solely for branding. This avoids needless API churn beyond the intentional package-name change.

### Treat the package rename as breaking

The import specifier changes from `@servco/sarb` to `@nuveris/core`. Because the package is private and version `0.1.0`, no compatibility alias or deprecation release is required. Documentation must state the new import identity consistently.

## Naming Map

| Existing surface | Target surface | Treatment |
| --- | --- | --- |
| `@servco/sarb` | `@nuveris/core` | Rename package metadata and lockfile entry |
| “SArB core” | “Nuveris Core” | Rename reusable implementation identity |
| SArB | Servco Automotive Reality Benchmark | Retain as benchmark identity |
| Automotive service fixture | SArB reference fixture | Retain behavior and automotive vocabulary |
| Agentic control primitives | Agentic control primitives | Retain as generic component vocabulary |

## Migration and Verification

Implementation should search all package, documentation, and planning surfaces for wording that presents SArB as the core. After updates, the build, strict typecheck, and full test suite must pass unchanged. A final search should allow SArB only where it refers to the benchmark, automotive fixtures, historical planning lineage, or the repository-local Reffy identity.

## Reffy Inputs
- agentic-control-primitives-for-sarb.md
- naming-the-agentic-control-layer.md

## Open Questions
- Should SArB fixtures move to a dedicated package after Nuveris supports a second domain benchmark?
- Should the repository itself eventually be renamed or split once package boundaries stabilize?
- Does `@nuveris/core` require registry or organization-scope clearance before publication outside this private project?
