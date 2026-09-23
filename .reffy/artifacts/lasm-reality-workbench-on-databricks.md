# A Lasm Reality Workbench on Databricks

Status: exploratory
Date: 2026-09-17
Authors: Roberto Delgado, Codex

## Prompt

Explore how an application inspired by Databricks Genie Workbench could support the monitoring, auditing, and optimization of a Lasm implementation on the Databricks platform.

The motivating interpretation is that Lasm behaves like a **type definition of a business context**: a maintained, executable account of the concepts, relations, constraints, events, policies, evaluations, state, and authority that make a bounded part of business reality intelligible and actionable. It is adjacent to an ORM analogy, but the thing being mapped is broader than relational data.

## Source Snapshot

This exploration was informed by the following repository sources, inspected on 2026-09-16 and revised against the updated Servco direction on 2026-09-17:

- Revised Servco ontology conversational ledger: `servco-ontology-ledger-2.md`
- Genie Workbench repository and README: https://github.com/databricks-solutions/databricks-genie-workbench
- Genie Workbench architecture: https://github.com/databricks-solutions/databricks-genie-workbench/blob/main/docs/docs/getting-started/architecture-overview.md
- Genie Workbench Auto-Optimize design: https://github.com/databricks-solutions/databricks-genie-workbench/blob/main/docs/docs/features/auto-optimize.md

Genie Workbench is a Databricks App for creating, scanning, monitoring, and benchmark-optimizing Genie Agents. Its most transferable ideas are:

- one portfolio view over many governed artifacts;
- a fast deterministic readiness scan distinct from expensive behavioral evaluation;
- history, comparison, and organization-wide monitoring;
- benchmark-driven optimization using snapshots, bounded patch attempts, full reevaluation, acceptance gates, durable audit state, and rollback;
- Databricks-native composition across Apps, Unity Catalog, SQL Warehouses, Lakeflow Jobs, Lakebase, Model Serving, and platform authorization;
- a deliberate distinction between interactive user actions and privileged background work.

The useful analogy is not that a Lasm is a Genie Agent. It is that a Lasm may need the same kind of **lifecycle workbench** once it becomes operational infrastructure.

## Core Idea

> A Lasm Reality Workbench would be the control room in which domain stewards and platform teams inspect, test, release, monitor, contest, and improve the executable type definition of a business reality.

The workbench would not own the operational reality and would not replace Auto Bench. The responsibilities would remain:

| Layer | Responsibility |
| --- | --- |
| Operational reality | Supplies living sources, observed state, practice, commitments, disagreement, and accountable human judgment |
| Lasm | Compiles that reality into a sourced, versioned, contestable, executable business-context type and projects it into agent-facing surfaces |
| Auto Bench | Exercises the Lasm through consequential episodes and locates divergence among source, representation, projection, conduct, transition, and outcome |
| Lasm Reality Workbench | Makes the Lasm lifecycle operable: registry, inspection, monitoring, audit, evaluation orchestration, candidate optimization, review, release, and rollback |

The Workbench is therefore an adapter and operational surface around `@lasm/core`, not a reason to move persistence, networking, orchestration, or UI concerns into the Sans I/O library.

## Lasm as a Business-Reality Type System

The ORM analogy is productive if its limits stay explicit.

An object-relational mapper binds program objects to a storage representation. A Lasm would bind a business context to multiple kinds of operational representation and behavior:

- schemas and records that materialize state;
- policies and commitments that constrain action;
- application code and workflows that implement transitions;
- practitioner judgment and observed practice that reveal uncodified distinctions;
- skills, prompts, MCP tools, permissions, approvals, and application surfaces that project meaning to an agent;
- runtime evaluations and Auto Bench cases that make the type executable and testable.

A more exact description may be:

> Lasm is a versioned business-reality type system and mapping layer: many operational sources compile inward to one contestable logical assembly, while many consumer-specific projections compile outward from it.

This suggests several familiar type-system operations:

| Type-system idea | Lasm interpretation |
| --- | --- |
| Type declaration | Concepts, relations, constraints, events, policies, evaluations, provenance, and state contracts |
| Type checking | Structural validation plus runtime evaluation against a materialized assembly and state |
| Compilation | Reconciliation of source reality into a LogicalAssembly and generation of consumer-specific projections |
| Usage site | An agent, skill, tool, application, workflow, policy gate, or human decision surface governed by a projection |
| Compile error | Invalid references, unresolved required meaning, contradictory hard constraints, or an unbuildable projection |
| Runtime error | A prohibited transition, failed policy/evaluation, missing authority, or observed divergence during an episode |
| Schema migration | An explicitly reviewed change from one assembly version to another, including projection and case impact |
| Backward compatibility | Whether existing projections, cases, commitments, and valid operational paths remain supported |
| Type coverage | How much consequential behavior is actually addressed by evaluations and exercised through cases |

The analogy should not imply that one static model is objective truth. A business-reality type is scoped, sourced, versioned, and contestable. It may preserve disagreements and conditional interpretations until accountable owners resolve them.

## Relationship to Databricks' Native Semantic Surfaces

The Workbench should not create a parallel semantic registry when a Databricks-native primitive already carries the relevant meaning authoritatively.

| Native surface | Relationship to a Lasm |
| --- | --- |
| Data 360 primary tables | Materialized state and analytical contracts that may serve as Lasm sources, not the whole operational reality |
| Unity Catalog Metric Views | Governed KPI computations and dimensions that can implement or project specific Lasm concepts and relations |
| Domains and Pages | Business-domain scope, terminology, curation, and qualitative semantics that can serve as governed source or projection material, subject to current platform access and data-handling limits |
| Genie One | A workspace-wide analytical consumption surface through which governed semantic context is used |
| Genie monitoring and benchmark behavior | Evidence about whether analytical interpretations are working, not proof that the broader Lasm conforms |
| Skills, direct client MCP connections, Apps, and workflows | Other consumer-specific projections of business meaning, capability, and authority |

Lasm's distinct contribution is the wider binding: sources and definitions are connected to constraints, recognized events, authority, permitted state transitions, expected outcomes, runtime evaluations, agent-facing projections, and conformance evidence. The Workbench would reference and test Databricks-native semantic assets rather than copy their definitions into a second catalog.

Certification, popularity, query usage, and inferred authority can help prioritize sources, but they do not establish that a computation, interpretation, action, or business outcome is correct. They remain provenance and ranking evidence inside a broader conformance decision.

Databricks Domains are also permission boundaries, while a Lasm bounded context is a semantic and operational boundary. They may align, but the Workbench should not assume a one-to-one mapping. Cross-context collisions such as the two meanings of “TLE” need explicit context maps, translations, owners, and conformance cases rather than a global winner produced by merging definitions.

Pages currently require additional caution as a source surface: the ledger records that they are beta, lack a public authoring API, and are unsuitable for sensitive content under the current storage and replication constraints. A Workbench should reference safe Page content and its certification state without treating Pages as the canonical store for private policies, incidents, commitments, or episode evidence.

## Servco Operating-Model Constraints

The ontology work establishes several constraints that should shape the Workbench from the beginning:

### Native-first correction

Jidoka is the governing principle: meaning should be corrected in the most authoritative native layer instead of patched repeatedly in downstream prompts, skills, dashboards, or apps.

The Workbench should therefore implement failure routing, not merely patch generation:

| Finding | Preferred correction target |
| --- | --- |
| Defective material state or analytical contract | Data 360 primary table or its producing data process |
| Incorrect KPI semantics or computation | Domain-specific Metric View |
| Missing qualitative term or contextual distinction | Domain/Page or another approved governed semantic surface |
| Incorrect source selection or analytical interpretation | Genie One context behavior or its governed inputs |
| Procedural interaction or presentation behavior | Skill, app, or other consumer projection |
| Invalid authority, event, transition, or outcome rule | Lasm assembly/evaluation plus the accountable operational source |
| Faulty conformance claim | Auto Bench case or evaluator |

Lasm should record and test the binding across these layers, not become the place where every defect is permanently duplicated. Any custom gap-filler should be deletable when the native layer acquires the missing capability. The Workbench should actively identify duplicated semantic instructions that can be retired after an upstream correction.

