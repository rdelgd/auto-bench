import { evaluateBenchmark, type BenchmarkInput } from "../evaluate.js";
import type { HarnessDescriptor } from "../harness.js";
import type { McpSurfaceDescriptor } from "../mcp.js";
import type { Scenario } from "../scenario.js";
import type { SkillDescriptor } from "../skill.js";
import type { RawTraceEvent } from "../trace.js";

export const serviceAdvisorHarness: HarnessDescriptor = {
  id: "harness.service-advisor",
  name: "Service Advisor Workflow Harness",
  purpose: "Mediates customer scheduling work with scoped dealership-system access.",
  interactionMode: "interactive",
  contextSurfaces: [
    { id: "context.customer-request", description: "Materialized customer request", sensitivity: "sensitive" },
    { id: "context.service-policy", description: "Service scheduling policy", sensitivity: "internal" },
  ],
  affordances: ["read appointment availability", "propose an appointment", "request customer confirmation"],
  permissionModel: {
    defaultLevel: "read-only",
    scopedPermissions: ["appointments:read", "appointments:create"],
  },
  approvalFlow: {
    requiredFor: ["create customer appointment"],
    approverRoles: ["customer"],
  },
  handoffBoundaries: ["service advisor handles warranty exceptions"],
};

export const serviceSchedulingSkill: SkillDescriptor = {
  id: "skill.schedule-service",
  name: "Schedule Service",
  purpose: "Collects required vehicle context and schedules a policy-compliant service visit.",
  applicability: ["customer requests routine automotive service"],
  capabilities: ["verify scheduling prerequisites", "select an eligible appointment", "request confirmation"],
  references: [
    { kind: "instruction", name: "SKILL.md" },
    { kind: "reference", name: "service-scheduling-policy.md" },
  ],
};

export const dealershipOperationsMcp: McpSurfaceDescriptor = {
  id: "mcp.dealership-operations",
  name: "Dealership Operations",
  purpose: "Exposes scoped dealership scheduling primitives to agents.",
  resources: [
    {
      id: "resource.vehicle-eligibility",
      name: "Vehicle Eligibility",
      purpose: "Returns materialized service eligibility and relevant policy context.",
      risk: "low",
    },
  ],
  tools: [
    {
      id: "tool.appointment-availability",
      name: "Get Appointment Availability",
      purpose: "Lists eligible service appointment windows.",
      risk: "low",
      requiredPermission: "appointments:read",
    },
    {
      id: "tool.create-appointment",
      name: "Create Appointment",
      purpose: "Creates a confirmed service appointment.",
      risk: "moderate",
      requiredPermission: "appointments:create",
    },
  ],
  prompts: [],
};

export const routineMaintenanceScenario: Scenario = {
  id: "scenario.routine-maintenance-appointment",
  title: "Schedule a routine maintenance appointment",
  businessContext: {
    domain: "service",
    summary: "A customer needs routine maintenance and prefers a weekday morning at a qualified location.",
    stakeholders: ["customer", "service department"],
    requiredFacts: ["customer consent", "vehicle eligibility", "appointment availability"],
    sensitivities: ["customer contact information", "vehicle identification"],
  },
  intent: {
    explicitGoal: "Schedule an eligible weekday morning maintenance appointment after I confirm the time.",
    constraints: ["weekday morning", "customer must confirm before booking"],
  },
  expectedOutcomes: ["an eligible appointment is created", "the confirmed time is communicated to the customer"],
  expectedControlSurfaces: {
    harnessIds: [serviceAdvisorHarness.id],
    skillIds: [serviceSchedulingSkill.id],
    mcpServerIds: [dealershipOperationsMcp.id],
    mcpPrimitiveIds: ["resource.vehicle-eligibility", "tool.appointment-availability", "tool.create-appointment"],
  },
  evaluation: {
    requiredTraceTypes: [
      "intent.submitted",
      "harness.selected",
      "skill.activated",
      "mcp.primitives_listed",
      "policy.check_passed",
      "human.confirmation_received",
      "task.completed",
    ],
    requiresPolicyCheck: true,
    requiresHumanConfirmation: true,
  },
};

