from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict

from .conformance import ConformanceCase
from .domain import ValidationFinding
from .lasm import LasmProjectionReferences
from .mcp import McpSurfaceDescriptor, mcp_primitives
from .scenario import Scenario
from .trace import AgenticEventType, NormalizedTraceEvent, normalize_trace, trace_evidence_ref
from .validate import validate_conformance_case, validate_logical_assembly

EvaluationDimension: TypeAlias = Literal[
    "intent-fidelity",
    "semantic-fidelity",
    "reality-model-validity",
    "state-and-outcome-validity",
    "control-surface-quality",
    "reality-coverage",
    "evidence-and-attribution",
    "governance",
]
EvaluationStatus: TypeAlias = Literal["pass", "warning", "fail"]
EvaluationFindingSeverity: TypeAlias = Literal["info", "warning", "error"]
DivergenceSource: TypeAlias = Literal[
    "reality-model",
    "projection",
    "control-surface",
    "agent-conduct",
    "external-system",
    "insufficient-evidence",
]


class EvaluationFinding(TypedDict):
    code: str
    severity: EvaluationFindingSeverity
    message: str
    evidenceRefs: Sequence[str]
    assemblyEntryIds: Sequence[str]
    transitionIds: Sequence[str]
    outcomeIds: Sequence[str]
    attribution: NotRequired[DivergenceSource]


class DimensionResult(TypedDict):
    dimension: EvaluationDimension
    status: EvaluationStatus
    findings: Sequence[EvaluationFinding]
    evidenceRefs: Sequence[str]


class ConformanceEvaluation(TypedDict):
    assemblyId: str
    assemblyVersion: str
    scenarioId: str
    valid: bool
    conformant: bool
    validationFindings: Sequence[ValidationFinding]
    dimensions: Sequence[DimensionResult]


def _events_of_type(events: Sequence[NormalizedTraceEvent], *types: AgenticEventType) -> list[NormalizedTraceEvent]:
    return [event for event in events if event["type"] in types]


def _subject_ids(events: Iterable[NormalizedTraceEvent]) -> dict[str, None]:
    """Subject identifiers in first-occurrence order (an insertion-ordered set)."""
    return dict.fromkeys(event["subjectId"] for event in events if "subjectId" in event)


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _refs(events: Iterable[NormalizedTraceEvent]) -> list[str]:
    return [trace_evidence_ref(event) for event in events]


def _result(dimension: EvaluationDimension, findings: Sequence[EvaluationFinding]) -> DimensionResult:
    severities = {finding["severity"] for finding in findings}
    status: EvaluationStatus = "fail" if "error" in severities else "warning" if "warning" in severities else "pass"
    return {
        "dimension": dimension,
        "status": status,
        "findings": findings,
        "evidenceRefs": _unique(ref for finding in findings for ref in finding["evidenceRefs"]),
    }


def _finding(
    code: str,
    severity: EvaluationFindingSeverity,
    message: str,
    *,
    evidence_refs: Sequence[str] = (),
    assembly_entry_ids: Sequence[str] = (),
    transition_ids: Sequence[str] = (),
    outcome_ids: Sequence[str] = (),
    attribution: DivergenceSource | None = None,
) -> EvaluationFinding:
    finding: EvaluationFinding = {
        "code": code,
        "severity": severity,
        "message": message,
        "evidenceRefs": list(evidence_refs),
        "assemblyEntryIds": list(assembly_entry_ids),
        "transitionIds": list(transition_ids),
        "outcomeIds": list(outcome_ids),
    }
    if attribution is not None:
        finding["attribution"] = attribution
    return finding


def _passing_finding(
    code: str,
    message: str,
    events: Sequence[NormalizedTraceEvent],
    *,
    assembly_entry_ids: Sequence[str] = (),
    transition_ids: Sequence[str] = (),
    outcome_ids: Sequence[str] = (),
) -> EvaluationFinding:
    return _finding(
        code,
        "info",
        message,
        evidence_refs=_refs(events),
        assembly_entry_ids=assembly_entry_ids,
        transition_ids=transition_ids,
        outcome_ids=outcome_ids,
    )


