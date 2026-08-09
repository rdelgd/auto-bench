import assert from "node:assert/strict";
import test from "node:test";
import { evaluateBenchmark } from "../src/evaluate.js";
import { routineMaintenanceBenchmark, routineMaintenanceEvaluation } from "../src/fixtures/index.js";

test("complete automotive fixture evaluates without I/O dependencies", () => {
  assert.equal(routineMaintenanceEvaluation.valid, true);
  assert.deepEqual(
    routineMaintenanceEvaluation.dimensions.map(({ dimension, status }) => [dimension, status]),
    [
      ["intent-fidelity", "pass"],
      ["control-surface-quality", "pass"],
      ["business-realism", "pass"],
      ["observability", "pass"],
      ["governance", "pass"],
    ],
  );
  assert.ok(routineMaintenanceEvaluation.dimensions.every(({ findings }) =>
    findings.every(({ evidenceRefs }) => evidenceRefs.every((reference) => reference.startsWith("trace:")))));
});

test("evaluation explains missing confirmation and control primitive", () => {
  const trace = routineMaintenanceBenchmark.trace.filter(({ type, subjectId }) =>
    type !== "human.confirmation_received" && subjectId !== "tool.create-appointment");
  const evaluation = evaluateBenchmark({ ...routineMaintenanceBenchmark, trace });
  const governance = evaluation.dimensions.find(({ dimension }) => dimension === "governance");
  const control = evaluation.dimensions.find(({ dimension }) => dimension === "control-surface-quality");

  assert.equal(governance?.status, "fail");
  assert.ok(governance?.findings.some(({ code }) => code === "governance.confirmation_missing"));
  assert.equal(control?.status, "fail");
  assert.ok(control?.findings.some(({ code }) => code === "control.mcp_primitive_not_used"));
});

test("governance requires confirmation before a sensitive tool call", () => {
  const trace = routineMaintenanceBenchmark.trace.map((event) =>
    event.type === "human.confirmation_received" ? { ...event, sequence: 17 } : event);
  const evaluation = evaluateBenchmark({ ...routineMaintenanceBenchmark, trace });
  const governance = evaluation.dimensions.find(({ dimension }) => dimension === "governance");

  assert.equal(governance?.status, "fail");
  assert.ok(governance?.findings.some(({ code }) => code === "governance.confirmation_too_late"));
});