export const routineMaintenanceTrace: readonly RawTraceEvent[] = [
  {
    type: "intent.submitted",
    sequence: 1,
    actorId: "customer",
    subjectId: routineMaintenanceScenario.id,
    evidence: { goal: routineMaintenanceScenario.intent.explicitGoal },
  },
  {
    type: "agent.role_selected",
    sequence: 2,
    actorId: "harness",
    subjectId: "role.service-scheduling-assistant",
    evidence: { reason: "routine service scheduling request" },
  },
  {
    type: "harness.selected",
    sequence: 3,
    actorId: "system",
    subjectId: serviceAdvisorHarness.id,
    evidence: { interactionMode: serviceAdvisorHarness.interactionMode },
  },
  {
    type: "harness.context_loaded",
    sequence: 4,
    actorId: "harness",
    subjectId: "context.customer-request",
    evidence: { businessFacts: ["customer consent"] },
  },
  {
    type: "skill.activated",
    sequence: 5,
    actorId: "agent",
    subjectId: serviceSchedulingSkill.id,
    evidence: { applicability: "routine automotive service" },
  },
  {
    type: "mcp.server_connected",
    sequence: 6,
    actorId: "harness",
    subjectId: dealershipOperationsMcp.id,
    evidence: { transport: "fixture" },
  },
  {
    type: "mcp.primitives_listed",
    sequence: 7,
    actorId: "agent",
    subjectId: dealershipOperationsMcp.id,
    evidence: { primitiveCount: 3 },
  },
  {
    type: "mcp.resource_read",
    sequence: 8,
    actorId: "agent",
    subjectId: "resource.vehicle-eligibility",
    evidence: { businessFacts: ["vehicle eligibility"] },
  },
  {
    type: "mcp.tool_called",
    sequence: 9,
    actorId: "agent",
    subjectId: "tool.appointment-availability",
    evidence: { businessFacts: ["appointment availability"], result: "weekday morning available" },
  },
  {
    type: "policy.check_requested",
    sequence: 10,
    actorId: "agent",
    subjectId: "policy.scheduling-eligibility",
    evidence: { requestedAction: "create customer appointment" },
  },
  {
    type: "policy.check_passed",
    sequence: 11,
    actorId: "policy-engine",
    subjectId: "policy.scheduling-eligibility",
    evidence: { decision: "allow after customer confirmation" },
  },
  {
    type: "human.confirmation_requested",
    sequence: 12,
    actorId: "agent",
    subjectId: "customer",
    evidence: { proposedTime: "weekday 09:00" },
  },
  {
    type: "human.confirmation_received",
    sequence: 13,
    actorId: "customer",
    subjectId: "customer",
    evidence: { confirmed: true, proposedTime: "weekday 09:00" },
  },
  {
    type: "harness.permission_granted",
    sequence: 14,
    actorId: "harness",
    subjectId: "appointments:create",
    evidence: { scope: "confirmed appointment" },
  },
  {
    type: "mcp.tool_called",
    sequence: 15,
    actorId: "agent",
    subjectId: "tool.create-appointment",
    evidence: { action: "appointment created", authorization: "customer confirmation" },
  },
  {
    type: "task.completed",
    sequence: 16,
    actorId: "agent",
    subjectId: routineMaintenanceScenario.id,
    evidence: { outcome: "eligible confirmed service appointment created" },
  },
];

export const routineMaintenanceBenchmark: BenchmarkInput = {
  scenario: routineMaintenanceScenario,
  harnesses: [serviceAdvisorHarness],
  skills: [serviceSchedulingSkill],
  mcpSurfaces: [dealershipOperationsMcp],
  trace: routineMaintenanceTrace,
};

export const routineMaintenanceEvaluation = evaluateBenchmark(routineMaintenanceBenchmark);
