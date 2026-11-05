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
    adapters: NotRequired[Sequence[AdapterMatch]]


class VerdictInvalidatedData(TypedDict):
    instrument: str
    scope: InvalidationScope
    cites: LedgerEventRef
    reason: str


class InvalidationRetractedData(TypedDict):
    cites: str
    reason: str


class AdapterIdentity(TypedDict):
    kind: str
    model: str
    host: str
    route: NotRequired[str]
    served: str


class RunInput(TypedDict):
    role: str
    runId: str
    recordsDigest: str
    seeds: NotRequired[str]


class MeasurementItem(TypedDict, total=False):
    """One measured quantity; ``carrier`` and ``tunedThreshold`` are named, other keys are free-form."""

    carrier: str
    tunedThreshold: float


class EvidenceRecordedDataV2(TypedDict):
    runId: str
    attempt: int
    runKind: str
    recordsDigest: str
    patchrigCommit: str
    claimScope: str
    adapter: AdapterIdentity
    measurements: Sequence[MeasurementItem]
    inputs: NotRequired[Sequence[RunInput]]
    fixture: NotRequired[Mapping[str, JsonValue]]
    preregistration: NotRequired[str]
    tier: NotRequired[str]


class VerdictRecordedDataV2(TypedDict):
    runId: str
    attempt: int
    claimId: str
    claim: str
    cites: LedgerEventRef
    preregistration: str
    scorerVersion: str
    verdict: VerdictValue
    supersedes: NotRequired[str]
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    predicted: NotRequired[Sequence[VerdictValue]]
    statistics: NotRequired[Mapping[str, JsonValue]]
    policyEvent: NotRequired[LedgerEventRef]


class AdapterMatch(TypedDict):
    model: str
    host: str
    kind: NotRequired[str]
    route: NotRequired[str]
    served: NotRequired[str]


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


class ProjectedRunVerdict(TypedDict):
    runId: str
    attempt: int
    claimId: str
    claim: str
    preregistration: str
    scorerVersion: str
    verdict: VerdictValue
    cannotTellReason: NotRequired[CannotTellReason]
    detail: NotRequired[str]
    predicted: NotRequired[Sequence[VerdictValue]]
    statistics: NotRequired[Mapping[str, JsonValue]]
    policyEvent: NotRequired[LedgerEventRef]
    adapter: AdapterIdentity
    source: LedgerEventRef
    measurement: LedgerEventRef


class RunVerdict(TypedDict):
    runId: str
    attempt: int
    claimId: str
    preregistration: str
    status: CellVerdictStatus
    current: NotRequired[ProjectedRunVerdict]
    candidates: NotRequired[Sequence[LedgerEventRef]]
    invalidatedBy: NotRequired[Sequence[str]]


class VerdictProjection(TypedDict):
    cells: Sequence[CellVerdict]
    runs: Sequence[RunVerdict]
    findings: Sequence[ValidationFinding]


_CellKey: TypeAlias = tuple[str, int, str]          # (cellId, attempt, preregistration)
_RunKey: TypeAlias = tuple[str, int, str, str]      # (runId, attempt, claimId, preregistration)

# Scope list -> (whether it reads the verdict rather than the measurement, the field it matches).
# A measurement that lacks the field never matches, so version 1 pins never reach version 2 runs.
_SCOPE_FIELDS: dict[str, tuple[bool, str]] = {
    "patchrigCommits": (False, "patchrigCommit"),
    "scorerVersions": (True, "scorerVersion"),
    "vindexPins": (False, "vindexPin"),
    "larqlVersions": (False, "larqlVersion"),
}

_GROUP_WORDS = {1: "cell, attempt, and pre-registration", 2: "run, attempt, claim, and pre-registration"}


class _Verdict(TypedDict):
    index: int
    version: int
    ref: LedgerEventRef
    data: Mapping[str, object]


class _Measurement(TypedDict):
    version: int
    data: Mapping[str, object]


class _Invalidation(TypedDict):
    index: int
    scope: InvalidationScope
    cites: list[tuple[int, LedgerEventRef]]


def _ref(event: RecordedEvent) -> LedgerEventRef:
    return {"streamId": event["streamId"], "streamVersion": event["streamVersion"]}


def _ref_key(ref: object) -> tuple[str, int]:
    citation = cast(LedgerEventRef, ref)
    return (citation["streamId"], citation["streamVersion"])


def _cell_key(data: Mapping[str, object]) -> _CellKey:
    return (cast(str, data["cellId"]), cast(int, data["attempt"]), cast(str, data["preregistration"]))


def _run_key(data: Mapping[str, object]) -> _RunKey:
    return (cast(str, data["runId"]), cast(int, data["attempt"]), cast(str, data["claimId"]), cast(str, data["preregistration"]))


def _group(verdict: _Verdict) -> tuple[int, _CellKey | _RunKey]:
    # The version tag keeps a cell and a run with equal ids from ever meeting.
    data = verdict["data"]
    return (1, _cell_key(data)) if verdict["version"] == 1 else (2, _run_key(data))


