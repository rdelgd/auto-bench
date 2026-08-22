# Lasm: Agentic Control Primitives

Status: exploratory
Date: 2026-07-14
Authors: Roberto Delgado, Iden Watanabe, Codex

## Source Notes

This artifact captures the emerging **Lasm** thesis: agents are surrounded by an inspectable control plane composed of harnesses, skills, MCP surfaces, governance boundaries, and evidence. These surfaces are projections through which a LogicalAssembly binds agent action to an organization's operational reality rather than merely recording agent activity. The artifact also explores how this thesis may reshape the purpose of Auto Bench, Servco's automotive conformance workbench.

“Agentic control plane” remains a descriptive category, and “agentic control primitives” names its composable elements. Lasm names the overall thesis, semantic model, and reusable library.

Relevant external references:

- Durable Forms, Chapter 7, “Anatomy of a LogicalAssembly”: https://roskideluge.github.io/durable-forms/07-anatomy-of-a-logicalassembly.html
- Agent Skills: https://agentskills.io/home
- SkillOpt: https://github.com/RoskiDeluge/SkillOpt
- Model Context Protocol: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP architecture: https://modelcontextprotocol.io/docs/learn/architecture

## Core Thesis

The agent is becoming a dominant abstraction for mediated interaction: not only human-to-machine interaction, but also a growing share of human-to-human coordination when one or more sides are represented by agentic proxies.

If that is true, the central problem is not simply how to capture and analyze agent behavior. Generic analytics platforms can extend familiar telemetry primitives to sessions, tool calls, latency, errors, and agent funnels. Those signals are useful, but they do not establish whether the agent understood the world correctly, acted within the organization's meaning and authority, or produced an acceptable real-world state.

The more durable focus is **reality validation**: testing the relationship between the organization's represented operational reality, the agent's interpretation of it, the action taken, and the state that results. This has two directions. The represented reality must remain sufficiently true and current to support action, and agent behavior must remain faithful to that reality while transforming it.

The subsequent Durable Forms work identifies what this stack must preserve: the organization's own distinctions, relationships, legal states, meaningful changes, commitments, and criteria for successful behavior. Agentic control without an explicit substrate of organizational meaning can make action governable while still allowing the wrong meaning to be governed efficiently.

> The Lasm–Auto Bench stack validates whether agents perceive, preserve, and act within an organization's operational reality—and whether that represented reality remains fit for action.

Here, **operational reality** does not mean an exhaustive digital twin or a claim to timeless objective truth. It means the smallest sourced, versioned, and contestable set of meanings, states, constraints, authorities, events, and expected outcomes needed to judge a consequential episode.

## Observations

Tools such as Codex, Claude Code, and OpenCode are better understood as harnesses for the agent abstraction rather than the agent abstraction itself. A harness is the runtime or product surface that frames the agent's interaction loop: workspace access, tool permissions, approval flows, context loading, transcript shape, invocation modes, and handoff boundaries.

Agent Skills appear to be more than reusable instruction bundles. They are emerging as control surfaces for agent behavior: discoverable, versionable, portable and trainable* directories that define procedural knowledge, workflow constraints, supporting scripts, references, and assets.

<!-- * The SkillOpt method (.reffy/artifacts/skillopt.pdf) implements this.  https://github.com/RoskiDeluge/SkillOpt -->

MCP similarly turns external systems into standardized agent-facing surfaces. Its core primitives, especially tools, resources, and prompts, define what an agent can discover, read, invoke, or reuse. This makes MCP a protocol-level affordance for controlling what actions and context are available to an agent.

Together, harnesses, skills, and MCP begin to resemble platform primitives. HTML and JavaScript put web interaction and programmability into user-controllable artifacts. Harnesses, skills, and MCP may do something similar for agentic systems: they make parts of agent behavior inspectable, composable, portable, and governable outside the opaque model call.

As adoption standardizes around these primitives, they become natural sources of telemetry. Large analytics and observability platforms are well positioned to capture generic agent activity by extending infrastructure already used for web, application, and system analytics. Lasm and Auto Bench should not compete to become a universal agent-analytics layer.

Telemetry remains necessary, but as evidence rather than purpose. The stack should capture only enough to determine which reality and policy versions governed an episode, what the agent perceived and inferred, which capabilities and approvals were available, what action occurred, how state changed, and where any divergence can be attributed. Dashboards and aggregate analysis may be derived from that evidence or supplied by other platforms; they are not the organizing thesis.

