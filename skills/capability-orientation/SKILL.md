---
name: capability-orientation
description: Orient a repository or execution environment before planning changes. Use when tool availability, permissions, mounts, checkouts, runtimes, network, CI, or connector capabilities materially affect what can be proven or changed.
---

# capability-orientation

Establish the real topology before choosing a path.

## Use when

Orient a repository or execution environment before planning changes. Use when tool availability, permissions, mounts, checkouts, runtimes, network, CI, or connector capabilities materially affect what can be proven or changed.

## Inputs

- Subject repository or environment.
- Requested outcome and acceptance boundary.

## Procedure

1. Inventory source transports and exact refs.
2. Inventory local tree/mount state separately from connector visibility.
3. Inventory mutation authority separately from read authority.
4. Inventory runtimes, compilers, package managers, test runners, containers, and network.
5. Inventory local and hosted verification paths.
6. Record typed failures without collapsing the graph.
7. Pass the surviving capability frontier to DfCM.

## Output

A capability matrix with AVAILABLE, BLOCKED, UNSUPPORTED, and UNKNOWN edges plus evidence for each.

## Falsifiers and refusals

- A connector object is not a mounted tree.
- A workflow definition is not a successful run.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
