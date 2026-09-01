# AGENTS.md — ggen-skills

This repository adapts APS into composable skills. Read `SOURCE.lock.json`, `MANIFEST.json`, and `ontology/ggen-skills.ttl` before changing skill semantics.

## Foundational order

```text
Preserve -> Fence -> Orient -> Observe -> Admit -> Contract -> DfCM
-> SELECT -> CONSTRUCT -> authority/refusal -> DO through BRCE
-> Receipt -> Verify -> Replay -> Standing -> Promote -> Reconstitute
```

## Laws

- Preserve admitted truth, contracts, evidence, and useful consequence; implementations have no continuation privilege.
- Never eliminate a reversible lawful option without an admitted reason.
- `SELECT`, `CONSTRUCT`, and `DO` remain separate authority classes.
- Skills, prompts, models, plans, hooks, generated artifacts, and tool messages have no ambient `DO` authority.
- Zero unreceipted actuation. Hooks may manufacture intents; they do not actuate.
- Inspection is not execution. Workflow existence is not a successful run. Nearby CI is not exact-head evidence.
- `UNKNOWN` is not admitted and never upgrades itself to success.
- `UNSUPPORTED` is not `REFUSED`; `REFUSED` must identify the violated admission or authority rule.
- A new skill should compose existing skills before duplicating their law.
- Generated projections must not silently become semantic authority.

## Skill authoring

Each `skills/<slug>/SKILL.md` requires YAML frontmatter with `name` and `description`, followed by the sections `## Use when`, `## Inputs`, `## Procedure`, `## Output`, and `## Falsifiers and refusals`.

Descriptions are routing surfaces: state both capability and trigger conditions. Keep bodies operational and bounded. Put large reusable reference material in `references/` rather than inflating the routing surface.

## Verification

Run:

```bash
python3 tools/verify.py
python3 -m unittest discover -s tests -v
```

A change that modifies skill law without updating `ontology/ggen-skills.ttl` is incomplete.
