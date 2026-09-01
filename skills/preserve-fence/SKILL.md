---
name: preserve-fence
description: Recover the reason, behavior, contract, evidence, and boundary behind an existing structure before removing or replacing it. Use for rewrites, migrations, deletions, architecture changes, or sunk-cost resets.
---

# preserve-fence

Preserve truth without granting implementation continuation privilege.

## Use when

Recover the reason, behavior, contract, evidence, and boundary behind an existing structure before removing or replacing it. Use for rewrites, migrations, deletions, architecture changes, or sunk-cost resets.

## Inputs

- Existing subject and proposed change.
- Observable behavior, callers, contracts, history, tests, and receipts.

## Procedure

1. Identify what the structure currently protects or enables.
2. Separate durable truth from accidental implementation.
3. Identify downstream dependencies and failure consequences.
4. State what evidence would justify removal or replacement.
5. Carry preserved truth into the successor contract.

## Output

A preservation ledger: truth to retain, structure allowed to sink, dependencies, evidence, and falsifier.

## Falsifiers and refusals

- Do not keep structure merely because it exists.
- Do not remove structure merely because it looks obsolete.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
