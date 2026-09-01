# v26.9.1 Jira Plan — ggen-skills

## Define

This repository (`ggen-skills`) manufactures a set of Claude-facing skill definitions
and their supporting ontology/tooling under a DfCM (Design for Combinatorial
Maximalism) and APS (Admissible Possibility Space) discipline. As of 2026-08-31, three
concurrent workstreams exist as branches, plus a direct merge to `main`:

- `adapt/aps-dfcm-max` — an APS-kernel-plus-DfCM-admission-frontier build of the
  skills tree (authority/receipts/verifier surfaces, manufacturing proof against
  ggen equivalence). This branch has already been merged into `main` via PR #4.
- `feat/aps-skill-factory-v26-9-1` — a competing/parallel skill-factory approach:
  builds an `aps-core.ttl` ontology family (epistemics-governance,
  manufacture-actuation, meta, protocol-kernel) plus SPARQL gates
  (`gates/010_required_skill_contract.rq` etc.), a `templates/skill.tera` generator
  template, and a Python verifier (`tools/verify.py`) with CI wiring
  (`fix(ci): export pinned ggen coordinate before resolution`).
- `feat/core-team-dod-dfcm` — a "Definition of Done" governance workstream:
  `docs/validation/DEFINITION_OF_DONE.json`, a `scripts/verify_repo.py` checker, a
  `core-team-dod.yml` CI workflow, and Tera templates for `agents.md`, `readme.md`,
  and a `registry.json` — oriented toward standardizing repo compliance/reporting
  rather than skill content itself.

The v26.9.1 charter is: reconcile these three admissible candidates into one
mergeable skills tree, without collapsing any workstream's real content — the
manufacturing frontier (`adapt/aps-dfcm-max`, already in `main`), the ontology-driven
skill factory (`feat/aps-skill-factory-v26-9-1`), and the compliance/DoD tooling
(`feat/core-team-dod-dfcm`) are complementary artifacts, not competing
implementations of the same job.

## Measure

Real branch state as of `git log`/`git branch -a` against
`https://github.com/seanchatmangpt/ggen-skills.git`, since 2026-08-31 (all commits
below fall on that single date):

### `main` (HEAD, default branch)

- `ce8353f` 2026-08-31 23:01:16 -0700 — Merge PR #4: adapt APS into DfCM-maximal ggen
  skills
- `61731d5` 2026-08-31 22:59:19 -0700 — chore: preserve exact DfCM candidate tree
- `db1f71e` 2026-08-31 22:58:43 -0700 — docs: refresh README after DfCM qualification
- `debe0cd` 2026-08-31 22:15:20 -0700 — fix: remove nondeterministic no-op inference
- `189881f` 2026-08-31 22:14:30 -0700 — manufacturing: prove GGen equivalence before
  authority inversion
- `a0c6f92` 2026-08-31 22:07:42 -0700 — skills: add DfCM meta-skill lifecycle
- `405a8ed` 2026-08-31 22:07:15 -0700 — skills: add manufacture, authority, evidence,
  and governance skills
- `2830a1a` 2026-08-31 22:06:34 -0700 — skills: add APS kernel and DfCM admission
  frontier
- `53b2985` 2026-08-31 22:05:40 -0700 — foundation: add APS authority, receipts, and
  verifier surfaces
- `f0b23ce` 2026-08-31 22:04:48 -0700 — bootstrap: initialize ggen-skills authority
  surface
- `2dfca01` 2026-08-31 22:03:40 -0700 — chore: establish empty-repo bootstrap fence

### `adapt/aps-dfcm-max`

Identical HEAD to `main` (`61731d5` is the pre-merge-commit tip, folded into `main`
at `ce8353f`). `git rev-parse` confirms `adapt/aps-dfcm-max` = `61731d5...`, already
fully merged — this branch is DONE, no further action needed except cleanup.

### `feat/aps-skill-factory-v26-9-1`

Diverges from the shared root at `f0b23ce`/`2dfca01`; not merged into `main`.

- `dd22dba` 2026-08-31 22:20:54 -0700 — fix(ci): export pinned ggen coordinate before
  resolution
