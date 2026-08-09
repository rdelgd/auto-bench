# HLE as a Template for a Generalized Reality Benchmark

Status: exploratory
Date: 2026-07-15
Authors: Roberto Delgado, Codex

## Source Snapshot

This artifact synthesizes two supplied resources:

- `~/Downloads/hle.pdf` - *Humanity's Last Exam*, arXiv `2501.14249v10`, dated 2026-02-20. The supplied paper describes HLE as 2,500 multimodal, closed-ended academic questions across more than one hundred subjects.
- https://github.com/RoskiDeluge/hle - Roberto's fork of the HLE repository, inspected at commit `26dca2e253b405105b4c3d8c2f5af06f86f90c66` (2026-02-20). Relevant implementation files are `README.md`, `hle_eval/run_model_predictions.py`, `hle_eval/run_judge_results.py`, and `hle-rolling-changes.txt`.

The paper is the primary source for HLE's intent, collection and review process, and stated results. The repository shows the smaller operational surface actually released for running predictions, judging responses, calculating aggregate metrics, and recording rolling dataset changes.

## Core Thesis

HLE is a useful template for Auto Bench, but not because expert questions can simply be replaced with business questions.

Its most reusable contribution is a benchmark-production system:

> Find a capability frontier, recruit people who possess hard-to-reproduce knowledge, turn that knowledge into evaluable artifacts, filter with current models, peer-review the survivors, protect a held-out set, standardize execution, publish auditable metrics, and keep the benchmark alive through feedback and rolling revisions.

Auto Bench can adopt that system while changing the unit of evaluation. HLE's unit is an isolated question with a short, known answer. A business reality benchmark's unit should be an episode in a stateful process: intent enters a changing environment, multiple actors and systems mediate it, actions create consequences, policy constrains acceptable paths, and success may only become visible downstream.

HLE asks whether a model can produce the right answer. A generalized Auto Bench should ask whether an agentic system can bring about an acceptable business state, through an acceptable process, with calibrated awareness of risk and uncertainty.

## What HLE Demonstrates

### A frontier must be deliberately constructed

HLE responds to benchmark saturation. Its authors did not sample ordinary academic questions and hope they remained difficult. Contributors tested submissions against frontier models before submission. Exact-match questions had to stump all tested models; multiple-choice questions had to stump all but one to allow for guessing. About 70,000 model attempts produced roughly 13,000 candidates for expert review, from which the benchmark was curated.

This produces discriminative headroom, but it also means HLE difficulty is partly conditional on the models used during collection. The paper appropriately cautions that small score changes near zero may not establish real progress.

For Auto Bench, frontier filtering should be one gate, not the definition of realism. A rare workflow that current agents fail may be useful, but benchmark coverage must also reflect representative, consequential, and failure-prone business processes. Otherwise Auto Bench could become an adversarial-agent puzzle set rather than a model of reality.

### Expert provenance is part of the data

HLE collected original questions from nearly 1,000 contributors associated with more than 500 institutions in 50 countries. Submissions included the question, answer specification, detailed rationale, subject, and contributor identity and affiliation. The prize structure and paper authorship made contribution valuable, while attribution created accountability.

The analogue for Auto Bench is practitioner provenance. A high-value workflow fixture may require the tacit knowledge of an experienced service advisor, warranty administrator, controller, compliance specialist, dispatcher, claims adjuster, or other process owner. That knowledge should be represented as reviewable evidence, not flattened into an anonymous prompt.

### Difficulty and quality are different gates

HLE explicitly recognizes that merely stumping models does not make a good question. Candidates passed through an iterative review round with one to three graduate-level reviewers, followed by a selection round conducted by organizers and stronger reviewers. Rubrics screened for precision, originality, genuine expertise, verifiability, formatting, artificial difficulty, and searchability.

For process benchmarks, a parallel review should separate at least four judgments:

- Is this process authentic and materially important?
- Is the scenario difficult for the right reasons?
- Are the acceptable outcomes and prohibited outcomes sufficiently grounded?
- Can independent evaluators reconstruct and score what happened?

### Ground truth remains sociotechnical

