---
name: exact-head-verification
description: Verify the exact candidate identity rather than a branch-adjacent, stale, or predecessor state. Use for pull requests, releases, generated artifacts, deployments, or any claim tied to a specific revision.
---

# exact-head-verification

Prevent checkpoint evidence from being promoted to a crown claim.

## Use when

Verify the exact candidate identity rather than a branch-adjacent, stale, or predecessor state. Use for pull requests, releases, generated artifacts, deployments, or any claim tied to a specific revision.

## Inputs

- Candidate immutable identity.
- Acceptance commands or behavioral proof.

## Procedure

1. Resolve the candidate to an immutable identity.
2. Run the narrowest real verifier against that identity.
3. Record commands, environment/toolchain identity, and exit/result.
4. Expand to integration/e2e only after narrow gates succeed.
5. For hosted CI, inspect runs associated with the exact candidate head.
6. Reject stale green runs as evidence for moved heads.

## Output

An exact-identity verification record with observed execution and bounded standing.

## Falsifiers and refusals

- Workflow presence is not execution.
- Green CI on a different SHA is not exact-head evidence.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
