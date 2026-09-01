---
name: skill-auditor
description: Audit an Agent Skill or skill repository for trigger quality, overlap, authority leakage, unverifiable claims, portability, evidence discipline, replay, and composition quality. Use for reviews, repositories of third-party skills, or release qualification.
---

# skill-auditor

Audit the operational contract, not just prompt prose.

## Use when

Audit an Agent Skill or skill repository for trigger quality, overlap, authority leakage, unverifiable claims, portability, evidence discipline, replay, and composition quality. Use for reviews, repositories of third-party skills, or release qualification.

## Inputs

- Skill files and bundled resources.
- Target harness and tool model.

## Procedure

1. Check metadata routing specificity and collision risk.
2. Check procedure completeness and bounded inputs/outputs.
3. Check authority separation and prohibited ambient DO grants.
4. Check that claims name executable evidence boundaries.
5. Check portability assumptions and hidden dependencies.
6. Check replay/standing semantics.
7. Check overlap and composition opportunities.
8. Manufacture adversarial trigger and behavior cases.

## Output

An audit with observed defects, inferred risks, falsifiers, repair candidates, and standing.

## Falsifiers and refusals

- Inspection alone cannot earn operational ALIVE.
- Unsupported harness features are UNSUPPORTED, not REFUSED.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
