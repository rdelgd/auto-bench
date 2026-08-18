import assert from "node:assert/strict";
import test from "node:test";
import {
  dealershipOperationsMcp,
  routineMaintenanceConformanceCase,
  routineMaintenanceScenario,
  routineMaintenanceTrace,
  serviceAdvisorHarness,
  serviceSchedulingAssembly,
  serviceSchedulingInitialState,
  serviceSchedulingObservations,
  serviceSchedulingOutcomes,
  serviceSchedulingSkill,
  serviceSchedulingTransitions,
} from "../src/fixtures/index.js";
import {
  validateActorObservation,
  validateConformanceCase,
  validateHarness,
  validateLogicalAssembly,
  validateMcpSurface,
  validateOperationalState,
  validateOutcome,
  validateScenario,
  validateSkill,
  validateStateTransition,
  validateTrace,
} from "../src/validate.js";

test("representative Lasm, projections, state, episode, and evidence pass validation", () => {
  assert.equal(validateLogicalAssembly(serviceSchedulingAssembly).valid, true);
  assert.equal(validateOperationalState(serviceSchedulingInitialState, serviceSchedulingAssembly).valid, true);
  assert.equal(validateActorObservation(serviceSchedulingObservations[0]!, serviceSchedulingInitialState).valid, true);
  assert.equal(validateStateTransition(serviceSchedulingTransitions[0]!, serviceSchedulingInitialState, serviceSchedulingAssembly).valid, true);
  assert.equal(validateOutcome(serviceSchedulingOutcomes[0]!, serviceSchedulingInitialState).valid, true);
  assert.equal(validateScenario(routineMaintenanceScenario).valid, true);
  assert.equal(validateHarness(serviceAdvisorHarness, serviceSchedulingAssembly, serviceSchedulingInitialState).valid, true);
  assert.equal(validateSkill(serviceSchedulingSkill, serviceSchedulingAssembly, serviceSchedulingInitialState).valid, true);
  assert.equal(validateMcpSurface(dealershipOperationsMcp, serviceSchedulingAssembly, serviceSchedulingInitialState).valid, true);
  assert.equal(validateTrace(routineMaintenanceTrace).valid, true);
  assert.equal(validateConformanceCase(routineMaintenanceConformanceCase).valid, true);
});

test("validators return structured findings for malformed scenarios and traces", () => {
  const scenarioResult = validateScenario({
    ...routineMaintenanceScenario,
    title: "",
    reality: { ...routineMaintenanceScenario.reality, outcomeIds: [] },
  });
  assert.equal(scenarioResult.valid, false);
  assert.deepEqual(
    scenarioResult.findings.map(({ code, path }) => [code, path]),
    [
      ["fixture.required", "scenario.title"],
      ["fixture.non_empty", "scenario.reality.outcomeIds"],
    ],
  );

  const traceResult = validateTrace([{ type: "custom.event", sequence: -1 }]);
  assert.equal(traceResult.valid, false);
  assert.deepEqual(new Set(traceResult.findings.map(({ code }) => code)), new Set([
    "trace.unknown_event_type",
    "trace.missing_actor",
    "trace.invalid_sequence",
  ]));
});

test("LogicalAssembly validation reports duplicate and dangling semantic references", () => {
  const duplicateConcept = { ...serviceSchedulingAssembly.concepts[0]!, name: "Duplicate consent" };
  const assembly = {
    ...serviceSchedulingAssembly,
    concepts: [...serviceSchedulingAssembly.concepts, duplicateConcept],
    evaluations: serviceSchedulingAssembly.evaluations.map((evaluation) => ({
      ...evaluation,
      addressedEntryIds: [...evaluation.addressedEntryIds, "constraint.missing"],
    })),
  };
  const result = validateLogicalAssembly(assembly);

  assert.equal(result.valid, false);
  assert.ok(result.findings.some(({ code, path }) => code === "fixture.duplicate_id" && path === "assembly.entries"));
  assert.ok(result.findings.some(({ code }) => code === "assembly.unknown_entry"));
});

test("projection validation reports references outside the assembly and state", () => {
  const skill = {
    ...serviceSchedulingSkill,
    projection: {
      assemblyEntryIds: ["policy.missing"],
      stateFieldIds: ["field.missing"],
    },
  };
  const result = validateSkill(skill, serviceSchedulingAssembly, serviceSchedulingInitialState);

  assert.equal(result.valid, false);
  assert.deepEqual(new Set(result.findings.map(({ code }) => code)), new Set([
    "projection.unknown_assembly_entry",
    "projection.unknown_state_field",
  ]));
});

test("conformance-case validation reports mismatched and missing reality inputs", () => {
  const scenario = {
    ...routineMaintenanceScenario,
    reality: {
      ...routineMaintenanceScenario.reality,
      assemblyVersion: "stale-version",
      transitionIds: ["transition.missing"],
    },
  };
  const result = validateConformanceCase({ ...routineMaintenanceConformanceCase, scenario });

  assert.equal(result.valid, false);
  assert.ok(result.findings.some(({ code }) => code === "scenario.version_mismatch"));
  assert.ok(result.findings.some(({ code }) => code === "scenario.unknown_transition"));
});
