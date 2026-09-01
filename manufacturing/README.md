# Manufacturing closure

This directory closes the gap between the existing APS-derived skill corpus and a GGen-owned projection model **without discarding behavior before equivalence is observed**.

## Preserve → prove → invert

The transition is deliberately two-stage.

### Stage 1 — equivalence bootstrap

The currently admitted `skills/*/SKILL.md`, `AGENTS.md`, and `README.md` are preserved as predecessor observations. `tools/export_skill_content.py` deterministically projects those bytes plus routing metadata into a public-ontology semantic candidate at `manufacturing/ontology/skill-content.ttl`.

The exact-head Core Team DoD workflow then:

1. binds the candidate SHA;
2. validates the existing skill constitution;
3. exports the semantic candidate;
4. snapshots the preserved projection bytes;
5. installs a checksum-pinned GGen producer;
6. executes `ggen sync run` against that semantic candidate;
7. verifies the GGen receipt;
8. requires `git diff --exit-code -- skills AGENTS.md README.md`;
9. executes GGen a second time;
10. requires byte-identical replay;
11. emits the exported ontology, receipts, snapshots, and exact-subject receipt as workflow artifacts.

A mismatch is `REFUSED[NON_EQUIVALENT_RECONSTITUTION]`, not permission to hand-fix generated files.

### Stage 2 — authority inversion

Only after Stage 1 succeeds may the exact exported ontology artifact be committed and promoted to canonical manufacturing source. At that point normal development edits semantic source and GGen owns the projections. The bootstrap exporter becomes a preservation/equivalence checker rather than the normal source path.

## Authority

The manufacturing rail is read-only with respect to GitHub. It has no push, merge, deployment, credential-brokering, or production `DO` authority. Successful manufacture can establish standing only for the exact subject and exact consequence it observed.
