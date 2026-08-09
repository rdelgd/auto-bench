## 1. Planning
- [x] 1.1 Review the reality-validation artifact and current canonical spec.
- [x] 1.2 Update project context with the Lasm–Nuveris–Auto Bench responsibilities and non-goals.
- [x] 1.3 Define the materialized assembly, state-transition, evidence, and evaluation boundaries.
- [x] 1.4 Validate this change before implementation.

## 2. Domain Model
- [ ] 2.1 Add serializable LogicalAssembly slice types for concepts, relations, constraints, events, policies, runtime evaluations, version, and provenance.
- [ ] 2.2 Add explicit operational state, actor observation, state-transition, and outcome types.
- [ ] 2.3 Extend scenarios and control-surface fixtures with assembly/state references and expectations.
- [ ] 2.4 Add validation for assembly reference integrity, minimum provenance, transition contracts, and acceptable/prohibited outcomes.

## 3. Evidence And Evaluation
- [ ] 3.1 Expand normalized evidence event types for assembly use, state transitions, runtime evaluations, outcomes, links, and attribution.
- [ ] 3.2 Implement the new reality-validation dimensions with structured findings and evidence references.
- [ ] 3.3 Keep runtime Lasm evaluation evidence distinct from Auto Bench metaevaluation results.
- [ ] 3.4 Update public exports without adding analytics, ingestion, persistence, or runtime orchestration.

## 4. Fixtures And Verification
- [ ] 4.1 Convert the automotive service fixture into a complete materialized reality-validation episode.
- [ ] 4.2 Add tests for stale/missing assembly meaning, lossy projections, invalid state transitions, unacceptable outcomes, and attribution gaps.
- [ ] 4.3 Run typecheck, build, and the full test suite.
- [ ] 4.4 Validate and review `center-reality-validation-stack`.
- [ ] 4.5 Archive the change only after implementation is shipped and canonical specs can be updated truthfully.