def _projection_references(input: ConformanceCase) -> list[LasmProjectionReferences]:
    references: list[LasmProjectionReferences | None] = []
    for harness in input["harnesses"]:
        references.append(harness.get("projection"))
        references.extend(surface.get("projection") for surface in harness["contextSurfaces"])
        references.append(harness["permissionModel"].get("projection"))
        references.append(harness["approvalFlow"].get("projection"))
        references.extend(boundary.get("projection") for boundary in harness["handoffBoundaries"])
    references.extend(skill.get("projection") for skill in input["skills"])
    for surface in input["mcpSurfaces"]:
        references.append(surface.get("projection"))
        references.extend(primitive.get("projection") for primitive in mcp_primitives(surface))
    return [projection for projection in references if projection is not None]


def _evaluate_intent(scenario: Scenario, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    submitted = _events_of_type(events, "intent.submitted")
    outcomes = _events_of_type(events, "task.completed", "task.failed")
    explicit_goal = scenario["intent"]["explicitGoal"]
    preserved = [event for event in submitted if _json_equals(event["evidence"].get("goal"), explicit_goal)]
    findings: list[EvaluationFinding] = []
    findings.append(
        _passing_finding("intent.explicit_goal_observed", "The submitted intent matches the scenario's explicit goal.", preserved)
        if preserved
        else _finding(
            "intent.explicit_goal_missing",
            "error",
            "The trace does not preserve the scenario's explicit goal.",
            evidence_refs=_refs(submitted),
            attribution="agent-conduct",
        )
    )
    findings.append(
        _passing_finding("intent.outcome_completed", "The trace records a completed business outcome.", outcomes)
        if any(event["type"] == "task.completed" for event in outcomes)
        else _finding(
            "intent.outcome_incomplete",
            "error",
            "The trace does not record successful task completion.",
            evidence_refs=_refs(outcomes),
            attribution="agent-conduct",
        )
    )
    return _result("intent-fidelity", findings)


def _evaluate_semantic_fidelity(input: ConformanceCase, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    relevant_entry_ids = input["scenario"]["reality"]["assemblyEntryIds"]
    consulted_events = _events_of_type(events, "lasm.entry_consulted")
    consulted_ids = _subject_ids(consulted_events)
    divergence_events = _events_of_type(events, "lasm.divergence_detected")
    findings: list[EvaluationFinding] = []

    for id in relevant_entry_ids:
        matching = [event for event in consulted_events if event.get("subjectId") == id]
        findings.append(
            _passing_finding("semantic.entry_consulted", f"Relevant assembly entry was consulted: {id}", matching, assembly_entry_ids=[id])
            if id in consulted_ids
            else _finding(
                "semantic.entry_not_consulted",
                "error",
                f"Relevant assembly entry was not evidenced as consulted: {id}",
                assembly_entry_ids=[id],
                attribution="insufficient-evidence",
            )
        )
    for divergence in divergence_events:
        findings.append(_finding(
            "semantic.divergence_detected",
            "error",
            "The episode records semantic divergence.",
            evidence_refs=[trace_evidence_ref(divergence)],
            assembly_entry_ids=[divergence["subjectId"]] if "subjectId" in divergence else [],
            attribution="projection",
        ))
    return _result("semantic-fidelity", findings)


def _evaluate_reality_model(input: ConformanceCase, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    assembly = input["assembly"]
    findings: list[EvaluationFinding] = []
    for validation in validate_logical_assembly(assembly)["findings"]:
        findings.append(_finding(
            "reality.invalid_assembly",
            "error" if validation["severity"] == "error" else "warning",
            validation["message"],
            attribution="reality-model",
        ))
    for source in assembly["provenance"]:
        if source["status"] == "stale":
            findings.append(_finding("reality.stale_source", "error", f"Assembly provenance is stale: {source['id']}", attribution="reality-model"))
        elif source["status"] == "disputed":
            findings.append(_finding("reality.disputed_source", "warning", f"Assembly provenance is disputed: {source['id']}", attribution="reality-model"))
    selected = [
        event
        for event in _events_of_type(events, "lasm.version_selected")
        if event.get("subjectId") == assembly["id"] and _json_equals(event["evidence"].get("version"), assembly["version"])
    ]
    findings.append(
        _passing_finding("reality.version_selected", "The episode identifies the governing assembly and version.", selected)
        if selected
        else _finding(
            "reality.version_not_selected",
            "error",
            "The trace does not identify the governing assembly version.",
            attribution="insufficient-evidence",
        )
    )
    if len(findings) == 1 and selected:
        findings.append(_finding("reality.sources_current", "info", "All assembly provenance sources are current."))
    return _result("reality-model-validity", findings)


def _evaluate_state_and_outcomes(input: ConformanceCase, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    findings: list[EvaluationFinding] = []
    observed_ids = _subject_ids(_events_of_type(events, "state.observed"))
    for observation in input["observations"]:
        observation_id = observation["id"]
        findings.append(
            _passing_finding(
                "state.observation_evidenced",
                f"Actor observation was evidenced: {observation_id}",
                [event for event in events if event["type"] == "state.observed" and event.get("subjectId") == observation_id],
            )
            if observation_id in observed_ids
            else _finding(
                "state.observation_missing",
                "error",
                f"Required actor observation is missing: {observation_id}",
                attribution="insufficient-evidence",
            )
        )

    committed = _events_of_type(events, "state.transition_committed")
    committed_ids = _subject_ids(committed)
    for transition in input["transitions"]:
        transition_id = transition["id"]
        matching = [event for event in committed if event.get("subjectId") == transition_id]
        if transition["disposition"] == "prohibited" and transition_id in committed_ids:
            findings.append(_finding(
                "state.prohibited_transition_committed",
                "error",
                f"A prohibited state transition was committed: {transition_id}",
                evidence_refs=_refs(matching),
                transition_ids=[transition_id],
                attribution="agent-conduct",
            ))
        elif transition["disposition"] == "permitted" and transition["required"] and transition_id not in committed_ids:
            findings.append(_finding(
                "state.required_transition_missing",
                "error",
                f"A required state transition was not committed: {transition_id}",
                transition_ids=[transition_id],
                attribution="insufficient-evidence",
            ))
        else:
            findings.append(_passing_finding(
                "state.transition_conformant",
                f"State transition evidence conforms: {transition_id}",
                matching,
                transition_ids=[transition_id],
            ))

    observed_outcomes = _events_of_type(events, "outcome.observed")
    validated_outcomes = _events_of_type(events, "outcome.validated")
    observed_outcome_ids = _subject_ids(observed_outcomes)
    validated_outcome_ids = _subject_ids(validated_outcomes)
    for outcome in input["outcomes"]:
        outcome_id = outcome["id"]
        matching = [event for event in [*observed_outcomes, *validated_outcomes] if event.get("subjectId") == outcome_id]
        if outcome["disposition"] == "prohibited" and outcome_id in observed_outcome_ids:
            findings.append(_finding(
                "outcome.prohibited_observed",
                "error",
                f"A prohibited outcome was observed: {outcome_id}",
                evidence_refs=_refs(matching),
                outcome_ids=[outcome_id],
                attribution="agent-conduct",
            ))
        elif outcome["disposition"] == "acceptable" and outcome["required"] and outcome_id not in validated_outcome_ids:
            findings.append(_finding(
                "outcome.required_not_validated",
                "error",
                f"A required acceptable outcome was not validated: {outcome_id}",
                outcome_ids=[outcome_id],
                attribution="insufficient-evidence",
            ))
        else:
            findings.append(_passing_finding(
                "outcome.expectation_satisfied",
                f"Outcome evidence conforms: {outcome_id}",
                matching,
                outcome_ids=[outcome_id],
            ))
    return _result("state-and-outcome-validity", findings)


def _evaluate_control_surfaces(input: ConformanceCase, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    expected = input["scenario"]["expectedControlSurfaces"]
    fixture_harness_ids = frozenset(harness["id"] for harness in input["harnesses"])
    fixture_skill_ids = frozenset(skill["id"] for skill in input["skills"])
    fixture_server_ids = frozenset(surface["id"] for surface in input["mcpSurfaces"])
    fixture_primitive_ids = frozenset(primitive["id"] for surface in input["mcpSurfaces"] for primitive in mcp_primitives(surface))
    selected_harness_ids = _subject_ids(_events_of_type(events, "harness.selected"))
    activated_skill_ids = _subject_ids(_events_of_type(events, "skill.activated"))
    connected_server_ids = _subject_ids(_events_of_type(events, "mcp.server_connected"))
    used_primitive_ids = _subject_ids(_events_of_type(events, "mcp.tool_selected", "mcp.tool_called", "mcp.resource_read", "mcp.prompt_used"))
    findings: list[EvaluationFinding] = []

    checks: tuple[tuple[str, str, Sequence[str], frozenset[str], dict[str, None]], ...] = (
        ("harness", "harness", expected["harnessIds"], fixture_harness_ids, selected_harness_ids),
        ("skill", "skill", expected["skillIds"], fixture_skill_ids, activated_skill_ids),
        ("mcp_server", "MCP server", expected["mcpServerIds"], fixture_server_ids, connected_server_ids),
        ("mcp_primitive", "MCP primitive", expected["mcpPrimitiveIds"], fixture_primitive_ids, used_primitive_ids),
    )
    for code, label, expected_ids, fixture_ids, observed_ids in checks:
        for id in expected_ids:
            if id not in fixture_ids:
                findings.append(_finding(f"control.{code}_fixture_missing", "error", f"Expected {label} fixture is missing: {id}", attribution="control-surface"))
            elif id not in observed_ids:
                findings.append(_finding(f"control.{code}_not_used", "error", f"Expected {label} was not observed in the trace: {id}", attribution="agent-conduct"))
        for id in observed_ids:
            if id not in fixture_ids:
                findings.append(_finding(f"control.{code}_unmodeled", "error", f"Trace used an unmodeled {label}: {id}", attribution="control-surface"))
    if not findings:
        expected_ids = [
            *expected["harnessIds"],
            *expected["skillIds"],
            *expected["mcpServerIds"],
            *expected["mcpPrimitiveIds"],
        ]
        findings.append(_passing_finding(
            "control.expected_surfaces_used",
            "All expected Lasm projections and control surfaces were modeled and used.",
            [event for event in events if "subjectId" in event and event["subjectId"] in expected_ids],
        ))
    return _result("control-surface-quality", findings)


def _evaluate_reality_coverage(input: ConformanceCase, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    findings: list[EvaluationFinding] = []
    reality_entry_ids = input["scenario"]["reality"]["assemblyEntryIds"]
    projected_entry_ids = frozenset(id for projection in _projection_references(input) for id in projection["assemblyEntryIds"])
    for id in reality_entry_ids:
        if id not in projected_entry_ids:
            findings.append(_finding(
                "coverage.assembly_entry_not_projected",
                "error",
                f"Relevant assembly entry is absent from agent-facing projections: {id}",
                assembly_entry_ids=[id],
                attribution="projection",
            ))

    observed_facts: set[str] = set()
    for event in events:
        facts = event["evidence"].get("businessFacts")
        if isinstance(facts, (list, tuple)):
            observed_facts.update(fact for fact in facts if isinstance(fact, str))
    for fact in input["scenario"]["businessContext"]["requiredFacts"]:
        if fact not in observed_facts:
            findings.append(_finding("coverage.required_fact_missing", "error", f"Required operational fact is not evidenced: {fact}", attribution="insufficient-evidence"))
    if not findings:
        findings.append(_passing_finding(
            "coverage.relevant_reality_covered",
            "Relevant assembly entries and operational facts are covered.",
            [event for event in events if isinstance(event["evidence"].get("businessFacts"), (list, tuple))],
            assembly_entry_ids=reality_entry_ids,
        ))
    return _result("reality-coverage", findings)


def _evaluate_evidence_and_attribution(scenario: Scenario, events: Sequence[NormalizedTraceEvent]) -> DimensionResult:
    findings: list[EvaluationFinding] = []
    for event_type in scenario["evaluation"]["requiredTraceTypes"]:
        if not _events_of_type(events, event_type):
            findings.append(_finding("evidence.required_event_missing", "error", f"Required evidence event is missing: {event_type}", attribution="insufficient-evidence"))
    without_evidence = [event for event in events if len(event["evidence"]) == 0]
    if without_evidence:
        findings.append(_finding(
            "evidence.empty_payload",
            "warning",
            f"{len(without_evidence)} event(s) have no evidence payload.",
            evidence_refs=_refs(without_evidence),
            attribution="insufficient-evidence",
        ))
    linked = _events_of_type(events, "evidence.linked")
    if not linked:
        findings.append(_finding("evidence.links_missing", "error", "The episode contains no explicit evidence link.", attribution="insufficient-evidence"))
    divergences = _events_of_type(events, "lasm.divergence_detected", "lasm.evaluation_failed")
    attributed = _events_of_type(events, "lasm.failure_attributed")
    for divergence in divergences:
        subject_id = divergence.get("subjectId")
        if not any(event.get("subjectId") == subject_id for event in attributed):
            findings.append(_finding(
                "attribution.failure_unattributed",
                "error",
                f"Failure lacks attribution: {'<unknown>' if subject_id is None else subject_id}",
                evidence_refs=[trace_evidence_ref(divergence)],
                assembly_entry_ids=[] if subject_id is None else [subject_id],
                attribution="insufficient-evidence",
            ))
    if not findings:
        findings.append(_passing_finding("evidence.episode_attributable", "Required evidence is present and failures are attributable.", linked))
    return _result("evidence-and-attribution", findings)


def _evaluate_governance(
    scenario: Scenario,
    mcp_surfaces: Sequence[McpSurfaceDescriptor],
    events: Sequence[NormalizedTraceEvent],
) -> DimensionResult:
    findings: list[EvaluationFinding] = []
    expectations = scenario["evaluation"]
    failed_policy = _events_of_type(events, "policy.check_failed", "lasm.evaluation_failed")
    passed_policy = _events_of_type(events, "policy.check_passed", "lasm.evaluation_passed")
    confirmation = _events_of_type(events, "human.confirmation_received")
    denied_permission = _events_of_type(events, "harness.permission_denied")
    if failed_policy:
        findings.append(_finding("governance.policy_failed", "error", "A policy or runtime Lasm evaluation failed.", evidence_refs=_refs(failed_policy), attribution="agent-conduct"))
    if denied_permission:
        findings.append(_finding("governance.permission_denied", "error", "A required harness permission was denied.", evidence_refs=_refs(denied_permission), attribution="control-surface"))
    if expectations["requiresPolicyCheck"]:
        findings.append(
            _passing_finding("governance.policy_passed", "The required policy or Lasm runtime evaluation passed.", passed_policy)
            if passed_policy
            else _finding("governance.policy_missing", "error", "The scenario requires a passing policy or Lasm runtime evaluation.", attribution="insufficient-evidence")
        )
    if expectations["requiresHumanConfirmation"]:
        findings.append(
            _passing_finding("governance.confirmation_received", "The required human confirmation was received.", confirmation)
            if confirmation
            else _finding("governance.confirmation_missing", "error", "The scenario requires human confirmation.", attribution="agent-conduct")
        )
    governed_tool_ids = frozenset(tool["id"] for surface in mcp_surfaces for tool in surface["tools"] if tool["risk"] != "low")
    governed_calls = [
        event
        for event in _events_of_type(events, "mcp.tool_called")
        if "subjectId" in event and event["subjectId"] in governed_tool_ids
    ]
    for call in governed_calls:
        if expectations["requiresPolicyCheck"] and not any(event["position"] < call["position"] for event in passed_policy):
            findings.append(_finding(
                "governance.policy_too_late",
                "error",
                f"A passing policy check was not recorded before governed tool call: {call['subjectId']}",
                evidence_refs=[trace_evidence_ref(call)],
                attribution="agent-conduct",
            ))
        if expectations["requiresHumanConfirmation"] and not any(event["position"] < call["position"] for event in confirmation):
            findings.append(_finding(
                "governance.confirmation_too_late",
                "error",
                f"Human confirmation was not recorded before governed tool call: {call['subjectId']}",
                evidence_refs=[trace_evidence_ref(call)],
                attribution="agent-conduct",
            ))
    if not findings:
        findings.append(_passing_finding("governance.no_required_gates", "No governance gates were required or failed.", []))
    return _result("governance", findings)


def _json_equals(value: object, expected: str) -> bool:
    # Evidence is arbitrary JSON: only an identical string matches, with no coercion.
    return isinstance(value, str) and value == expected


def evaluate_conformance(input: ConformanceCase) -> ConformanceEvaluation:
    validation = validate_conformance_case(input)
    normalized = normalize_trace(input["trace"])
    validation_keys = {(finding["code"], finding["path"]) for finding in validation["findings"]}
    validation_findings = [
        *validation["findings"],
        *(finding for finding in normalized["findings"] if (finding["code"], finding["path"]) not in validation_keys),
    ]
    events = normalized["events"]
    dimensions = [
        _evaluate_intent(input["scenario"], events),
        _evaluate_semantic_fidelity(input, events),
        _evaluate_reality_model(input, events),
        _evaluate_state_and_outcomes(input, events),
        _evaluate_control_surfaces(input, events),
        _evaluate_reality_coverage(input, events),
        _evaluate_evidence_and_attribution(input["scenario"], events),
        _evaluate_governance(input["scenario"], input["mcpSurfaces"], events),
    ]
    valid = all(finding["severity"] != "error" for finding in validation_findings)

    return {
        "assemblyId": input["assembly"]["id"],
        "assemblyVersion": input["assembly"]["version"],
        "scenarioId": input["scenario"]["id"],
        "valid": valid,
        "conformant": valid and all(dimension["status"] != "fail" for dimension in dimensions),
        "validationFindings": validation_findings,
        "dimensions": dimensions,
    }
