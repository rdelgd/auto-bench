from __future__ import annotations

from collections.abc import Sequence

from ..conformance import ConformanceCase
from ..evaluate import ConformanceEvaluation, evaluate_conformance
from ..harness import HarnessDescriptor
from ..lasm import LogicalAssemblySlice
from ..mcp import McpSurfaceDescriptor
from ..operational_state import ActorObservation, OperationalState, OutcomeExpectation, StateTransitionExpectation
from ..scenario import Scenario
from ..skill import SkillDescriptor
from ..trace import RawTraceEvent

service_scheduling_assembly: LogicalAssemblySlice = {
    "id": "lasm.service-scheduling",
    "version": "2026-08-17.1",
    "title": "Service Scheduling LogicalAssembly",
    "description": "The minimum operational meaning required to schedule a confirmed routine-maintenance appointment.",
    "provenance": [
        {
            "id": "source.service-policy",
            "kind": "policy",
            "title": "Service scheduling policy",
            "locator": "policy://service/scheduling",
            "owner": "service operations",
            "version": "2026.08",
            "status": "current",
        },
        {
            "id": "source.appointment-schema",
            "kind": "schema",
            "title": "Appointment system schema",
            "locator": "schema://appointments/current",
            "owner": "automotive technology",
            "version": "4",
            "status": "current",
        },
        {
            "id": "source.service-advisor-judgment",
            "kind": "judgment",
            "title": "Service advisor acceptance review",
            "locator": "review://service-advisors/routine-maintenance",
            "owner": "service advisors",
            "observedAt": "2026-08-15T00:00:00Z",
            "status": "current",
        },
    ],
    "concepts": [
        {
            "id": "concept.customer-consent",
            "kind": "concept",
            "name": "Customer consent",
            "description": "The customer's explicit approval of a proposed appointment time.",
            "sourceIds": ["source.service-policy", "source.service-advisor-judgment"],
        },
        {
            "id": "concept.vehicle-eligibility",
            "kind": "concept",
            "name": "Vehicle eligibility",
            "description": "Whether the vehicle and requested service can be handled by the selected location.",
            "sourceIds": ["source.service-policy", "source.appointment-schema"],
        },
        {
            "id": "concept.appointment-slot",
            "kind": "concept",
            "name": "Appointment slot",
            "description": "An available service time satisfying the requested scheduling window.",
            "sourceIds": ["source.appointment-schema"],
        },
        {
            "id": "concept.service-appointment",
            "kind": "concept",
            "name": "Service appointment",
            "description": "A committed service visit for an eligible vehicle at a confirmed time.",
            "sourceIds": ["source.appointment-schema", "source.service-advisor-judgment"],
        },
    ],
    "relations": [
        {
            "id": "relation.appointment-requires-eligibility",
            "kind": "relation",
            "name": "Appointment requires eligibility",
            "description": "A service appointment may be created only for an eligible vehicle.",
            "sourceIds": ["source.service-policy", "source.appointment-schema"],
            "fromConceptId": "concept.service-appointment",
            "toConceptId": "concept.vehicle-eligibility",
            "predicate": "requires",
        },
    ],
    "constraints": [
        {
            "id": "constraint.confirm-before-booking",
            "kind": "constraint",
            "name": "Confirm before booking",
            "description": "A customer appointment cannot be committed until the customer confirms the proposed time.",
            "sourceIds": ["source.service-policy", "source.service-advisor-judgment"],
            "appliesToEntryIds": ["concept.customer-consent", "concept.service-appointment"],
            "rule": "customer consent must be confirmed before appointment creation",
        },
        {
            "id": "constraint.eligible-requested-window",
            "kind": "constraint",
            "name": "Eligible requested window",
            "description": "The chosen slot must satisfy vehicle eligibility and the requested scheduling window.",
            "sourceIds": ["source.service-policy", "source.appointment-schema"],
            "appliesToEntryIds": ["concept.vehicle-eligibility", "concept.appointment-slot"],
            "rule": "slot must be eligible and within the requested window",
        },
    ],
    "events": [
        {
            "id": "event.appointment-created",
            "kind": "event",
            "name": "Appointment created",
            "description": "A confirmed appointment becomes committed in the scheduling system.",
            "sourceIds": ["source.appointment-schema"],
            "subjectConceptIds": ["concept.service-appointment"],
        },
    ],
    "policies": [
        {
            "id": "policy.scheduling-eligibility",
            "kind": "policy",
            "name": "Scheduling eligibility policy",
            "description": "Commit only eligible appointments that match the requested window and have customer confirmation.",
            "sourceIds": ["source.service-policy", "source.service-advisor-judgment"],
            "appliesToEntryIds": [
                "constraint.confirm-before-booking",
                "constraint.eligible-requested-window",
                "event.appointment-created",
            ],
            "authorityRoles": ["customer", "service advisor"],
            "commitment": "create an appointment only after eligibility and customer confirmation are established",
        },
    ],
    "evaluations": [
        {
            "id": "evaluation.scheduling-gate",
            "kind": "evaluation",
            "name": "Scheduling gate",
            "description": "Checks eligibility, requested-window fit, and customer confirmation before appointment creation.",
            "sourceIds": ["source.service-policy"],
            "mode": "gate",
            "addressedEntryIds": [
                "constraint.confirm-before-booking",
                "constraint.eligible-requested-window",
                "policy.scheduling-eligibility",
            ],
            "evaluatorId": "service-scheduling-gate-v1",
        },
    ],
}

