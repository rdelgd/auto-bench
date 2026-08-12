# Operational Conformance First, Benchmark Second

Status: exploratory
Date: 2026-08-11
Authors: Roberto Delgado, Codex

## Source Snapshot

This artifact began as a synthesis of two primary sources, inspected on 2026-08-11:

- Cognition, “Introducing FrontierCode”: https://cognition.com/blog/frontier-code
- Harbor Framework: https://github.com/harbor-framework/harbor

FrontierCode offered a model for constructing trustworthy evaluations: practitioner-authored tasks, acceptance criteria that extend beyond functional completion, multiple verifier types, hard blockers, alternate valid solutions, repeated trials, and adversarial quality control.

Harbor offered a model for portable execution: separable tasks, datasets, agents, models, container environments, trials, jobs, adapters, and verifier artifacts.

Those ideas remain useful, but the initial synthesis put the benchmark before the source of truth. The more important realization is that Servco does not need an invented external benchmark to tell it what successful automotive operation looks like. Its century of continued operation is already the strongest empirical reference available. The immediate problem is whether the operational reality responsible for that success can be faithfully codified in a LogicalAssembly and expressed, enforced, and evolved through Nuveris.

Any broadly useful benchmark should be a later distillation of that conformance work.

## The Dawning Realization

The original framing asked how Auto Bench could become a real benchmark for agentic systems. That question starts one layer too late.

Servco already contains the relevant reality:

- distinctions experienced practitioners make when a generic workflow description is insufficient;
- relationships among customers, vehicles, appointments, repair orders, parts, warranties, commitments, roles, and systems;
- constraints that separate a legal or acceptable state from a merely convenient one;
- events that the business recognizes as consequential;
- policies that encode commitments, authority, consent, escalation, and customer care;
- evaluations, both formal and tacit, by which people determine whether work was actually done correctly.

The primary task is not to simulate an automotive business well enough to benchmark an agent. It is to discover which parts of this living operational system are load-bearing, compile them into Lasm, project them through Nuveris, and test that those projections still govern agentic action faithfully.

Auto Bench therefore becomes a **conformance bench** before it becomes a benchmark.

## Core Thesis

> Servco's lived operational reality is the reference. Lasm codifies that reality. Nuveris steers agentic proxies within it. Auto Bench tests conformance among the three.

The first-order question is:

> Does the Nuveris–Lasm system preserve the distinctions, authority, commitments, state transitions, and outcomes that make the real process valid?

Only after that question can be answered should a second-order question be asked:

> Can the reusable parts of this conformance corpus be distilled into a benchmark that helps other automotive companies validate agentic proxies against their own complex operational reality?

This reverses the dependency:

1. Operational reality precedes the representation.
2. Lasm is compiled from and reconciled against that reality.
3. Nuveris projects and enforces Lasm for agentic action.
4. Auto Bench tests the fidelity of the compilation, projection, enforcement, and resulting action.
5. A portable benchmark may be distilled from mature, repeatedly validated conformance cases.

The benchmark is an export of the work, not the reason for doing it.

## Survival as Evidence, Not Dogma

Servco's longevity matters because it demonstrates that the operational system as a whole has repeatedly adapted well enough to remain viable. Its processes have encountered real customers, vehicles, regulations, technologies, disruptions, economic cycles, and organizational changes. That history is more meaningful than a benchmark designer's imagined ideal workflow.

Longevity does not prove that every current process is optimal, internally consistent, documented correctly, or worth preserving. Existing practice can include:

- obsolete policy that outlived its rationale;
- local workarounds compensating for system limitations;
- differences between written procedure and effective practice;
- conflicting interpretations across roles or locations;
- accidental complexity that should be removed rather than formalized;
- practices that produced historical success but no longer fit current commitments.

Lasm should not turn inheritance into dogma. It should make operational meaning explicit, sourced, versioned, executable, and contestable. When sources disagree, the disagreement should be represented and resolved by accountable people rather than silently flattened. When a conformance test fails, the possible conclusion is not only that the agent is wrong; the assembly, projection, policy, source system, or process itself may need correction.

This is why reality validation remains a better description than process automation.

## Reassigning the Roles

The layers now have clearer responsibilities:

| Layer | Primary responsibility | Conformance question |
| --- | --- | --- |
| Servco operations | Supply the living source reality and accountable human judgment | What distinctions and outcomes actually make this process valid? |
| LogicalAssembly | Compile load-bearing meaning into concepts, relations, constraints, events, policies, and evaluations | Does the assembly faithfully represent the relevant operational reality? |
| Nuveris | Project that meaning into agent-facing context, capabilities, permissions, approvals, and evidence | Does the control plane expose and enforce the assembly without distortion? |
| Agentic proxy | Perceive, reason, act, clarify, abstain, escalate, and hand off within those surfaces | Does conduct conform to the available meaning and authority? |
| Auto Bench | Exercise the complete binding and locate divergence | Where did reality, representation, projection, conduct, or outcome cease to conform? |
| Derived public benchmark | Package generalized conformance patterns for reuse | Can another company test its proxies against its own automotive reality using the distilled method? |

Auto Bench should not claim that a synthetic episode is more authoritative than the business process from which it was derived. Its authority comes from traceable correspondence with that process and from accountable review of any abstraction.

## The Conformance Model

Conformance is not one comparison. It is a chain of relationships that must hold simultaneously.

### 1. Source conformance

Does the Lasm slice correspond to the operational sources that currently carry meaning?

Relevant sources may include policy, schemas, code, role definitions, system behavior, customer commitments, training material, observed practice, incident history, and practitioner judgment. The assembly should record provenance and unresolved disagreements rather than pretending these sources always align.

### 2. Semantic conformance

Does the assembly preserve the distinctions practitioners depend on?

A model can reproduce familiar vocabulary while collapsing important states, relationships, exceptions, or authorities. Semantic conformance tests whether the representation is usable for the consequential decisions the process actually requires.

### 3. Projection conformance

Do Nuveris surfaces faithfully express the governing Lasm slice?

Skills, prompts, MCP resources and tools, harness context, schemas, permissions, and approval flows are consumer-specific projections. Conformance requires that they neither omit load-bearing meaning nor introduce capabilities and interpretations unsupported by the assembly.

### 4. Behavioral conformance

Does the agentic proxy act within the projected meaning, authority, and process commitments?

The relevant evidence includes what the proxy observed, inferred, asked, selected, changed, refused, escalated, and handed off. Completion is insufficient if the conduct exceeded authority or relied on a false account of reality.

### 5. State-transition conformance

Did consequential actions move the operational system only through permitted states?

This includes intermediate states, reversibility, side effects, downstream commitments, and delayed consequences. A valid-looking terminal state can hide an invalid path or an obligation that will fail later.

### 6. Outcome conformance

Did the resulting reality satisfy the legitimate intent and the business's acceptance envelope?

The answer should come from observable state and attributable evidence, not from the agent's own declaration of success.

### 7. Evolution conformance

When policy, systems, roles, skills, models, or practices change, does the binding remain valid?

Conformance must be rerunnable. Drift detection and version comparison are core requirements because the operational reality is living rather than frozen.

## Auto Bench as a Conformance Harness

Auto Bench should exercise and diagnose this chain. A conformance case is not primarily a challenge question for a model. It is an executable claim about correspondence among reality, Lasm, Nuveris, agent conduct, and outcome.

A case should contain:

1. **Operational provenance:** the process, sources, owners, observations, incidents, and decisions from which the case was derived.
2. **Lasm slice:** the exact concepts, relations, constraints, events, policies, and evaluations required by the case.
3. **Initial state:** the materialized world state, time, actors, actor-specific observations, disagreements, and hidden facts.
4. **Nuveris projection:** the harness configuration, skills, MCP surfaces, permissions, approvals, handoffs, and evidence contract exposed to the proxy.
5. **Intent:** the legitimate goal and explicit constraints presented to the proxy.
6. **Conformance claims:** the semantic distinctions, permitted transitions, prohibited effects, required commitments, and acceptable outcome envelope being tested.
7. **Perturbation:** a stale fact, missing input, conflicting source, tool failure, role boundary, changed policy, delayed effect, or other condition that reveals whether the binding is real.
8. **Evaluations:** deterministic checks, counterfactual checks, practitioner rubrics, evidence requirements, and attribution rules.
9. **Observed episode:** the proxy trace, runtime Lasm evaluations, state history, handoffs, outcome observations, and evaluator results.
10. **Finding:** a location of conformity or divergence in the source, assembly, projection, control surface, proxy, external system, outcome, or evaluator.

The most valuable output is not a leaderboard score. It is a precise finding that tells the organization what part of the binding needs correction.