def _scope_lists(scope: InvalidationScope) -> dict[str, Sequence[object]]:
    return {name: values for name, values in scope.items() if values}  # type: ignore[misc]


def _adapter_matches(entries: Sequence[object], adapter: object) -> bool:
    if not isinstance(adapter, Mapping):
        return False
    return any(
        all(adapter.get(key) == value for key, value in cast(Mapping[str, object], entry).items())
        for entry in entries
    )


def _matches(scope: InvalidationScope, verdict: Mapping[str, object], measurement: Mapping[str, object]) -> bool:
    lists = _scope_lists(scope)
    if not lists:
        return False
    for name, values in lists.items():
        if name == "adapters":
            if not _adapter_matches(values, measurement.get("adapter")):
                return False
            continue
        from_verdict, field = _SCOPE_FIELDS[name]
        source = verdict if from_verdict else measurement
        if field not in source or source[field] not in values:
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


def _copy_optional(source: Mapping[str, object], target: dict[str, object], keys: Sequence[str]) -> None:
    for key in keys:
        if key in source:
            target[key] = source[key]


def _projected_cell(verdict: _Verdict, measurement: Mapping[str, object]) -> ProjectedVerdict:
    data = cast(VerdictRecordedData, verdict["data"])
    projected: dict[str, object] = {
        "cellId": data["cellId"],
        "attempt": data["attempt"],
        "preregistration": data["preregistration"],
        "scorerVersion": data["scorerVersion"],
        "verdict": data["verdict"],
        "manipulationCheck": measurement["manipulationCheck"],
        "source": verdict["ref"],
        "measurement": data["cites"],
    }
    _copy_optional(data, projected, ("cannotTellReason", "detail", "policyEvent"))
    return cast(ProjectedVerdict, projected)


def _projected_run(verdict: _Verdict, measurement: Mapping[str, object]) -> ProjectedRunVerdict:
    data = cast(VerdictRecordedDataV2, verdict["data"])
    projected: dict[str, object] = {
        "runId": data["runId"],
        "attempt": data["attempt"],
        "claimId": data["claimId"],
        "claim": data["claim"],
        "preregistration": data["preregistration"],
        "scorerVersion": data["scorerVersion"],
        "verdict": data["verdict"],
        "adapter": measurement["adapter"],
        "source": verdict["ref"],
        "measurement": data["cites"],
    }
    _copy_optional(data, projected, ("cannotTellReason", "detail", "predicted", "statistics", "policyEvent"))
    return cast(ProjectedRunVerdict, projected)


