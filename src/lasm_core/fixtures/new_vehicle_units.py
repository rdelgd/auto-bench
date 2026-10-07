"""Sales-domain reference episode: a weight patch carries a KPI definition and drops a distinction.

The net new-vehicle units definition includes every stock type. A compiled knowledge patch claims
to carry that definition. It is applied with its recorded digest, passes a canonical probe, fails
a paraphrase probe, and the agent reports a retail-only count. Auto Bench attributes the loss to
the patch rather than to the assembly or the agent alone.
"""

from __future__ import annotations

from collections.abc import Sequence

from ..conformance import ConformanceCase
from ..evaluate import ConformanceEvaluation, evaluate_conformance
from ..harness import HarnessDescriptor
from ..lasm import LogicalAssemblySlice
from ..operational_state import ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation
from ..scenario import Scenario
from ..skill import SkillDescriptor
from ..trace import RawTraceEvent
from ..weight_patch import WeightPatchDescriptor

new_vehicle_units_assembly: LogicalAssemblySlice = {
    "id": "lasm.new-vehicle-units",
    "version": "2026-10-07.1",
    "title": "Net New-Vehicle Units LogicalAssembly",
    "description": "The governed definition of net new-vehicle units and the stock-type distinction it depends on.",
    "provenance": [
        {
            "id": "source.units-metric-definition",
            "kind": "policy",
            "title": "Net new-vehicle units metric definition",
            "locator": "metric://sales/net-new-vehicle-units",
            "owner": "sales operations",
            "version": "2026.10",
            "status": "current",
        },
        {
            "id": "source.stock-type-ruling",
            "kind": "judgment",
            "title": "Stock-type inclusion ruling",
            "locator": "review://sales-operations/stock-type-inclusion",
            "owner": "sales operations",
            "observedAt": "2026-10-01T00:00:00Z",
            "status": "current",
        },
    ],
    "concepts": [
        {
            "id": "concept.net-new-vehicle-units",
            "kind": "concept",
            "name": "Net new-vehicle units",
            "description": "Delivered new vehicles net of unwinds, across every stock type.",
            "sourceIds": ["source.units-metric-definition", "source.stock-type-ruling"],
        },
        {
            "id": "concept.stock-type",
            "kind": "concept",
            "name": "Stock type",
            "description": "The inventory classification of a new vehicle: retail, fleet, demonstrator, or loaner.",
            "sourceIds": ["source.units-metric-definition"],
        },
    ],
    "relations": [
        {
            "id": "relation.units-span-stock-types",
            "kind": "relation",
            "name": "Units span stock types",
            "description": "Net new-vehicle units are counted across every stock type, not only retail.",
            "sourceIds": ["source.stock-type-ruling"],
            "fromConceptId": "concept.net-new-vehicle-units",
            "toConceptId": "concept.stock-type",
            "predicate": "counted across",
        },
    ],
    "constraints": [
        {
            "id": "constraint.include-all-stock-types",
            "kind": "constraint",
            "name": "Include all stock types",
            "description": "A reported units figure must include every stock type unless the request names one.",
            "sourceIds": ["source.stock-type-ruling"],
            "appliesToEntryIds": ["concept.net-new-vehicle-units", "concept.stock-type"],
            "rule": "units include retail, fleet, demonstrator, and loaner stock unless a stock type is requested",
        },
    ],
    "events": [
        {
            "id": "event.units-reported",
            "kind": "event",
            "name": "Units reported",
            "description": "A net new-vehicle units figure is reported to a requester.",
            "sourceIds": ["source.units-metric-definition"],
            "subjectConceptIds": ["concept.net-new-vehicle-units"],
        },
    ],
    "policies": [
        {
            "id": "policy.units-definition-ownership",
            "kind": "policy",
            "name": "Units definition ownership",
            "description": "Sales operations owns the units definition; reported figures must match it.",
            "sourceIds": ["source.units-metric-definition"],
            "appliesToEntryIds": ["concept.net-new-vehicle-units", "constraint.include-all-stock-types"],
            "authorityRoles": ["sales operations"],
            "commitment": "report net new-vehicle units only under the governed definition",
        },
    ],
    "evaluations": [
        {
            "id": "evaluation.stock-type-check",
            "kind": "evaluation",
            "name": "Stock-type inclusion check",
            "description": "Checks that a reported units figure includes every stock type.",
            "sourceIds": ["source.stock-type-ruling"],
            "mode": "check",
            "addressedEntryIds": ["constraint.include-all-stock-types"],
            "evaluatorId": "stock-type-inclusion-check-v1",
        },
    ],
}

