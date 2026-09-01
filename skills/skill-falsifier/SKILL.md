---
name: skill-falsifier
description: Manufacture adversarial examples, counterexamples, sabotage fixtures, and negative trigger cases for a skill or composed workflow. Use when a skill claim needs evidence beyond happy-path examples.
---

# skill-falsifier

Search for the cheapest decisive failure states.

## Use when

Manufacture adversarial examples, counterexamples, sabotage fixtures, and negative trigger cases for a skill or composed workflow. Use when a skill claim needs evidence beyond happy-path examples.

## Inputs

- Claimed behavior and scope.
- Skill contract and available execution harness.

## Procedure

1. Enumerate boundary, ambiguity, stale-state, authority, replay, and consequence failures.
2. Generate positive controls and negative/sabotage fixtures.
3. Execute the narrowest high-information cases first when tooling permits.
4. Classify failure transition rather than merely recording final error.
5. Feed admitted failures back into contract or skill law.

## Output

A falsifier suite and result matrix linked to the exact skill version.

## Falsifiers and refusals

- Do not hard-code tests merely to satisfy current examples.
- A non-reproduced failure remains a candidate, not a proven defect.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
