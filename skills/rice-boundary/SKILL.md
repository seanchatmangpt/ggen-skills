---
name: rice-boundary
description: Apply Rice’s Theorem as an epistemic boundary for nontrivial semantic claims about arbitrary programs. Use when someone proposes universal static inspection, reviewer omniscience, or proof-by-LLM over unrestricted code.
---

# rice-boundary

Move important meaning upstream instead of pretending arbitrary code can always be semantically decided.

## Use when

Apply Rice’s Theorem as an epistemic boundary for nontrivial semantic claims about arbitrary programs. Use when someone proposes universal static inspection, reviewer omniscience, or proof-by-LLM over unrestricted code.

## Inputs

- Semantic claim and program class.
- Restrictions, contracts, generators, and observable consequence boundaries.

## Procedure

1. Determine whether the requested property is a nontrivial semantic property over an unrestricted program class.
2. If so, refuse universal-decision framing.
3. Identify admissible restrictions or upstream semantic contracts.
4. Constrain manufacture to qualified patterns where possible.
5. Observe actual consequence and record bounded standing/residual unknowns.

## Output

A bounded epistemic strategy: decidable restricted checks, runtime falsifiers, or explicit UNKNOWN where universal proof is unavailable.

## Falsifiers and refusals

- Do not use Rice’s Theorem to excuse checks that are decidable under the actual restricted domain.
- Do not convert bounded evidence into universal semantic certainty.

## Composition

This skill may be composed by `aps-protocol`. Preserve explicit handoff state and do not infer authority across skill boundaries.