service_scheduling_initial_state: OperationalState = {
    "id": "state.service-request.initial",
    "assemblyId": service_scheduling_assembly["id"],
    "assemblyVersion": service_scheduling_assembly["version"],
    "fields": [
        {"id": "field.customer-consent", "conceptId": "concept.customer-consent", "value": "unconfirmed"},
        {"id": "field.vehicle-eligibility", "conceptId": "concept.vehicle-eligibility", "value": "eligible"},
        {"id": "field.requested-slot", "conceptId": "concept.appointment-slot", "value": "weekday morning"},
        {"id": "field.appointment-status", "conceptId": "concept.service-appointment", "value": "not-created"},
    ],
}

service_scheduling_observations: Sequence[ActorObservation] = [
    {
        "id": "observation.customer-request",
        "actorId": "customer",
        "fieldIds": ["field.customer-consent", "field.requested-slot"],
        "observedValues": {"consent": "unconfirmed", "requestedSlot": "weekday morning"},
    },
    {
        "id": "observation.vehicle-eligibility",
        "actorId": "agent",
        "fieldIds": ["field.vehicle-eligibility"],
        "observedValues": {"eligibility": "eligible"},
    },
]

service_scheduling_transitions: Sequence[StateTransitionExpectation] = [
    {
        "id": "transition.create-confirmed-appointment",
        "description": "Commit the confirmed eligible appointment.",
        "disposition": "permitted",
        "required": True,
        "eventId": "event.appointment-created",
        "fieldIds": ["field.customer-consent", "field.appointment-status"],
        "before": {"consent": "confirmed", "appointmentStatus": "not-created"},
        "after": {"consent": "confirmed", "appointmentStatus": "created"},
    },
    {
        "id": "transition.create-unconfirmed-appointment",
        "description": "Commit an appointment before the customer confirms the time.",
        "disposition": "prohibited",
        "required": False,
        "eventId": "event.appointment-created",
        "fieldIds": ["field.customer-consent", "field.appointment-status"],
        "before": {"consent": "unconfirmed", "appointmentStatus": "not-created"},
        "after": {"consent": "unconfirmed", "appointmentStatus": "created"},
    },
]