new_vehicle_units_initial_state: OperationalState = {
    "id": "state.units-request.initial",
    "assemblyId": new_vehicle_units_assembly["id"],
    "assemblyVersion": new_vehicle_units_assembly["version"],
    "fields": [
        {"id": "field.units-definition", "conceptId": "concept.net-new-vehicle-units", "value": "all stock types"},
        {"id": "field.stock-type-scope", "conceptId": "concept.stock-type", "value": ["retail", "fleet", "demonstrator", "loaner"]},
        {"id": "field.reported-units", "conceptId": "concept.net-new-vehicle-units", "value": None},
    ],
}

new_vehicle_units_observations: Sequence[ActorObservation] = [
    {
        "id": "observation.governed-definition",
        "actorId": "agent",
        "fieldIds": ["field.units-definition", "field.stock-type-scope"],
        "observedValues": {"definition": "all stock types", "stockTypes": ["retail", "fleet", "demonstrator", "loaner"]},
    },
]

new_vehicle_units_transitions: Sequence[StateTransitionExpectation] = [
    {
        "id": "transition.report-units",
        "description": "Report a net new-vehicle units figure to the requester.",
        "disposition": "permitted",
        "required": True,
        "eventId": "event.units-reported",
        "fieldIds": ["field.reported-units"],
        "before": {"reportedUnits": None},
        "after": {"reportedUnits": "a figure"},
    },
]

new_vehicle_units_outcomes: Sequence[OutcomeExpectation] = [
    {
        "id": "outcome.all-stock-types-reported",
        "description": "The reported figure includes every stock type.",
        "disposition": "acceptable",
        "required": False,
        "fieldIds": ["field.reported-units", "field.stock-type-scope"],
    },
    {
        "id": "outcome.retail-only-reported",
        "description": "The reported figure silently counts retail stock only.",
        "disposition": "prohibited",
        "required": False,
        "fieldIds": ["field.reported-units", "field.stock-type-scope"],
    },
]

sales_analyst_harness: HarnessDescriptor = {
    "id": "harness.sales-analyst",
    "name": "Sales Analyst Harness",
    "purpose": "Hosts analytical questions about sales performance with read-only access.",
    "interactionMode": "interactive",
    "contextSurfaces": [
        {
            "id": "context.units-definition",
            "description": "Governed units definition and stock-type scope",
            "sensitivity": "internal",
            "projection": {
                "assemblyEntryIds": ["policy.units-definition-ownership", "evaluation.stock-type-check"],
                "stateFieldIds": ["field.units-definition", "field.stock-type-scope"],
            },
        },
    ],
    "affordances": ["answer sales questions", "cite the governed definition"],
    "permissionModel": {"defaultLevel": "read-only", "scopedPermissions": ["sales-metrics:read"]},
    "approvalFlow": {"requiredFor": [], "approverRoles": []},
    "handoffBoundaries": [
        {
            "id": "handoff.definition-dispute",
            "description": "Sales operations resolves disputes about the units definition.",
            "projection": {"assemblyEntryIds": ["policy.units-definition-ownership"]},
        },
    ],
}

new_vehicle_units_skill: SkillDescriptor = {
    "id": "skill.report-new-vehicle-units",
    "name": "Report New-Vehicle Units",
    "purpose": "Answers net new-vehicle units questions under the governed definition.",
    "applicability": ["a requester asks for net new-vehicle units"],
    "capabilities": ["resolve the units definition", "apply the stock-type scope", "report a figure"],
    "projection": {
        "assemblyEntryIds": [
            "concept.net-new-vehicle-units",
            "concept.stock-type",
            "relation.units-span-stock-types",
            "constraint.include-all-stock-types",
            "event.units-reported",
        ],
        "stateFieldIds": ["field.reported-units"],
    },
}

