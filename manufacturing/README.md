# Manufacturing closure

The repository is intentionally **ggen-first without pretending ggen execution already occurred**.

Current active skills are portable projections adapted from the pinned APS source. The next manufacturing closure is to admit or create a qualified `ggen-skills` pack whose canonical input is `ontology/ggen-skills.ttl`, whose projections are `skills/*/SKILL.md`, and whose verifier proves byte-identical replay.

Until that exact ggen execution is observed and receipted, the ggen-manufacturing dimension remains `PARTIAL_ALIVE`. Do not add an unexecuted `ggen.toml` merely to upgrade appearance.

Promotion acceptance:

```text
pinned ggen binary
+ admitted skill ontology
+ qualified skill pack/templates
-> manufacture skills tree
-> validate skill contracts
-> second manufacture
-> byte-identical comparison
-> receipt
-> exact-head CI
```
