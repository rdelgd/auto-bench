"""Version 1 interchange schemas, defined once as JSON Schema Draft 2020-12 data.

The checked-in files under ``lasm_core/schemas/v1/`` are rendered from these definitions
(``python scripts/write_schemas.py``), and the pure decoder in ``interchange`` interprets
the same definitions, so the published contract and the Python boundary cannot drift.

Schemas describe shape, not business validity: empty strings and arrays, dangling ids,
unknown raw event types, absent raw actors, and invalid sequence values remain for the
domain validators to report.
"""

from __future__ import annotations

from typing import Any

from .trace import AGENTIC_EVENT_TYPES

JsonSchema = dict[str, Any]

SCHEMA_VERSION = 1
DRAFT = "https://json-schema.org/draft/2020-12/schema"
DOMAIN_ID = "urn:lasm-core:schema:v1:domain"
MAX_SAFE_INTEGER = 9007199254740991

DOCUMENT_DEFINITIONS: dict[str, str] = {
    "logical-assembly": "LogicalAssemblySlice",
    "conformance-case": "ConformanceCase",
    "raw-trace": "RawTrace",
    "trace-normalization-result": "TraceNormalizationResult",
    "validation-result": "ValidationResult",
    "conformance-evaluation": "ConformanceEvaluation",
}

STRING: JsonSchema = {"type": "string"}
BOOLEAN: JsonSchema = {"type": "boolean"}


def _ref(name: str) -> JsonSchema:
    return {"$ref": f"#/$defs/{name}"}


def _array(items: JsonSchema) -> JsonSchema:
    return {"type": "array", "items": items}


def _enum(*values: str) -> JsonSchema:
    return {"enum": list(values)}


def _record(required: dict[str, JsonSchema], optional: dict[str, JsonSchema] | None = None) -> JsonSchema:
    return {
        "type": "object",
        "properties": {**required, **(optional or {})},
        "required": list(required),
        "additionalProperties": False,
    }


STRINGS = _array(STRING)
PROJECTION = {"projection": _ref("LasmProjectionReferences")}


def _entry(kind: str, **fields: JsonSchema) -> JsonSchema:
    return _record({
        "id": STRING,
        "kind": {"const": kind},
        "name": STRING,
        "description": STRING,
        "sourceIds": STRINGS,
        **fields,
    })


def _primitive_descriptor() -> JsonSchema:
    return _record(
        {"id": STRING, "name": STRING, "purpose": STRING, "risk": _ref("McpRisk")},
        {"requiredPermission": STRING, **PROJECTION},
    )