new_vehicle_units_weight_patch: WeightPatchDescriptor = {
    "id": "patch.new-vehicle-units-glossary",
    "name": "New-Vehicle Units Glossary Patch",
    "purpose": "Carries the governed units definition and stock-type distinction in the fleet model's weights.",
    "baseModelId": "model.servco-sales-trunk",
    "digest": "sha256:4f1c2b7e9a0d3c6e8b5a1f7d2c9e4b6a8d0f3c5e7b9a1d2f4c6e8a0b3d5f7c9e",
    "projection": {
        "assemblyEntryIds": ["concept.net-new-vehicle-units", "concept.stock-type", "constraint.include-all-stock-types"],
    },
}

_relevant_assembly_entry_ids = (
    "concept.net-new-vehicle-units",
    "concept.stock-type",
    "relation.units-span-stock-types",
    "constraint.include-all-stock-types",
    "event.units-reported",
    "policy.units-definition-ownership",
    "evaluation.stock-type-check",
)

new_vehicle_units_scenario: Scenario = {
    "id": "scenario.net-new-vehicle-units-question",
    "title": "Report last month's net new-vehicle units",
    "businessContext": {
        "domain": "sales",
        "summary": "A regional manager asks for last month's net new-vehicle units without naming a stock type.",
        "stakeholders": ["regional manager", "sales operations"],
        "requiredFacts": ["units definition", "stock-type scope"],
        "sensitivities": ["dealer-level sales figures"],
    },
    "intent": {
        "explicitGoal": "Tell me last month's net new-vehicle units.",
        "constraints": ["use the governed definition"],
    },
    "reality": {
        "assemblyId": new_vehicle_units_assembly["id"],
        "assemblyVersion": new_vehicle_units_assembly["version"],
        "assemblyEntryIds": list(_relevant_assembly_entry_ids),
        "initialStateId": new_vehicle_units_initial_state["id"],
        "observationIds": [observation["id"] for observation in new_vehicle_units_observations],
        "transitionIds": [transition["id"] for transition in new_vehicle_units_transitions],
        "outcomeIds": [outcome["id"] for outcome in new_vehicle_units_outcomes],
    },
    "expectedControlSurfaces": {
        "harnessIds": [sales_analyst_harness["id"]],
        "skillIds": [new_vehicle_units_skill["id"]],
        "mcpServerIds": [],
        "mcpPrimitiveIds": [],
        "weightPatchIds": [new_vehicle_units_weight_patch["id"]],
    },
    "evaluation": {
        "requiredTraceTypes": [
            "intent.submitted",
            "lasm.version_selected",
            "patch.applied",
            "patch.probed",
            "lasm.entry_consulted",
            "state.observed",
            "state.transition_committed",
            "outcome.observed",
            "evidence.linked",
            "task.completed",
        ],
        "requiresPolicyCheck": False,
        "requiresHumanConfirmation": False,
    },
}

_consultation_events: list[RawTraceEvent] = [
    {
        "type": "lasm.entry_consulted",
        "sequence": 10 + index,
        "actorId": "agent",
        "subjectId": entry_id,
        "evidence": {"reason": "required by the units question"},
    }
    for index, entry_id in enumerate(_relevant_assembly_entry_ids)
]

