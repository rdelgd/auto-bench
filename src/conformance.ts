import type { HarnessDescriptor } from "./harness.js";
import type { LogicalAssemblySlice } from "./lasm.js";
import type { McpSurfaceDescriptor } from "./mcp.js";
import type { ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation } from "./operational-state.js";
import type { Scenario } from "./scenario.js";
import type { SkillDescriptor } from "./skill.js";
import type { RawTraceEvent } from "./trace.js";

export interface ConformanceCase {
  readonly assembly: LogicalAssemblySlice;
  readonly scenario: Scenario;
  readonly initialState: OperationalState;
  readonly observations: readonly ActorObservation[];
  readonly transitions: readonly StateTransitionExpectation[];
  readonly outcomes: readonly OutcomeExpectation[];
  readonly harnesses: readonly HarnessDescriptor[];
  readonly skills: readonly SkillDescriptor[];
  readonly mcpSurfaces: readonly McpSurfaceDescriptor[];
  readonly trace: readonly RawTraceEvent[];
}
