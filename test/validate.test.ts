import assert from "node:assert/strict";
import test from "node:test";
import {
  dealershipOperationsMcp,
  routineMaintenanceScenario,
  routineMaintenanceTrace,
  serviceAdvisorHarness,
  serviceSchedulingSkill,
} from "../src/fixtures/index.js";
import { validateHarness, validateMcpSurface, validateScenario, validateSkill, validateTrace } from "../src/validate.js";

test("representative fixtures and trace pass validation", () => {
  assert.equal(validateScenario(routineMaintenanceScenario).valid, true);
  assert.equal(validateHarness(serviceAdvisorHarness).valid, true);
  assert.equal(validateSkill(serviceSchedulingSkill).valid, true);
  assert.equal(validateMcpSurface(dealershipOperationsMcp).valid, true);
  assert.equal(validateTrace(routineMaintenanceTrace).valid, true);
});

test("validators return structured findings for malformed values", () => {
  const scenarioResult = validateScenario({ ...routineMaintenanceScenario, title: "", expectedOutcomes: [] });
  assert.equal(scenarioResult.valid, false);
  assert.deepEqual(
    scenarioResult.findings.map(({ code, path }) => [code, path]),
    [
      ["fixture.required", "scenario.title"],
      ["fixture.non_empty", "scenario.expectedOutcomes"],
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