### Existing lifecycle and system of record

Servco's current build lifecycle is:

> Nominate → Prioritize → Define → Specify expected behavior → Implement → Validate and publish

Post-publication evaluation and monitoring are a separate intake loop. JSM is the system of record for both nominated work and findings returned for revision, certification, or retirement.

The Workbench can supply evidence, execute checks, prepare candidate diffs, and update linked workflow state, but it should not establish a competing approval queue or semantic change process. A Workbench finding should link to or create the appropriate JSM intake record; an accepted change should traverse the existing six stages before release.

### Genie One consolidation

Servco's strategy consolidates analytical behavior in Genie One, scoped by domain, and removes standalone Genie Agents from the target operating model. Inspiration from Genie Workbench is methodological—portfolio scanning, monitoring, benchmarks, durable optimization history—not an architectural proposal to introduce another fleet of Genie Agents.

### Direct connector topology and infrastructure restraint

Servco has abandoned the proposed centralized AI Gateway strategy. Each consuming surface, such as Claude or ChatGPT, will instead connect directly to Databricks through its own client-specific MCP endpoints. The accepted operational cost is duplicated connection management; the avoided cost is owning gateway middleware that harness vendors are likely to absorb into their platforms.

The Workbench should honor that decision rather than becoming a gateway by another name. It may inventory and test connections, but each connector remains an independently deployed projection boundary with its own endpoint, caller identity, permissions, exposed operations, version, health, and audit evidence. A gateway-like connector name is not evidence of a shared control plane or common capabilities.

This changes the status of connection diagnostics. A connector-helper surface may be durable operational tooling under the direct-connection model rather than temporary cutover scaffolding. Its implementation should still remain thin and replaceable as client platforms gain native connection and identity support.

### Guardrails as historical evidence

The sales intelligence skill is a useful source of “negative requirements”: each special instruction testifies to a failure or gap that once required compensation. The Workbench should help classify every guardrail as one of:

- a business definition to migrate upstream into a governed semantic surface;
- a data-engineering workaround to retire after the underlying defect is fixed;
- genuinely consumer-specific behavior that remains in the projection;
- a regression or conformance case that should survive even after the instruction is removed.

This turns prompt and skill cleanup into observable projection-debt reduction without discarding the failure knowledge those artifacts accumulated.

## Translation from Genie Workbench to a Lasm Workbench

| Genie Workbench pattern | Lasm Workbench analogue |
| --- | --- |
| Genie Agent portfolio | Registry of Lasm domains, assemblies, versions, owners, projections, and deployment environments |
| IQ readiness scan | Deterministic assembly-health scan for provenance, reference integrity, evaluative reach, projection coverage, release hygiene, and evidence readiness |
| Agent detail | Assembly explorer showing entries, sources, state contracts, projections, evaluations, and impacted cases |
| Conversation monitoring | Episode and evidence monitoring across the business actions governed by a Lasm version |
| Native benchmark corpus | Auto Bench conformance cases with known-good, known-bad, perturbation, and legitimate alternate-path episodes |
| Auto-Optimize | Bounded candidate improvement loop over assembly entries, projections, evaluators, or cases, with regression checks and accountable approval |
| Scan and optimization history | Immutable history of health snapshots, conformance runs, findings, proposed patches, decisions, releases, and rollbacks |
| Quick fixes | Low-risk mechanical repairs such as broken references or incomplete metadata; semantic changes remain reviewed proposals |
| Agent config diff and revert | Assembly/projection/evaluation diff, compatibility analysis, controlled promotion, and version rollback |

The separation between fast scan and behavioral evaluation is especially valuable. A structurally healthy assembly can still encode stale or incorrect reality, just as a well-configured agent can still answer business questions incorrectly.

## The Three Operating Loops

### 1. Monitor the binding

Monitoring should answer whether the currently released Lasm is still connected to the reality, consumers, and operational episodes it is meant to govern.

Candidate signals include:

- **Source freshness:** current, stale, disputed, unreachable, or changed since the assembly version was approved.
- **Assembly integrity:** valid references among concepts, relations, constraints, events, policies, and evaluations.
- **Projection version skew:** production skills, prompts, tools, schemas, and applications still using an older or unexpected assembly projection.
- **Connector drift:** a direct client connection's endpoint, effective identity, permissions, supported operations, or projected Lasm version differs from its approved contract.
- **Evaluation reach:** load-bearing entries with no runtime gate, check, or Auto Bench case.
- **Episode usage:** which assembly version, entries, projections, and evaluations actually shaped consequential activity.
- **Evidence completeness:** whether intent, initial state, authority, action, transition, outcome, and attribution can be reconstructed.
- **Conformance trend:** blockers, warnings, regressions, recurring divergences, and legitimate alternate paths rejected by the current model.
- **Operational drift:** source-system, policy, role, workflow, or practice changes that invalidate assumptions in the released assembly.
- **Outcome drift:** increasing cases in which runtime gates pass but observed business outcomes fail Auto Bench expectations.
- **Semantic-authority drift:** popular inferred snippets or query patterns gaining influence despite conflicting with certified definitions or validated computations.
- **Projection debt:** business definitions duplicated in downstream skills, prompts, and apps after an authoritative upstream representation exists.

This is not generic agent observability. Telemetry belongs here only when it can support a conformance, drift, coverage, or attribution decision.

### 2. Audit meaning and change

An audit should reconstruct not only what an agent did, but what account of reality authorized and shaped the action.

For any consequential episode, the Workbench should be able to answer:

1. What legitimate intent entered the system?
2. Which Lasm domain and exact version governed the episode?
3. Which source versions supported the relevant assembly entries?
4. Which projections were available, and which were actually consulted?
5. What operational state was observed, by whom, and with what visibility limitations?
6. Which permissions, policies, runtime evaluations, approvals, and handoffs applied?
7. What transition was proposed and what transition was committed?
8. What outcome was observed, and how was it validated?
9. If the episode diverged, was the defect in a source, assembly, projection, proxy, external system, outcome observation, or evaluator?
10. Who accepted, rejected, waived, superseded, or rolled back the relevant change?

The same auditability should apply to the Lasm itself:

- version-to-version semantic diff;
- source additions, removals, version changes, and status changes;
- impact analysis over projections, state fields, runtime evaluations, and Auto Bench cases;
- author, reviewer, accountable domain owner, decision rationale, and evidence;
- release environment and effective period;
- exceptions, waivers, unresolved disputes, and planned review dates;
- linked JSM intake, build-lifecycle stage, and post-publication evaluation finding;
- rollback target and evidence that rollback completed coherently.

An activity log is insufficient. The durable object is an **evidence-linked chain of meaning, authority, action, outcome, and change**.

### 3. Optimize without inventing reality

Genie configuration can be improved against a benchmark corpus. Lasm optimization is more sensitive because the candidate being changed is an authoritative account of business reality.

The safe optimization unit is therefore a **candidate hypothesis**, never an automatically accepted new truth.

A bounded loop could be:

1. Snapshot the released assembly, projections, evaluation descriptors, case corpus, and source references.
2. Select a concrete finding or objective: uncovered policy, stale projection, recurring misattribution, false-positive gate, rejected alternate path, poor outcome, or excessive human burden.
3. Diagnose the smallest plausible change location: source reconciliation, assembly entry, projection, runtime evaluator, Auto Bench case, or external process.
4. Propose one bounded candidate patch with rationale and cited evidence.
5. Run structural validation and compatibility checks.
6. Replay the affected cases, then the full regression corpus.
7. Compare blockers, outcome fidelity, alternate-path tolerance, evidence completeness, and human burden against the current release.
8. Reject and record the candidate if it violates an invariant, improves only a proxy metric, or lacks adequate evidence.
9. Present a diff and impact report to accountable domain reviewers and route the finding into the linked JSM intake.
10. If accepted, send the candidate through the existing six-stage build lifecycle; publish a new version only after its required validation and approval, retaining the prior release as a rollback target.

Unlike a simple hill-climbing score, acceptance should be lexicographic:

1. No new hard-invariant violation.
2. No unsupported expansion of authority or modeled truth.
3. No unacceptable regression in previously valid episodes or alternate paths.
4. Demonstrable improvement in the targeted conformance problem.
5. Sufficient provenance, evidence, and accountable approval.

A composite health score may help sort a portfolio, but it should never hide blockers or collapse contested meaning into false precision.

## Candidate Workbench Surfaces

The likely product genre is an **analytic repository**: an overview for triage, with hierarchical drill-down into exact evidence, versions, and cases. It should optimize for domain stewards, control owners, platform engineers, and Auto Bench authors rather than executives alone.

A managed AI/BI dashboard could publish a read-only portfolio summary, but the full Workbench is justified as a custom Databricks App by its governed drill-down, run control, review actions, and change preparation.

### Portfolio

A stratified overview of all Lasm domains:

- released version and environment;
- accountable owner and review status;
- current blockers, warnings, and unresolved disputes;
- source freshness and projection skew;
- evaluative reach and latest Auto Bench outcome;
- open candidate changes and approvals;
- freshness timestamp and exact data source for every headline measure.

The title should state the operational message, such as “Two production Lasm domains have source drift; one governs active projections.” Status color should be semantic and redundant with text or icons.

### Assembly Explorer

A navigable contract view for one LogicalAssembly:

- concepts, relations, constraints, events, policies, and evaluations;
- provenance graph and source status;
- referenced operational-state fields;
- inbound dependencies and outward projections;
- runtime and Auto Bench evaluation coverage;
- owners, disputes, and review decisions.

The primary representation should be structured tables and dependency views, not an ornamental ontology graph. Exact lookup, filtering, and traceability matter more than visual spectacle.

### Reality and Source Drift

A work queue showing changed, stale, disputed, or unobserved sources and the assembly entries they support. A source change should not automatically rewrite the assembly; it should open an impact assessment with accountable owners.

### Projection Matrix

A matrix of assembly entries and state fields against each skill, prompt, direct client MCP connection, application, permission boundary, and approval flow. It should expose:

- client, endpoint, authentication mode, effective caller, permission scope, and supported operations for each connection;
- expected versus observed projection version;
- required meaning omitted from a surface;
- capabilities not supported by the governing assembly;
- production usage of deprecated projections;
- relevant cases and findings.

### Conformance Runs

An Auto Bench run view with:

- baseline or candidate assembly version;
- episode and perturbation;
- hard invariants and quality signals;
- state-transition timeline;
- runtime evaluation results as evidence;
- Auto Bench findings by attribution;
- known-good, known-bad, and alternate-path comparison;
- links to exact evidence rather than only aggregate scores.

### Episode Audit

A chronological evidence narrative from submitted intent through validated outcome. The interface should allow an auditor to pivot from any event to the governing assembly entry, source, projection, authority decision, state transition, or finding.

### Change Studio

A controlled diff-and-review experience for candidate assembly, projection, evaluator, and case changes:

- side-by-side semantic and structural diff;
- source citations and proposed rationale;
- dependency and compatibility impact;
- targeted and full-regression results;
- approval requirements and reviewer comments;
- prepare for lifecycle promotion, reject, supersede, or initiate a controlled rollback.

### Ask the Lasm

A conversational surface could help a steward ask:

- “Which policies governing loaner vehicles have no hard gate?”
- “What changed in the service-scheduling reality model since the last accepted release?”
- “Why was this appointment transition rejected?”
- “Which production skills still project the prior warranty interpretation?”
- “Show the evidence behind this divergence attribution.”

The assistant should query the Workbench's governed registry and evidence model, not improvise business reality. Each answer should disclose the signed-in identity, sources, freshness, generated query or retrieval path, relevant Lasm version, and an AI-generated/verify warning. It may prepare candidate changes, but it should not silently mutate an assembly or approve its own proposal.

This would be an administrative and conformance assistant, not a new standalone Genie Agent. Ordinary governed analytical questions should remain in Genie One. The Workbench surface earns its existence only for lifecycle operations Genie One does not own: version inspection, evidence attribution, conformance runs, impact analysis, and controlled change preparation.

## Candidate Databricks Architecture

