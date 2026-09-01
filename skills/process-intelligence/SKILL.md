---
name: process-intelligence
description: Model consequential work as object-centric process evidence for conformance, variants, bottlenecks, rework, authority exceptions, failure propagation, economics, and process fitness. Use when artifact correctness alone is insufficient.
---

# process-intelligence

Make the execution process itself observable and comparable.

## Use when

Model consequential work as object-centric process evidence for conformance, variants, bottlenecks, rework, authority exceptions, failure propagation, economics, and process fitness. Use when artifact correctness alone is insufficient.

## Inputs

- Objects, events, actors/authorities, timestamps, outcomes, and receipts.

## Procedure

1. Identify stable process objects and lifecycle events.
2. Link events to objects and authority/receipt evidence.
3. Preserve variants rather than forcing one happy path.
4. Measure rework, wait, failure propagation, exceptions, and consequence quality.
5. Test process fitness separately from artifact conformance.

## Output

An object-centric event model and process-fitness findings linked to receipts.

## Falsifiers and refusals

- A perfectly conformant unsafe process is still unsafe.
- Do not infer event execution from planned workflow structure.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
