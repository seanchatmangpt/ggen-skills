---
name: adversarial-requirements
description: Turn credible criticism, objections, threat models, and skeptical reviews into candidate falsifiers before converting them into requirements. Use when pressure-testing architecture, safety, compliance, reliability, or adoption claims.
---

# adversarial-requirements

Treat criticism as unexplored state space.

## Use when

Turn credible criticism, objections, threat models, and skeptical reviews into candidate falsifiers before converting them into requirements. Use when pressure-testing architecture, safety, compliance, reliability, or adoption claims.

## Inputs

- Claim or proposed design.
- Critic loss functions and consequence boundaries.

## Procedure

1. Extract the concrete feared failure state.
2. Construct the cheapest valid falsifier or sabotage case.
3. Execute or specify the evidence boundary needed to observe it.
4. If falsified, derive the narrowest necessary requirement.
5. If not falsified, retain the residual risk without inventing architecture.

## Output

A mapping: objection -> failure state -> falsifier -> evidence -> admitted requirement or bounded residual risk.

## Falsifiers and refusals

- A criticism is not automatically a requirement.
- Absence of a reproduced failure is not universal proof of safety.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