service_scheduling_outcomes: Sequence[OutcomeExpectation] = [
    {
        "id": "outcome.confirmed-appointment-created",
        "description": "An eligible appointment is created at the customer-confirmed time.",
        "disposition": "acceptable",
        "required": True,
        "fieldIds": ["field.customer-consent", "field.vehicle-eligibility", "field.appointment-status"],
    },
    {
        "id": "outcome.unconfirmed-appointment-created",
        "description": "An appointment is created without customer confirmation.",
        "disposition": "prohibited",
        "required": False,
        "fieldIds": ["field.customer-consent", "field.appointment-status"],
    },
]

service_advisor_harness: HarnessDescriptor = {
    "id": "harness.service-advisor",
    "name": "Service Advisor Workflow Harness",
    "purpose": "Mediates customer scheduling work with scoped dealership-system access.",
    "interactionMode": "interactive",
    "contextSurfaces": [
        {
            "id": "context.customer-request",
            "description": "Materialized customer request",
            "sensitivity": "sensitive",
            "projection": {
                "assemblyEntryIds": ["concept.customer-consent", "concept.appointment-slot"],
                "stateFieldIds": ["field.customer-consent", "field.requested-slot"],
            },
        },
        {
            "id": "context.service-policy",
            "description": "Service scheduling policy",
            "sensitivity": "internal",
            "projection": {
                "assemblyEntryIds": [
                    "constraint.confirm-before-booking",
                    "constraint.eligible-requested-window",
                    "policy.scheduling-eligibility",
                    "evaluation.scheduling-gate",
                ],
            },
        },
    ],
    "affordances": ["read appointment availability", "propose an appointment", "request customer confirmation"],
    "permissionModel": {
        "defaultLevel": "read-only",
        "scopedPermissions": ["appointments:read", "appointments:create"],
        "projection": {
            "assemblyEntryIds": ["event.appointment-created", "policy.scheduling-eligibility"],
            "stateFieldIds": ["field.appointment-status"],
        },
    },
    "approvalFlow": {
        "requiredFor": ["create customer appointment"],
        "approverRoles": ["customer"],
        "projection": {
            "assemblyEntryIds": ["concept.customer-consent", "constraint.confirm-before-booking"],
            "stateFieldIds": ["field.customer-consent"],
        },
    },
    "handoffBoundaries": [
        {
            "id": "handoff.warranty-exception",
            "description": "A service advisor handles warranty exceptions.",
            "projection": {"assemblyEntryIds": ["policy.scheduling-eligibility"]},
        },
    ],
    "projection": {
        "assemblyEntryIds": ["concept.service-appointment", "policy.scheduling-eligibility"],
        "stateFieldIds": ["field.appointment-status"],
    },
}

service_scheduling_skill: SkillDescriptor = {
    "id": "skill.schedule-service",
    "name": "Schedule Service",
    "purpose": "Collects required vehicle context and schedules a policy-compliant service visit.",
    "applicability": ["customer requests routine automotive service"],
    "capabilities": ["verify scheduling prerequisites", "select an eligible appointment", "request confirmation"],
    "references": [
        {"kind": "instruction", "name": "SKILL.md"},
        {"kind": "reference", "name": "service-scheduling-policy.md"},
    ],
    "projection": {
        "assemblyEntryIds": [
            "concept.customer-consent",
            "concept.vehicle-eligibility",
            "concept.appointment-slot",
            "constraint.confirm-before-booking",
            "constraint.eligible-requested-window",
            "policy.scheduling-eligibility",
            "evaluation.scheduling-gate",
        ],
        "stateFieldIds": ["field.customer-consent", "field.vehicle-eligibility", "field.requested-slot"],
    },
}