### Logical Assemblies As The Semantic Substrate

The Durable Forms esssay proposes a **LogicalAssembly** (Lasm) as an explicit, maintained representation of the domain meaning on which an organization acts. It is composed of six kinds of entry:

- **Concepts** define the distinctions the organization depends on.
- **Relations** define how those concepts compose.
- **Constraints** define the invariants of a legal domain state.
- **Events** define the changes the organization recognizes as meaningful.
- **Policies** define commitments about what action should occur, under what conditions, and with whose authority.
- **Evaluations** execute checks of behavior against the other five components and identify where a failure occurred.

The sixth component changes the character of the artifact. Concepts, relations, constraints, events, and policies can otherwise decay into another ontology or knowledge base. Evaluations make selected meaning load-bearing: consequential action is checked against it, divergence fails visibly, and the failure can be traced to a specific semantic entry. This also supplies a disciplined scoping rule. An entry belongs in the assembly when an executable evaluation depends on it; meaning with no evaluative consumer is either deliberately excluded or remains documentation rather than infrastructure.

A LogicalAssembly has four important properties for agentic systems:

- It is a **target, not a source**: meaning is compiled and reconciled from schemas, code, policy documents, and observed practice rather than authored as a universal model from scratch.
- It is **runtime-independent**: the organization's meaning does not belong to one application, vendor, model, or agent harness.
- It is **enforced**: evaluations gate consequential behavior instead of merely describing preferred behavior.
- It is a **narrow waist**: many sources of meaning compile inward, while prompts, skills, application models, reports, and other consumer-specific projections derive outward.

Agents make this substrate newly urgent and newly sustainable. A human reader often supplies an organization's tacit codebook between a message and an action. An agent can consume a representation and act without that interpretive step. Semantic drift therefore becomes an operational error with a cost, timestamp, trace, and owner. The same fact creates the maintenance loop: if an agent's action can be attributed to the assembly entry and projection it consulted, stale meaning produces a concrete failure signal rather than a quietly aging document.

### Relationship Between Lasm And Auto Bench

Lasm and Auto Bench should be treated as complementary responsibilities rather than competing names for the same system:

| Layer | Primary responsibility | Representative surfaces |
| --- | --- | --- |
| Lasm | Define and continuously test the organization's load-bearing operational reality, then project it into agent-facing action | Concepts, relations, constraints, events, policies, runtime evaluations, harnesses, skills, MCP surfaces, permissions, approvals, handoffs, traces |
| Auto Bench | Evaluate whether the Lasm remains faithful across realistic automotive episodes | Scenarios, fixtures, perturbations, evidence, findings |

A Lasm projects its LogicalAssembly through agent-facing control surfaces. A skill may encode a workflow over assembly concepts and policies; an MCP primitive may expose actions and resources typed by those concepts; a harness may enforce assembly-derived constraints and approvals; and a trace may record which assembly version, entries, projections, and evaluations shaped an action.

The two uses of **evaluation** should remain distinct. A Lasm evaluation is part of the operational enforcement loop: it gates or checks behavior against maintained organizational meaning. An Auto Bench evaluation judges whether the agent, the Lasm's projections, and the resulting business episode preserved intent and meaning and produced an acceptable outcome. Auto Bench may reuse Lasm evaluations as evidence, but it should not reduce conformance to whether runtime gates happened to pass.

## Implication For Auto Bench

Auto Bench can be reframed from a benchmark that merely resembles automotive business reality into a benchmark that validates an agentic system against it.

The question becomes:

> Can Auto Bench determine whether an agentic system perceived the right automotive reality, preserved its meaning and authority boundaries, changed it acceptably, and left enough evidence to locate divergence?

This suggests that Auto Bench should model a scoped, versioned slice of dealership, service, parts, sales, finance, customer experience, compliance, and operational reality together with the Lasm projections through which an agent encounters and changes it.

## Possible Auto Bench Role

Auto Bench could track the evidence chain between represented reality, agent conduct, and resulting reality:

- The user intent entering the system.
- The LogicalAssembly version and domain slice governing the episode.
- The concepts, relations, constraints, events, and policies relevant to that intent.
- The consumer-specific projections derived from the assembly.
- The agent role or proxy acting on that intent.
- The harness mediating the agent's workspace, permissions, tools, approvals, and interaction loop.
- The skill or workflow bundle activated.
- The MCP servers and primitives exposed at that moment.
- The tools/resources/prompts discovered.
- The selected calls, inputs, outputs, and intermediate state.
- The permissions, policy checks, and human confirmations encountered.
- The runtime evaluations invoked, their results, and the semantic entries they address.
- The business context used or missed.
- The operational result produced.
- The trace of where user intent was preserved, distorted, expanded, or blocked.

This could make Auto Bench useful not only for evaluating whether an agent completes a task, but for validating whether the reality model was fit for action, whether the agent remained grounded in it, and whether the resulting state is both acceptable and explainable.

## Candidate Benchmark Dimensions

Intent fidelity:

- Did the agent preserve the user's actual business goal across skills, tools, and handoffs?
- Did the agent distinguish explicit instructions from inferred intent?
- Did the agent ask for clarification when intent was underspecified?

Semantic fidelity:

- Did the agent and its projections preserve the relevant organizational distinctions and relations?
- Did actions respect assembly constraints and policies and recognize the right domain events?
- Can a semantic failure be attributed to an assembly entry, a projection, agent inference, or control-plane behavior?
- Would the same meaning remain enforceable if the model, harness, or application were replaced?

Reality-model validity:

- Was the governing LogicalAssembly slice current, internally coherent, and supported by identifiable operational sources?
- Were disagreements among schemas, code, policy, and observed practice reconciled or exposed rather than silently flattened?
- Did the episode reveal stale, missing, or incorrectly scoped organizational meaning?

State and outcome validity:

- Did the agent perceive the relevant initial state accurately enough to act?
- Did each consequential action produce a permitted state transition?
- Was success established from observable business state and evidence rather than the agent's own completion claim?
- Were delayed effects, side effects, and unacceptable terminal states detected?

Control surface quality:

- Did the harness provide the right context, permissions, approval boundaries, and interaction affordances?
- Were the relevant skills discoverable and activated at the right time?
- Were tool/resource/prompt boundaries clear enough for the agent to choose correctly?
- Did the available primitives create useful guardrails or dangerous affordances?

Reality coverage:

- Did the task require cross-functional context, such as customer history, inventory, warranty, scheduling, compliance, pricing, or operational policy?
- Did the benchmark include realistic ambiguity, missing data, conflicting incentives, and permissions?

Evidence and attribution:

- Can an evaluator reconstruct why a skill or tool was used?
- Can evidence distinguish user intent, represented reality, agent inference, harness behavior, policy constraint, system capability, action, and outcome?
- Can a failure be located in the reality model, its projection, a control surface, agent conduct, an external system, or the evaluation itself?
- Can traces be compared across agents or versions?

Governance:

- Can harnesses, skills, and MCP surfaces be versioned, reviewed, approved, and rolled back?
- Can harness configuration, permissions, and approval flows be inspected and compared?
- Can sensitive actions require explicit policy or human confirmation?
- Can benchmark runs expose unsafe tool availability, overbroad resources, or weak prompt boundaries?
- Are consequential assembly entries covered by executable evaluations rather than only documentation?
- Can assembly sources, reconciliations, versions, projections, and evaluation reach be reviewed and audited?

## Evidence Markers For Reality Validation

These markers are a candidate minimum evidence contract for validation, not a universal agent-analytics schema:

- `intent.submitted`
- `lasm.version_selected`
- `lasm.projection_loaded`
- `lasm.entry_consulted`
- `lasm.evaluation_requested`
- `lasm.evaluation_passed`
- `lasm.evaluation_failed`
- `lasm.divergence_detected`
- `lasm.failure_attributed`
- `state.observed`
- `state.transition_proposed`
- `state.transition_committed`
- `state.transition_rejected`
- `agent.role_selected`
- `harness.selected`
- `harness.configured`
- `harness.context_loaded`
- `harness.permission_requested`
- `harness.permission_granted`
- `harness.permission_denied`
- `skill.discovered`
- `skill.activated`
- `skill.reference_loaded`
- `mcp.server_connected`
- `mcp.primitives_listed`
- `mcp.tool_selected`
- `mcp.tool_called`
- `mcp.resource_read`
- `mcp.prompt_used`
- `policy.check_requested`
- `policy.check_passed`
- `policy.check_failed`
- `human.confirmation_requested`
- `human.confirmation_received`
- `handoff.created`
- `task.completed`
- `task.failed`
- `outcome.observed`
- `outcome.validated`
- `evidence.linked`
- `intent.fidelity_assessed`
- `reality.validation_assessed`