def project_verdicts(events: Sequence[RecordedEvent]) -> VerdictProjection:
    """Project current verdicts from events in log order.

    Version 1 verdicts are grouped per (cell, attempt, pre-registration) into ``cells``, and
    version 2 verdicts per (run, attempt, claim, pre-registration) into ``runs``; both follow
    the same rules. Supersession is applied before invalidation and is permanent. A group is
    ``current`` with one verdict, ``conflicting`` with several, ``invalidated`` when
    invalidations removed the rest, or ``unresolved`` when nothing remains for any other reason.
    Adapters must not act on a group whose status is conflicting or unresolved, or that has a
    finding addressed to its events.
    """
    findings: list[ValidationFinding] = []
    measurements: dict[tuple[str, int], _Measurement] = {}
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
        data = cast(Mapping[str, object], event["data"])
        if event_type == "evidence.recorded":
            measurements[_ref_key(_ref(event))] = {"version": event["schemaVersion"], "data": data}
        elif event_type == "verdict.recorded":
            verdicts.setdefault(event["streamId"], {"index": index, "version": event["schemaVersion"], "ref": _ref(event), "data": data})
        elif event_type == "verdict.invalidated":
            invalidated = cast(VerdictInvalidatedData, data)
            known = invalidations.get(event["streamId"])
            if known is None:
                invalidations[event["streamId"]] = {"index": index, "scope": invalidated["scope"], "cites": [(index, invalidated["cites"])]}
                if not _scope_lists(invalidated["scope"]):
                    findings.append(finding("invalidation.empty_scope", f"{path}.scope", "An invalidation with no scope matches only the verdicts it cites."))
            else:
                known["cites"].append((index, invalidated["cites"]))
                first = cast(VerdictInvalidatedData, events[known["index"]]["data"])
                if (invalidated["instrument"], invalidated["scope"], invalidated["reason"]) != (first["instrument"], first["scope"], first["reason"]):
                    findings.append(finding(
                        "invalidation.inconsistent_condition",
                        path,
                        f"Every event in {event['streamId']} must state the same instrument, scope, and reason; the first event's condition is used.",
                    ))
        else:
            retractions.append((index, cast(InvalidationRetractedData, data)["cites"]))

    retracted: set[str] = set()
    for index, withdrawn in retractions:
        if withdrawn in invalidations:
            retracted.add(withdrawn)
        else:
            findings.append(finding("retraction.unknown_invalidation", f"events[{index}].data.cites", f"No invalidation stream {withdrawn} is in the log."))
    active = {stream: invalidation for stream, invalidation in invalidations.items() if stream not in retracted}

    def cited_measurement(verdict: _Verdict) -> _Measurement | None:
        measurement = measurements.get(_ref_key(verdict["data"]["cites"]))
        return measurement if measurement is not None and measurement["version"] == verdict["version"] else None

    # A cited verdict outside the invalidation's own condition is still removed, but reported.
    for invalidation in active.values():
        if not _scope_lists(invalidation["scope"]):
            continue
        for index, cited in invalidation["cites"]:
            verdict = verdicts.get(cited["streamId"])
            if verdict is None or _ref_key(verdict["ref"]) != _ref_key(cited):
                continue
            measurement = cited_measurement(verdict)
            if measurement is not None and not _matches(invalidation["scope"], verdict["data"], measurement["data"]):
                findings.append(finding(
                    "invalidation.cited_outside_scope",
                    f"events[{index}].data.cites",
                    f"Verdict {cited['streamId']} is cited but does not match the invalidation's scope.",
                ))

    def resolve(version: int, members: list[str]) -> dict[str, object]:
        """Resolve one group's verdicts into its status, reporting what can't be resolved."""
        words = _GROUP_WORDS[version]
        group_id = _group(verdicts[members[0]])
        candidates: list[str] = []
        edges: dict[str, str] = {}
        for stream in members:
            verdict = verdicts[stream]
            path = f"events[{verdict['index']}].data"
            cites = cast(LedgerEventRef, verdict["data"]["cites"])
            found = measurements.get(_ref_key(cites))
            if found is None:
                findings.append(finding("verdict.unknown_measurement", f"{path}.cites", f"Measurement {cites['streamId']} is not in the log."))
            elif found["version"] != version:
                findings.append(finding(
                    "verdict.measurement_version_mismatch",
                    f"{path}.cites",
                    f"A version {version} verdict cites a version {found['version']} measurement.",
                ))
            else:
                candidates.append(stream)
            replaced = verdict["data"].get("supersedes")
            if replaced is None:
                continue
            assert isinstance(replaced, str)
            if replaced in verdicts and _group(verdicts[replaced]) == group_id:
                edges[stream] = replaced
            else:
                findings.append(finding("verdict.invalid_supersedes", f"{path}.supersedes", f"{replaced} is not a verdict for the same {words}."))

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
                or _matches(invalidation["scope"], verdict["data"], measurement["data"])
            }
            if removers:
                invalidated_by |= removers
            else:
                remaining.append(stream)

        group: dict[str, object] = {"status": "unresolved"}
        if len(remaining) == 1:
            verdict = verdicts[remaining[0]]
            measured = measurements[_ref_key(verdict["data"]["cites"])]["data"]
            group["status"] = "current"
            group["current"] = _projected_cell(verdict, measured) if version == 1 else _projected_run(verdict, measured)
        elif remaining:
            group["status"] = "conflicting"
            group["candidates"] = [verdicts[stream]["ref"] for stream in remaining]
            for stream in remaining:
                findings.append(finding(
                    "verdict.conflict",
                    f"events[{verdicts[stream]['index']}]",
                    f"Verdicts {', '.join(remaining)} share a {words}, and none supersedes the others.",
                ))
        elif invalidated_by:
            group["status"] = "invalidated"
        if invalidated_by:
            group["invalidatedBy"] = sorted(invalidated_by)
        return group

    cell_groups: dict[_CellKey, list[str]] = {}
    run_groups: dict[_RunKey, list[str]] = {}
    for stream, verdict in verdicts.items():
        if verdict["version"] == 1:
            cell_groups.setdefault(_cell_key(verdict["data"]), []).append(stream)
        else:
            run_groups.setdefault(_run_key(verdict["data"]), []).append(stream)

    def in_log_order(members: list[str]) -> list[str]:
        return sorted(members, key=lambda stream: verdicts[stream]["index"])

    cells: list[CellVerdict] = []
    for cell_id, attempt, preregistration in sorted(cell_groups):
        group = resolve(1, in_log_order(cell_groups[(cell_id, attempt, preregistration)]))
        cells.append(cast(CellVerdict, {"cellId": cell_id, "attempt": attempt, "preregistration": preregistration, **group}))
    runs: list[RunVerdict] = []
    for run_id, attempt, claim_id, preregistration in sorted(run_groups):
        group = resolve(2, in_log_order(run_groups[(run_id, attempt, claim_id, preregistration)]))
        runs.append(cast(RunVerdict, {"runId": run_id, "attempt": attempt, "claimId": claim_id, "preregistration": preregistration, **group}))

    return {"cells": cells, "runs": runs, "findings": findings}