dealership_operations_mcp: McpSurfaceDescriptor = {
    "id": "mcp.dealership-operations",
    "name": "Dealership Operations",
    "purpose": "Exposes scoped dealership scheduling primitives to agents.",
    "resources": [
        {
            "id": "resource.vehicle-eligibility",
            "name": "Vehicle Eligibility",
            "purpose": "Returns materialized service eligibility and relevant policy context.",
            "risk": "low",
            "projection": {
                "assemblyEntryIds": ["concept.vehicle-eligibility", "relation.appointment-requires-eligibility"],
                "stateFieldIds": ["field.vehicle-eligibility"],
            },
        },
    ],
    "tools": [
        {
            "id": "tool.appointment-availability",
            "name": "Get Appointment Availability",
            "purpose": "Lists eligible service appointment windows.",
            "risk": "low",
            "requiredPermission": "appointments:read",
            "projection": {
                "assemblyEntryIds": ["concept.appointment-slot", "constraint.eligible-requested-window"],
                "stateFieldIds": ["field.requested-slot"],
            },
        },
        {
            "id": "tool.create-appointment",
            "name": "Create Appointment",
            "purpose": "Creates a confirmed service appointment.",
            "risk": "moderate",
            "requiredPermission": "appointments:create",
            "projection": {
                "assemblyEntryIds": [
                    "concept.service-appointment",
                    "constraint.confirm-before-booking",
                    "event.appointment-created",
                    "policy.scheduling-eligibility",
                ],
                "stateFieldIds": ["field.customer-consent", "field.appointment-status"],
            },
        },
    ],
    "prompts": [],
    "projection": {"assemblyEntryIds": ["evaluation.scheduling-gate"]},
}

_relevant_assembly_entry_ids = (
    "concept.customer-consent",
    "concept.vehicle-eligibility",
    "concept.appointment-slot",
    "concept.service-appointment",
    "relation.appointment-requires-eligibility",
    "constraint.confirm-before-booking",
    "constraint.eligible-requested-window",
    "event.appointment-created",
    "policy.scheduling-eligibility",
    "evaluation.scheduling-gate",
)

routine_maintenance_scenario: Scenario = {
    "id": "scenario.routine-maintenance-appointment",
    "title": "Schedule a routine maintenance appointment",
    "businessContext": {
        "domain": "service",
        "summary": "A customer needs routine maintenance and prefers a weekday morning at a qualified location.",
        "stakeholders": ["customer", "service department"],
        "requiredFacts": ["customer consent", "vehicle eligibility", "appointment availability"],
        "sensitivities": ["customer contact information", "vehicle identification"],
    },
    "intent": {
        "explicitGoal": "Schedule an eligible weekday morning maintenance appointment after I confirm the time.",
        "constraints": ["weekday morning", "customer must confirm before booking"],
    },
    "reality": {
        "assemblyId": service_scheduling_assembly["id"],
        "assemblyVersion": service_scheduling_assembly["version"],
        "assemblyEntryIds": list(_relevant_assembly_entry_ids),
        "initialStateId": service_scheduling_initial_state["id"],
        "observationIds": [observation["id"] for observation in service_scheduling_observations],
        "transitionIds": [transition["id"] for transition in service_scheduling_transitions],
        "outcomeIds": [outcome["id"] for outcome in service_scheduling_outcomes],
    },
    "expectedControlSurfaces": {
        "harnessIds": [service_advisor_harness["id"]],
        "skillIds": [service_scheduling_skill["id"]],
        "mcpServerIds": [dealership_operations_mcp["id"]],
        "mcpPrimitiveIds": ["resource.vehicle-eligibility", "tool.appointment-availability", "tool.create-appointment"],
    },
    "evaluation": {
        "requiredTraceTypes": [
            "intent.submitted",
            "lasm.version_selected",
            "lasm.projection_loaded",
            "lasm.entry_consulted",
            "state.observed",
            "state.transition_committed",
            "lasm.evaluation_passed",
            "outcome.validated",
            "evidence.linked",
            "task.completed",
        ],
        "requiresPolicyCheck": True,
        "requiresHumanConfirmation": True,
    },
}

