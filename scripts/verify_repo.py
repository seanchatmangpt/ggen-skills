#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("meta-router", "skill-admission", "evidence-optimizer")
RUNTIMES = ("codex", "claude", "gemini")
EXPECTED_OUTPUTS = {
    *(f"projections/{runtime}/{skill}/SKILL.md" for runtime in RUNTIMES for skill in SKILLS),
    "AGENTS.md",
    "README.md",
    "generated/registry.json",
}
PUBLIC_PREFIXES = {"prov", "dcterms", "skos"}
GGEN_RELEASE = "v26.8.27"
GGEN_ASSET_SHA256 = "ab442ced90a9836fd4eb07a5d61eb58293843cd515d864699fc0d0453444a035"
VOLT_AGENT_SHA = "5e1f3aebcf5de90b5b11fb35a607f95bdddf987e"

class Refusal(RuntimeError):
    pass

def refuse(kind: str, detail: str) -> None:
    raise Refusal(f"REFUSED[{kind}]: {detail}")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def load_toml(path: Path) -> dict:
    try:
        return tomllib.loads(path.read_text())
    except Exception as exc:
        refuse("TOML_INVALID", f"{rel(path)}: {exc}")

def check_output_contract(outputs: set[str]) -> None:
    if outputs != EXPECTED_OUTPUTS:
        missing = sorted(EXPECTED_OUTPUTS - outputs)
        extra = sorted(outputs - EXPECTED_OUTPUTS)
        refuse("OUTPUT_OWNERSHIP_MISMATCH", f"missing={missing} extra={extra}")
    for output in outputs:
        p = Path(output)
        if p.is_absolute() or ".." in p.parts:
            refuse("OUTPUT_ESCAPES_ROOT", output)
        if output.startswith(".github/") or output.startswith("scripts/"):
            refuse("OUTPUT_CROSSES_AUTHORITY_BOUNDARY", output)
        if output in {"ontology.ttl", "ggen.toml", "sources.lock.toml", "BOOTSTRAP.md", "Justfile"}:
            refuse("OUTPUT_OVERWRITES_SOURCE", output)

