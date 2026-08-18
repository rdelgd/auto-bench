import assert from "node:assert/strict";
import test from "node:test";
import * as core from "../src/index.js";
import * as fixtures from "../src/fixtures/index.js";
import { evaluateConformance } from "../src/evaluate.js";
import { routineMaintenanceConformanceCase, routineMaintenanceEvaluation } from "../src/fixtures/index.js";

test("Auto Bench fixture evaluates a complete Lasm episode without I/O dependencies", () => {
  assert.equal(routineMaintenanceEvaluation.valid, true);
  assert.equal(routineMaintenanceEvaluation.conformant, true);
  assert.deepEqual(
    routineMaintenanceEvaluation.dimensions.map(({ dimension, status }) => [dimension, status]),
    [
      ["intent-fidelity", "pass"],
      ["semantic-fidelity", "pass"],
      ["reality-model-validity", "pass"],
      ["state-and-outcome-validity", "pass"],
      ["control-surface-quality", "pass"],
      ["reality-coverage", "pass"],
      ["evidence-and-attribution", "pass"],
      ["governance", "pass"],
    ],
  );
  assert.ok(routineMaintenanceEvaluation.dimensions.every(({ findings }) =>
    findings.every(({ evidenceRefs }) => evidenceRefs.every((reference) => reference.startsWith("trace:")))));
});

test("public runtime exports expose the Lasm models, conformance evaluator, and fixture", () => {
  assert.equal(core.evaluateConformance, evaluateConformance);
  assert.equal(core.logicalAssemblyEntries(fixtures.serviceSchedulingAssembly).length, 10);
  assert.equal(fixtures.routineMaintenanceConformanceCase, routineMaintenanceConformanceCase);
});

test("evaluation explains missing confirmation and control primitive", () => {
  const trace = routineMaintenanceConformanceCase.trace.filter(({ type, subjectId }) =>
    type !== "human.confirmation_received" && subjectId !== "tool.create-appointment");
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, trace });
  const governance = evaluation.dimensions.find(({ dimension }) => dimension === "governance");
  const control = evaluation.dimensions.find(({ dimension }) => dimension === "control-surface-quality");

  assert.equal(evaluation.conformant, false);
  assert.equal(governance?.status, "fail");
  assert.ok(governance?.findings.some(({ code }) => code === "governance.confirmation_missing"));
  assert.equal(control?.status, "fail");
  assert.ok(control?.findings.some(({ code }) => code === "control.mcp_primitive_not_used"));
});

test("governance requires confirmation before a sensitive tool call", () => {
  const trace = routineMaintenanceConformanceCase.trace.map((event) =>
    event.type === "human.confirmation_received" ? { ...event, sequence: 41 } : event);
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, trace });
  const governance = evaluation.dimensions.find(({ dimension }) => dimension === "governance");

  assert.equal(governance?.status, "fail");
  assert.ok(governance?.findings.some(({ code }) => code === "governance.confirmation_too_late"));
});

test("reality-model validity identifies stale assembly provenance", () => {
  const assembly = {
    ...routineMaintenanceConformanceCase.assembly,
    provenance: routineMaintenanceConformanceCase.assembly.provenance.map((source, index) =>
      index === 0 ? { ...source, status: "stale" as const } : source),
  };
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, assembly });
  const reality = evaluation.dimensions.find(({ dimension }) => dimension === "reality-model-validity");

  assert.equal(reality?.status, "fail");
  assert.ok(reality?.findings.some(({ code, attribution }) => code === "reality.stale_source" && attribution === "reality-model"));
});

test("reality coverage attributes a lossy projection", () => {
  const mcpSurfaces = routineMaintenanceConformanceCase.mcpSurfaces.map((surface) => ({
    ...surface,
    resources: surface.resources.map((resource) => resource.id === "resource.vehicle-eligibility"
      ? {
          ...resource,
          projection: {
            ...resource.projection,
            assemblyEntryIds: resource.projection?.assemblyEntryIds.filter((id) => id !== "relation.appointment-requires-eligibility") ?? [],
          },
        }
      : resource),
  }));
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, mcpSurfaces });
  const coverage = evaluation.dimensions.find(({ dimension }) => dimension === "reality-coverage");

  assert.equal(coverage?.status, "fail");
  assert.ok(coverage?.findings.some(({ code, attribution, assemblyEntryIds }) =>
    code === "coverage.assembly_entry_not_projected"
    && attribution === "projection"
    && assemblyEntryIds.includes("relation.appointment-requires-eligibility")));
});

test("state evaluation rejects prohibited transitions and outcomes", () => {
  const trace = [
    ...routineMaintenanceConformanceCase.trace,
    {
      type: "state.transition_committed",
      sequence: 41,
      actorId: "appointment-system",
      subjectId: "transition.create-unconfirmed-appointment",
      evidence: { appointmentStatus: "created" },
    },
    {
      type: "outcome.observed",
      sequence: 42,
      actorId: "auto-bench",
      subjectId: "outcome.unconfirmed-appointment-created",
      evidence: { consent: "unconfirmed" },
    },
  ] as const;
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, trace });
  const state = evaluation.dimensions.find(({ dimension }) => dimension === "state-and-outcome-validity");

  assert.equal(state?.status, "fail");
  assert.ok(state?.findings.some(({ code }) => code === "state.prohibited_transition_committed"));
  assert.ok(state?.findings.some(({ code }) => code === "outcome.prohibited_observed"));
});

test("evidence evaluation identifies an attribution gap", () => {
  const trace = [
    ...routineMaintenanceConformanceCase.trace,
    {
      type: "lasm.divergence_detected",
      sequence: 41,
      actorId: "auto-bench",
      subjectId: "constraint.confirm-before-booking",
      evidence: { reason: "projection omitted confirmation rule" },
    },
  ] as const;
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, trace });
  const evidence = evaluation.dimensions.find(({ dimension }) => dimension === "evidence-and-attribution");

  assert.equal(evidence?.status, "fail");
  assert.ok(evidence?.findings.some(({ code }) => code === "attribution.failure_unattributed"));
});

test("reality coverage identifies missing required operational facts", () => {
  const trace = routineMaintenanceConformanceCase.trace.map((event) => ({
    ...event,
    evidence: Object.fromEntries(Object.entries(event.evidence ?? {}).filter(([key]) => key !== "businessFacts")),
  }));
  const evaluation = evaluateConformance({ ...routineMaintenanceConformanceCase, trace });
  const coverage = evaluation.dimensions.find(({ dimension }) => dimension === "reality-coverage");

  assert.equal(coverage?.status, "fail");
  assert.ok(coverage?.findings.some(({ code }) => code === "coverage.required_fact_missing"));
});
