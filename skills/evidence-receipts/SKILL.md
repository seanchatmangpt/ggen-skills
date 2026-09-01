---
name: evidence-receipts
description: Design and inspect evidence receipts that bind identity, authority, execution, consequence, replay, and standing. Use after consequential execution or when auditing whether an action is actually proven.
---

# evidence-receipts

Make receipts evidence objects rather than narrative labels.

## Use when

Design and inspect evidence receipts that bind identity, authority, execution, consequence, replay, and standing. Use after consequential execution or when auditing whether an action is actually proven.

## Inputs

- Exact subject identity.
- Actuation intent and authority.
- Execution observations and verifier outputs.

## Procedure

1. Bind source/base/head or equivalent identity.
2. Bind authority and admitted intent.
3. Bind command/action identity and exit/result.
4. Bind observed consequence separately from intended consequence.
5. Bind verifier identity and evidence.
6. Bind replay inputs or reconstruction path.
7. State residual unknowns and standing scope.

## Output

A machine-readable or structured receipt sufficient to distinguish intended, executed, changed, and verified state.

## Falsifiers and refusals

- A file named receipt is not automatically a receipt.
- Status metadata without underlying execution evidence is insufficient when logs/results are required.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