## What Remains Useful From FrontierCode

FrontierCode's benchmark methods become conformance-quality methods rather than the product thesis.

### Accountable acceptance

“Would the maintainer merge this?” translates more accurately to:

> Would the accountable process owners recognize this Lasm representation, Nuveris projection, agent conduct, and outcome as faithful to the process they are responsible for?

The accountable people should author and review conformance claims. Benchmark specialists can help make those claims executable, but should not invent the operational standard.

### Hard blockers and quality signals

Conformance cases should distinguish:

- **Hard invariants:** authorization, consent, safety, privacy, compliance, ledger integrity, required approvals, prohibited transitions, and binding customer commitments.
- **Quality signals:** clarity, resilience, customer experience, appropriate clarification, evidence quality, handoff quality, human burden, and efficiency.

No quality gain should compensate for violating a hard invariant. Unlike a public leaderboard, however, the internal conformance report should always retain every diagnostic result after a blocker failure.

### Multiple verifier forms

The verifier ensemble still maps well:

| FrontierCode method | Conformance use |
| --- | --- |
| Classical test | Check explicit state, event, policy, or outcome predicates. |
| Command check | Validate schema, system integrity, evaluator execution, and projection generation. |
| Reverse-classical | Confirm that the same evidence or decision rule rejects a seeded invalid state or missing precondition. |
| Adaptive classical | Normalize legitimate variations into canonical Lasm concepts and state claims before deterministic evaluation. |
| Scope check | Detect excess authority, unnecessary system access, overbroad record changes, avoidable cost, or expanded blast radius. |
| Prompt rubric | Let qualified reviewers assess context-dependent fidelity that cannot honestly be reduced to a binary predicate. |

### Adversarial quality control

Each conformance case should be attacked in both directions:

- Can an invalid representation, projection, action, or outcome still pass?
- Can a valid alternate practice fail because the case encodes one preferred path too rigidly?

Calibration traces, alternate valid paths, deliberately incomplete cases, independent review, and repeated agent runs test whether the conformance claim is trustworthy. They are a discipline for validating the validation.

## What Remains Useful From Harbor

Harbor remains a plausible execution substrate, but it is not the source of meaning.

Its separations among tasks, datasets, agents, models, environments, trials, and jobs can help Auto Bench:

- run the same conformance case against different proxies and harnesses;
- isolate synthetic systems and private verifiers;
- repeat stochastic trials;
- collect comparable artifacts;
- package versioned internal suites;
- execute locally or across managed container environments;
- later distribute a sanitized public corpus.

A Harbor adapter should remain outside the Nuveris Core Sans I/O boundary. The core owns serializable Lasm, Nuveris, state, evidence, and conformance models. The adapter materializes those models into runnable environments and translates results back into structured findings.

The container is a laboratory for replay and perturbation. It is not the operational truth. Harbor can make a case portable without proving that the case corresponds to the business.

## Internal Conformance Corpus Before Public Benchmark

The first durable asset should be a private, evolving corpus of conformance cases derived from real processes.

Candidate cases might cover:

- service scheduling involving warranty eligibility, recall work, transportation needs, technician capability, and changing capacity;
- a parts backorder that changes a feasible repair plan after a customer commitment;
- ambiguous symptoms that require safety-aware escalation rather than premature repair certainty;
- customer communication constrained by consent, channel preference, accessibility, and promised follow-up;
- service, parts, and warranty handoffs where actor views or source systems disagree;
- a stale record that must be exposed and reconciled rather than treated as truth;
- pricing, finance, or goodwill decisions constrained by disclosure and authority;
- delayed consequences that reveal an apparently complete episode left an invalid commitment.

These are not initially “questions for agents.” Each is a test of whether a piece of operational reality can survive compilation into Lasm, projection through Nuveris, action by a proxy, and validation against resulting state.

The corpus should grow from:

- practitioner interviews and observed decisions;
- existing procedures, policies, schemas, and application behavior;
- customer and operational incidents;
- recurring exceptions and escalations;
- known source disagreements and workarounds;
- changes that previously caused confusion or regression;
- successful handoffs and recoveries, not only failures.

## Distilling a Public Automotive Benchmark

A suitable benchmark may emerge once conformance cases have demonstrated value internally. The distillation must preserve the structure of the problem without publishing Servco's confidential reality or presenting Servco-specific practice as universal.