The Genie Workbench composition offers a plausible reference architecture, with different canonical boundaries.

| Databricks capability | Candidate Lasm Workbench responsibility |
| --- | --- |
| Databricks App | OBO-aware React/AppKit workbench for portfolio, exploration, audit, runs, and controlled review actions |
| `@lasm/core` service adapter | Deserialize assemblies and evidence, run pure validation/evaluation, and return structured results |
| Unity Catalog + Delta | Durable registry indexes, immutable version manifests, evaluation runs, findings, evidence references, releases, approval references, and audit records |
| Unity Catalog Volumes or Git-backed workspace assets | Canonical serialized assembly, projection, case, and evaluator artifacts when file form is preferable to normalized tables |
| SQL Warehouse | Portfolio analytics, coverage analysis, drift queries, system-table joins, and reporting |
| Lakeflow Jobs | Scheduled scans, source comparison, projection checks, Auto Bench execution, regression suites, candidate evaluation, and reporting/audit stages |
| Lakebase | Optional low-latency application state such as sessions, drafts, work queues, stars, and cached read models; not the canonical Lasm or audit ledger |
| Model Serving | Candidate diagnosis, source summarization, steward assistance, and patch proposal under explicit evidence and approval constraints |
| MLflow tracing | Optional pointers to agent and model traces that support episode evidence and attribution; not the sole conformance record |
| Unity Catalog system tables | Supporting evidence for access, lineage, query, job, compute, and cost behavior where it bears on a Lasm finding |
| DABs and Git | Environment promotion, reviewable infrastructure/configuration changes, reproducible jobs, and release automation |
| Direct client MCP endpoints | Per-consumer access to Databricks or approved external systems, modeled with explicit client, endpoint, identity, capability, permission, and health metadata |
| JSM through an approved direct integration surface | Authoritative intake and lifecycle record linked from findings, candidates, reviews, and releases |

Two identities should remain explicit:

- **On-behalf-of user identity** for browsing governed material and requesting or approving changes according to the user's own permissions.
- **Application service principal** for scheduled scans and controlled background jobs against explicitly granted resources.

The service principal's broader access must never substitute for checking whether the requesting person is authorized to view, propose, approve, release, or roll back a particular Lasm domain.

Direct connectors add another identity boundary: the effective caller may be a human on whose behalf the client acts, the Workbench service principal, or a connector-specific credential. Every connector-derived observation should therefore record the client, endpoint, authentication mode, effective principal, and permission scope. It should not infer authority from the connector's display name.

Connector capabilities must also be discovered and governed per client. A working Atlassian read/write connection does not establish that another client or an ontology endpoint can read, enumerate, author, or certify the same resources. Until a specific connection supports those operations, the Workbench should use explicit links, import/export artifacts, and human workflow rather than simulate unsupported authoring access.

The Workbench may supply a shared diagnostic and conformance view over these connections, but it should not proxy all client traffic or own centralized credential routing. That would recreate the retired gateway architecture and concentrate authority the direct-connection decision intentionally leaves distributed.

Unity Catalog can retain immutable evidence that an approval occurred and exactly what content it covered, while JSM remains authoritative for workflow status, ownership, and lifecycle progression.

## Candidate Durable Records

The exact physical model remains open, but the Workbench likely needs durable concepts equivalent to:

- Lasm domain and ownership;
- immutable assembly version and content digest;
- assembly entry and provenance source;
- projection identity, version, target, and release status;
- connector client, endpoint, authentication mode, effective principal, permission scope, capability snapshot, and observed health;
- runtime evaluation descriptor and implementation reference;
- Auto Bench case and corpus version;
- scan snapshot and health finding;
- evaluation run, episode, transition, outcome, and evidence reference;
- divergence finding and attribution;
- candidate patch, impact report, regression result, and reflection;
- approval decision, waiver, release, rollback, and supersession;
- JSM request identity and lifecycle-stage references;
- deployed consumer and observed version.

Canonical artifacts should be content-addressed or digested so an audit can establish that the evaluated, approved, released, and used values were identical.

## A Workbench Health Model

A deterministic scan could report a profile rather than one opaque score:

| Dimension | Example checks |
| --- | --- |
| Source fitness | Ownership, locators, current/stale/disputed status, review age, version identity, unresolved disagreement |
| Assembly integrity | Unique IDs, valid cross-references, coherent addressed entries, complete required metadata |
| Semantic accountability | Named owners, rationale, contestability, decision records, explicit scope |
| Evaluative reach | Load-bearing entries addressed by gates/checks and exercised by Auto Bench cases |
| Projection fidelity | Required references present, unsupported capability absent, deployed version matches release, each direct connector matches its approved identity and capability contract |
| Evidence readiness | Required intent, state, action, authority, transition, outcome, and attribution markers available |
| Conformance quality | Hard blockers, outcome fidelity, alternate-path tolerance, perturbation sensitivity, attribution completeness |
| Evolution safety | Compatibility analysis, regression coverage, approval state, release and rollback readiness |

Any portfolio score should be derived from these inspectable checks. Hard blockers should remain visible regardless of the aggregate.

## A Four-Stage Improvement Job

Borrowing the useful shape of Genie Workbench's durable multi-stage optimizer, a Lasm improvement run could be:

1. **Intake and Snapshot** — validate scope, authorization, objective, current release, corpus version, and rollback material.
2. **Evidence and Case Quality** — verify source availability, finding quality, evaluator validity, counterexamples, and leakage between expected outcomes and agent-visible projections.
3. **Candidate and Conformance** — propose bounded hypotheses, validate them, replay targeted cases, then run the full corpus without mutating the released Lasm.
4. **Report, Route, and Audit** — produce the semantic diff and impact record; link or create the JSM evaluation intake; record the complete terminal reason; never publish a semantic change directly from the optimization run.

Every stage should exchange durable state by run ID. A failed or abandoned run should remain intelligible without relying on ephemeral task output.

If the candidate is accepted for implementation, the separate six-stage build lifecycle owns definition, implementation, validation, approval, and publication. This preserves the ledger's deliberate separation between building governed meaning and evaluating it after publication.

## Important Differences from Genie Optimization

Several limits prevent a direct copy of the Genie Workbench model:

- **Configuration quality is not reality truth.** A benchmark improvement cannot by itself authorize a change to business meaning.
- **The target is multi-part.** A failure may require changing a source reconciliation, assembly, projection, evaluator, case, process, or external system.
- **Expected answers can leak.** Auto Bench outcome expectations and private verifier logic must not be projected into the acting agent's context.
- **Alternate valid practices matter.** Optimization must avoid tightening a case around one preferred path when several conformant paths exist.
- **Blockers dominate averages.** A gain in efficiency or answer quality cannot compensate for an authorization, safety, consent, compliance, or commitment violation.
- **Human authority is part of the type.** Domain-owner review is not merely a deployment ceremony; it is evidence about which interpretation is accountable.
- **Rollback may not reverse reality.** A Lasm version can be rolled back, but business actions already committed under it may require reconciliation rather than technical reversion.

## Two Complementary First Slices

A useful technical reference slice would remain narrow:

1. Register the existing service-scheduling LogicalAssembly fixture and its projections.
2. Persist immutable assembly and corpus versions with digests and owners.
3. Implement deterministic health checks from the existing `@lasm/core` validation and evaluation contracts.
4. Show one portfolio row and one assembly detail surface.
5. Run the existing service-appointment Auto Bench case as a Databricks job adapter.
6. Persist the run, findings, and evidence references in Unity Catalog.
7. Add a version diff and a human-reviewed candidate change flow.
8. Seed one source-drift perturbation, one lossy-projection perturbation, and one legitimate alternate path.
9. Demonstrate that the Workbench attributes each failure differently and never treats a passing runtime gate as proof of overall conformance.

This would test the Workbench mechanics without first building an organization-wide ontology browser or general agent-observability platform.

The first Servco-facing proving slice should align with the already selected net new-vehicle unit/stock-type KPI work rather than create a competing pilot. That slice has known guardrails, an emerging benchmark bank, domain-specific Metric View intent, JSM lifecycle ownership, and a production analytical consumer. It would test native-first correction, semantic authority, expected-behavior specification, and post-publish evaluation.