These markers should exist only where they help Auto Bench establish reality, conduct, state transition, outcome, or attribution. Broader product analytics can consume the same evidence or collect additional telemetry elsewhere.

## Non-Goals

- Build a general-purpose agent analytics, engagement, funnel, or dashboard product.
- Define a universal taxonomy for every agent interaction.
- Replace telemetry, tracing, or observability infrastructure supplied by harness vendors and analytics platforms.
- Centralize every organizational data source or construct an omniscient digital twin.
- Treat operational reality as singular, timeless, or uncontested; benchmark reality should be scoped, versioned, sourced, and capable of representing disagreement.
- Measure activity merely because it is measurable. Evidence earns inclusion by supporting a validation or attribution decision.

## Open Questions

- Is Auto Bench primarily a benchmark dataset, a reality-validation protocol, a simulation environment, or a combination of all three?
<!-- I'm leaning toward a combination of all three. See ideas here for reference: .reffy/artifacts/hle-template-for-a-generalized-reality-benchmark.md -->
- Should an Auto Bench fixture carry a complete LogicalAssembly slice, or only stable references to the entries and projections exercised by the episode?
<!-- only stable references -->
- What minimum evaluative reach makes a LogicalAssembly slice sufficiently load-bearing for benchmark use?
<!-- as complete as possible reach given the use case as revealed through use. load-bearing is a property that is discovered, even when it's confidently asserted in the beginning -->
- How should Auto Bench distinguish a stale assembly entry from a lossy projection, incorrect agent inference, or weak Lasm control surface?
<!-- Lasm should never be a weak control surface. It's definition is as the most authoritative projection of business reality, thus Auto Bench should assume lossy projections or incorrect inferences, never a "weak" Lasm -->
- Which Lasm evaluations should run as hard gates during an episode, and which should remain benchmark observations?
<!-- The most load bearing are the gates, everything else is a benchmark observation -->
- Can model, harness, skill, or application replacement serve as a practical test that organizational meaning is genuinely runtime-independent?
<!-- sure, but weighted properly as something that lives in code and needs to be validated in the real world -->
- What is the minimum evidence Auto Bench must own, and what generic telemetry should it accept from external platforms?
<!-- Auto Bench at a minimum needs to see evidence that load bearing agent actions are included in the telemetry, or derived from it -->
- What automotive workflows are complex enough to reveal failures of reality representation, agent grounding, state transition, or outcome validation?
<!-- At Servco, the overall data strategy is to decompose the data of the business into 360 domains. Each of those domains, or the equivalents in other businesses, should contain complex workflows with sufficient complexity -->
- Should Auto Bench define canonical harness fixtures, skills, and MCP servers as part of the benchmark fixture?
<!-- No, these aspects will become commodified or incorporated into protocols -->
- How much of the benchmark should measure business outcome versus control-layer legibility?
<!-- Business outcome is what matters. The benchmark should just measure that -->
- What does a "good" agentic trace look like in Servco's actual operating context?
<!-- To be determined -->
- Can Auto Bench become a way to evaluate the quality of agent-facing abstractions before they are deployed into production workflows?
<!-- That's the idea. As more agentic experiences are either built in-house or sold to Servco (or any business) there will be demand for precisely an evaluation of agent-facing abstractions -->

## Working Hypothesis

The Lasm–Auto Bench stack is a reality-validation system.

A Lasm defines a scoped, versioned, and executable representation of the operational reality on which action depends, projects that meaning into agent perception and capability, governs consequential action, and produces attributable evidence. Auto Bench subjects the Lasm to realistic automotive episodes and determines whether the reality model remained fit, the agent remained faithful to it, and the resulting state was acceptable.

Analytics is a derived use of the evidence, not the product thesis. The stack succeeds when it can say what reality governed an action, whether that reality and action were valid, what changed, and exactly where correction is needed.