Despite HLE's emphasis on unambiguous answers, the paper reports an estimated expert disagreement rate of 15.4% on the public set and about 18% on a targeted biology, chemistry, and health subset. It argues for multiple experts, author rebuttal, and consensus rather than treating one reviewer as an oracle. Post-release refinement included a feedback bounty, manual verification, audits in which reviewers fully solved sampled questions, and removal of easily searchable questions.

Business-process ground truth will likely be more contestable than HLE's. A policy-compliant outcome can still be commercially poor; a customer-friendly exception can still violate authority; two experts may endorse different paths. Auto Bench therefore should preserve reviewer disagreement, rationales, policy versions, and adjudication history rather than force every judgment into a timeless scalar label.

### A benchmark needs both a stable exam and a living edge

HLE keeps public questions and private held-out questions, uses a benchmark canary to discourage training contamination, and proposes HLE-Rolling for fixes and future questions. The supplied fork makes this evolution visible in `hle-rolling-changes.txt` through re-add, remove, and update records keyed by item ID.

The source snapshot itself illustrates why explicit versions matter: the paper and README describe 2,500 questions, while the repository's sample evaluation output uses `n = 2700`. A score without an immutable dataset snapshot, protocol version, model configuration, and change manifest is not fully comparable.

For Auto Bench, the equivalent should be a versioned public development corpus, private certification suites, and a rolling frontier. Organization-sensitive facts may remain private while scenario contracts, evaluators, and aggregate findings remain inspectable.

### Evaluation is a protocol, not just a dataset

HLE standardizes the model response as explanation, answer, and confidence. Its released scripts load a named dataset, execute questions through an OpenAI-compatible chat-completions interface, cache responses by question ID, use a structured model judge to compare predictions with reference answers, and report accuracy plus RMS calibration error. The paper also reports completion-token usage and argues that progress should be compute-efficient.

Confidence is especially important: HLE finds that models are frequently wrong with high confidence. A generalized Auto Bench can carry this insight deeper into the episode by asking for confidence or escalation decisions at consequential choice points, not merely after the final action.

The repository should be treated as a clear reference implementation, not a complete reproducibility standard. It has useful minimalism, but the parsed `--temperature` value is not passed to the model call, behavior is inferred from model-name strings, missing predictions affect the accuracy denominator without a separate availability metric, and automated judge output is asserted as `strict` rather than independently validated. These details reinforce a broader lesson for Auto Bench: the runner, environment, judge, and metrics must themselves be versioned and tested as benchmark artifacts.

## Where the HLE Analogy Ends

HLE deliberately narrows the problem to closed-ended academic capability. Its paper states that high HLE performance would not by itself demonstrate autonomous research or general intelligence. The same boundary is important for Auto Bench.

Real business processes add forms of complexity that isolated questions mostly remove:

- **State:** actions mutate appointments, inventory, financial records, customer commitments, queues, and permissions.
- **Time:** facts expire, deadlines and service levels matter, and outcomes can be delayed.
- **Partial observability:** no actor sees the entire organization, and some data must remain unavailable.
- **Multiple actors:** customers, employees, agents, vendors, regulators, and systems have distinct authority and incentives.
- **Multiple valid paths:** there may be no single reference trace even when some terminal states are clearly unacceptable.
- **Asymmetric consequences:** a small policy breach can matter more than several efficiently completed tasks.
- **Interruption and recovery:** tools fail, humans do not respond, inventory changes, and work crosses shifts or departments.
- **Governance:** permission, consent, segregation of duties, privacy, and auditability are part of correctness.
- **Local variation:** the same process differs across organizations, jurisdictions, product lines, and operating models.
- **Longitudinal effects:** customer trust, rework, downstream cost, and compliance exposure can outlive the benchmark episode.

This suggests that “reality benchmark level” should not mean “a harder collection of business questions.” It should mean that the benchmark preserves enough causal, organizational, temporal, and governance structure for success and failure to resemble their real-world counterparts.

## A Translation From HLE to Auto Bench

