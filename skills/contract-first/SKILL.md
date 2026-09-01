---
name: contract-first
description: Define semantic subjects, invariants, preconditions, postconditions, refusals, authority, idempotency, resource bounds, evidence, compatibility, and standing before choosing implementation. Use for any nontrivial change or generated artifact.
---

# contract-first

Make implementation and verification sibling consequences of an explicit contract.

## Use when

Define semantic subjects, invariants, preconditions, postconditions, refusals, authority, idempotency, resource bounds, evidence, compatibility, and standing before choosing implementation. Use for any nontrivial change or generated artifact.

## Inputs

- Admitted `O*`.
- Requested consequence and acceptance boundary.

## Procedure

1. Name the exact semantic subject.
2. Define preconditions and postconditions.
3. Define invariants and compatibility obligations.
4. Define refusal conditions and authority required for each transition.
5. Define idempotency/replay expectations and resource bounds.
6. Define evidence needed to verify success and failure.
7. Only then admit implementation candidates.

## Output

An executable or inspectable contract that can drive both construction and verification.

## Falsifiers and refusals

- If the success condition cannot falsify a bad implementation, the contract is incomplete.
- Do not let implementation details become accidental requirements.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
