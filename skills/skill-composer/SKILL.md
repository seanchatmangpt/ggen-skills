---
name: skill-composer
description: Compose multiple Agent Skills into a workflow while preserving each skill’s contract and authority boundary. Use when a task spans admission, planning, manufacture, verification, or governance capabilities.
---

# skill-composer

Compose morphisms without collapsing semantic or authority distinctions.

## Use when

Compose multiple Agent Skills into a workflow while preserving each skill’s contract and authority boundary. Use when a task spans admission, planning, manufacture, verification, or governance capabilities.

## Inputs

- Ordered or partially ordered skill candidates.
- Shared subject identity and cross-skill contracts.

## Procedure

1. Identify required state transitions.
2. Select the narrowest skills for each transition.
3. Define handoff artifacts and invariants.
4. Keep SELECT, CONSTRUCT, and DO skills separated.
5. Define failure routing and which reversible alternatives remain.
6. Define the final receipt/standing aggregator.

## Output

A composition DAG with skill nodes, handoff contracts, authority edges, failure routes, and terminal standing.

## Falsifiers and refusals

- Do not merge skills merely to reduce file count.
- A failed edge should reroute when lawful alternatives remain.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
