---
name: replay-standing
description: Replay a prior consequence or verification capsule and assign bounded standing. Use when determinism, reproducibility, long-horizon reconstruction, or release confidence matters.
---

# replay-standing

Turn receipts into re-executable evidence and scoped standing.

## Use when

Replay a prior consequence or verification capsule and assign bounded standing. Use when determinism, reproducibility, long-horizon reconstruction, or release confidence matters.

## Inputs

- Receipt DAG or replay inputs.
- Exact source/validator/toolchain/config/environment identities.

## Procedure

1. Check identity compatibility before reusing verifier evidence.
2. Replay the smallest deterministic capsule available.
3. Compare consequence and verifier outputs.
4. Classify drift as source, validator, toolchain, config, environment, or nondeterminism.
5. Assign only the standing earned by observed execution.

## Output

Replay result plus `UNKNOWN | PARTIAL_ALIVE | ALIVE | BLOCKED | BUILD_BROKEN | UNSUPPORTED | REFUSED` and scope.

## Falsifiers and refusals

- Do not reuse VERIFIER_ALIVE when validator/toolchain identities differ materially.
- SUBJECT_ALIVE must be proven separately from verifier availability.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
