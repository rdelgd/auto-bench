## 1. Package and Documentation Migration
- [x] 1.1 Rename the package from `@servco/sarb` to `@nuveris/core` in `package.json` and the lockfile.
- [x] 1.2 Update the package description and root README to present the implementation as Nuveris Core.
- [x] 1.3 Document SArB as the automotive reference benchmark built with Nuveris.
- [x] 1.4 Update `.reffy/reffyspec/project.md` so future planning distinguishes Nuveris Core from SArB.
- [x] 1.5 Review source, test, and example naming; change only surfaces that incorrectly identify the reusable core as SArB.

## 2. Compatibility and Scope
- [x] 2.1 Preserve existing exported TypeScript domain names and evaluator behavior.
- [x] 2.2 Keep the automotive fixture intact as the SArB reference benchmark.
- [x] 2.3 Confirm no filesystem, network, process, database, clock, persistence, or live MCP behavior enters the core.
- [x] 2.4 Document the package import migration from `@servco/sarb` to `@nuveris/core`; do not add a compatibility alias.

## 3. Verification
- [x] 3.1 Run strict TypeScript typechecking and the complete test suite.
- [x] 3.2 Search package and documentation surfaces for stale uses of SArB as the reusable core identity.
- [x] 3.3 Validate the change with `reffy plan validate rename-sarb-core-to-nuveris`.
- [x] 3.4 Review the pivot for scope drift into domain generalization or runtime architecture changes.