A candidate distillation process is:

1. **Prove the case internally.** Establish provenance, practitioner acceptance, valid alternate paths, useful findings, and stable execution.
2. **Identify the transferable structure.** Separate automotive concepts and failure patterns from Servco-specific systems, policies, thresholds, data, and organizational choices.
3. **Create a synthetic organization overlay.** Replace private details with internally coherent fictional policies, source systems, roles, records, and commitments.
4. **Preserve the conformance challenge.** The public case should retain the semantic distinction, authority boundary, state transition, disagreement, or delayed outcome that made the internal case valuable.
5. **Audit the abstraction.** Servco practitioners and, where possible, practitioners from other automotive companies review whether the synthetic case remains realistic without claiming universality.
6. **Attack the evaluator.** Invalid solutions, alternate valid paths, different proxies, and repeated trials expose false positives, false negatives, leakage, and accidental coupling.
7. **Version and publish.** Release the task contract, synthetic Lasm, Nuveris projection, environment, verifier provenance, reporting method, and known limitations.
8. **Support organization substitution.** Make it possible for another company to replace the synthetic overlay with its own Lasm and private conformance cases.

The public benchmark should not ask whether another company conforms to Servco. It should ask whether an agentic proxy can be faithfully steered by a versioned automotive reality, and whether the surrounding system can detect where that steering fails.

## What the Derived Benchmark Could Measure

The portable benchmark could evaluate capabilities such as:

- grounding action in an explicit company-specific reality rather than generic automotive knowledge;
- preserving important distinctions across Lasm projections, skills, MCP surfaces, and harness context;
- respecting role, authority, approval, consent, and policy boundaries;
- reconciling or escalating conflicting sources rather than flattening them;
- operating across multiple systems and actor-specific views;
- selecting only necessary actions and limiting side effects;
- detecting when represented reality is stale or insufficient for action;
- producing attributable evidence for state transitions and outcomes;
- remaining conformant when the model, harness, policy version, or organization overlay changes;
- distinguishing agent failure from assembly, projection, system, or evaluator failure.

This is a more useful benchmark than testing whether a model knows a canonical dealership workflow. It tests whether an agentic system can operate inside a supplied, complex, contestable organizational reality.

## What Can Be Shared

A public Auto Bench distribution could eventually include:

- the conformance-case schema and validation protocol;
- a synthetic automotive LogicalAssembly and organization overlay;
- representative Nuveris skills, MCP surfaces, permissions, and approvals;
- synthetic source systems and stateful episode environments;
- conformance evaluators, counterfactual tests, and attribution formats;
- public scenario families and procedurally generated variants;
- Harbor or other runner adapters;
- task-authoring and adversarial-review guidance;
- reporting conventions for blockers, findings, uncertainty, and evaluator disagreement;
- examples showing how another company substitutes its own private Lasm and overlays.

Servco should be able to retain privately:

- operational data and customer information;
- exact internal policy, thresholds, role boundaries, and system vulnerabilities;
- sensitive incident-derived cases;
- private conformance suites and certification variants;
- details whose publication would create security, privacy, gaming, or competitive risk.

The shared benchmark is therefore a gift of method, structure, and carefully distilled automotive complexity—not an export of Servco's operational internals.

## Measures That Matter Internally

Before public scoring, Auto Bench should report conformance health:

- **Assembly coverage:** which consequential concepts, relations, constraints, events, policies, and evaluations are represented.
- **Evaluative reach:** which Lasm entries are exercised by executable checks and consequential episodes.
- **Projection fidelity:** whether agent-facing surfaces preserve the governing assembly meaning.
- **Invariant preservation:** whether hard constraints survive agentic action.
- **Outcome fidelity:** whether legitimate intent and commitments result in acceptable observable state.
- **Attribution completeness:** whether divergence can be located in the source, assembly, projection, proxy, system, outcome, or evaluator.
- **Alternate-path tolerance:** whether multiple valid practices pass without weakening hard constraints.
- **Drift sensitivity:** whether changes in policy, system behavior, or practice trigger relevant conformance failures.
- **Replacement resilience:** whether organizational meaning survives a change of model, harness, skill projection, or application.
- **Practitioner disagreement:** where accountable people do not yet share one operational interpretation.

These measures make the system improve the organization even if no public benchmark is ever released.

## A Conformance-First Sequence

The next useful sequence is:

