## 1. Planning
- [x] 1.1 Review the reality-validation and naming artifacts and the current canonical spec.
- [x] 1.2 Reorient the change from a Lasm–Nuveris–Auto Bench stack to a Lasm–Auto Bench stack.
- [x] 1.3 Define the Lasm package, materialized assembly, projection, state-transition, evidence, and Auto Bench evaluation boundaries.
- [x] 1.4 Validate this change before implementation.

## 2. Lasm Identity And Package
- [x] 2.1 Rename the package from `@nuveris/core` to `@lasm/core` in package metadata and the lockfile.
- [x] 2.2 Replace Nuveris with Lasm in active README, project context, canonical-spec migration inputs, examples, and Reffy workspace metadata while preserving archived ReffySpec history.
- [x] 2.3 Update imports, exports, fixtures, and tests for the Lasm package identity without adding redundant `Lasm` prefixes to domain-driven APIs.
- [x] 2.4 Document the direct import migration and do not add a compatibility alias for the private pre-release package.

## 3. Domain Model And Projections
- [x] 3.1 Add serializable LogicalAssembly slice types for concepts, relations, constraints, events, policies, runtime evaluations, version, and provenance.
- [x] 3.2 Add explicit operational state, actor observation, state-transition, and outcome types.
- [x] 3.3 Treat harness, skill, MCP, prompt, permission, approval, and handoff fixtures as Lasm projections or control surfaces with assembly and state references.
- [x] 3.4 Add validation for assembly reference integrity, minimum provenance, projection references, transition contracts, and acceptable or prohibited outcomes.

## 4. Evidence And Auto Bench Evaluation
- [x] 4.1 Expand normalized evidence event types for assembly use, projections, state transitions, runtime evaluations, outcomes, links, and attribution.
- [x] 4.2 Implement the reality-validation dimensions with structured findings and evidence references that let Auto Bench evaluate the Lasm.
- [x] 4.3 Keep Lasm runtime evaluation evidence distinct from Auto Bench evaluation results.
- [x] 4.4 Update public exports without adding analytics, ingestion, persistence, or runtime orchestration.

## 5. Fixtures And Verification
- [x] 5.1 Convert the automotive service conformance case into a complete materialized Lasm evaluation episode.
- [x] 5.2 Add tests for stale or missing assembly meaning, lossy projections, invalid state transitions, unacceptable outcomes, and attribution gaps.
- [x] 5.3 Assert that active package metadata, documentation, examples, and imports no longer use the Nuveris identity.
- [x] 5.4 Run typecheck, build, and the full test suite.
- [x] 5.5 Validate and review `center-reality-validation-stack`.
- [x] 5.6 Archive the change only after implementation is shipped and canonical specs can be updated truthfully.