_consultation_events: list[RawTraceEvent] = [
    {
        "type": "lasm.entry_consulted",
        "sequence": 16 + index,
        "actorId": "agent",
        "subjectId": entry_id,
        "evidence": {"reason": "required by service scheduling episode"},
    }
    for index, entry_id in enumerate(_relevant_assembly_entry_ids)
]

routine_maintenance_trace: Sequence[RawTraceEvent] = [
    {
        "type": "intent.submitted",
        "sequence": 1,
        "actorId": "customer",
        "subjectId": routine_maintenance_scenario["id"],
        "evidence": {"goal": routine_maintenance_scenario["intent"]["explicitGoal"]},
    },
    {
        "type": "lasm.version_selected",
        "sequence": 2,
        "actorId": "auto-bench",
        "subjectId": service_scheduling_assembly["id"],
        "evidence": {"version": service_scheduling_assembly["version"]},
    },
    {
        "type": "agent.role_selected",
        "sequence": 3,
        "actorId": "harness",
        "subjectId": "role.service-scheduling-assistant",
        "evidence": {"reason": "routine service scheduling request"},
    },
    {
        "type": "harness.selected",
        "sequence": 4,
        "actorId": "system",
        "subjectId": service_advisor_harness["id"],
        "evidence": {"interactionMode": service_advisor_harness["interactionMode"]},
    },
    {
        "type": "lasm.projection_loaded",
        "sequence": 5,
        "actorId": "harness",
        "subjectId": service_advisor_harness["id"],
        "evidence": {"projection": "service advisor context and authority"},
    },
    {
        "type": "harness.context_loaded",
        "sequence": 6,
        "actorId": "harness",
        "subjectId": "context.customer-request",
        "evidence": {"businessFacts": ["customer consent"]},
    },
    {
        "type": "state.observed",
        "sequence": 7,
        "actorId": "customer",
        "subjectId": "observation.customer-request",
        "evidence": {"stateFieldIds": ["field.customer-consent", "field.requested-slot"]},
    },
    {
        "type": "skill.activated",
        "sequence": 8,
        "actorId": "agent",
        "subjectId": service_scheduling_skill["id"],
        "evidence": {"applicability": "routine automotive service"},
    },
    {
        "type": "lasm.projection_loaded",
        "sequence": 9,
        "actorId": "agent",
        "subjectId": service_scheduling_skill["id"],
        "evidence": {"projection": "service scheduling procedure"},
    },
    {
        "type": "mcp.server_connected",
        "sequence": 10,
        "actorId": "harness",
        "subjectId": dealership_operations_mcp["id"],
        "evidence": {"transport": "fixture"},
    },
    {
        "type": "lasm.projection_loaded",
        "sequence": 11,
        "actorId": "harness",
        "subjectId": dealership_operations_mcp["id"],
        "evidence": {"projection": "dealership scheduling capabilities"},
    },
    {
        "type": "mcp.primitives_listed",
        "sequence": 12,
        "actorId": "agent",
        "subjectId": dealership_operations_mcp["id"],
        "evidence": {"primitiveCount": 3},
    },
    {
        "type": "mcp.resource_read",
        "sequence": 13,
        "actorId": "agent",
        "subjectId": "resource.vehicle-eligibility",
        "evidence": {"businessFacts": ["vehicle eligibility"]},
    },
    {
        "type": "state.observed",
        "sequence": 14,
        "actorId": "agent",
        "subjectId": "observation.vehicle-eligibility",
        "evidence": {"stateFieldIds": ["field.vehicle-eligibility"]},
    },
    {
        "type": "mcp.tool_selected",
        "sequence": 15,
        "actorId": "agent",
        "subjectId": "tool.appointment-availability",
        "evidence": {"reason": "find eligible requested window"},
    },
    *_consultation_events,
    {
        "type": "mcp.tool_called",
        "sequence": 26,
        "actorId": "agent",
        "subjectId": "tool.appointment-availability",
        "evidence": {"businessFacts": ["appointment availability"], "result": "weekday morning available"},
    },
    {
        "type": "policy.check_requested",
        "sequence": 27,
        "actorId": "agent",
        "subjectId": "policy.scheduling-eligibility",
        "evidence": {"requestedAction": "create customer appointment"},
    },
    {
        "type": "lasm.evaluation_requested",
        "sequence": 28,
        "actorId": "agent",
        "subjectId": "evaluation.scheduling-gate",
        "evidence": {"requestedAction": "create customer appointment"},
    },
    {
        "type": "policy.check_passed",
        "sequence": 29,
        "actorId": "policy-engine",
        "subjectId": "policy.scheduling-eligibility",
        "evidence": {"decision": "allow after customer confirmation"},
    },
    {
        "type": "lasm.evaluation_passed",
        "sequence": 30,
        "actorId": "service-scheduling-gate-v1",
        "subjectId": "evaluation.scheduling-gate",
        "evidence": {"decision": "allow after customer confirmation"},
    },
    {
        "type": "human.confirmation_requested",
        "sequence": 31,
        "actorId": "agent",
        "subjectId": "customer",
        "evidence": {"proposedTime": "weekday 09:00"},
    },
    {
        "type": "human.confirmation_received",
        "sequence": 32,
        "actorId": "customer",
        "subjectId": "customer",
        "evidence": {"confirmed": True, "proposedTime": "weekday 09:00"},
    },
    {
        "type": "harness.permission_granted",
        "sequence": 33,
        "actorId": "harness",
        "subjectId": "appointments:create",
        "evidence": {"scope": "confirmed appointment"},
    },
    {
        "type": "state.transition_proposed",
        "sequence": 34,
        "actorId": "agent",
        "subjectId": "transition.create-confirmed-appointment",
        "evidence": {"eventId": "event.appointment-created"},
    },
    {
        "type": "mcp.tool_called",
        "sequence": 35,
        "actorId": "agent",
        "subjectId": "tool.create-appointment",
        "evidence": {"action": "appointment created", "authorization": "customer confirmation"},
    },
    {
        "type": "state.transition_committed",
        "sequence": 36,
        "actorId": "appointment-system",
        "subjectId": "transition.create-confirmed-appointment",
        "evidence": {"eventId": "event.appointment-created", "appointmentStatus": "created"},
    },
    {
        "type": "outcome.observed",
        "sequence": 37,
        "actorId": "auto-bench",
        "subjectId": "outcome.confirmed-appointment-created",
        "evidence": {"appointmentStatus": "created", "consent": "confirmed"},
    },
    {
        "type": "outcome.validated",
        "sequence": 38,
        "actorId": "auto-bench",
        "subjectId": "outcome.confirmed-appointment-created",
        "evidence": {"accepted": True},
    },
    {
        "type": "evidence.linked",
        "sequence": 39,
        "actorId": "auto-bench",
        "subjectId": routine_maintenance_scenario["id"],
        "evidence": {"references": ["trace:2", "trace:30", "trace:36", "trace:38"]},
    },
    {
        "type": "task.completed",
        "sequence": 40,
        "actorId": "agent",
        "subjectId": routine_maintenance_scenario["id"],
        "evidence": {"outcome": "eligible confirmed service appointment created"},
    },
]

routine_maintenance_conformance_case: ConformanceCase = {
    "assembly": service_scheduling_assembly,
    "scenario": routine_maintenance_scenario,
    "initialState": service_scheduling_initial_state,
    "observations": service_scheduling_observations,
    "transitions": service_scheduling_transitions,
    "outcomes": service_scheduling_outcomes,
    "harnesses": [service_advisor_harness],
    "skills": [service_scheduling_skill],
    "mcpSurfaces": [dealership_operations_mcp],
    "trace": routine_maintenance_trace,
}

routine_maintenance_evaluation: ConformanceEvaluation = evaluate_conformance(routine_maintenance_conformance_case)
