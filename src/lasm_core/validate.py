from __future__ import annotations

from collections.abc import Collection, Sequence, Set

from .conformance import ConformanceCase
from .domain import ValidationFinding, ValidationResult, validation_result
from .harness import HarnessDescriptor
from .lasm import LasmProjectionReferences, LogicalAssemblySlice, logical_assembly_entries, logical_assembly_entry_ids
from .mcp import McpSurfaceDescriptor, mcp_primitives
from .operational_state import ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation
from .scenario import Scenario
from .skill import SkillDescriptor
from .trace import RawTraceEvent, is_agentic_event_type


def _required(value: str, path: str, findings: list[ValidationFinding]) -> None:
    if not value.strip():
        findings.append({"code": "fixture.required", "severity": "error", "path": path, "message": "A non-empty value is required."})


def _non_empty(values: Collection[object], path: str, findings: list[ValidationFinding]) -> None:
    if len(values) == 0:
        findings.append({"code": "fixture.non_empty", "severity": "error", "path": path, "message": "At least one item is required."})


def _unique_ids(ids: Sequence[str], path: str, findings: list[ValidationFinding]) -> None:
    # Report each duplicate once, in the order of its second occurrence.
    seen: set[str] = set()
    duplicates: dict[str, None] = {}
    for id in ids:
        if id in seen:
            duplicates.setdefault(id)
        else:
            seen.add(id)
    for id in duplicates:
        findings.append({"code": "fixture.duplicate_id", "severity": "error", "path": path, "message": f"Duplicate id: {id}"})


def _unique_sequences(trace: Sequence[RawTraceEvent], findings: list[ValidationFinding]) -> None:
    # Sequences are compared as numbers, so 1 and 1.0 are the same sequence.
    seen: set[int | float] = set()
    duplicates: dict[int | float, None] = {}
    for event in trace:
        sequence = event.get("sequence")
        if sequence is None:
            continue
        if sequence in seen:
            duplicates.setdefault(sequence)
        else:
            seen.add(sequence)
    for sequence in duplicates:
        findings.append({"code": "fixture.duplicate_id", "severity": "error", "path": "trace.sequence", "message": f"Duplicate id: {sequence}"})


def _is_integer_valued(value: int | float) -> bool:
    # JSON does not distinguish 2 from 2.0, so an integer-valued float is an integer sequence.
    return isinstance(value, int) or value.is_integer()


def _reference(
    id: str,
    known_ids: Set[str],
    path: str,
    code: str,
    label: str,
    findings: list[ValidationFinding],
) -> None:
    if id not in known_ids:
        findings.append({"code": code, "severity": "error", "path": path, "message": f"Unknown {label}: {id}"})


def _state_field_ids(state: OperationalState | None) -> frozenset[str] | None:
    return None if state is None else frozenset(field["id"] for field in state["fields"])


def _validate_projection_references(
    projection: LasmProjectionReferences | None,
    path: str,
    assembly_entry_ids: Set[str] | None,
    state_field_ids: Set[str] | None,
    findings: list[ValidationFinding],
) -> None:
    if projection is None:
        return
    state_ids = projection.get("stateFieldIds") or []
    if len(projection["assemblyEntryIds"]) == 0 and len(state_ids) == 0:
        findings.append({
            "code": "projection.empty",
            "severity": "error",
            "path": path,
            "message": "A projection must reference assembly entries or operational-state fields.",
        })
    _unique_ids(projection["assemblyEntryIds"], f"{path}.assemblyEntryIds", findings)
    _unique_ids(state_ids, f"{path}.stateFieldIds", findings)
    if assembly_entry_ids is not None:
        for index, id in enumerate(projection["assemblyEntryIds"]):
            _reference(id, assembly_entry_ids, f"{path}.assemblyEntryIds[{index}]", "projection.unknown_assembly_entry", "assembly entry", findings)
    if state_field_ids is not None:
        for index, id in enumerate(state_ids):
            _reference(id, state_field_ids, f"{path}.stateFieldIds[{index}]", "projection.unknown_state_field", "state field", findings)