| HLE primitive | Generalized reality-benchmark analogue |
| --- | --- |
| Question | Stateful process episode or scenario family |
| Subject | Industry, business capability, process family, role, and jurisdiction taxonomy |
| Prompt text and optional image | Initial world state, artifacts, communications, interfaces, and observations |
| Exact or multiple-choice answer | Acceptable terminal-state set plus prohibited states and invariants |
| Solution rationale | Process rationale, policy basis, evidence requirements, and acceptable path variants |
| Model response | Action trace across agents, humans, tools, skills, systems, and handoffs |
| Correctness judge | Deterministic state checks plus rubric judges and expert adjudication |
| Accuracy | Outcome utility and hard-gate pass rate |
| Confidence | Decision-level calibration, escalation quality, and abstention quality |
| Subject expert | Practitioner, process owner, risk owner, customer advocate, or regulator-domain expert |
| Model difficulty filter | Baseline-agent challenge run across multiple harness and tool configurations |
| Private split | Confidential workflow variants, hidden facts, and held-out perturbations |
| HLE-Rolling | Versioned process packs with additions, corrections, retirements, and policy drift |
| Canary | Provenance markers, access controls, secret rotation, and contamination audits |

## Three Ways To Use HLE as a Template

These directions are compatible, but each emphasizes a different product identity for Auto Bench.

### 1. Auto Bench as a curated corpus of “last-mile” workflows

In this interpretation, Auto Bench closely adopts HLE's contributor and review pipeline. Practitioners submit processes that are consequential, tacit-knowledge-heavy, and difficult for current agents. Each contribution includes:

- a process objective and why it matters;
- the initial state and information visible to each actor;
- the systems, skills, tools, permissions, and policies available;
- hidden facts, expected disturbances, and ambiguity;
- acceptable outcomes, prohibited outcomes, and non-negotiable invariants;
- evidence needed to score the run;
- known valid paths and instructive failure paths;
- contributor provenance, sensitivity classification, and review history.

Baseline agents attempt the scenario, but expert review determines whether failures reveal meaningful capability gaps. The corpus is stratified so that frontier difficulty does not crowd out common high-impact processes.

This is the most direct path from the current automotive fixture toward a substantial benchmark dataset. Its main risk is creating impressive episodes without a sufficiently reusable execution model.

### 2. Auto Bench as a domain-neutral benchmark protocol with domain packs

In this interpretation, the primary artifact is a portable contract rather than a central dataset. The current Sans I/O core becomes the beginning of a domain-neutral kernel:

- **Benchmark kernel:** actors, intent, state, observations, actions, tools, permissions, policies, events, outcomes, evidence, evaluators, and versions.
- **Domain pack:** automotive service, insurance claims, healthcare administration, logistics, procurement, finance operations, or another process family.
- **Organization overlay:** Servco-specific systems, policy versions, role boundaries, terminology, and private scenario parameters.

The kernel should stop encoding automotive as a type-level assumption; automotive becomes the first proving domain and reference pack. A scenario contract should support multiple valid traces and evaluate the observed trace against state transitions and invariants.

This direction best supports generalization beyond Servco while preserving the value of deep local realism. Its main risk is premature abstraction: the kernel should be extracted from several authentic domains, not designed solely from imagined universality.

### 3. Auto Bench as a federated reality-benchmark program

In this interpretation, Auto Bench defines how organizations create, operate, and compare private or semi-private reality benchmarks. Public assets include the schema, runner protocol, evaluator tests, synthetic reference packs, and reporting standard. Organizations retain sensitive process data and private certification suites, but can publish aggregate capability profiles or run third-party audits.

An HLE-like contribution and governance program could support:

- practitioner authorship and incentives;
- multi-role review, including process, risk, and customer perspectives;
- adversarial and counterfactual variants;
- private test pools and periodic rotation;
- feedback bounties and incident-driven scenario additions;
- rolling change manifests and score migration guidance;
- cross-organization benchmark exchanges using sanitized scenario shells.

This is the strongest route to “reality benchmark level,” because much of business reality cannot be published safely or reduced to one company's ontology. Its main risk is comparability: federation requires a strict protocol for versions, evaluator quality, confidentiality, and which aggregate scores are legitimately comparable.

## A Candidate Hybrid Shape

The three directions suggest a layered benchmark rather than a choice between a dataset and a framework:

1. A domain-neutral episode and trace kernel.
2. Public domain packs with synthetic but practitioner-audited workflows.
3. Organization overlays containing real policies, systems, and private variants.
4. A curated frontier set chosen through multi-agent filtering and expert review.
5. A stable certification snapshot alongside a rolling challenge set.

The current Auto Bench concepts already map to part of this structure: user intent, harnesses, skills, MCP surfaces, policy checks, human confirmations, handoffs, evidence, traces, and structured evaluation dimensions. Generalization would require adding explicit world state and transitions, actor-specific observations and authority, temporal constraints, perturbations, acceptable outcome sets, hard invariants, evaluator provenance, and benchmark/protocol versions.

## Candidate Scoring Shape

A single accuracy number would hide the most important business failures. A generalized scorecard could combine:

- **Hard gates:** authorization, consent, safety, privacy, compliance, ledger or state integrity, and other invariants. A critical violation cannot be averaged away.
- **Outcome quality:** whether the intended business state was reached, including partial and delayed outcomes.
- **Intent fidelity:** whether explicit constraints and legitimate inferred goals survived the process.
- **Process quality:** policy adherence, evidence use, handoffs, sequencing, and avoidance of unnecessary side effects.
- **Resilience:** recovery from missing information, tool failure, changing state, and human delay.
- **Calibration:** confidence, abstention, clarification, and escalation at consequential decisions.
- **Human burden:** interventions, confirmations, corrections, and avoidable escalations.
- **Efficiency:** time, cost, tokens, tool calls, rework, and opportunity cost, reported only after hard constraints are met.
- **Observability:** whether the result can be reconstructed and attributed from the trace.

Scores should be reported by process family and difficulty axis, with uncertainty and evaluator disagreement, before any composite is offered. The benchmark should distinguish capability failure, runtime failure, tool failure, policy denial, and evaluator uncertainty.

## Difficulty Without Losing Reality

HLE selects for questions current models cannot answer. Auto Bench can preserve frontier pressure while defining difficulty across independent axes:

- number of roles and handoffs;
- amount of hidden, conflicting, stale, or sensitive information;
- process duration and delayed consequences;
- tool and system heterogeneity;
- policy density and permission boundaries;
- frequency and severity of disturbances;
- ambiguity in intent or acceptable outcomes;
- cost of error and reversibility of actions;
- novelty across organizations, industries, and jurisdictions.

A scenario family can vary one or more axes while holding the underlying business intent constant. Held-out evaluation can then test transfer to a new organization overlay, process variant, policy version, or industry rather than merely test recall of a public episode.

## Open Questions

- What is the smallest episode contract that can represent both automotive scheduling and a materially different business process without erasing important differences?
- Which hard invariants should be universal, and which belong only in a domain or organization overlay?
- How should Auto Bench validate evaluator reliability when expert disagreement is expected and outcomes may be delayed?
- What mix of deterministic state checks, simulation, model judging, and human adjudication is acceptable for certification?
- How should representative operational frequency, business consequence, and frontier-agent difficulty be balanced when selecting scenarios?
- Can private organization overlays produce comparable aggregate results without exposing confidential policy, customer, employee, or system data?
- What constitutes contamination when agents can legitimately search documentation, learn skills, or retain experience across episodes?
- Should a benchmark reward discovery of a process defect, even when following the documented process would have produced the nominal expected state?
- When does a scenario become obsolete because the underlying policy, system, or organization changed?
- What evidence would justify renaming or reframing Auto Bench once automotive becomes one domain pack rather than its defining boundary?

## Working Hypothesis

HLE can serve as a template for the social and technical machinery of Auto Bench: frontier construction, expert contribution, peer review, held-out tests, standardized execution, calibration, audit, and rolling maintenance.

The generalization move is to replace HLE's closed-ended question with a versioned, stateful process episode and replace its single correct answer with an evidence-backed envelope of acceptable outcomes and paths. Servco automotive should remain the first deep proving ground, while the benchmark kernel is gradually separated from the automotive domain pack and Servco-specific overlay.

If that separation works across several genuinely different processes, Auto Bench could evolve from a Servco-specific automotive benchmark into a reusable method for measuring whether agentic systems can operate inside reality, not merely answer questions about it.
