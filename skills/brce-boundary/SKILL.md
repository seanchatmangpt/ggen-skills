---
name: brce-boundary
description: Broker consequential execution through an explicit bounded receipt-carrying execution boundary. Use before writes, deployments, sends, merges, deletions, infrastructure changes, or other externally consequential operations.
---

# brce-boundary

Enforce zero unreceipted actuation.

## Use when

Broker consequential execution through an explicit bounded receipt-carrying execution boundary. Use before writes, deployments, sends, merges, deletions, infrastructure changes, or other externally consequential operations.

## Inputs

- Actuation intent.
- Exact subject and consequence.
- Authority token/policy and preconditions.

## Procedure

1. Validate subject identity and requested consequence.
2. Check authority scope, expiry, and preconditions.
3. Admit or emit a typed REFUSED result.
4. Execute only the admitted operation.
5. Observe the immediate consequence.
6. Emit a receipt binding intent, authority, subject, execution identity, result, and verifier hooks.

## Output

A receipt for executed consequence or a typed refusal with no actuation.

## Falsifiers and refusals

- No receipt means no successful DO claim.
- Do not widen authority because a narrower path failed.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
