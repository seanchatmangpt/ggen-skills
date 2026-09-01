---
name: source-admission
description: Pin source identity and admit bounded knowledge before derivation. Use when work depends on repositories, documents, APIs, schemas, models, prior artifacts, or potentially stale observations.
---

# source-admission

Turn partial observations into a traceable admission boundary.

## Use when

Pin source identity and admit bounded knowledge before derivation. Use when work depends on repositories, documents, APIs, schemas, models, prior artifacts, or potentially stale observations.

## Inputs

- Source locators and exact versions when available.
- Observation timestamps and trust/authority context.

## Procedure

1. Resolve source identity to the strongest available immutable coordinate.
2. Record transport used and any gaps.
3. Classify each material statement as observed, admitted, inferred, or unknown.
4. Reject stale or adjacent evidence as proof of the exact subject.
5. Emit an admission record consumed by contracts and verifiers.

## Output

An admission record with subject identity, evidence references, bounded claims, unknowns, and expiry/revalidation conditions.

## Falsifiers and refusals

- UNKNOWN is not ADMITTED.
- A branch name without a resolved SHA is not immutable identity.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