def validate_logical_assembly(assembly: LogicalAssemblySlice) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(assembly["id"], "assembly.id", findings)
    _required(assembly["version"], "assembly.version", findings)
    _required(assembly["title"], "assembly.title", findings)
    _required(assembly["description"], "assembly.description", findings)
    _non_empty(assembly["provenance"], "assembly.provenance", findings)
    _non_empty(assembly["concepts"], "assembly.concepts", findings)
    _non_empty(assembly["evaluations"], "assembly.evaluations", findings)

    _unique_ids([source["id"] for source in assembly["provenance"]], "assembly.provenance", findings)
    source_ids = frozenset(source["id"] for source in assembly["provenance"])
    for index, source in enumerate(assembly["provenance"]):
        _required(source["id"], f"assembly.provenance[{index}].id", findings)
        _required(source["title"], f"assembly.provenance[{index}].title", findings)
        _required(source["locator"], f"assembly.provenance[{index}].locator", findings)

    entries = logical_assembly_entries(assembly)
    _unique_ids([entry["id"] for entry in entries], "assembly.entries", findings)
    entry_ids = frozenset(entry["id"] for entry in entries)
    concept_ids = frozenset(concept["id"] for concept in assembly["concepts"])
    for index, entry in enumerate(entries):
        _required(entry["id"], f"assembly.entries[{index}].id", findings)
        _required(entry["name"], f"assembly.entries[{index}].name", findings)
        _required(entry["description"], f"assembly.entries[{index}].description", findings)
        _non_empty(entry["sourceIds"], f"assembly.entries[{index}].sourceIds", findings)
        for source_index, id in enumerate(entry["sourceIds"]):
            _reference(id, source_ids, f"assembly.entries[{index}].sourceIds[{source_index}]", "assembly.unknown_provenance", "provenance source", findings)

    for index, relation in enumerate(assembly["relations"]):
        _reference(relation["fromConceptId"], concept_ids, f"assembly.relations[{index}].fromConceptId", "assembly.unknown_concept", "concept", findings)
        _reference(relation["toConceptId"], concept_ids, f"assembly.relations[{index}].toConceptId", "assembly.unknown_concept", "concept", findings)
        _required(relation["predicate"], f"assembly.relations[{index}].predicate", findings)
    for index, constraint in enumerate(assembly["constraints"]):
        _non_empty(constraint["appliesToEntryIds"], f"assembly.constraints[{index}].appliesToEntryIds", findings)
        for ref_index, id in enumerate(constraint["appliesToEntryIds"]):
            _reference(id, entry_ids, f"assembly.constraints[{index}].appliesToEntryIds[{ref_index}]", "assembly.unknown_entry", "assembly entry", findings)
        _required(constraint["rule"], f"assembly.constraints[{index}].rule", findings)
    for index, event in enumerate(assembly["events"]):
        _non_empty(event["subjectConceptIds"], f"assembly.events[{index}].subjectConceptIds", findings)
        for ref_index, id in enumerate(event["subjectConceptIds"]):
            _reference(id, concept_ids, f"assembly.events[{index}].subjectConceptIds[{ref_index}]", "assembly.unknown_concept", "concept", findings)
    for index, policy in enumerate(assembly["policies"]):
        _non_empty(policy["appliesToEntryIds"], f"assembly.policies[{index}].appliesToEntryIds", findings)
        _non_empty(policy["authorityRoles"], f"assembly.policies[{index}].authorityRoles", findings)
        for ref_index, id in enumerate(policy["appliesToEntryIds"]):
            _reference(id, entry_ids, f"assembly.policies[{index}].appliesToEntryIds[{ref_index}]", "assembly.unknown_entry", "assembly entry", findings)
        _required(policy["commitment"], f"assembly.policies[{index}].commitment", findings)
    for index, evaluation in enumerate(assembly["evaluations"]):
        _non_empty(evaluation["addressedEntryIds"], f"assembly.evaluations[{index}].addressedEntryIds", findings)
        for ref_index, id in enumerate(evaluation["addressedEntryIds"]):
            _reference(id, entry_ids, f"assembly.evaluations[{index}].addressedEntryIds[{ref_index}]", "assembly.unknown_entry", "assembly entry", findings)
        _required(evaluation["evaluatorId"], f"assembly.evaluations[{index}].evaluatorId", findings)
    return validation_result(findings)


def validate_operational_state(state: OperationalState, assembly: LogicalAssemblySlice) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(state["id"], "initialState.id", findings)
    if state["assemblyId"] != assembly["id"]:
        findings.append({"code": "state.assembly_mismatch", "severity": "error", "path": "initialState.assemblyId", "message": "Initial state references a different assembly."})
    if state["assemblyVersion"] != assembly["version"]:
        findings.append({"code": "state.version_mismatch", "severity": "error", "path": "initialState.assemblyVersion", "message": "Initial state references a different assembly version."})
    _non_empty(state["fields"], "initialState.fields", findings)
    _unique_ids([field["id"] for field in state["fields"]], "initialState.fields", findings)
    concept_ids = frozenset(concept["id"] for concept in assembly["concepts"])
    for index, field in enumerate(state["fields"]):
        _required(field["id"], f"initialState.fields[{index}].id", findings)
        _reference(field["conceptId"], concept_ids, f"initialState.fields[{index}].conceptId", "state.unknown_concept", "concept", findings)
    return validation_result(findings)


