## 1. Planning
- [x] 1.1 Review the current benchmark naming in Reffy artifacts and canonical specs.
- [x] 1.2 Record the rename as a change superseding the prior SArB naming decisions.
- [x] 1.3 Validate the proposal before implementation.

## 2. Implementation
- [x] 2.1 Replace current prose references to SArB with Auto Bench.
- [x] 2.2 Rename current artifact and canonical-spec paths to `auto-bench` identifiers.
- [x] 2.3 Update Reffy project and manifest metadata without rewriting archived changes.

## 3. Verification
- [x] 3.1 Verify remaining SArB references are confined to immutable history.
- [x] 3.2 Run Reffy reindexing and validation.
- [x] 3.3 Run typecheck and tests to confirm the naming-only change preserves behavior.
- [x] 3.4 Validate and archive `adopt-auto-bench-name`.
