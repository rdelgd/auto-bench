# Change: Add Evidence and Verdict Events to lasm_core

## Why

`lasm-core` 0.4.0 gave the world ledger its first semantics: paseo-core's governance rules. The next writer is patchrig, the in-vitro-patching rig. It measures whether a weight patch carries the meaning it claims, and judges each measurement against pre-registered thresholds. Its events reach the ledger through `lasm_core` schemas, so that LogicalAssembly can project them and decide whether a weight projection may be enabled.

The contract has been negotiated across LogicalAssembly, patchrig, Rastro, and auto-bench, and is recorded in the evidence section of `lasm-paseo-assembly-source-of-truth.md`. It has four event types, four verdict values, five cannot-tell reasons, and the rules for the verdict projection. Patchrig's step 1 report confirms that nothing it found changes those shapes, and that `lasm-core` can write them now, before the first verified cell.

## What Changes

- Add four ledger event types, each with version 1 data schemas under `src/lasm_core/schemas/ledger/`:
  - `evidence.recorded`: a measurement, on an `experiment:` stream;
  - `verdict.recorded`: a judgement of one measurement, on a `judgement:` stream;
  - `verdict.invalidated`: a flaw stated as a condition, citing one verdict known to be affected, on a `judgement:invalidation@…` stream;
  - `invalidation.retracted`: withdraws a whole invalidation stream.
- Encode the agreed rules in the `verdict.recorded` schema:
  - four verdict values: `holds`, `inconclusive`, `fails`, `cannot-tell`;
  - `cannotTellReason` from a closed set of five codes, required with `cannot-tell` and forbidden with any other verdict;
  - an optional free-text `detail`.
- Add `patchrigCommit`, `larqlVersion`, and the descriptive `larqlBinarySha256` to `evidence.recorded`, and `scorerVersions` to an invalidation's scope, as agreed with patchrig. Without them, an invalidation's scope can't be matched against verdicts.
- Add `project_verdicts(events)`, a pure projection that follows the global log. It folds verdicts per (cell, attempt, pre-registration), applies `supersedes`, then applies unretracted invalidations by condition and by citation. It gives every group one of four statuses, and reports conflicts, supersession cycles, and unreadable or dangling events as findings.
- Extend the shared schema checker with `else` and `not`, which the conditional reason-code rule needs, kept in agreement with `jsonschema`.
- Extend `LedgerEventType`, `LEDGER_EVENT_TYPES`, and `validate_ledger_event_data` to cover the new types.
- Bump the package to `0.5.0`.

## Impact

- Affected capability: `evidence-and-verdict-events` (new). `world-ledger-governance-events` from `add-world-ledger-governance-events` is unchanged. If that change is archived first, `LEDGER_EVENT_TYPES` simply grows.
- Affected implementation: `src/lasm_core/ledger.py`, `src/lasm_core/verdict.py` (new), `src/lasm_core/_schema_ledger.py`, `src/lasm_core/_json_schema.py`, `__init__.py`, rendered schemas, `tests/`, `docs/api-inventory.md`, `README.md`, `.reffy/reffyspec/project.md`, `pyproject.toml`.
- Compatibility: additive. The 0.4.0 governance schemas, the interchange version 1 schemas, the parity corpus, and every existing export behave as before. A reader pinned to 0.4.0 reports the new event types as unsupported, which `project_decision_rules` already ignores.
- Consumers: LogicalAssembly runs the projection and pins `v0.5.0`. Patchrig builds event data to these schemas from its run directories. Rastro authorizes the event types per witness.
- Out of scope:
  - `evidence.recorded` on `evaluation:` streams. Auto-bench's own Auto Bench findings need their own shape, which a later version will add.
  - Ranking several criteria into one summary. That happens inside the rig.
  - Deciding whether a verdict means a policy holds. That's LogicalAssembly's projection.
  - Writer-side checks against outstanding invalidations, in the rig.
  - Any I/O, polling, or stream listing.

## Supersedes

None

## Reffy References

- `lasm-paseo-assembly-source-of-truth.md` (project `nuveris`) - the evidence contract: the four event types, their example data, the verdict projection's four rules, the two things that are never `cannot-tell`, and the order for adding a reason code
- `lasm-core-reply-on-retracting-invalidations.md` - `invalidation.retracted`, `cites` as a stream id versus an event reference, never parsing stream ids, and camelCase data
- `lasm-core-reply-on-four-verdict-values.md` - patchrig's four verdict values, `cannotTellReason` as a closed set, and `detail`
- `lasm-core-reply-on-cannot-tell-reasons.md` - the five reason codes and the two exclusions
- `in-vitro-patching-step-1-fruitfly-compose-check.md` - confirmation that the event shapes stand, and that the change can start now
- `lasm-review-evidence-and-verdict-events.md` (project `nuveris`) - LogicalAssembly's acceptance: the `unresolved` status, supersession cycles, superseded-then-invalidated, and the suggested `claimScope` rename
- `in-vitro-patching-reply-on-invalidation-scope-fields.md` (project `in-vitro-patching`) - patchrig's answers: the three measurement fields, separate `scorerVersions`, and attempts as separate groups
- `in-vitro-patching-reply-on-measurement-scope-rename.md` (project `in-vitro-patching`) - the measurement's `scope` renamed to `claimScope` before the tag