The two slices answer different questions:

- **Service scheduling** tests the full Lasm thesis around authority, consequential events, state transitions, outcomes, and attribution.
- **Net new-vehicle units/stock type** tests whether the Workbench complements Servco's actual Databricks ontology lifecycle without duplicating it.

## Possible Later Capabilities

- estate-wide detection of which deployed agentic surfaces depend on which Lasm versions;
- source-to-assembly and assembly-to-projection lineage;
- automatic generation of candidate Auto Bench cases from incidents and recurrent exceptions;
- counterfactual replay against proposed policy or projection changes;
- promotion gates for agentic applications that require passing domain-specific conformance suites;
- cross-domain composition for episodes spanning multiple 360 domains;
- comparison of conformance across models, harnesses, and projection implementations;
- per-client connector conformance and drift comparison without centralizing connector traffic or credentials;
- a sanitized public benchmark export that preserves conformance structure without exposing Servco reality;
- a steward assistant that converts interviews and source changes into cited candidate patches and tests.

## Non-Goals

- Make the Workbench the source of business truth.
- Treat Unity Catalog metadata or a data model as the complete operational reality.
- Recreate native Metric View, Domain, Page, Genie One, or JSM responsibilities in a parallel registry or workflow.
- Reintroduce standalone Genie Agents into Servco's target analytical architecture.
- Build or operate a centralized MCP gateway for external client connections.
- Build a universal agent analytics product.
- Collapse Lasm runtime evaluation and Auto Bench evaluation into one score.
- Allow an LLM or optimizer to publish business meaning without accountable approval.
- Reward benchmark gains that violate hard invariants or narrow legitimate alternate practices.
- Move Databricks-specific I/O, persistence, jobs, or authentication into `@lasm/core`.
- Model the whole company before proving one consequential domain slice.

## Open Questions

- Is “Lasm Reality Workbench” the right product name, or should Auto Bench itself be the user-facing workbench while Lasm remains the evaluand?
- Is a separate Workbench justified before exhausting Genie One, native monitoring, Unity Catalog, JSM, and emerging Databricks ontology capabilities?
- What is the canonical serialized form of a Lasm release: JSON artifact, normalized Delta model, both, or a Git-authored source compiled to both?
- Which sources can be mechanically monitored for drift, and which require scheduled practitioner attestation?
- How are disputed sources and competing valid interpretations represented without producing an unusable union type?
- What makes a Lasm change backward-compatible when its consumers include humans, agents, tools, policies, and stateful workflows?
- Which assembly entries are “load-bearing” enough to require hard gates, and how is that status discovered and revised?
- How should projection fidelity be measured when the projection is natural-language instruction rather than a typed interface?
- What exact evidence proves that a deployed skill, prompt, or tool used the released projection rather than merely claiming its version?
- How should connector contracts and conformance evidence be normalized across clients whose MCP endpoints, identity models, and operation sets differ?
- Which optimization targets are safe for mechanical quick fixes, and which always require domain-owner judgment?
- Should candidate changes branch at the whole-assembly level or at independently releasable domain slices?
- How are cross-domain episodes evaluated when two Lasm domains disagree about shared concepts or authority?
- How should Lasm bounded contexts map to permission-bearing Databricks Domains, including many-to-one and cross-domain cases?
- What retention, privacy, and access boundaries apply to incident-derived cases and episode evidence?
- Can the same Workbench support both private operational conformance and later public benchmark distillation without weakening either boundary?

## Working Hypothesis

The Genie Workbench pattern reveals a plausible missing operational layer for Lasm: not another semantic-model editor and not another observability dashboard, but a governed lifecycle environment for **business-reality types**.

Its defining loop would be:

> observe living reality and deployed use → detect drift or divergence → locate the authoritative correction layer → route an evidence-backed finding into the existing lifecycle → replay conformance cases → release through accountable review → monitor the binding again.

If that loop works for one consequential Servco domain, the result would make the Lasm thesis tangible on Databricks. The organization would be able to see not only what its agents and systems are doing, but which explicit version of business reality made those actions intelligible, permissible, testable, and revisable.
