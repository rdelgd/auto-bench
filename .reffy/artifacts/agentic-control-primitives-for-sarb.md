# Agentic Control Primitives for SArB

Status: exploratory
Date: 2026-07-14
Authors: Roberto Delgado, Iden Watanabe, Codex

## Source Notes

This artifact captures an emerging thesis about agents, harnesses, skills, MCP, analytics, and how those ideas may reshape the purpose of SArB, originally imagined as the Servco Automotive Reality Benchmark.

Relevant external references:

- Agent Skills: https://agentskills.io/home
- Model Context Protocol: https://modelcontextprotocol.io/docs/getting-started/intro
- MCP architecture: https://modelcontextprotocol.io/docs/learn/architecture

## Core Thesis

The agent is becoming a dominant abstraction for mediated interaction: not only human-to-machine interaction, but also a growing share of human-to-human coordination when one or more sides are represented by agentic proxies.

If that is true, then the meaningful unit to benchmark is not only the model response, tool result, or task outcome. It is the full agentic abstraction through which intent is expressed, constrained, delegated, transformed, executed, observed, and audited.

## Observations

Tools such as Codex, Claude Code, and OpenCode are better understood as harnesses for the agent abstraction rather than the agent abstraction itself. A harness is the runtime or product surface that frames the agent's interaction loop: workspace access, tool permissions, approval flows, context loading, transcript shape, invocation modes, and handoff boundaries.

Agent Skills appear to be more than reusable instruction bundles. They are emerging as control surfaces for agent behavior: discoverable, versionable, portable directories that define procedural knowledge, workflow constraints, supporting scripts, references, and assets.

MCP similarly turns external systems into standardized agent-facing surfaces. Its core primitives, especially tools, resources, and prompts, define what an agent can discover, read, invoke, or reuse. This makes MCP a protocol-level affordance for controlling what actions and context are available to an agent.

Together, harnesses, skills, and MCP begin to resemble platform primitives. HTML and JavaScript put web interaction and programmability into user-controllable artifacts. Harnesses, skills, and MCP may do something similar for agentic systems: they make parts of agent behavior inspectable, composable, portable, and governable outside the opaque model call.

As adoption standardizes around these primitives, they also become natural places for agentic analytics. The most valuable behavioral data may shift from clicks, page views, and form submissions toward markers such as selected harnesses, harness permissions, selected skills, activated instructions, tool discovery, tool calls, resource reads, prompt templates, permission gates, retries, refusals, delegations, and user confirmations.

In that world, intent is increasingly mediated by agentic abstractions. The behavioral data that matters is no longer just what the user did directly, but what the user attempted to delegate, what the agent inferred, what primitives were available, which primitives were selected, and where execution succeeded, failed, or required human intervention.

## Implication For SArB

SArB can be reframed from a benchmark of automotive business realism into a benchmark of agentic mediation inside an automotive business reality.

The question becomes:

> Can SArB represent, measure, and compare how well agentic abstractions handle the messy intent, context, controls, permissions, handoffs, and outcomes that occur in a real automotive business?

This suggests that SArB should not only model dealership, service, parts, sales, finance, customer experience, compliance, and operational workflows. It should also model the agent-facing control layer over those workflows.

## Possible SArB Role

SArB could track the agentic abstraction itself as a first-class benchmark object:

- The user intent entering the system.
- The agent role or proxy acting on that intent.
- The harness mediating the agent's workspace, permissions, tools, approvals, and interaction loop.
- The skill or workflow bundle activated.
- The MCP servers and primitives exposed at that moment.
- The tools/resources/prompts discovered.
- The selected calls, inputs, outputs, and intermediate state.
- The permissions, policy checks, and human confirmations encountered.
- The business context used or missed.
- The operational result produced.
- The trace of where user intent was preserved, distorted, expanded, or blocked.

This could make SArB useful not only for evaluating whether an agent completes a task, but for evaluating whether the agentic control layer is legible, governable, analyzable, and aligned with the business environment.

## Candidate Benchmark Dimensions

Intent fidelity:

- Did the agent preserve the user's actual business goal across skills, tools, and handoffs?
- Did the agent distinguish explicit instructions from inferred intent?
- Did the agent ask for clarification when intent was underspecified?

Control surface quality:

- Did the harness provide the right context, permissions, approval boundaries, and interaction affordances?
- Were the relevant skills discoverable and activated at the right time?
- Were tool/resource/prompt boundaries clear enough for the agent to choose correctly?
- Did the available primitives create useful guardrails or dangerous affordances?

Business realism:

- Did the task require cross-functional context, such as customer history, inventory, warranty, scheduling, compliance, pricing, or operational policy?
- Did the benchmark include realistic ambiguity, missing data, conflicting incentives, and permissions?

Observability:

- Can an evaluator reconstruct why a skill or tool was used?
- Can analytics identify the difference between user intent, agent inference, harness behavior, policy constraint, and system capability?
- Can traces be compared across agents or versions?

Governance:

- Can harnesses, skills, and MCP surfaces be versioned, reviewed, approved, and rolled back?
- Can harness configuration, permissions, and approval flows be inspected and compared?
- Can sensitive actions require explicit policy or human confirmation?
- Can benchmark runs expose unsafe tool availability, overbroad resources, or weak prompt boundaries?

## Agentic Markers To Capture

Potential event markers:

- `intent.submitted`
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
- `intent.fidelity_assessed`

These markers would let SArB compare agents not only by final answer quality, but by how they navigated the agentic surface area.

## Open Questions

- Is SArB primarily a benchmark dataset, a simulation environment, an observability schema, or a combination of all three?
- What automotive workflows are complex enough to reveal the value of tracking harnesses, skills, and MCP primitives?
- Should SArB define canonical harness fixtures, skills, and MCP servers as part of the benchmark fixture?
- How much of the benchmark should measure business outcome versus control-layer legibility?
- What does a "good" agentic trace look like in Servco's actual operating context?
- Can SArB become a way to evaluate the quality of agent-facing abstractions before they are deployed into production workflows?

## Working Hypothesis

SArB may be most valuable if it treats the agentic abstraction as part of the business reality being benchmarked.

The benchmark should not only ask whether an agent can complete realistic automotive tasks. It should ask whether the harnesses, skills, MCP primitives, policies, traces, and analytics around that agent make the work controllable, inspectable, and improvable.