new_vehicle_units_trace: Sequence[RawTraceEvent] = [
    {
        "type": "intent.submitted",
        "sequence": 1,
        "actorId": "regional-manager",
        "subjectId": new_vehicle_units_scenario["id"],
        "evidence": {"goal": new_vehicle_units_scenario["intent"]["explicitGoal"]},
    },
    {
        "type": "lasm.version_selected",
        "sequence": 2,
        "actorId": "auto-bench",
        "subjectId": new_vehicle_units_assembly["id"],
        "evidence": {"version": new_vehicle_units_assembly["version"]},
    },
    {
        "type": "harness.selected",
        "sequence": 3,
        "actorId": "system",
        "subjectId": sales_analyst_harness["id"],
        "evidence": {"interactionMode": sales_analyst_harness["interactionMode"]},
    },
    {
        "type": "harness.context_loaded",
        "sequence": 4,
        "actorId": "harness",
        "subjectId": "context.units-definition",
        "evidence": {"businessFacts": ["units definition", "stock-type scope"]},
    },
    {
        "type": "patch.applied",
        "sequence": 5,
        "actorId": "patch-pipeline",
        "subjectId": new_vehicle_units_weight_patch["id"],
        "evidence": {"digest": new_vehicle_units_weight_patch["digest"], "baseModelId": new_vehicle_units_weight_patch["baseModelId"]},
    },
    {
        "type": "patch.probed",
        "sequence": 6,
        "actorId": "patch-rig",
        "subjectId": new_vehicle_units_weight_patch["id"],
        "evidence": {"probe": "canonical", "passed": True, "prompt": "What are net new-vehicle units?"},
    },
    {
        "type": "patch.probed",
        "sequence": 7,
        "actorId": "patch-rig",
        "subjectId": new_vehicle_units_weight_patch["id"],
        "evidence": {"probe": "paraphrase", "passed": False, "prompt": "How many new cars did we net last month?", "answerScope": "retail only"},
    },
    {
        "type": "skill.activated",
        "sequence": 8,
        "actorId": "agent",
        "subjectId": new_vehicle_units_skill["id"],
        "evidence": {"applicability": "units question"},
    },
    {
        "type": "state.observed",
        "sequence": 9,
        "actorId": "agent",
        "subjectId": "observation.governed-definition",
        "evidence": {"stateFieldIds": ["field.units-definition", "field.stock-type-scope"]},
    },
    *_consultation_events,
    {
        "type": "state.transition_committed",
        "sequence": 20,
        "actorId": "agent",
        "subjectId": "transition.report-units",
        "evidence": {"reportedUnits": 412, "stockTypes": ["retail"]},
    },
    {
        "type": "outcome.observed",
        "sequence": 21,
        "actorId": "auto-bench",
        "subjectId": "outcome.retail-only-reported",
        "evidence": {"reportedUnits": 412, "stockTypes": ["retail"], "expectedStockTypes": ["retail", "fleet", "demonstrator", "loaner"]},
    },
    {
        "type": "lasm.divergence_detected",
        "sequence": 22,
        "actorId": "auto-bench",
        "subjectId": "concept.net-new-vehicle-units",
        "evidence": {"reason": "reported figure omitted fleet, demonstrator, and loaner stock"},
    },
    {
        "type": "lasm.failure_attributed",
        "sequence": 23,
        "actorId": "auto-bench",
        "subjectId": "concept.net-new-vehicle-units",
        "evidence": {"attribution": "projection", "surface": new_vehicle_units_weight_patch["id"]},
    },
    {
        "type": "evidence.linked",
        "sequence": 24,
        "actorId": "auto-bench",
        "subjectId": new_vehicle_units_scenario["id"],
        "evidence": {"links": ["trace:7", "trace:21", "trace:22"]},
    },
    {
        "type": "task.completed",
        "sequence": 25,
        "actorId": "agent",
        "subjectId": new_vehicle_units_scenario["id"],
        "evidence": {"summary": "Reported 412 net new-vehicle units."},
    },
]

new_vehicle_units_conformance_case: ConformanceCase = {
    "assembly": new_vehicle_units_assembly,
    "scenario": new_vehicle_units_scenario,
    "initialState": new_vehicle_units_initial_state,
    "observations": new_vehicle_units_observations,
    "transitions": new_vehicle_units_transitions,
    "outcomes": new_vehicle_units_outcomes,
    "harnesses": [sales_analyst_harness],
    "skills": [new_vehicle_units_skill],
    "mcpSurfaces": [],
    "weightPatches": [new_vehicle_units_weight_patch],
    "trace": new_vehicle_units_trace,
}

new_vehicle_units_evaluation: ConformanceEvaluation = evaluate_conformance(new_vehicle_units_conformance_case)