def check_source() -> None:
    required = ["BOOTSTRAP.md", "ontology.ttl", "ggen.toml", "sources.lock.toml", "Justfile", "scripts/verify_repo.py", "docs/validation/DEFINITION_OF_DONE.json", "templates/skill.md.tera", "templates/agents.md.tera", "templates/readme.md.tera", "templates/registry.json.tera", ".github/workflows/core-team-dod.yml"]
    for item in required:
        if not (ROOT / item).is_file():
            refuse("SOURCE_MISSING", item)
    manifest = load_toml(ROOT / "ggen.toml")
    if manifest.get("project", {}).get("name") != "ggen-skills":
        refuse("PROJECT_IDENTITY", "ggen.toml project.name must be ggen-skills")
    if manifest.get("ontology", {}).get("source") != "ontology.ttl":
        refuse("ONTOLOGY_IDENTITY", "ggen.toml must source ontology.ttl")
    rules = manifest.get("generation", {}).get("rules", [])
    if len(rules) != 12:
        refuse("RULE_COUNT", f"expected=12 actual={len(rules)}")
    outputs = {rule.get("output_file", "") for rule in rules}
    check_output_contract(outputs)
    for rule in rules:
        template = rule.get("template", {}).get("file", "")
        if not template.startswith("templates/") or not (ROOT / template).is_file():
            refuse("TEMPLATE_IDENTITY", f"{rule.get('name')}: {template}")
        if rule.get("mode") != "Overwrite":
            refuse("GENERATION_MODE", f"{rule.get('name')} must be Overwrite")
    ontology = (ROOT / "ontology.ttl").read_text()
    prefixes = set(re.findall(r"@prefix\s+([A-Za-z0-9_-]+):", ontology))
    if prefixes != PUBLIC_PREFIXES:
        refuse("ONTOLOGY_PREFIX_SET", f"expected={sorted(PUBLIC_PREFIXES)} actual={sorted(prefixes)}")
    if ontology.count('dcterms:type "META_SKILL"') != len(SKILLS):
        refuse("SKILL_CARDINALITY", "expected exactly three canonical meta-skills")
    if ontology.count('dcterms:type "RUNTIME"') != len(RUNTIMES):
        refuse("RUNTIME_CARDINALITY", "expected exactly three runtime targets")
    if ontology.count('dcterms:accessRights "SELECT_CONSTRUCT_ONLY"') != len(SKILLS):
        refuse("AMBIENT_AUTHORITY", "every canonical skill must have SELECT_CONSTRUCT_ONLY access rights")
    for skill in SKILLS:
        if f'dcterms:identifier "{skill}"' not in ontology:
            refuse("SKILL_IDENTITY", skill)
    for runtime in RUNTIMES:
        if f'dcterms:identifier "{runtime}"' not in ontology:
            refuse("RUNTIME_IDENTITY", runtime)
    for law in ("Preserve -> Fence -> Calculus -> Exclusions -> Falsifier -> Extension -> Operationalization", "SELECT, CONSTRUCT, and DO are distinct", "zero ambient DO authority"):
        if law not in ontology:
            refuse("DOCTRINE_MISSING", law)
    lock = load_toml(ROOT / "sources.lock.toml")
    if lock.get("ggen", {}).get("release") != GGEN_RELEASE:
        refuse("GGEN_RELEASE_DRIFT", str(lock.get("ggen", {}).get("release")))
    if lock.get("ggen", {}).get("linux_x86_64_asset_sha256") != GGEN_ASSET_SHA256:
        refuse("GGEN_ASSET_DRIFT", str(lock.get("ggen", {}).get("linux_x86_64_asset_sha256")))
    if lock.get("discovery", {}).get("voltagent", {}).get("commit") != VOLT_AGENT_SHA:
        refuse("DISCOVERY_IDENTITY_DRIFT", str(lock.get("discovery", {}).get("voltagent", {}).get("commit")))
    if lock.get("discovery", {}).get("voltagent", {}).get("role") != "observation-corpus-only":
        refuse("CATALOG_AUTHORITY", "VoltAgent catalog must remain observation-only")
    dod = json.loads((ROOT / "docs/validation/DEFINITION_OF_DONE.json").read_text())
    required_alive = set(dod.get("alive_requires", []))
    expected_alive = {"exact_subject_sha", "source_admission", "pinned_ggen_identity", "real_ggen_sync_run", "generated_consequence_verification", "ggen_receipt_verify", "second_sync", "byte_identical_replay", "exact_subject_receipt_binding", "exact_head_ci"}
    if required_alive != expected_alive:
        refuse("DOD_ALIVE_CONTRACT", f"expected={sorted(expected_alive)} actual={sorted(required_alive)}")
    if len(dod.get("gates", [])) < 12:
        refuse("DOD_GATE_COUNT", "expected at least 12 explicit gates")
    skill_template = (ROOT / "templates/skill.md.tera").read_text()
    for token in ("GENERATED by `ggen sync run`", "No ambient DO authority", "results[0].body"):
        if token not in skill_template:
            refuse("SKILL_TEMPLATE_BOUNDARY", token)
    workflow = (ROOT / ".github/workflows/core-team-dod.yml").read_text()
    for forbidden in ("contents: write", "packages: write", "pull-requests: write", "id-token: write"):
        if forbidden in workflow:
            refuse("CI_AUTHORITY_EXPANSION", forbidden)
    for required_text in ("permissions:", "contents: read", GGEN_RELEASE, GGEN_ASSET_SHA256, "ggen sync run", "ggen receipt verify", "verify_repo.py snapshot"):
        if required_text not in workflow:
            refuse("CI_GATE_MISSING", required_text)

def check_projection_text(path: Path, runtime: str, skill: str) -> None:
    text = path.read_text()
    if not text.startswith("---\n"):
        refuse("SKILL_FRONTMATTER", rel(path))
    if f"name: {skill}" not in text:
        refuse("SKILL_NAME", rel(path))
    if f"for the {runtime} runtime" not in text:
        refuse("RUNTIME_PROJECTION", rel(path))
    for token in ("Effect ceiling:", "Authority ceiling: SELECT_CONSTRUCT_ONLY", "No ambient DO authority", "Inspection or installation does not establish `ALIVE`"):
        if token not in text:
            refuse("PROJECTION_BOUNDARY", f"{rel(path)} missing {token}")

