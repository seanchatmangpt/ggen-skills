---
name: observe-admit
description: Convert raw observations into admitted bounded knowledge O*. Use when requirements, repository state, runtime evidence, or user claims must be separated from inference before design or execution.
---

# observe-admit

Make the boundary between O and O* explicit.

## Use when

Convert raw observations into admitted bounded knowledge O*. Use when requirements, repository state, runtime evidence, or user claims must be separated from inference before design or execution.

## Inputs

- Raw observations `O`.
- Admission rules and scope.

## Procedure

1. Normalize observations without erasing provenance.
2. Separate direct observation from inference and user-declared authority.
3. Apply admission rules and resource/scope bounds.
4. Retain residual unknowns and contradictions.
5. Produce `O*` only for claims that survived admission.

## Output

`O*` plus rejected, unknown, and inferred claims, each with provenance.

## Falsifiers and refusals

- Do not admit a claim because it is plausible.
- Contradiction must remain visible until resolved or bounded.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