- `02d1cdf` 2026-08-31 22:19:30 -0700 — feat(factory): manufacture and qualify APS
  skills with ggen
- `9d26a6c` 2026-08-31 22:18:33 -0700 — feat(ontology): admit APS skill contract graph
- `f0b23ce` 2026-08-31 22:04:48 -0700 — bootstrap: initialize ggen-skills authority
  surface (shared with main)
- `2dfca01` 2026-08-31 22:03:40 -0700 — chore: establish empty-repo bootstrap fence
  (shared with main)

Top-level tree: `ontology/aps-core.ttl`, `ontology/skills-epistemics-governance.ttl`,
`ontology/skills-manufacture-actuation.ttl`, `ontology/skills-meta.ttl`,
`ontology/skills-protocol-kernel.ttl`, `ontology/skills.ttl`, `gates/*.rq` (4 SPARQL
gate files), `templates/skill.tera`, `tools/verify.py`,
`tools/requirements-ci.txt`, `tests/test_repository.py`.

### `feat/core-team-dod-dfcm`

Diverges from the shared root at `2dfca01`; not merged into `main`.

- `5884165` 2026-08-31 22:09:20 -0700 — feat: manufacture governed meta-skill
  bootstrap
- `2dfca01` 2026-08-31 22:03:40 -0700 — chore: establish empty-repo bootstrap fence
  (shared with main)

Top-level tree: `docs/validation/DEFINITION_OF_DONE.json`,
`scripts/verify_repo.py`, `.github/workflows/core-team-dod.yml`, `ontology.ttl`,
`sources.lock.toml`, `templates/agents.md.tera`, `templates/readme.md.tera`,
`templates/registry.json.tera`.

## Explore

Options implied by the three branch shapes, given `adapt/aps-dfcm-max` is already
in `main`:

1. **Sequential rebase-and-merge** — rebase `feat/aps-skill-factory-v26-9-1` onto
   current `main`, resolve any ontology/path collisions (both trees use
   `ontology/` and `ggen.toml`), then rebase `feat/core-team-dod-dfcm` on top.
   Lowest branch count, but risks silently overwriting `main`'s
   `ontology/ggen-skills.ttl` with the factory branch's `ontology/skills*.ttl` if
   paths collide without a rename plan.
