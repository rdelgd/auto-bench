## 1. Implementation
- [ ] 1.1 Initialize the TypeScript project/package structure for SArB.
- [ ] 1.2 Add core domain types for scenarios, intent, business context, harnesses, codified skills, MCP surfaces, trace events, and evaluation results.
- [ ] 1.3 Add pure validation helpers for scenario fixtures, harness descriptors, skill descriptors, MCP descriptors, and traces.
- [ ] 1.4 Add deterministic trace normalization for agentic markers relevant to harnesses, skills, MCP, policy, human confirmation, handoff, and task outcome.
- [ ] 1.5 Add initial rule-based evaluators for intent fidelity, control surface quality, business realism, observability, and governance.
- [ ] 1.6 Add fixture examples showing at least one automotive scenario with an associated harness, skills, MCP primitives, trace events, and evaluation output.
- [ ] 1.7 Keep all core modules Sans I/O; move any filesystem, process, network, clock, or persistence behavior outside the core.

## 2. Verification
- [ ] 2.1 Add unit tests for pure validators, trace normalization, and evaluators.
- [ ] 2.2 Add a fixture-level test that evaluates a complete SArB scenario without any filesystem, network, database, or live MCP dependency inside the core.
- [ ] 2.3 Run TypeScript typechecking and the project test command.
- [ ] 2.4 Validate the change with `reffy plan validate establish-sarb-sans-io-core`.
- [ ] 2.5 Review the ReffySpec files for scope drift before implementation starts.
