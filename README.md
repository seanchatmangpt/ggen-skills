# ggen-skills

A DfCM-maximal skill system adapted from the Agile Protocol Specification (APS).

Source authority is pinned to `seanchatmangpt/agile-protocol-specification@b5916330905195b124409ca0e857f43b897ffc80`. The target is not a prose copy of APS. It reconstitutes APS as composable Agent Skills with explicit admission, selection, construction, actuation, evidence, replay, standing, and promotion boundaries.

## Core law

```text
A = mu(O*)
```

```text
orient -> preserve -> observe -> admit -> contract -> DfCM -> SELECT -> CONSTRUCT
       -> authority/refusal -> DO through BRCE -> receipt -> verify -> replay -> standing
       -> promote reusable knowledge -> reconstitute
```

`SELECT`, `CONSTRUCT`, and `DO` are separate authority classes. A skill may plan or construct without receiving ambient actuation authority.

## Skill graph

### Protocol kernel

- `aps-protocol` — full APS state machine and standing discipline.
- `capability-orientation` — inventory tools, authority, runtime, mounts, network, and evidence surfaces.
- `preserve-fence` — recover useful truth and constraints before removal or replacement.
- `source-admission` — pin source identity and classify admitted vs inferred knowledge.
- `observe-admit` — turn partial observations into bounded `O*`.
- `contract-first` — define subjects, invariants, authority, evidence, and falsifiers before mechanism.
- `dfcm` — maximize the reversible lawful candidate frontier.
- `adversarial-requirements` — convert objections into falsifiers before requirements.

### Manufacture and actuation

- `ggen-first` — prefer known manufacturing knowledge and generated tool invocation.
- `select-construct-do` — prevent authority collapse across planning, artifact construction, and actuation.
- `brce-boundary` — admit/refuse DO and require a receipt for consequence.
- `evidence-receipts` — bind subject, authority, execution, consequence, and verifier evidence.
- `exact-head-verification` — validate the exact candidate identity rather than nearby state.
- `replay-standing` — replay evidence and assign bounded standing.
- `reconstitution` — sunset implementation privilege while preserving admitted truth.

### Epistemics, maturity, and governance

- `rice-boundary` — refuse universal semantic claims over arbitrary programs and move meaning upstream.
- `jig-maturity` — assess five maturity levels across seven independent dimensions.
- `process-intelligence` — model consequential work as object-centric process evidence.
- `governance-compression` — govern bounded source classes rather than manually reviewing every projection.

### Meta-skills

- `skill-creator-dfcm` — create a new skill while maximizing reversible design choices.
- `skill-composer` — compose atomic skills into lawful workflows without merging authority classes.
- `skill-auditor` — audit skill trigger, law, authority, evidence, replay, and portability.
- `skill-falsifier` — manufacture counterexamples and sabotage cases for a skill claim.
- `skill-qualifier` — execute the narrowest real verifier and assign standing.
- `skill-promoter` — turn qualified novelty into reusable manufacturing knowledge.

## Compatibility

Every skill uses the portable `skills/<name>/SKILL.md` layout with YAML frontmatter containing at least `name` and `description`. Bundled resources can be added below each skill without changing the top-level graph.

## Verification

```bash
python3 tools/verify.py
python3 -m unittest discover -s tests -v
```

The verifier checks frontmatter, unique skill identities, required constitutional sections, source pin integrity, ontology coverage, and absence of ambient `DO` grants.

## Standing

This repository can earn `ALIVE` for **skill-repository structural and constitutional conformance** when the exact target head executes the verifier successfully. The ggen projection/manufacturing closure remains `PARTIAL_ALIVE` until a qualified ggen skill pack is executed against this exact ontology and proves deterministic replay. No file in this repository grants production actuation authority.