def check_registry(doc: dict) -> None:
    rows = doc.get("projections")
    if not isinstance(rows, list):
        refuse("REGISTRY_SHAPE", "projections must be a list")
    pairs = {(row.get("skill"), row.get("runtime")) for row in rows if isinstance(row, dict)}
    expected = {(skill, runtime) for skill in SKILLS for runtime in RUNTIMES}
    if pairs != expected or len(rows) != len(expected):
        refuse("REGISTRY_CARDINALITY", f"expected={len(expected)} actual={len(rows)}")
    for row in rows:
        if row.get("authority") != "SELECT_CONSTRUCT_ONLY":
            refuse("REGISTRY_AUTHORITY", str(row))

def check_generated() -> None:
    for output in sorted(EXPECTED_OUTPUTS):
        if not (ROOT / output).is_file():
            refuse("GENERATED_MISSING", output)
        if (ROOT / output).is_symlink():
            refuse("GENERATED_SYMLINK", output)
    actual_projection_files = {rel(p) for p in (ROOT / "projections").rglob("*") if p.is_file()}
    expected_projection_files = {p for p in EXPECTED_OUTPUTS if p.startswith("projections/")}
    if actual_projection_files != expected_projection_files:
        refuse("PROJECTION_SURFACE_DRIFT", f"missing={sorted(expected_projection_files-actual_projection_files)} extra={sorted(actual_projection_files-expected_projection_files)}")
    for runtime in RUNTIMES:
        for skill in SKILLS:
            check_projection_text(ROOT / f"projections/{runtime}/{skill}/SKILL.md", runtime, skill)
    registry = json.loads((ROOT / "generated/registry.json").read_text())
    check_registry(registry)
    for output in ("AGENTS.md", "README.md"):
        text = (ROOT / output).read_text()
        if "GENERATED by `ggen sync run`" not in text:
            refuse("GENERATED_DOC_OWNERSHIP", output)
    agents = (ROOT / "AGENTS.md").read_text()
    for token in ("SELECT, CONSTRUCT, and DO are distinct", "zero ambient DO authority", "just chicago", "merge only the inspected head when explicitly authorized"):
        if token not in agents:
            refuse("GENERATED_DOCTRINE", token)

def snapshot() -> str:
    missing = [p for p in sorted(EXPECTED_OUTPUTS) if not (ROOT / p).is_file()]
    if missing:
        refuse("SNAPSHOT_MISSING", ",".join(missing))
    h = hashlib.sha256()
    for output in sorted(EXPECTED_OUTPUTS):
        data = (ROOT / output).read_bytes()
        h.update(output.encode()); h.update(b"\0"); h.update(str(len(data)).encode()); h.update(b"\0"); h.update(data); h.update(b"\0")
    return h.hexdigest()

def expect_refused(fn, label: str) -> None:
    try:
        fn()
    except Refusal:
        return
    refuse("FALSIFIER_FAILED", label)

def falsify() -> None:
    expect_refused(lambda: check_output_contract((EXPECTED_OUTPUTS - {"README.md"}) | {"../README.md"}), "root escape")
    expect_refused(lambda: check_output_contract((EXPECTED_OUTPUTS - {"README.md"}) | {".github/workflows/owned.yml"}), "workflow authority crossing")
    bad_projection = ROOT / ".falsifier-skill.tmp"
    bad_projection.write_text("---\nname: meta-router\n---\nno authority boundary\n")
    try:
        expect_refused(lambda: check_projection_text(bad_projection, "codex", "meta-router"), "missing projection authority boundary")
    finally:
        bad_projection.unlink(missing_ok=True)
    bad_registry = {"projections": [{"skill": "meta-router", "runtime": "codex", "authority": "ACTUATE"}]}
    expect_refused(lambda: check_registry(bad_registry), "registry cardinality/authority mutation")

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("source", "generated", "snapshot", "falsify"))
    args = parser.parse_args()
    try:
        if args.phase == "source":
            check_source(); print("PARTIAL_ALIVE: source/admission/ownership contracts verified")
        elif args.phase == "generated":
            check_generated(); print("PARTIAL_ALIVE: generated consequence independently verified")
        elif args.phase == "snapshot":
            print(snapshot())
        elif args.phase == "falsify":
            falsify(); print("PARTIAL_ALIVE: negative fixtures refused as designed")
        return 0
    except Refusal as exc:
        print(str(exc), file=sys.stderr); return 2
    except Exception as exc:
        print(f"BUILD_BROKEN[VERIFIER_EXCEPTION]: {exc}", file=sys.stderr); return 3

if __name__ == "__main__":
    raise SystemExit(main())
