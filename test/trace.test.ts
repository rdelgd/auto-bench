import assert from "node:assert/strict";
import test from "node:test";
import { normalizeTrace } from "../src/trace.js";

test("normalization orders events deterministically and assigns positions", () => {
  const result = normalizeTrace([
    { type: "task.completed", sequence: 20, actorId: "agent", evidence: { outcome: "done" } },
    { type: "intent.submitted", sequence: 10, actorId: "customer", evidence: { goal: "service" } },
  ]);

  assert.deepEqual(result.events.map(({ type, position }) => [type, position]), [
    ["intent.submitted", 1],
    ["task.completed", 2],
  ]);
  assert.deepEqual(result.findings, []);
});

test("normalization reports and omits unknown or malformed events", () => {
  const result = normalizeTrace([
    { type: "unknown.event", sequence: 1, actorId: "agent" },
    { type: "task.completed", sequence: 2 },
  ]);

  assert.equal(result.events.length, 0);
  assert.deepEqual(result.findings.map(({ code }) => code), ["trace.unknown_event_type", "trace.missing_actor"]);
});
