"""Evidence and verdict events, and the projection of each cell's current verdict.

Measurements are written once and never revised. Verdicts judge one measurement against a
dated pre-registration and are revised only by new streams: a re-score names what it
supersedes, an invalidation states a flaw as a condition, and a retraction withdraws an
invalidation. The projection follows the global log, reads citations rather than stream
ids, and reports what it cannot resolve instead of guessing.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Literal, NotRequired, TypeAlias, TypedDict, cast, get_args

from ._json_schema import finding
from .domain import JsonValue, ValidationFinding
from .ledger import LedgerEventRef, RecordedEvent, _readable_event_data

VerdictValue: TypeAlias = Literal["holds", "inconclusive", "fails", "cannot-tell"]
CannotTellReason: TypeAlias = Literal[
    "no-probes",
    "too-few-values",
    "degenerate-stratum",
    "instrument-gate-failed",
    "no-eligible-chains",
]
ManipulationCheck: TypeAlias = Literal["passed", "failed", "not-applicable"]
CellVerdictStatus: TypeAlias = Literal["current", "invalidated", "conflicting", "unresolved"]

VERDICT_VALUES: tuple[VerdictValue, ...] = get_args(VerdictValue)
CANNOT_TELL_REASONS: tuple[CannotTellReason, ...] = get_args(CannotTellReason)


class MeasurementTarget(TypedDict):
    binding: str
    ref: str


class MeasurementEnvironment(TypedDict):
    host: str
    fingerprint: str


class EvidenceRecordedData(TypedDict):
    cellId: str
    attempt: int
    shardIndex: NotRequired[int]
    shardCount: NotRequired[int]
    target: MeasurementTarget
    vindexPin: str
    patchDigest: str
    patchrigCommit: str
    larqlVersion: str
    larqlBinarySha256: str
    manipulationCheck: ManipulationCheck
    tier: str
    claimScope: str
    controlsState: str
    measurements: Mapping[str, JsonValue]
    recordsDigest: str
    environment: MeasurementEnvironment
    ledgerPosition: NotRequired[int]


class VerdictRecordedData(TypedDict):
    cellId: str
    attempt: int
    cites: LedgerEventRef
    preregistration: str
    scorerVersion: str
    supersedes: NotRequired[str]
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    policyEvent: NotRequired[LedgerEventRef]


class InvalidationScope(TypedDict):
    patchrigCommits: NotRequired[Sequence[str]]
    scorerVersions: NotRequired[Sequence[str]]
    vindexPins: NotRequired[Sequence[str]]
    larqlVersions: NotRequired[Sequence[str]]


class VerdictInvalidatedData(TypedDict):
    instrument: str
    scope: InvalidationScope
    cites: LedgerEventRef
    reason: str


class InvalidationRetractedData(TypedDict):
    cites: str
    reason: str


class ProjectedVerdict(TypedDict):
    cellId: str
    attempt: int
    preregistration: str
    scorerVersion: str
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    policyEvent: NotRequired[LedgerEventRef]
    manipulationCheck: ManipulationCheck
    source: LedgerEventRef
    measurement: LedgerEventRef


class CellVerdict(TypedDict):
    cellId: str
    attempt: int
    preregistration: str
    status: CellVerdictStatus
    current: NotRequired[ProjectedVerdict]
    candidates: NotRequired[Sequence[LedgerEventRef]]
    invalidatedBy: NotRequired[Sequence[str]]


class VerdictProjection(TypedDict):
    cells: Sequence[CellVerdict]
    findings: Sequence[ValidationFinding]


_GroupKey: TypeAlias = tuple[str, int, str]

# Scope list -> (whether it reads the verdict rather than the measurement, the field it matches).
_SCOPE_FIELDS: dict[str, tuple[bool, str]] = {
    "patchrigCommits": (False, "patchrigCommit"),
    "scorerVersions": (True, "scorerVersion"),
    "vindexPins": (False, "vindexPin"),
    "larqlVersions": (False, "larqlVersion"),
}


class _Verdict(TypedDict):
    index: int
    ref: LedgerEventRef
    data: VerdictRecordedData


class _Invalidation(TypedDict):
    index: int
    scope: InvalidationScope
    cites: list[tuple[int, LedgerEventRef]]


def _ref(event: RecordedEvent) -> LedgerEventRef:
    return {"streamId": event["streamId"], "streamVersion": event["streamVersion"]}


def _ref_key(ref: LedgerEventRef) -> tuple[str, int]:
    return (ref["streamId"], ref["streamVersion"])


def _group(data: VerdictRecordedData) -> _GroupKey:
    return (data["cellId"], data["attempt"], data["preregistration"])


def _scope_lists(scope: InvalidationScope) -> dict[str, Sequence[str]]:
    return {name: values for name, values in scope.items() if values}  # type: ignore[misc]


def _matches(scope: InvalidationScope, verdict: VerdictRecordedData, measurement: EvidenceRecordedData) -> bool:
    lists = _scope_lists(scope)
    if not lists:
        return False
    for name, values in lists.items():
        from_verdict, field = _SCOPE_FIELDS[name]
        source = cast(Mapping[str, object], verdict if from_verdict else measurement)
        if source[field] not in values:
            return False
    return True


def _supersession_cycles(edges: Mapping[str, str]) -> set[str]:
    """Stream ids on a cycle of ``supersedes`` links; each verdict names at most one other."""
    on_cycle: set[str] = set()
    settled: set[str] = set()
    for start in edges:
        path: list[str] = []
        node: str | None = start
        while node is not None and node not in settled and node not in path:
            path.append(node)
            node = edges.get(node)
        if node is not None and node in path:
            on_cycle.update(path[path.index(node):])
        settled.update(path)
    return on_cycle


def _projected(verdict: _Verdict, measurement: EvidenceRecordedData) -> ProjectedVerdict:
    data = verdict["data"]
    projected: ProjectedVerdict = {
        "cellId": data["cellId"],
        "attempt": data["attempt"],
        "preregistration": data["preregistration"],
        "scorerVersion": data["scorerVersion"],
        "verdict": data["verdict"],
        "manipulationCheck": measurement["manipulationCheck"],
        "source": verdict["ref"],
        "measurement": data["cites"],
    }
    for key in ("cannotTellReason", "detail", "policyEvent"):
        if key in data:
            projected[key] = data[key]
    return projected


def project_verdicts(events: Sequence[RecordedEvent]) -> VerdictProjection:
    """Project the current verdict per (cell, attempt, pre-registration) from events in log order.

    Supersession is applied before invalidation and is permanent. A group is ``current`` with
    one verdict, ``conflicting`` with several, ``invalidated`` when invalidations removed the
    rest, or ``unresolved`` when nothing remains for any other reason. Adapters must not act on
    a group whose status is conflicting or unresolved, or that has a finding addressed to its events.
    """
    findings: list[ValidationFinding] = []
    measurements: dict[tuple[str, int], EvidenceRecordedData] = {}
    verdicts: dict[str, _Verdict] = {}
    invalidations: dict[str, _Invalidation] = {}
    retractions: list[tuple[int, str]] = []

    for index, event in enumerate(events):
        event_type = event["type"]
        if event_type not in ("evidence.recorded", "verdict.recorded", "verdict.invalidated", "invalidation.retracted"):
            continue
        if not _readable_event_data(event, index, findings):
            continue
        path = f"events[{index}].data"
        if event_type == "evidence.recorded":
            measurements[_ref_key(_ref(event))] = cast(EvidenceRecordedData, event["data"])
        elif event_type == "verdict.recorded":
            verdicts.setdefault(event["streamId"], {"index": index, "ref": _ref(event), "data": cast(VerdictRecordedData, event["data"])})
        elif event_type == "verdict.invalidated":
            data = cast(VerdictInvalidatedData, event["data"])
            known = invalidations.get(event["streamId"])
            if known is None:
                invalidations[event["streamId"]] = {"index": index, "scope": data["scope"], "cites": [(index, data["cites"])]}
                if not _scope_lists(data["scope"]):
                    findings.append(finding("invalidation.empty_scope", f"{path}.scope", "An invalidation with no scope matches only the verdicts it cites."))
            else:
                known["cites"].append((index, data["cites"]))
                first = cast(VerdictInvalidatedData, events[known["index"]]["data"])
                if (data["instrument"], data["scope"], data["reason"]) != (first["instrument"], first["scope"], first["reason"]):
                    findings.append(finding(
                        "invalidation.inconsistent_condition",
                        path,
                        f"Every event in {event['streamId']} must state the same instrument, scope, and reason; the first event's condition is used.",
                    ))
        else:
            retractions.append((index, cast(InvalidationRetractedData, event["data"])["cites"]))

    retracted: set[str] = set()
    for index, withdrawn in retractions:
        if withdrawn in invalidations:
            retracted.add(withdrawn)
        else:
            findings.append(finding("retraction.unknown_invalidation", f"events[{index}].data.cites", f"No invalidation stream {withdrawn} is in the log."))
    active = {stream: invalidation for stream, invalidation in invalidations.items() if stream not in retracted}

    # A cited verdict outside the invalidation's own condition is still removed, but reported.
    for invalidation in active.values():
        if not _scope_lists(invalidation["scope"]):
            continue
        for index, cited in invalidation["cites"]:
            verdict = verdicts.get(cited["streamId"])
            if verdict is None or _ref_key(verdict["ref"]) != _ref_key(cited):
                continue
            measurement = measurements.get(_ref_key(verdict["data"]["cites"]))
            if measurement is not None and not _matches(invalidation["scope"], verdict["data"], measurement):
                findings.append(finding(
                    "invalidation.cited_outside_scope",
                    f"events[{index}].data.cites",
                    f"Verdict {cited['streamId']} is cited but does not match the invalidation's scope.",
                ))

    groups: dict[_GroupKey, list[str]] = {}
    for stream, verdict in verdicts.items():
        groups.setdefault(_group(verdict["data"]), []).append(stream)

    cells: list[CellVerdict] = []
    for key in sorted(groups):
        members = sorted(groups[key], key=lambda stream: verdicts[stream]["index"])
        candidates: list[str] = []
        edges: dict[str, str] = {}
        for stream in members:
            verdict = verdicts[stream]
            path = f"events[{verdict['index']}].data"
            if _ref_key(verdict["data"]["cites"]) not in measurements:
                findings.append(finding("verdict.unknown_measurement", f"{path}.cites", f"Measurement {verdict['data']['cites']['streamId']} is not in the log."))
            else:
                candidates.append(stream)
            replaced = verdict["data"].get("supersedes")
            if replaced is None:
                continue
            if replaced in verdicts and _group(verdicts[replaced]["data"]) == key:
                edges[stream] = replaced
            else:
                findings.append(finding(
                    "verdict.invalid_supersedes",
                    f"{path}.supersedes",
                    f"{replaced} is not a verdict for the same cell, attempt, and pre-registration.",
                ))

        cycle = _supersession_cycles(edges)
        for stream in sorted(cycle, key=lambda stream: verdicts[stream]["index"]):
            findings.append(finding(
                "verdict.supersedes_cycle",
                f"events[{verdicts[stream]['index']}].data.supersedes",
                f"Verdict {stream} is in a supersession cycle.",
            ))
        superseded = set(edges.values()) | cycle
        candidates = [stream for stream in candidates if stream not in superseded]

        invalidated_by: set[str] = set()
        remaining: list[str] = []
        for stream in candidates:
            verdict = verdicts[stream]
            measurement = measurements[_ref_key(verdict["data"]["cites"])]
            removers = {
                invalidation_stream
                for invalidation_stream, invalidation in active.items()
                if any(_ref_key(cited) == _ref_key(verdict["ref"]) for _, cited in invalidation["cites"])
                or _matches(invalidation["scope"], verdict["data"], measurement)
            }
            if removers:
                invalidated_by |= removers
            else:
                remaining.append(stream)

        cell: CellVerdict = {"cellId": key[0], "attempt": key[1], "preregistration": key[2], "status": "unresolved"}
        if len(remaining) == 1:
            verdict = verdicts[remaining[0]]
            cell["status"] = "current"
            cell["current"] = _projected(verdict, measurements[_ref_key(verdict["data"]["cites"])])
        elif remaining:
            cell["status"] = "conflicting"
            cell["candidates"] = [verdicts[stream]["ref"] for stream in remaining]
            for stream in remaining:
                findings.append(finding(
                    "verdict.conflict",
                    f"events[{verdicts[stream]['index']}]",
                    f"Verdicts {', '.join(remaining)} share a cell, attempt, and pre-registration, and none supersedes the others.",
                ))
        elif invalidated_by:
            cell["status"] = "invalidated"
        if invalidated_by:
            cell["invalidatedBy"] = sorted(invalidated_by)
        cells.append(cell)

    return {"cells": cells, "findings": findings}