def validate_actor_observation(observation: ActorObservation, state: OperationalState) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(observation["id"], "observation.id", findings)
    _required(observation["actorId"], "observation.actorId", findings)
    _non_empty(observation["fieldIds"], "observation.fieldIds", findings)
    field_ids = frozenset(field["id"] for field in state["fields"])
    for index, id in enumerate(observation["fieldIds"]):
        _reference(id, field_ids, f"observation.fieldIds[{index}]", "observation.unknown_state_field", "state field", findings)
    return validation_result(findings)


def validate_state_transition(
    transition: StateTransitionExpectation,
    state: OperationalState,
    assembly: LogicalAssemblySlice,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(transition["id"], "transition.id", findings)
    _required(transition["description"], "transition.description", findings)
    _non_empty(transition["fieldIds"], "transition.fieldIds", findings)
    field_ids = frozenset(field["id"] for field in state["fields"])
    for index, id in enumerate(transition["fieldIds"]):
        _reference(id, field_ids, f"transition.fieldIds[{index}]", "transition.unknown_state_field", "state field", findings)
    if "eventId" in transition:
        _reference(
            transition["eventId"],
            frozenset(event["id"] for event in assembly["events"]),
            "transition.eventId",
            "transition.unknown_event",
            "assembly event",
            findings,
        )
    return validation_result(findings)


def validate_outcome(outcome: OutcomeExpectation, state: OperationalState) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(outcome["id"], "outcome.id", findings)
    _required(outcome["description"], "outcome.description", findings)
    _non_empty(outcome["fieldIds"], "outcome.fieldIds", findings)
    field_ids = frozenset(field["id"] for field in state["fields"])
    for index, id in enumerate(outcome["fieldIds"]):
        _reference(id, field_ids, f"outcome.fieldIds[{index}]", "outcome.unknown_state_field", "state field", findings)
    return validation_result(findings)


def validate_scenario(scenario: Scenario) -> ValidationResult:
    findings: list[ValidationFinding] = []
    business_context = scenario["businessContext"]
    reality = scenario["reality"]
    expected = scenario["expectedControlSurfaces"]
    _required(scenario["id"], "scenario.id", findings)
    _required(scenario["title"], "scenario.title", findings)
    _required(business_context["summary"], "scenario.businessContext.summary", findings)
    _required(scenario["intent"]["explicitGoal"], "scenario.intent.explicitGoal", findings)
    _required(reality["assemblyId"], "scenario.reality.assemblyId", findings)
    _required(reality["assemblyVersion"], "scenario.reality.assemblyVersion", findings)
    _required(reality["initialStateId"], "scenario.reality.initialStateId", findings)
    _non_empty(business_context["stakeholders"], "scenario.businessContext.stakeholders", findings)
    _non_empty(business_context["requiredFacts"], "scenario.businessContext.requiredFacts", findings)
    _non_empty(reality["assemblyEntryIds"], "scenario.reality.assemblyEntryIds", findings)
    _non_empty(reality["observationIds"], "scenario.reality.observationIds", findings)
    _non_empty(reality["transitionIds"], "scenario.reality.transitionIds", findings)
    _non_empty(reality["outcomeIds"], "scenario.reality.outcomeIds", findings)
    _non_empty(expected["harnessIds"], "scenario.expectedControlSurfaces.harnessIds", findings)
    _unique_ids(
        [
            *expected["harnessIds"],
            *expected["skillIds"],
            *expected["mcpServerIds"],
            *expected["mcpPrimitiveIds"],
        ],
        "scenario.expectedControlSurfaces",
        findings,
    )
    return validation_result(findings)


def validate_harness(
    harness: HarnessDescriptor,
    assembly: LogicalAssemblySlice | None = None,
    state: OperationalState | None = None,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(harness["id"], "harness.id", findings)
    _required(harness["name"], "harness.name", findings)
    _required(harness["purpose"], "harness.purpose", findings)
    _non_empty(harness["contextSurfaces"], "harness.contextSurfaces", findings)
    _non_empty(harness["affordances"], "harness.affordances", findings)
    _non_empty(harness["permissionModel"]["scopedPermissions"], "harness.permissionModel.scopedPermissions", findings)
    _non_empty(harness["handoffBoundaries"], "harness.handoffBoundaries", findings)
    _unique_ids([surface["id"] for surface in harness["contextSurfaces"]], "harness.contextSurfaces", findings)
    _unique_ids([boundary["id"] for boundary in harness["handoffBoundaries"]], "harness.handoffBoundaries", findings)
    entry_ids = None if assembly is None else logical_assembly_entry_ids(assembly)
    field_ids = _state_field_ids(state)
    _validate_projection_references(harness.get("projection"), "harness.projection", entry_ids, field_ids, findings)
    for index, surface in enumerate(harness["contextSurfaces"]):
        _validate_projection_references(surface.get("projection"), f"harness.contextSurfaces[{index}].projection", entry_ids, field_ids, findings)
    _validate_projection_references(harness["permissionModel"].get("projection"), "harness.permissionModel.projection", entry_ids, field_ids, findings)
    _validate_projection_references(harness["approvalFlow"].get("projection"), "harness.approvalFlow.projection", entry_ids, field_ids, findings)
    for index, boundary in enumerate(harness["handoffBoundaries"]):
        _validate_projection_references(boundary.get("projection"), f"harness.handoffBoundaries[{index}].projection", entry_ids, field_ids, findings)
    return validation_result(findings)


def validate_skill(
    skill: SkillDescriptor,
    assembly: LogicalAssemblySlice | None = None,
    state: OperationalState | None = None,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(skill["id"], "skill.id", findings)
    _required(skill["name"], "skill.name", findings)
    _required(skill["purpose"], "skill.purpose", findings)
    _non_empty(skill["applicability"], "skill.applicability", findings)
    _non_empty(skill["capabilities"], "skill.capabilities", findings)
    _validate_projection_references(
        skill.get("projection"),
        "skill.projection",
        None if assembly is None else logical_assembly_entry_ids(assembly),
        _state_field_ids(state),
        findings,
    )
    return validation_result(findings)


def validate_mcp_surface(
    surface: McpSurfaceDescriptor,
    assembly: LogicalAssemblySlice | None = None,
    state: OperationalState | None = None,
) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _required(surface["id"], "mcp.id", findings)
    _required(surface["name"], "mcp.name", findings)
    _required(surface["purpose"], "mcp.purpose", findings)
    primitives = mcp_primitives(surface)
    _non_empty(primitives, "mcp.primitives", findings)
    _unique_ids([primitive["id"] for primitive in primitives], "mcp.primitives", findings)
    entry_ids = None if assembly is None else logical_assembly_entry_ids(assembly)
    field_ids = _state_field_ids(state)
    _validate_projection_references(surface.get("projection"), "mcp.projection", entry_ids, field_ids, findings)
    for index, primitive in enumerate(primitives):
        _required(primitive["id"], f"mcp.primitives[{index}].id", findings)
        _required(primitive["name"], f"mcp.primitives[{index}].name", findings)
        _required(primitive["purpose"], f"mcp.primitives[{index}].purpose", findings)
        _validate_projection_references(primitive.get("projection"), f"mcp.primitives[{index}].projection", entry_ids, field_ids, findings)
    return validation_result(findings)


def validate_trace(trace: Sequence[RawTraceEvent]) -> ValidationResult:
    findings: list[ValidationFinding] = []
    _non_empty(trace, "trace", findings)
    _unique_sequences(trace, findings)

    for index, event in enumerate(trace):
        if not is_agentic_event_type(event["type"]):
            findings.append({
                "code": "trace.unknown_event_type",
                "severity": "error",
                "path": f"trace[{index}].type",
                "message": f"Unknown agentic event type: {event['type'] or '<empty>'}",
            })
        actor_id = event.get("actorId")
        if actor_id is None or not actor_id.strip():
            findings.append({
                "code": "trace.missing_actor",
                "severity": "error",
                "path": f"trace[{index}].actorId",
                "message": "Trace events require an actor identifier.",
            })
        sequence = event.get("sequence")
        if sequence is not None and (not _is_integer_valued(sequence) or sequence < 0):
            findings.append({
                "code": "trace.invalid_sequence",
                "severity": "error",
                "path": f"trace[{index}].sequence",
                "message": "Sequence must be a non-negative integer.",
            })
    return validation_result(findings)


def validate_conformance_case(input: ConformanceCase) -> ValidationResult:
    assembly = input["assembly"]
    initial_state = input["initialState"]
    findings: list[ValidationFinding] = [
        *validate_logical_assembly(assembly)["findings"],
        *validate_operational_state(initial_state, assembly)["findings"],
        *validate_scenario(input["scenario"])["findings"],
    ]
    for observation in input["observations"]:
        findings.extend(validate_actor_observation(observation, initial_state)["findings"])
    for transition in input["transitions"]:
        findings.extend(validate_state_transition(transition, initial_state, assembly)["findings"])
    for outcome in input["outcomes"]:
        findings.extend(validate_outcome(outcome, initial_state)["findings"])
    for harness in input["harnesses"]:
        findings.extend(validate_harness(harness, assembly, initial_state)["findings"])
    for skill in input["skills"]:
        findings.extend(validate_skill(skill, assembly, initial_state)["findings"])
    for surface in input["mcpSurfaces"]:
        findings.extend(validate_mcp_surface(surface, assembly, initial_state)["findings"])
    findings.extend(validate_trace(input["trace"])["findings"])

    reality = input["scenario"]["reality"]
    assembly_entry_ids = logical_assembly_entry_ids(assembly)
    observation_ids = frozenset(observation["id"] for observation in input["observations"])
    transition_ids = frozenset(transition["id"] for transition in input["transitions"])
    outcome_ids = frozenset(outcome["id"] for outcome in input["outcomes"])
    if reality["assemblyId"] != assembly["id"]:
        findings.append({"code": "scenario.assembly_mismatch", "severity": "error", "path": "scenario.reality.assemblyId", "message": "Scenario references a different assembly."})
    if reality["assemblyVersion"] != assembly["version"]:
        findings.append({"code": "scenario.version_mismatch", "severity": "error", "path": "scenario.reality.assemblyVersion", "message": "Scenario references a different assembly version."})
    if reality["initialStateId"] != initial_state["id"]:
        findings.append({"code": "scenario.state_mismatch", "severity": "error", "path": "scenario.reality.initialStateId", "message": "Scenario references a different initial state."})
    for index, id in enumerate(reality["assemblyEntryIds"]):
        _reference(id, assembly_entry_ids, f"scenario.reality.assemblyEntryIds[{index}]", "scenario.unknown_assembly_entry", "assembly entry", findings)
    for index, id in enumerate(reality["observationIds"]):
        _reference(id, observation_ids, f"scenario.reality.observationIds[{index}]", "scenario.unknown_observation", "observation", findings)
    for index, id in enumerate(reality["transitionIds"]):
        _reference(id, transition_ids, f"scenario.reality.transitionIds[{index}]", "scenario.unknown_transition", "transition", findings)
    for index, id in enumerate(reality["outcomeIds"]):
        _reference(id, outcome_ids, f"scenario.reality.outcomeIds[{index}]", "scenario.unknown_outcome", "outcome", findings)

    expected = input["scenario"]["expectedControlSurfaces"]
    harness_ids = frozenset(harness["id"] for harness in input["harnesses"])
    skill_ids = frozenset(skill["id"] for skill in input["skills"])
    server_ids = frozenset(surface["id"] for surface in input["mcpSurfaces"])
    primitive_ids = frozenset(primitive["id"] for surface in input["mcpSurfaces"] for primitive in mcp_primitives(surface))
    for index, id in enumerate(expected["harnessIds"]):
        _reference(id, harness_ids, f"scenario.expectedControlSurfaces.harnessIds[{index}]", "scenario.unknown_harness", "harness", findings)
    for index, id in enumerate(expected["skillIds"]):
        _reference(id, skill_ids, f"scenario.expectedControlSurfaces.skillIds[{index}]", "scenario.unknown_skill", "skill", findings)
    for index, id in enumerate(expected["mcpServerIds"]):
        _reference(id, server_ids, f"scenario.expectedControlSurfaces.mcpServerIds[{index}]", "scenario.unknown_mcp_server", "MCP server", findings)
    for index, id in enumerate(expected["mcpPrimitiveIds"]):
        _reference(id, primitive_ids, f"scenario.expectedControlSurfaces.mcpPrimitiveIds[{index}]", "scenario.unknown_mcp_primitive", "MCP primitive", findings)

    _unique_ids([observation["id"] for observation in input["observations"]], "observations", findings)
    _unique_ids([transition["id"] for transition in input["transitions"]], "transitions", findings)
    _unique_ids([outcome["id"] for outcome in input["outcomes"]], "outcomes", findings)
    _unique_ids([harness["id"] for harness in input["harnesses"]], "harnesses", findings)
    _unique_ids([skill["id"] for skill in input["skills"]], "skills", findings)
    _unique_ids([surface["id"] for surface in input["mcpSurfaces"]], "mcpSurfaces", findings)

    return validation_result(findings)
