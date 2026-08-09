import type { AgenticEventType } from "./trace.js";

export type AutomotiveDomain =
  | "service"
  | "parts"
  | "sales"
  | "finance"
  | "customer-experience"
  | "inventory"
  | "warranty"
  | "compliance"
  | "operations";

export interface BusinessContext {
  readonly domain: AutomotiveDomain;
  readonly summary: string;
  readonly stakeholders: readonly string[];
  readonly requiredFacts: readonly string[];
  readonly sensitivities: readonly string[];
}

export interface UserIntent {
  readonly explicitGoal: string;
  readonly constraints: readonly string[];
  readonly inferredGoals?: readonly string[];
}

export interface ExpectedControlSurfaces {
  readonly harnessIds: readonly string[];
  readonly skillIds: readonly string[];
  readonly mcpServerIds: readonly string[];
  readonly mcpPrimitiveIds: readonly string[];
}

export interface EvaluationExpectations {
  readonly requiredTraceTypes: readonly AgenticEventType[];
  readonly requiresPolicyCheck: boolean;
  readonly requiresHumanConfirmation: boolean;
}

export interface Scenario {
  readonly id: string;
  readonly title: string;
  readonly businessContext: BusinessContext;
  readonly intent: UserIntent;
  readonly expectedOutcomes: readonly string[];
  readonly expectedControlSurfaces: ExpectedControlSurfaces;
  readonly evaluation: EvaluationExpectations;
}