1. Select one bounded but consequential automotive process.
2. Identify its accountable practitioners and load-bearing sources.
3. Capture the minimum Lasm slice needed to evaluate the process.
4. Reconcile or explicitly represent disagreements among sources and practice.
5. Generate the Nuveris projections through which a proxy will perceive and act.
6. Author conformance claims, perturbations, evidence requirements, and attribution rules.
7. Replay known-good, known-bad, and legitimate alternate episodes.
8. Run agentic proxies and inspect whether failures reveal problems in the proxy or elsewhere in the binding.
9. Correct the assembly, projections, process, systems, or evaluators as findings require.
10. Only after repeated internal usefulness, attempt a synthetic, portable distillation.

This sequence builds organizational capability first. Benchmark credibility becomes evidence accumulated through the process rather than a branding claim made at the beginning.

## Risks and Boundaries

- **Fossilizing current practice:** conformance must remain sourced and contestable rather than equating “current” with “correct.”
- **Confusing documentation with reality:** a written policy is one source, not automatically the whole operational truth.
- **Overfitting Lasm to one episode:** the assembly should preserve reusable meaning without pretending to model the entire company.
- **Letting Nuveris hide semantic loss:** a polished skill or tool surface can still project the wrong distinction or authority.
- **Treating every failure as agent failure:** source, assembly, projection, process, external system, and evaluator defects must remain first-class findings.
- **Premature generalization:** public schemas should be extracted from several authentic cases rather than imagined before conformance work.
- **Exporting Servco as a universal norm:** other companies need a method for validating their reality, not an obligation to copy Servco's.
- **Losing the valuable difficulty during sanitization:** synthetic cases must retain the semantic and operational structure that made the private case meaningful.
- **Publishing sensitive operational detail:** internal and public corpora require an explicit privacy, security, and competitive-information boundary.
- **Mistaking execution infrastructure for validity:** Harbor can reproduce a case but cannot establish its correspondence with lived operations.

## Decisions Suggested by This Reframing

1. Define Auto Bench first as the conformance harness for the Servco–Lasm–Nuveris binding.
2. Treat Servco's lived processes and accountable practitioners as the source reference, not as subjects awaiting an external benchmark.
3. Make structured divergence findings more important than aggregate agent scores.
4. Use FrontierCode's methods to harden conformance claims and evaluators, not to force the project into a leaderboard product.
5. Use Harbor as an optional runner and distribution substrate outside the core, not as the architecture of operational reality.
6. Build a private conformance corpus before designing a public benchmark corpus.
7. Distill only transferable structure, synthetic automotive reality, and validation methods for public use.
8. Design any derived benchmark so another company can supply its own Lasm and validate its proxies against its own reality.

## Open Questions

- Which Servco process offers the best first test of the full reality-to-Lasm-to-Nuveris-to-outcome chain?
- What evidence is sufficient to say a Lasm entry conforms to lived practice?
- Who has authority to resolve disagreement among policy, system behavior, local practice, and customer commitment?
- How should conformance cases distinguish a tolerated workaround from a legitimate operational rule?
- Which Nuveris projections should be generated mechanically from Lasm, and which require authored interpretation?
- What minimum evaluator reach makes a Lasm slice sufficiently load-bearing for agentic steering?
- How should findings feed changes back into Lasm, Nuveris, source systems, training, or the underlying process?
- When has an internal case matured enough to be distilled safely?
- What aspects of automotive reality are common enough for a public domain pack, and which must always remain organization overlays?
- Can a public benchmark test organization-specific grounding without rewarding memorization of its synthetic overlay?
- Should “Auto Bench” name the internal conformance harness, the derived public benchmark, or the shared protocol encompassing both?

## Working Hypothesis

The central product is not a benchmark imposed on Servco. It is the capability to compile Servco's load-bearing operational reality into Lasm, project and enforce it through Nuveris, and continuously test that agentic conduct and resulting state conform to it.

Auto Bench is the workbench on which that binding is exercised, challenged, diagnosed, and improved.

If this work produces a stable corpus of well-sourced, practitioner-accepted, adversarially hardened conformance cases, then a benchmark can be distilled from it. That benchmark can be shared with other automotive companies as a synthetic reference implementation and validation method. Its purpose would not be to make their proxies conform to Servco, but to help them determine whether their proxies can operate faithfully inside their own complex, versioned, and contestable automotive reality.