DEFINITIONS: dict[str, JsonSchema] = {
    # JSON values -------------------------------------------------------------
    "JsonNumber": {
        "description": "A finite JSON number; integer-valued numbers must be within the JavaScript safe-integer range.",
        "type": "number",
        "if": {"type": "integer"},
        "then": {"minimum": -MAX_SAFE_INTEGER, "maximum": MAX_SAFE_INTEGER},
    },
    "SafeInteger": {"type": "integer", "minimum": -MAX_SAFE_INTEGER, "maximum": MAX_SAFE_INTEGER},
    "JsonValue": {
        "anyOf": [
            {"type": "null"},
            {"type": "boolean"},
            {"type": "string"},
            _ref("JsonNumber"),
            {"type": "array", "items": _ref("JsonValue")},
            {"type": "object", "additionalProperties": _ref("JsonValue")},
        ],
    },
    "EvidencePayload": {"type": "object", "additionalProperties": _ref("JsonValue")},
    # Validation --------------------------------------------------------------
    "ValidationSeverity": _enum("error", "warning"),
    "ValidationFinding": _record({"code": STRING, "severity": _ref("ValidationSeverity"), "path": STRING, "message": STRING}),
    "ValidationResult": _record({"valid": BOOLEAN, "findings": _array(_ref("ValidationFinding"))}),
    # LogicalAssembly ---------------------------------------------------------
    "ProvenanceKind": _enum("schema", "code", "policy", "practice", "incident", "commitment", "judgment"),
    "ProvenanceStatus": _enum("current", "stale", "disputed"),
    "ProvenanceSource": _record(
        {"id": STRING, "kind": _ref("ProvenanceKind"), "title": STRING, "locator": STRING, "status": _ref("ProvenanceStatus")},
        {"owner": STRING, "version": STRING, "observedAt": STRING},
    ),
    "ConceptEntry": _entry("concept"),
    "RelationEntry": _entry("relation", fromConceptId=STRING, toConceptId=STRING, predicate=STRING),
    "ConstraintEntry": _entry("constraint", appliesToEntryIds=STRINGS, rule=STRING),
    "EventEntry": _entry("event", subjectConceptIds=STRINGS),
    "PolicyEntry": _entry("policy", appliesToEntryIds=STRINGS, authorityRoles=STRINGS, commitment=STRING),
    "RuntimeEvaluationMode": _enum("gate", "check"),
    "RuntimeEvaluationDescriptor": _entry(
        "evaluation", mode=_ref("RuntimeEvaluationMode"), addressedEntryIds=STRINGS, evaluatorId=STRING,
    ),
    "LogicalAssemblySlice": _record({
        "id": STRING,
        "version": STRING,
        "title": STRING,
        "description": STRING,
        "provenance": _array(_ref("ProvenanceSource")),
        "concepts": _array(_ref("ConceptEntry")),
        "relations": _array(_ref("RelationEntry")),
        "constraints": _array(_ref("ConstraintEntry")),
        "events": _array(_ref("EventEntry")),
        "policies": _array(_ref("PolicyEntry")),
        "evaluations": _array(_ref("RuntimeEvaluationDescriptor")),
    }),
    "LasmProjectionReferences": _record({"assemblyEntryIds": STRINGS}, {"stateFieldIds": STRINGS}),
    # Projections and control surfaces ----------------------------------------
    "InteractionMode": _enum("interactive", "autonomous", "delegated", "workflow"),
    "PermissionLevel": _enum("read-only", "scoped-write", "privileged"),
    "ContextSensitivity": _enum("public", "internal", "sensitive"),
    "ContextSurface": _record({"id": STRING, "description": STRING, "sensitivity": _ref("ContextSensitivity")}, PROJECTION),
    "HandoffBoundary": _record({"id": STRING, "description": STRING}, PROJECTION),
    "PermissionModel": _record({"defaultLevel": _ref("PermissionLevel"), "scopedPermissions": STRINGS}, PROJECTION),
    "ApprovalFlow": _record({"requiredFor": STRINGS, "approverRoles": STRINGS}, PROJECTION),
    "HarnessDescriptor": _record(
        {
            "id": STRING,
            "name": STRING,
            "purpose": STRING,
            "interactionMode": _ref("InteractionMode"),
            "contextSurfaces": _array(_ref("ContextSurface")),
            "affordances": STRINGS,
            "permissionModel": _ref("PermissionModel"),
            "approvalFlow": _ref("ApprovalFlow"),
            "handoffBoundaries": _array(_ref("HandoffBoundary")),
        },
        PROJECTION,
    ),
    "SkillReferenceKind": _enum("instruction", "reference", "script", "asset"),
    "SkillReference": _record({"kind": _ref("SkillReferenceKind"), "name": STRING}),
    "SkillDescriptor": _record(
        {"id": STRING, "name": STRING, "purpose": STRING, "applicability": STRINGS, "capabilities": STRINGS},
        {"references": _array(_ref("SkillReference")), **PROJECTION},
    ),
    "McpRisk": _enum("low", "moderate", "high"),
    "McpPrimitiveDescriptor": _primitive_descriptor(),
    "McpSurfaceDescriptor": _record(
        {
            "id": STRING,
            "name": STRING,
            "purpose": STRING,
            "tools": _array(_ref("McpPrimitiveDescriptor")),
            "resources": _array(_ref("McpPrimitiveDescriptor")),
            "prompts": _array(_ref("McpPrimitiveDescriptor")),
        },
        PROJECTION,
    ),
    # Operational state -------------------------------------------------------
    "OperationalStateField": _record({"id": STRING, "conceptId": STRING, "value": _ref("JsonValue")}),
    "OperationalState": _record({
        "id": STRING,
        "assemblyId": STRING,
        "assemblyVersion": STRING,
        "fields": _array(_ref("OperationalStateField")),
    }),
    "ActorObservation": _record({
        "id": STRING,
        "actorId": STRING,
        "fieldIds": STRINGS,
        "observedValues": _ref("EvidencePayload"),
    }),
    "TransitionDisposition": _enum("permitted", "prohibited"),
    "StateTransitionExpectation": _record(
        {
            "id": STRING,
            "description": STRING,
            "disposition": _ref("TransitionDisposition"),
            "required": BOOLEAN,
            "fieldIds": STRINGS,
        },
        {"eventId": STRING, "before": _ref("EvidencePayload"), "after": _ref("EvidencePayload")},
    ),
    "OutcomeDisposition": _enum("acceptable", "prohibited"),
    "OutcomeExpectation": _record({
        "id": STRING,
        "description": STRING,
        "disposition": _ref("OutcomeDisposition"),
        "required": BOOLEAN,
        "fieldIds": STRINGS,
    }),
    # Scenario ----------------------------------------------------------------
    "AutomotiveDomain": _enum(
        "service", "parts", "sales", "finance", "customer-experience", "inventory", "warranty", "compliance", "operations",
    ),
    "BusinessContext": _record({
        "domain": _ref("AutomotiveDomain"),
        "summary": STRING,
        "stakeholders": STRINGS,
        "requiredFacts": STRINGS,
        "sensitivities": STRINGS,
    }),
    "UserIntent": _record({"explicitGoal": STRING, "constraints": STRINGS}, {"inferredGoals": STRINGS}),
    "ExpectedControlSurfaces": _record({
        "harnessIds": STRINGS,
        "skillIds": STRINGS,
        "mcpServerIds": STRINGS,
        "mcpPrimitiveIds": STRINGS,
    }),
    "RealityReferenceSet": _record({
        "assemblyId": STRING,
        "assemblyVersion": STRING,
        "assemblyEntryIds": STRINGS,
        "initialStateId": STRING,
        "observationIds": STRINGS,
        "transitionIds": STRINGS,
        "outcomeIds": STRINGS,
    }),
    "EvaluationExpectations": _record({
        "requiredTraceTypes": _array(_ref("AgenticEventType")),
        "requiresPolicyCheck": BOOLEAN,
        "requiresHumanConfirmation": BOOLEAN,
    }),
    "Scenario": _record({
        "id": STRING,
        "title": STRING,
        "businessContext": _ref("BusinessContext"),
        "intent": _ref("UserIntent"),
        "reality": _ref("RealityReferenceSet"),
        "expectedControlSurfaces": _ref("ExpectedControlSurfaces"),
        "evaluation": _ref("EvaluationExpectations"),
    }),
    # Evidence ----------------------------------------------------------------
    "AgenticEventType": _enum(*AGENTIC_EVENT_TYPES),
    "RawTraceEvent": {
        **_record(
            {"type": STRING},
            {
                "sequence": _ref("JsonNumber"),
                "timestamp": STRING,
                "actorId": STRING,
                "subjectId": STRING,
                "evidence": _ref("EvidencePayload"),
            },
        ),
        "description": "Raw evidence is intentionally permissive: event types, actors, and sequences are checked by domain validation.",
    },
    "RawTrace": _array(_ref("RawTraceEvent")),
    "NormalizedTraceEvent": _record(
        {"type": _ref("AgenticEventType"), "position": _ref("SafeInteger"), "actorId": STRING, "evidence": _ref("EvidencePayload")},
        {"timestamp": STRING, "subjectId": STRING},
    ),
    "TraceNormalizationResult": _record({
        "events": _array(_ref("NormalizedTraceEvent")),
        "findings": _array(_ref("ValidationFinding")),
    }),
    # Conformance -------------------------------------------------------------
    "ConformanceCase": _record({
        "assembly": _ref("LogicalAssemblySlice"),
        "scenario": _ref("Scenario"),
        "initialState": _ref("OperationalState"),
        "observations": _array(_ref("ActorObservation")),
        "transitions": _array(_ref("StateTransitionExpectation")),
        "outcomes": _array(_ref("OutcomeExpectation")),
        "harnesses": _array(_ref("HarnessDescriptor")),
        "skills": _array(_ref("SkillDescriptor")),
        "mcpSurfaces": _array(_ref("McpSurfaceDescriptor")),
        "trace": _ref("RawTrace"),
    }),
    "EvaluationDimension": _enum(
        "intent-fidelity",
        "semantic-fidelity",
        "reality-model-validity",
        "state-and-outcome-validity",
        "control-surface-quality",
        "reality-coverage",
        "evidence-and-attribution",
        "governance",
    ),
    "EvaluationStatus": _enum("pass", "warning", "fail"),
    "EvaluationFindingSeverity": _enum("info", "warning", "error"),
    "DivergenceSource": _enum(
        "reality-model", "projection", "control-surface", "agent-conduct", "external-system", "insufficient-evidence",
    ),
    "EvaluationFinding": _record(
        {
            "code": STRING,
            "severity": _ref("EvaluationFindingSeverity"),
            "message": STRING,
            "evidenceRefs": STRINGS,
            "assemblyEntryIds": STRINGS,
            "transitionIds": STRINGS,
            "outcomeIds": STRINGS,
        },
        {"attribution": _ref("DivergenceSource")},
    ),
    "DimensionResult": _record({
        "dimension": _ref("EvaluationDimension"),
        "status": _ref("EvaluationStatus"),
        "findings": _array(_ref("EvaluationFinding")),
        "evidenceRefs": STRINGS,
    }),
    "ConformanceEvaluation": _record({
        "assemblyId": STRING,
        "assemblyVersion": STRING,
        "scenarioId": STRING,
        "valid": BOOLEAN,
        "conformant": BOOLEAN,
        "validationFindings": _array(_ref("ValidationFinding")),
        "dimensions": _array(_ref("DimensionResult")),
    }),
}

DOMAIN_SCHEMA: JsonSchema = {
    "$schema": DRAFT,
    "$id": DOMAIN_ID,
    "title": "Lasm core interchange records, version 1",
    "$defs": DEFINITIONS,
}


def document_schema_id(kind: str) -> str:
    return f"urn:lasm-core:schema:v1:{kind}"


def document_schema(kind: str) -> JsonSchema:
    return {
        "$schema": DRAFT,
        "$id": document_schema_id(kind),
        "title": f"Lasm {kind} document, version 1",
        "type": "object",
        "properties": {
            "schemaVersion": {"const": SCHEMA_VERSION},
            "kind": {"const": kind},
            "value": {"$ref": f"{DOMAIN_ID}#/$defs/{DOCUMENT_DEFINITIONS[kind]}"},
        },
        "required": ["schemaVersion", "kind", "value"],
        "additionalProperties": False,
    }


def schema_files() -> dict[str, JsonSchema]:
    """The checked-in schema files, keyed by file name."""
    files = {"domain.schema.json": DOMAIN_SCHEMA}
    for kind in DOCUMENT_DEFINITIONS:
        files[f"{kind}.schema.json"] = document_schema(kind)
    return files