2. **Namespace-separated merge** — merge each branch's ontology/tooling into
   distinct subdirectories (e.g. `factory/` for the skill-factory branch's
   ontology+gates+templates, `governance/` for the DoD branch's DoD tooling),
   preserving `main`'s existing `ontology/ggen-skills.ttl` and `skills/*/SKILL.md`
   untouched. Highest content-preservation, more directory reshuffling.
3. **DoD-as-CI-only merge** — merge only `feat/core-team-dod-dfcm`'s CI workflow and
   verification script as a repo-wide compliance gate (applied to the already-merged
   `main` tree), treating its Tera templates and ontology as a parked/reference
   alternative rather than wholesale-adopted, since `main` already has its own
   `manufacturing/templates/verbatim.tera` and `skills:` layout.
4. **Park the skill-factory branch** — if `feat/aps-skill-factory-v26-9-1`'s
   `ontology/skills.ttl` family is judged a genuine competing design to `main`'s
   `ontology/ggen-skills.ttl` (rather than a complement), keep it unmerged as a
   documented alternative-design branch and record the non-dominated comparison in
   this document rather than forcing a merge.

No option is selected here; Develop below prepares each branch for a mergeability
decision rather than presupposing option 1.

## Develop

Concrete next engineering steps, per branch:

### `adapt/aps-dfcm-max` (already merged)

- No further development needed on this branch. Delete the remote branch ref after
  confirming no other work depends on it (`git push origin --delete
  adapt/aps-dfcm-max`), since `main` already contains its exact tree
  (`61731d5` == branch tip, folded via merge commit `ce8353f`).

### `feat/aps-skill-factory-v26-9-1`

1. Rebase onto current `main` (`git rebase origin/main`) to surface any path
   collisions against `main`'s `ontology/ggen-skills.ttl`, `ggen.toml`, and
   `.github/workflows/verify.yml` (both branches touch this workflow file
   independently — diff required, not a blind overwrite).
2. Run `tools/verify.py` and `tests/test_repository.py` against the rebased tree to
   confirm the SPARQL gates (`gates/010_required_skill_contract.rq` through
   `gates/040_source_coordinate.rq`) still pass against `main`'s existing
   `skills/*/SKILL.md` files, since those gates were authored against this branch's
   own tree, not `main`'s merged tree.
3. Resolve the CI export fix (`dd22dba`, "export pinned ggen coordinate before
   resolution") against `main`'s own `SOURCE.lock.json`/`ggen.toml` pinning scheme —
   confirm both branches pin the same ggen coordinate or reconcile the divergence
   explicitly.
4. Decide the namespace question from Explore option 2 vs 4 before opening any
   merge: either relocate `ontology/skills*.ttl` to avoid colliding with `main`'s
   `ontology/ggen-skills.ttl`, or keep this branch parked as a documented
   alternative.

### `feat/core-team-dod-dfcm`

1. Rebase onto current `main` (`git rebase origin/main`).
2. Run `scripts/verify_repo.py` against `main`'s merged tree to check whether the
   Definition-of-Done checks in `docs/validation/DEFINITION_OF_DONE.json` already
   pass, partially pass, or need new checks added for the DfCM/APS skills that
   landed via PR #4.
3. Confirm `.github/workflows/core-team-dod.yml` does not conflict with `main`'s
   existing `.github/workflows/verify.yml` — either merge them into one workflow
   file with distinct jobs, or keep both as separate workflow files if their
   triggers/scopes are disjoint.
4. Evaluate whether `templates/agents.md.tera`, `templates/readme.md.tera`, and
   `templates/registry.json.tera` duplicate or should replace `main`'s
   `manufacturing/templates/verbatim.tera` and `README.md`/`AGENTS.md` — this is a
   template-ownership decision, not an automatic merge.

## Implement

### Merge order

1. `adapt/aps-dfcm-max` — already merged; only remaining action is branch cleanup
   (delete stale ref), not a merge.
2. `feat/core-team-dod-dfcm` — smallest diff (one commit beyond the shared root),
   lowest collision surface; merge first once its DoD checks are confirmed to pass
   against `main`'s post-PR#4 tree.
3. `feat/aps-skill-factory-v26-9-1` — largest diff (3 commits, full ontology/gates/
   template/tooling family); merge last, after the namespace decision from Explore
   is made explicit in a follow-up commit on that branch itself (not resolved
   silently during the merge).

### Verification/test gates

- Each branch's own verifier must pass against its own rebased tree before merge:
  `tools/verify.py` + `pytest tests/test_repository.py` for the skill-factory
  branch; `scripts/verify_repo.py` for the DoD branch.
- After each merge to `main`, re-run `main`'s existing
  `.github/workflows/verify.yml` checks locally (or via `gh workflow run`) before
  merging the next branch in the sequence — one gate closed and re-verified before
  advancing, per the staged-rollout discipline this plan follows.
- No branch merge proceeds if it silently overwrites another branch's already-merged
  file without an explicit diff review (particularly `ggen.toml`,
  `.github/workflows/verify.yml`, and any `ontology/*.ttl` path collision).

### Rollout / monitoring

- After both remaining branches are merged, tag the resulting `main` HEAD as the
  v26.9.1 skills-tree baseline and record its SHA in this document's revision
  history (append, do not overwrite the Measure section above).
- Add a standing check (a scheduled CI run or a periodic `run-ggen`/`mcp-doctor`
  pass) that re-verifies `tools/verify.py`, `scripts/verify_repo.py`, and `main`'s
  existing `verify.yml` all pass together post-merge, catching regression rather
  than assuming the one-time merge holds forever.
- Delete `adapt/aps-dfcm-max` from `origin` once cleanup is confirmed safe, to keep
  the branch list reflecting only live work.

## See Also

- `README.md` — repo-level overview, refreshed post-DfCM-qualification at `db1f71e`
- `BOOTSTRAP.md` — present on every branch; shared bootstrap contract
- `AGENTS.md` — present on `main`; agent-facing operating instructions

Last Updated: 2026-09-01
