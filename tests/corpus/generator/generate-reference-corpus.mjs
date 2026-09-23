// Records the TypeScript `@lasm/core` reference outputs used to verify the Python port.
//
// This script is a provenance artifact. It runs only against a checkout of the recorded
// TypeScript source revision (see ../PROVENANCE.md) after `npm install && npm run build`:
//
//   node tests/corpus/generator/generate-reference-corpus.mjs <path-to-dist/src> <output-dir>
//
// Expected outputs come from the TypeScript implementation. Never regenerate them from Python.

import { mkdirSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [distArg, outArg] = process.argv.slice(2);
if (!distArg || !outArg) {
  console.error("usage: generate-reference-corpus.mjs <path-to-dist/src> <output-dir>");
  process.exit(2);
}
const dist = resolve(distArg);
const outDir = resolve(outArg);
const core = await import(pathToFileURL(join(dist, "index.js")).href);
const fixtures = await import(pathToFileURL(join(dist, "fixtures", "index.js")).href);

const clone = (value) => structuredClone(value);
const baseCase = () => clone(fixtures.routineMaintenanceConformanceCase);

// A JavaScript Set would serialize as `{}`; record set-valued results with explicit members.
function encode(value) {
  if (value instanceof Set) return { $set: [...value].sort() };
  return value;
}

function assertJsonSafe(value, path) {
  if (value === undefined) throw new Error(`undefined value at ${path}`);
  if (typeof value === "number" && (!Number.isFinite(value) || Object.is(value, -0))) {
    throw new Error(`number outside the corpus domain at ${path}`);
  }
  if (typeof value === "number" && Number.isInteger(value) && !Number.isSafeInteger(value)) {
    throw new Error(`integer outside the wire safe-integer range at ${path}`);
  }
  if (Array.isArray(value)) value.forEach((item, index) => assertJsonSafe(item, `${path}[${index}]`));
  else if (value !== null && typeof value === "object") {
    for (const [key, item] of Object.entries(value)) assertJsonSafe(item, `${path}.${key}`);
  }
}

const groups = new Map();
function record(fn, id, description, args) {
  const target = fn.startsWith("fixture:") ? null : core[fn];
  if (target === undefined) throw new Error(`unknown export ${fn}`);
  const before = JSON.stringify(args);
  let expected;
  if (fn.startsWith("fixture:")) expected = fixtures[fn.slice("fixture:".length)];
  else if (typeof target === "function") expected = target(...clone(args));
  else expected = target;
  if (JSON.stringify(args) !== before) throw new Error(`${id} mutated its recorded arguments`);
  const entry = { id, function: fn, description, args, expected: encode(expected) };
  assertJsonSafe(entry, id);
  const group = fn.startsWith("fixture:") ? "fixtures" : fn;
  if (!groups.has(group)) groups.set(group, []);
  if (groups.get(group).some((existing) => existing.id === id)) throw new Error(`duplicate case id ${id}`);
  groups.get(group).push(entry);
}

const f = fixtures;
const assembly = () => clone(f.serviceSchedulingAssembly);
const state = () => clone(f.serviceSchedulingInitialState);
const scenario = () => clone(f.routineMaintenanceScenario);
const harness = () => clone(f.serviceAdvisorHarness);
const skill = () => clone(f.serviceSchedulingSkill);
const mcp = () => clone(f.dealershipOperationsMcp);
const trace = () => clone(f.routineMaintenanceTrace);
const withTrace = (events) => ({ ...baseCase(), trace: events });

// ---------------------------------------------------------------------------
// Constants and fixture exports
// ---------------------------------------------------------------------------

record("agenticEventTypes", "constant.agentic-event-types", "The ordered agentic event vocabulary.", []);
for (const name of Object.keys(fixtures).sort()) {
  record(`fixture:${name}`, `fixture.${name}`, `Reference fixture export ${name}.`, []);
}

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

const error = { code: "x.error", severity: "error", path: "x", message: "An error." };
const warning = { code: "x.warning", severity: "warning", path: "y", message: "A warning." };
record("validationResult", "validation-result.empty", "No findings is valid.", [[]]);
record("validationResult", "validation-result.warning-only", "Warnings keep a result valid.", [[warning]]);
record("validationResult", "validation-result.mixed", "Errors invalidate and finding order is kept.", [[warning, error, warning]]);

record("logicalAssemblyEntries", "entries.fixture", "Entries are concatenated in collection order.", [assembly()]);
record("logicalAssemblyEntries", "entries.empty", "Empty collections produce no entries.", [{
  ...assembly(), concepts: [], relations: [], constraints: [], events: [], policies: [], evaluations: [],
}]);
record("logicalAssemblyEntryIds", "entry-ids.fixture", "Entry identifiers as a set.", [assembly()]);
record("logicalAssemblyEntryIds", "entry-ids.duplicates", "Duplicate identifiers collapse to one member.", [{
  ...assembly(), concepts: [...assembly().concepts, assembly().concepts[0]], policies: [{ ...assembly().policies[0], id: "concept.customer-consent" }],
}]);
record("logicalAssemblyEntryIds", "entry-ids.empty", "An empty assembly has no entry identifiers.", [{
  ...assembly(), concepts: [], relations: [], constraints: [], events: [], policies: [], evaluations: [],
}]);

record("mcpPrimitives", "primitives.fixture", "Tools, then resources, then prompts.", [mcp()]);
record("mcpPrimitives", "primitives.ordering", "Collection order is tools, resources, prompts regardless of key order.", [{
  prompts: [{ id: "prompt.a", name: "A", purpose: "a", risk: "low" }],
  resources: [{ id: "resource.b", name: "B", purpose: "b", risk: "moderate" }],
  tools: [{ id: "tool.c", name: "C", purpose: "c", risk: "high", requiredPermission: "p" }],
  id: "mcp.order", name: "Order", purpose: "ordering",
}]);
record("mcpPrimitives", "primitives.empty", "A surface without primitives.", [{ ...mcp(), tools: [], resources: [], prompts: [] }]);

for (const [id, value] of [
  ["known", "intent.submitted"],
  ["known-last", "reality.validation_assessed"],
  ["unknown", "custom.event"],
  ["empty", ""],
  ["case-sensitive", "Intent.Submitted"],
  ["whitespace", " intent.submitted"],
]) {
  record("isAgenticEventType", `is-event-type.${id}`, `Event-type membership for ${JSON.stringify(value)}.`, [value]);
}

record("traceEvidenceRef", "evidence-ref.position", "Evidence references use the one-based position.", [{
  type: "task.completed", position: 7, actorId: "agent", evidence: {},
}]);
record("traceEvidenceRef", "evidence-ref.first", "The first normalized event.", [{
  type: "intent.submitted", position: 1, actorId: "customer", subjectId: "scenario.x", timestamp: "2026-01-01T00:00:00Z", evidence: { goal: "g" },
}]);

// ---------------------------------------------------------------------------
// Trace normalization
// ---------------------------------------------------------------------------

record("normalizeTrace", "normalize.fixture", "The complete reference trace.", [trace()]);
record("normalizeTrace", "normalize.orders-by-sequence", "Existing test: ordering and positions.", [[
  { type: "task.completed", sequence: 20, actorId: "agent", evidence: { outcome: "done" } },
  { type: "intent.submitted", sequence: 10, actorId: "customer", evidence: { goal: "service" } },
]]);
record("normalizeTrace", "normalize.omits-malformed", "Existing test: unknown and actorless events are reported and omitted.", [[
  { type: "unknown.event", sequence: 1, actorId: "agent" },
  { type: "task.completed", sequence: 2 },
]]);
record("normalizeTrace", "normalize.empty", "An empty trace.", [[]]);
record("normalizeTrace", "normalize.equal-sequence-ties", "Equal sequences keep original input order.", [[
  { type: "state.observed", sequence: 5, actorId: "a", subjectId: "third" },
  { type: "state.observed", sequence: 1, actorId: "a", subjectId: "first" },
  { type: "state.observed", sequence: 5, actorId: "a", subjectId: "fourth" },
  { type: "state.observed", sequence: 1, actorId: "a", subjectId: "second" },
  { type: "state.observed", sequence: 5, actorId: "a", subjectId: "fifth" },
]]);
record("normalizeTrace", "normalize.omitted-sequences", "Omitted sequences sort after numbered events in input order.", [[
  { type: "task.completed", actorId: "a", subjectId: "unsequenced-1" },
  { type: "intent.submitted", sequence: 3, actorId: "a", subjectId: "three" },
  { type: "task.failed", actorId: "a", subjectId: "unsequenced-2" },
  { type: "state.observed", sequence: 1, actorId: "a", subjectId: "one" },
]]);
record("normalizeTrace", "normalize.max-safe-sentinel", "An explicit MAX_SAFE_INTEGER sequence ties with omitted sequences by input order.", [[
  { type: "task.completed", actorId: "a", subjectId: "omitted-first" },
  { type: "task.completed", sequence: 9007199254740991, actorId: "a", subjectId: "max-safe" },
  { type: "task.completed", actorId: "a", subjectId: "omitted-last" },
  { type: "task.completed", sequence: 9007199254740990, actorId: "a", subjectId: "below-max" },
]]);
record("normalizeTrace", "normalize.negative-fractional-duplicate", "Negative, fractional, and duplicate sequences still order numerically.", [[
  { type: "state.observed", sequence: 2.5, actorId: "a", subjectId: "two-point-five" },
  { type: "state.observed", sequence: -1, actorId: "a", subjectId: "negative" },
  { type: "state.observed", sequence: 2, actorId: "a", subjectId: "two" },
  { type: "state.observed", sequence: 0, actorId: "a", subjectId: "zero" },
  { type: "state.observed", sequence: 2, actorId: "a", subjectId: "two-again" },
  { type: "state.observed", sequence: -0.25, actorId: "a", subjectId: "negative-fraction" },
]]);
record("normalizeTrace", "normalize.findings-use-input-indices", "Findings address original indices, not sorted positions.", [[
  { type: "task.completed", sequence: 9, actorId: "agent" },
  { type: "", sequence: 3, actorId: "agent" },
  { type: "intent.submitted", sequence: 1, actorId: "   " },
  { type: "not.real", sequence: 2 },
  { type: "state.observed", sequence: 4, actorId: "\u00a0\ufeff" },
  { type: "state.observed", sequence: 5, actorId: "\u200b" },
  { type: "intent.submitted", sequence: 0, actorId: "customer" },
]]);
record("normalizeTrace", "normalize.optional-fields", "Timestamps and subjects are kept only when present; missing evidence becomes empty.", [[
  { type: "intent.submitted", sequence: 1, actorId: "customer", timestamp: "2026-09-22T10:00:00Z", subjectId: "scenario.x", evidence: { goal: "g" } },
  { type: "task.completed", sequence: 2, actorId: "agent" },
  { type: "task.completed", sequence: 3, actorId: "agent", timestamp: "", subjectId: "" },
]]);
record("normalizeTrace", "normalize.nested-evidence-scalars", "Nested falsy evidence values are preserved.", [[
  {
    type: "evidence.linked", sequence: 1, actorId: "auto-bench",
    evidence: { flag: false, count: 0, text: "", nothing: null, nested: { list: [false, 0, "", null, { deep: [] }], empty: {} }, fraction: 0.5, big: 9007199254740991 },
  },
]]);

// ---------------------------------------------------------------------------
// Individual validators
// ---------------------------------------------------------------------------

record("validateLogicalAssembly", "assembly.fixture", "The reference assembly is valid.", [assembly()]);
{
  const a = assembly();
  const duplicateConcept = { ...a.concepts[0], name: "Duplicate consent" };
  record("validateLogicalAssembly", "assembly.duplicate-and-dangling", "Existing test: duplicate entry and dangling evaluation reference.", [{
    ...a,
    concepts: [...a.concepts, duplicateConcept],
    evaluations: a.evaluations.map((evaluation) => ({ ...evaluation, addressedEntryIds: [...evaluation.addressedEntryIds, "constraint.missing"] })),
  }]);
}
record("validateLogicalAssembly", "assembly.blank-strings", "Blank and whitespace-only required strings.", [{
  ...assembly(), id: "", version: "   ", title: "\t\n", description: "\u00a0\ufeff\u2028",
}]);
record("validateLogicalAssembly", "assembly.non-whitespace-invisible", "Characters JavaScript does not trim count as content.", [{
  ...assembly(), id: "\u200b", version: "\u001c", title: "\u0085", description: "\u180e",
}]);
record("validateLogicalAssembly", "assembly.empty-collections", "Empty required collections and no entries.", [{
  ...assembly(), provenance: [], concepts: [], relations: [], constraints: [], events: [], policies: [], evaluations: [],
}]);
{
  const a = assembly();
  record("validateLogicalAssembly", "assembly.provenance-problems", "Duplicate provenance ids, blank provenance fields, and unknown sources.", [{
    ...a,
    provenance: [
      ...a.provenance,
      { ...a.provenance[0], title: "", locator: " " },
      { id: "", kind: "code", title: "t", locator: "l", status: "current" },
      { ...a.provenance[1] },
      { ...a.provenance[0] },
    ],
    concepts: a.concepts.map((concept, index) => index === 1 ? { ...concept, sourceIds: ["source.missing", concept.sourceIds[0], "source.other-missing"] } : concept),
  }]);
}
{
  const a = assembly();
  record("validateLogicalAssembly", "assembly.duplicate-order", "Repeated duplicates are reported once in second-occurrence order.", [{
    ...a,
    concepts: [
      { ...a.concepts[0], id: "concept.b" },
      { ...a.concepts[1], id: "concept.a" },
      { ...a.concepts[2], id: "concept.a" },
      { ...a.concepts[3], id: "concept.b" },
      { ...a.concepts[0], id: "concept.a" },
      { ...a.concepts[0], id: "relation.appointment-requires-eligibility" },
    ],
  }]);
}
{
  const a = assembly();
  record("validateLogicalAssembly", "assembly.dangling-references", "Every entry kind with dangling and empty references.", [{
    ...a,
    concepts: [...a.concepts, { id: "concept.blank", kind: "concept", name: "", description: " ", sourceIds: [] }],
    relations: [{ ...a.relations[0], fromConceptId: "concept.missing", toConceptId: "", predicate: " " }],
    constraints: [
      { ...a.constraints[0], appliesToEntryIds: [], rule: "" },
      { ...a.constraints[1], appliesToEntryIds: ["concept.appointment-slot", "entry.missing", "concept.blank"] },
    ],
    events: [
      { ...a.events[0], subjectConceptIds: [] },
      { ...a.events[0], id: "event.other", subjectConceptIds: ["concept.missing", "relation.appointment-requires-eligibility"] },
    ],
    policies: [{ ...a.policies[0], appliesToEntryIds: [], authorityRoles: [], commitment: "\n" }, { ...a.policies[0], id: "policy.other", appliesToEntryIds: ["policy.missing"] }],
    evaluations: [{ ...a.evaluations[0], addressedEntryIds: [], evaluatorId: "" }, { ...a.evaluations[0], id: "evaluation.self", addressedEntryIds: ["evaluation.self", "missing"], mode: "check" }],
  }]);
}

record("validateOperationalState", "state.fixture", "The reference state is valid.", [state(), assembly()]);
record("validateOperationalState", "state.mismatches", "Assembly, version, blank id, and unknown concept.", [{
  ...state(), id: " ", assemblyId: "lasm.other", assemblyVersion: "old",
  fields: [...state().fields, { id: "", conceptId: "concept.missing", value: null }, { id: "field.customer-consent", conceptId: "relation.appointment-requires-eligibility", value: { nested: [0, false] } }],
}, assembly()]);
record("validateOperationalState", "state.empty-fields", "No fields.", [{ ...state(), fields: [] }, assembly()]);

record("validateActorObservation", "observation.fixture", "The reference observation is valid.", [f.serviceSchedulingObservations[0], state()]);
record("validateActorObservation", "observation.failures", "Blank ids, empty fields.", [{ id: "", actorId: " ", fieldIds: [], observedValues: {} }, state()]);
record("validateActorObservation", "observation.unknown-fields", "Unknown state fields.", [{ ...f.serviceSchedulingObservations[0], fieldIds: ["field.missing", "field.customer-consent", "field.other"] }, state()]);

record("validateStateTransition", "transition.fixture", "The reference transition is valid.", [f.serviceSchedulingTransitions[0], state(), assembly()]);
{
  const { eventId: _eventId, before: _before, after: _after, ...withoutEvent } = clone(f.serviceSchedulingTransitions[0]);
  record("validateStateTransition", "transition.no-event", "An omitted event id is not checked.", [withoutEvent, state(), assembly()]);
}
record("validateStateTransition", "transition.failures", "Blank fields, unknown event and fields.", [{
  ...f.serviceSchedulingTransitions[1], id: "", description: " ", eventId: "concept.customer-consent", fieldIds: ["field.missing", "field.appointment-status", "x"],
}, state(), assembly()]);
record("validateStateTransition", "transition.empty-event", "An empty event id is still checked as a reference.", [{ ...f.serviceSchedulingTransitions[0], eventId: "", fieldIds: [] }, state(), assembly()]);

record("validateOutcome", "outcome.fixture", "The reference outcome is valid.", [f.serviceSchedulingOutcomes[0], state()]);
record("validateOutcome", "outcome.failures", "Blank fields and unknown state references.", [{ ...f.serviceSchedulingOutcomes[1], id: "\t", description: "", fieldIds: ["field.missing"] }, state()]);
record("validateOutcome", "outcome.empty-fields", "No fields.", [{ ...f.serviceSchedulingOutcomes[0], fieldIds: [] }, state()]);

record("validateScenario", "scenario.fixture", "The reference scenario is valid.", [scenario()]);
record("validateScenario", "scenario.existing-test", "Existing test: blank title and no outcomes.", [{ ...scenario(), title: "", reality: { ...scenario().reality, outcomeIds: [] } }]);
record("validateScenario", "scenario.all-empty", "All checked strings and collections empty.", [{
  ...scenario(), id: " ", title: "",
  businessContext: { ...scenario().businessContext, summary: "", stakeholders: [], requiredFacts: [], sensitivities: [] },
  intent: { explicitGoal: "", constraints: [], inferredGoals: [] },
  reality: { assemblyId: "", assemblyVersion: "", assemblyEntryIds: [], initialStateId: "", observationIds: [], transitionIds: [], outcomeIds: [] },
  expectedControlSurfaces: { harnessIds: [], skillIds: [], mcpServerIds: [], mcpPrimitiveIds: [] },
  evaluation: { requiredTraceTypes: [], requiresPolicyCheck: false, requiresHumanConfirmation: false },
}]);
record("validateScenario", "scenario.duplicate-control-surfaces", "Duplicates across all control-surface categories.", [{
  ...scenario(),
  expectedControlSurfaces: { harnessIds: ["shared", "harness.a", "harness.a"], skillIds: ["shared", "tool.x"], mcpServerIds: ["mcp.a"], mcpPrimitiveIds: ["tool.x", "mcp.a", "shared"] },
}]);

record("validateHarness", "harness.fixture", "The reference harness is valid against assembly and state.", [harness(), assembly(), state()]);
record("validateHarness", "harness.standalone", "Without assembly or state, references are not resolved.", [{
  ...harness(), projection: { assemblyEntryIds: ["missing"], stateFieldIds: ["missing"] },
}]);
record("validateHarness", "harness.assembly-only", "With an assembly only, state references are not resolved.", [{
  ...harness(), projection: { assemblyEntryIds: ["missing"], stateFieldIds: ["missing"] },
}, assembly()]);
{
  const h = harness();
  record("validateHarness", "harness.failures", "Blank fields, empty collections, duplicate ids, and bad projections.", [{
    ...h, id: "", name: " ", purpose: "",
    contextSurfaces: [
      { ...h.contextSurfaces[0], projection: { assemblyEntryIds: [] } },
      { ...h.contextSurfaces[0], projection: { assemblyEntryIds: ["x", "x", "concept.customer-consent"], stateFieldIds: ["field.x", "field.x"] } },
      { ...h.contextSurfaces[1] },
      { id: "context.bare", description: "no projection", sensitivity: "public" },
    ],
    affordances: [],
    permissionModel: { defaultLevel: "privileged", scopedPermissions: [], projection: { assemblyEntryIds: [], stateFieldIds: [] } },
    approvalFlow: { requiredFor: [], approverRoles: [], projection: { assemblyEntryIds: [], stateFieldIds: ["field.customer-consent", "field.none"] } },
    handoffBoundaries: [],
  }, assembly(), state()]);
}
{
  const { projection: _projection, ...h } = harness();
  record("validateHarness", "harness.duplicate-surfaces", "Duplicate context surfaces and handoffs without top-level projection.", [{
    ...h,
    contextSurfaces: [...h.contextSurfaces, h.contextSurfaces[0]],
    handoffBoundaries: [...h.handoffBoundaries, h.handoffBoundaries[0], { ...h.handoffBoundaries[0], projection: { assemblyEntryIds: ["nope"] } }],
  }, assembly(), state()]);
}

record("validateSkill", "skill.fixture", "The reference skill is valid.", [skill(), assembly(), state()]);
record("validateSkill", "skill.existing-test", "Existing test: projection outside assembly and state.", [{
  ...skill(), projection: { assemblyEntryIds: ["policy.missing"], stateFieldIds: ["field.missing"] },
}, assembly(), state()]);
{
  const { projection: _projection, references: _references, ...s } = skill();
  record("validateSkill", "skill.no-projection", "Optional projection and references omitted.", [s, assembly(), state()]);
  record("validateSkill", "skill.failures", "Blank fields and empty collections.", [{ ...s, id: "", name: "", purpose: " ", applicability: [], capabilities: [] }]);
}
record("validateSkill", "skill.empty-projection", "A projection with no references and no state list.", [{ ...skill(), projection: { assemblyEntryIds: [] } }, assembly(), state()]);

record("validateMcpSurface", "mcp.fixture", "The reference MCP surface is valid.", [mcp(), assembly(), state()]);
record("validateMcpSurface", "mcp.empty", "No primitives and blank fields.", [{ ...mcp(), id: "", name: " ", purpose: "", tools: [], resources: [], prompts: [] }, assembly(), state()]);
{
  const m = mcp();
  record("validateMcpSurface", "mcp.primitive-failures", "Duplicate primitive ids, blank primitive fields, and bad projections across collections.", [{
    ...m,
    prompts: [{ id: "tool.create-appointment", name: "", purpose: " ", risk: "low", projection: { assemblyEntryIds: ["missing"], stateFieldIds: ["field.missing"] } }],
    resources: [...m.resources, { id: "", name: "n", purpose: "p", risk: "high", projection: { assemblyEntryIds: [] } }],
    projection: { assemblyEntryIds: ["evaluation.scheduling-gate", "evaluation.scheduling-gate"] },
  }, assembly(), state()]);
}
record("validateMcpSurface", "mcp.standalone", "Without assembly or state.", [{ ...mcp(), projection: { assemblyEntryIds: ["missing"] } }]);

record("validateTrace", "trace.fixture", "The reference trace is valid.", [trace()]);
record("validateTrace", "trace.existing-test", "Existing test: unknown type, no actor, negative sequence.", [[{ type: "custom.event", sequence: -1 }]]);
record("validateTrace", "trace.empty", "An empty trace.", [[]]);
record("validateTrace", "trace.sequence-problems", "Fractional, negative, and duplicate sequences, with omitted sequences ignored.", [[
  { type: "task.completed", sequence: 1, actorId: "a" },
  { type: "task.completed", sequence: 1.5, actorId: "a" },
  { type: "task.completed", sequence: 1, actorId: "a" },
  { type: "task.completed", actorId: "a" },
  { type: "task.completed", sequence: -2.5, actorId: "a" },
  { type: "task.completed", actorId: "a" },
  { type: "task.completed", sequence: 1.5, actorId: "a" },
  { type: "task.completed", sequence: 0, actorId: "a" },
  { type: "task.completed", sequence: 1, actorId: "a" },
]]);
record("validateTrace", "trace.sequence-spelling", "Duplicate-sequence messages use JavaScript number spelling.", [[
  { type: "task.completed", sequence: 1e-7, actorId: "a" },
  { type: "task.completed", sequence: 1e-7, actorId: "a" },
  { type: "task.completed", sequence: 123456.789, actorId: "a" },
  { type: "task.completed", sequence: 123456.789, actorId: "a" },
  { type: "task.completed", sequence: 9007199254740991, actorId: "a" },
  { type: "task.completed", sequence: 9007199254740991, actorId: "a" },
  { type: "task.completed", sequence: 0.000001, actorId: "a" },
  { type: "task.completed", sequence: 0.000001, actorId: "a" },
  { type: "task.completed", sequence: 1e15, actorId: "a" },
  { type: "task.completed", sequence: 2.5e-10, actorId: "a" },
  { type: "task.completed", sequence: 2.5e-10, actorId: "a" },
  { type: "task.completed", sequence: -0.1, actorId: "a" },
  { type: "task.completed", sequence: -0.1, actorId: "a" },
]]);
record("validateTrace", "trace.actor-and-type-problems", "Empty types and blank actors of several kinds.", [[
  { type: "", sequence: 1, actorId: "" },
  { type: "task.completed", sequence: 2, actorId: " \t" },
  { type: "task.completed", sequence: 3, actorId: "\ufeff" },
  { type: "task.completed", sequence: 4, actorId: "\u200b" },
  { type: "TASK.COMPLETED", sequence: 5, actorId: "agent" },
]]);

// ---------------------------------------------------------------------------
// Aggregate conformance-case validation
// ---------------------------------------------------------------------------

record("validateConformanceCase", "case.fixture", "The reference case is valid.", [baseCase()]);
record("validateConformanceCase", "case.existing-test", "Existing test: mismatched version and missing transition.", [{
  ...baseCase(), scenario: { ...scenario(), reality: { ...scenario().reality, assemblyVersion: "stale-version", transitionIds: ["transition.missing"] } },
}]);
{
  const c = baseCase();
  record("validateConformanceCase", "case.cross-reference-failures", "Unknown and duplicate cross references throughout the case.", [{
    ...c,
    scenario: {
      ...c.scenario,
      reality: {
        ...c.scenario.reality,
        assemblyId: "lasm.other", initialStateId: "state.other",
        assemblyEntryIds: [...c.scenario.reality.assemblyEntryIds, "entry.missing"],
        observationIds: ["observation.missing", ...c.scenario.reality.observationIds],
        outcomeIds: ["outcome.missing"],
      },
      expectedControlSurfaces: {
        harnessIds: ["harness.missing", "harness.service-advisor"],
        skillIds: ["skill.missing"],
        mcpServerIds: ["mcp.missing"],
        mcpPrimitiveIds: ["tool.create-appointment", "prompt.missing"],
      },
    },
    observations: [...c.observations, c.observations[0]],
    transitions: [...c.transitions, c.transitions[1]],
    outcomes: [...c.outcomes, c.outcomes[0], c.outcomes[0]],
    harnesses: [...c.harnesses, c.harnesses[0]],
    skills: [...c.skills, c.skills[0]],
    mcpSurfaces: [...c.mcpSurfaces, c.mcpSurfaces[0]],
  }]);
}
{
  const c = baseCase();
  record("validateConformanceCase", "case.nested-validator-order", "Findings from every nested validator in aggregate order.", [{
    ...c,
    assembly: { ...c.assembly, title: "" },
    initialState: { ...c.initialState, assemblyVersion: "v0" },
    scenario: { ...c.scenario, title: " " },
    observations: [{ ...c.observations[0], actorId: "" }],
    transitions: [{ ...c.transitions[0], eventId: "event.missing" }],
    outcomes: [{ ...c.outcomes[0], fieldIds: ["field.missing"] }],
    harnesses: [{ ...c.harnesses[0], purpose: "" }],
    skills: [{ ...c.skills[0], capabilities: [] }],
    mcpSurfaces: [{ ...c.mcpSurfaces[0], name: "" }],
    trace: [...c.trace, { type: "bogus", sequence: 1 }],
  }]);
}

// ---------------------------------------------------------------------------
// Conformance evaluation
// ---------------------------------------------------------------------------

record("evaluateConformance", "evaluate.fixture", "The complete passing service-scheduling episode.", [baseCase()]);
record("evaluateConformance", "evaluate.missing-confirmation-and-primitive", "Existing test: confirmation and create-appointment tool removed.", [withTrace(
  trace().filter(({ type, subjectId }) => type !== "human.confirmation_received" && subjectId !== "tool.create-appointment"),
)]);
record("evaluateConformance", "evaluate.late-confirmation", "Existing test: confirmation after the governed call.", [withTrace(
  trace().map((event) => event.type === "human.confirmation_received" ? { ...event, sequence: 41 } : event),
)]);
record("evaluateConformance", "evaluate.late-policy", "Policy and runtime gate recorded after the governed call.", [withTrace(
  trace().map((event) => event.type === "policy.check_passed" || event.type === "lasm.evaluation_passed" ? { ...event, sequence: event.sequence + 20 } : event),
)]);
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.stale-provenance", "Existing test: stale provenance source.", [{
    ...c, assembly: { ...c.assembly, provenance: c.assembly.provenance.map((source, index) => index === 0 ? { ...source, status: "stale" } : source) },
  }]);
  record("evaluateConformance", "evaluate.disputed-provenance", "A disputed source warns without failing conformance.", [{
    ...c, assembly: { ...c.assembly, provenance: c.assembly.provenance.map((source, index) => index === 2 ? { ...source, status: "disputed" } : source) },
  }]);
  record("evaluateConformance", "evaluate.stale-and-disputed", "Stale and disputed sources together.", [{
    ...c, assembly: { ...c.assembly, provenance: c.assembly.provenance.map((source, index) => ({ ...source, status: ["disputed", "stale", "disputed"][index] })) },
  }]);
}
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.lossy-projection", "Existing test: resource projection drops a relevant entry.", [{
    ...c,
    mcpSurfaces: c.mcpSurfaces.map((surface) => ({
      ...surface,
      resources: surface.resources.map((resource) => resource.id === "resource.vehicle-eligibility"
        ? { ...resource, projection: { ...resource.projection, assemblyEntryIds: resource.projection.assemblyEntryIds.filter((id) => id !== "relation.appointment-requires-eligibility") } }
        : resource),
    })),
  }]);
}
{
  const c = baseCase();
  const stripProjections = (value) => {
    if (Array.isArray(value)) return value.map(stripProjections);
    if (value !== null && typeof value === "object") {
      return Object.fromEntries(Object.entries(value).filter(([key]) => key !== "projection").map(([key, item]) => [key, stripProjections(item)]));
    }
    return value;
  };
  record("evaluateConformance", "evaluate.omitted-projections", "All projections omitted.", [{
    ...c, harnesses: stripProjections(c.harnesses), skills: stripProjections(c.skills), mcpSurfaces: stripProjections(c.mcpSurfaces),
  }]);
}
record("evaluateConformance", "evaluate.prohibited-transition-and-outcome", "Existing test: prohibited transition and outcome observed.", [withTrace([
  ...trace(),
  { type: "state.transition_committed", sequence: 41, actorId: "appointment-system", subjectId: "transition.create-unconfirmed-appointment", evidence: { appointmentStatus: "created" } },
  { type: "outcome.observed", sequence: 42, actorId: "auto-bench", subjectId: "outcome.unconfirmed-appointment-created", evidence: { consent: "unconfirmed" } },
])]);
record("evaluateConformance", "evaluate.unattributed-divergence", "Existing test: divergence without attribution.", [withTrace([
  ...trace(),
  { type: "lasm.divergence_detected", sequence: 41, actorId: "auto-bench", subjectId: "constraint.confirm-before-booking", evidence: { reason: "projection omitted confirmation rule" } },
])]);
record("evaluateConformance", "evaluate.attributed-and-subjectless-failures", "Attributed divergence, subjectless failures, and matching subjectless attribution.", [withTrace([
  ...trace(),
  { type: "lasm.divergence_detected", sequence: 41, actorId: "auto-bench", subjectId: "constraint.confirm-before-booking", evidence: { reason: "r" } },
  { type: "lasm.failure_attributed", sequence: 42, actorId: "auto-bench", subjectId: "constraint.confirm-before-booking", evidence: { source: "projection" } },
  { type: "lasm.divergence_detected", sequence: 43, actorId: "auto-bench", evidence: { reason: "no subject" } },
  { type: "lasm.evaluation_failed", sequence: 44, actorId: "gate", subjectId: "evaluation.scheduling-gate", evidence: { decision: "deny" } },
])]);
record("evaluateConformance", "evaluate.subjectless-failure-unattributed", "A subjectless failure without any subjectless attribution.", [withTrace([
  ...trace(),
  { type: "lasm.evaluation_failed", sequence: 41, actorId: "gate", evidence: {} },
  { type: "lasm.failure_attributed", sequence: 42, actorId: "auto-bench", subjectId: "something.else", evidence: { source: "x" } },
])]);
record("evaluateConformance", "evaluate.missing-business-facts", "Existing test: operational facts removed.", [withTrace(
  trace().map((event) => ({ ...event, evidence: Object.fromEntries(Object.entries(event.evidence ?? {}).filter(([key]) => key !== "businessFacts")) })),
)]);
record("evaluateConformance", "evaluate.non-string-business-facts", "Non-string and non-array business facts are ignored.", [withTrace(
  trace().map((event) => event.evidence?.businessFacts
    ? { ...event, evidence: { ...event.evidence, businessFacts: event.subjectId === "context.customer-request" ? [0, false, null, ["customer consent"], "customer consent"] : event.subjectId === "resource.vehicle-eligibility" ? "vehicle eligibility" : event.evidence.businessFacts } }
    : event),
)]);
record("evaluateConformance", "evaluate.permission-denied-and-policy-failed", "Denied permission and failed policy.", [withTrace([
  ...trace(),
  { type: "harness.permission_denied", sequence: 41, actorId: "harness", subjectId: "appointments:create", evidence: { reason: "scope" } },
  { type: "policy.check_failed", sequence: 42, actorId: "policy-engine", subjectId: "policy.scheduling-eligibility", evidence: { decision: "deny" } },
  { type: "lasm.failure_attributed", sequence: 43, actorId: "auto-bench", subjectId: "policy.scheduling-eligibility", evidence: {} },
])]);
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.no-required-gates", "No policy or confirmation requirement and no failures.", [{
    ...c, scenario: { ...c.scenario, evaluation: { ...c.scenario.evaluation, requiresPolicyCheck: false, requiresHumanConfirmation: false } },
  }]);
  record("evaluateConformance", "evaluate.gates-required-but-absent", "Required gates with no passing evidence.", [{
    ...c, trace: c.trace.filter(({ type }) => !["policy.check_passed", "lasm.evaluation_passed", "human.confirmation_received"].includes(type)),
  }]);
}
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.low-risk-tools-not-governed", "Only non-low-risk tools are governed.", [{
    ...c,
    mcpSurfaces: c.mcpSurfaces.map((surface) => ({ ...surface, tools: surface.tools.map((tool) => ({ ...tool, risk: "low" })) })),
    trace: c.trace.filter(({ type }) => type !== "human.confirmation_received"),
  }]);
  record("evaluateConformance", "evaluate.high-risk-availability", "A high-risk tool called before gates.", [{
    ...c,
    mcpSurfaces: c.mcpSurfaces.map((surface) => ({ ...surface, tools: surface.tools.map((tool) => ({ ...tool, risk: "high" })) })),
  }]);
}
record("evaluateConformance", "evaluate.intent-and-completion-failures", "Wrong goal and failed task.", [withTrace(
  trace().map((event) => event.type === "intent.submitted" ? { ...event, evidence: { goal: "Something else" } } : event.type === "task.completed" ? { ...event, type: "task.failed" } : event),
)]);
record("evaluateConformance", "evaluate.intent-goal-type", "A non-string goal never matches the explicit goal.", [withTrace(
  trace().map((event) => event.type === "intent.submitted" ? { ...event, evidence: { goal: true } } : event),
)]);
record("evaluateConformance", "evaluate.wrong-version-selected", "Version selection with a different version and subject.", [withTrace(
  trace().map((event) => event.type === "lasm.version_selected" ? { ...event, evidence: { version: "2026-01-01.0" } } : event),
)]);
record("evaluateConformance", "evaluate.version-selected-without-subject", "Version selection without a subject.", [withTrace(
  trace().map((event) => { if (event.type !== "lasm.version_selected") return event; const { subjectId: _s, ...rest } = event; return rest; }),
)]);
record("evaluateConformance", "evaluate.unmodeled-control-surfaces", "Trace uses harnesses, skills, servers, and primitives absent from fixtures.", [withTrace([
  ...trace(),
  { type: "harness.selected", sequence: 41, actorId: "system", subjectId: "harness.rogue", evidence: { x: 1 } },
  { type: "skill.activated", sequence: 42, actorId: "agent", subjectId: "skill.rogue", evidence: { x: 1 } },
  { type: "mcp.server_connected", sequence: 43, actorId: "harness", subjectId: "mcp.rogue", evidence: { x: 1 } },
  { type: "mcp.prompt_used", sequence: 44, actorId: "agent", subjectId: "prompt.rogue", evidence: { x: 1 } },
  { type: "mcp.tool_called", sequence: 45, actorId: "agent", subjectId: "tool.rogue", evidence: { x: 1 } },
  { type: "mcp.tool_selected", sequence: 46, actorId: "agent", evidence: { x: 1 } },
  { type: "harness.selected", sequence: 47, actorId: "system", subjectId: "harness.rogue", evidence: { x: 1 } },
])]);
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.missing-control-fixtures", "Expected control surfaces absent from fixtures.", [{
    ...c, harnesses: [], skills: [], mcpSurfaces: [],
  }]);
}
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.missing-state-and-outcome-evidence", "No observations, commits, or validated outcomes.", [{
    ...c, trace: c.trace.filter(({ type }) => !["state.observed", "state.transition_committed", "outcome.validated", "outcome.observed"].includes(type)),
  }]);
  record("evaluateConformance", "evaluate.optional-expectations", "Optional permitted and acceptable expectations without evidence.", [{
    ...c,
    transitions: [...c.transitions, { id: "transition.optional", description: "Optional.", disposition: "permitted", required: false, fieldIds: ["field.appointment-status"] }],
    outcomes: [...c.outcomes, { id: "outcome.optional", description: "Optional.", disposition: "acceptable", required: false, fieldIds: ["field.appointment-status"] }],
    scenario: { ...c.scenario, reality: { ...c.scenario.reality, transitionIds: [...c.scenario.reality.transitionIds, "transition.optional"], outcomeIds: [...c.scenario.reality.outcomeIds, "outcome.optional"] } },
  }]);
}
record("evaluateConformance", "evaluate.invalid-trace-events", "Unknown and actorless events produce deduplicated findings.", [withTrace([
  ...trace(),
  { type: "unknown.event", sequence: 41, actorId: "agent", evidence: { x: 1 } },
  { type: "task.completed", sequence: 42, evidence: { x: 1 } },
  { type: "task.completed", sequence: 1, actorId: "agent", evidence: { duplicate: true } },
  { type: "task.completed", sequence: 43.5, actorId: "agent" },
])]);
record("evaluateConformance", "evaluate.empty-evidence-payloads", "Events without evidence produce a warning.", [withTrace([
  ...trace().map((event, index) => index % 7 === 3 ? { ...event, evidence: {} } : event),
  { type: "handoff.created", sequence: 41, actorId: "agent", subjectId: "handoff.warranty-exception" },
])]);
record("evaluateConformance", "evaluate.equal-sequences", "Equal sequences keep input order for gate timing.", [withTrace(
  trace().map((event) => ["policy.check_passed", "lasm.evaluation_passed", "human.confirmation_received", "mcp.tool_called"].includes(event.type) ? { ...event, sequence: 30 } : event),
)]);
record("evaluateConformance", "evaluate.unsequenced-trace", "A trace with no sequences keeps input order.", [withTrace(
  trace().reverse().map(({ sequence: _sequence, ...event }) => event),
)]);
record("evaluateConformance", "evaluate.empty-trace", "An empty trace.", [withTrace([])]);
{
  const c = baseCase();
  record("evaluateConformance", "evaluate.invalid-assembly", "Assembly validation findings propagate to reality-model validity.", [{
    ...c, assembly: { ...c.assembly, description: "", evaluations: [{ ...c.assembly.evaluations[0], addressedEntryIds: ["entry.missing"] }] },
  }]);
  record("evaluateConformance", "evaluate.evidence-links-missing", "No evidence link and missing required trace types.", [{
    ...c, trace: c.trace.filter(({ type }) => type !== "evidence.linked" && type !== "lasm.projection_loaded"),
  }]);
  record("evaluateConformance", "evaluate.consultation-gaps", "Unconsulted relevant entries and a divergence without subject.", [{
    ...c,
    trace: [
      ...c.trace.filter(({ type, subjectId }) => !(type === "lasm.entry_consulted" && (subjectId === "concept.appointment-slot" || subjectId === "evaluation.scheduling-gate"))),
      { type: "lasm.divergence_detected", sequence: 41, actorId: "auto-bench", evidence: { reason: "unspecified" } },
      { type: "lasm.entry_consulted", sequence: 42, actorId: "agent", subjectId: "concept.customer-consent", evidence: { reason: "again" } },
    ],
  }]);
}
{
  const c = baseCase();
  const nested = { flag: false, count: 0, text: "", nothing: null, nested: { list: [false, 0, "", null] } };
  record("evaluateConformance", "evaluate.nested-evidence-scalars", "Falsy nested evidence and state values do not change passing results.", [{
    ...c,
    initialState: { ...c.initialState, fields: c.initialState.fields.map((field, index) => index === 0 ? { ...field, value: nested } : field) },
    observations: c.observations.map((observation) => ({ ...observation, observedValues: { ...observation.observedValues, ...nested } })),
    trace: c.trace.map((event) => event.type === "evidence.linked" ? { ...event, evidence: { ...event.evidence, ...nested } } : event),
  }]);
}

// ---------------------------------------------------------------------------

mkdirSync(outDir, { recursive: true });
let total = 0;
for (const [group, entries] of [...groups.entries()].sort(([a], [b]) => a.localeCompare(b))) {
  writeFileSync(join(outDir, `${group}.json`), `${JSON.stringify(entries, null, 2)}\n`);
  total += entries.length;
}
console.log(`wrote ${total} cases in ${groups.size} files to ${outDir}`);
