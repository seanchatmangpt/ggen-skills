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
SEMANTIC = ROOT / "manufacturing/ontology/skill-content.ttl"
SKILL_TEMPLATE = ROOT / "manufacturing/templates/verbatim.tera"
GGEN_RELEASE = "v26.8.27"
GGEN_ASSET_SHA256 = "ab442ced90a9836fd4eb07a5d61eb58293843cd515d864699fc0d0453444a035"
ALLOWED_DOCUMENTS = {"AGENTS.md", "README.md"}

class Refusal(RuntimeError):
    pass

def refuse(kind: str, detail: str) -> None:
    raise Refusal(f"REFUSED[{kind}]: {detail}")

def admitted_output(pattern: str) -> None:
    path = Path(pattern.replace("{{ name }}", "skill").replace("{{ path }}", "README.md"))
    if path.is_absolute() or ".." in path.parts:
        refuse("OUTPUT_ESCAPES_ROOT", pattern)
    if pattern.startswith(".github/") or pattern.startswith("tools/") or pattern.startswith("contracts/"):
        refuse("OUTPUT_CROSSES_AUTHORITY_BOUNDARY", pattern)
    if pattern not in {"skills/{{ name }}/SKILL.md", "{{ path }}"}:
        refuse("OUTPUT_PATTERN", pattern)

def snapshot() -> str:
    paths = sorted((ROOT / "skills").glob("*/SKILL.md")) + [ROOT / "AGENTS.md", ROOT / "README.md"]
    if len(paths) < 22:
        refuse("SNAPSHOT_SURFACE", f"expected >=22 artifacts, got {len(paths)}")
    h = hashlib.sha256()
    for path in paths:
        if not path.is_file() or path.is_symlink():
            refuse("SNAPSHOT_ARTIFACT", str(path))
        rel = path.relative_to(ROOT).as_posix()
        data = path.read_bytes()
        h.update(rel.encode()); h.update(b"\0"); h.update(str(len(data)).encode()); h.update(b"\0"); h.update(data); h.update(b"\0")
    return h.hexdigest()

def verify_source() -> None:
    required = ["ggen.toml", "manufacturing/templates/verbatim.tera", "tools/export_skill_content.py", "tools/verify_manufacturing.py", ".github/workflows/verify.yml", "SOURCE.lock.json"]
    for rel in required:
        if not (ROOT / rel).is_file():
            refuse("SOURCE_MISSING", rel)
    manifest = tomllib.loads((ROOT / "ggen.toml").read_text())
    if manifest.get("project", {}).get("name") != "ggen-skills":
        refuse("PROJECT_IDENTITY", str(manifest.get("project")))
    if manifest.get("ontology", {}).get("source") != "manufacturing/ontology/skill-content.ttl":
        refuse("SEMANTIC_SOURCE", str(manifest.get("ontology")))
    rules = manifest.get("generation", {}).get("rules", [])
    if len(rules) != 2:
        refuse("RULE_COUNT", f"expected=2 actual={len(rules)}")
    outputs = {rule.get("output_file", "") for rule in rules}
    if outputs != {"skills/{{ name }}/SKILL.md", "{{ path }}"}:
        refuse("OUTPUT_SET", str(sorted(outputs)))
    for rule in rules:
        admitted_output(rule.get("output_file", ""))
        if rule.get("template", {}).get("file") != "manufacturing/templates/verbatim.tera":
            refuse("TEMPLATE_IDENTITY", str(rule.get("template")))
        if rule.get("mode") != "Overwrite":
            refuse("GENERATION_MODE", str(rule.get("mode")))
    if SKILL_TEMPLATE.read_text() != "{{ content | safe }}":
        refuse("VERBATIM_TEMPLATE", "template must contain exactly the content projection")
    lock = json.loads((ROOT / "SOURCE.lock.json").read_text())
    commit = lock.get("adaptedFrom", {}).get("commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        refuse("SOURCE_COMMIT", str(commit))
    workflow = (ROOT / ".github/workflows/verify.yml").read_text()
    for forbidden in ("contents: write", "pull-requests: write", "packages: write", "id-token: write"):
        if forbidden in workflow:
            refuse("CI_AUTHORITY_EXPANSION", forbidden)
    for required_text in ("contents: read", GGEN_RELEASE, GGEN_ASSET_SHA256, "ggen sync run", "ggen receipt verify", "git diff --exit-code -- skills AGENTS.md README.md"):
        if required_text not in workflow:
            refuse("CI_GATE_MISSING", required_text)

def verify_ontology() -> None:
    if not SEMANTIC.is_file():
        refuse("SEMANTIC_CANDIDATE_MISSING", str(SEMANTIC.relative_to(ROOT)))
    text = SEMANTIC.read_text()
    prefixes = set(re.findall(r"@prefix\s+([A-Za-z0-9_-]+):", text))
    if prefixes != {"prov", "dcterms", "skos"}:
        refuse("PUBLIC_ONTOLOGY_PREFIXES", f"actual={sorted(prefixes)}")
    if "example.org" in text or "@prefix gs:" in text:
        refuse("PRIVATE_VOCABULARY", "semantic candidate must use public ontology vocabulary only")
    skill_count = text.count('dcterms:type "SKILL"')
    if skill_count < 20:
        refuse("SEMANTIC_SKILL_COUNT", str(skill_count))
    if text.count('dcterms:type "PROJECT_DOCUMENT"') != 2:
        refuse("SEMANTIC_DOCUMENT_COUNT", "expected AGENTS.md and README.md")
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        if f'dcterms:identifier "{skill.parent.name}"' not in text:
            refuse("SEMANTIC_SKILL_IDENTITY", skill.parent.name)
    for doc in sorted(ALLOWED_DOCUMENTS):
        if f'dcterms:identifier "{doc}"' not in text:
            refuse("SEMANTIC_DOCUMENT_IDENTITY", doc)

def falsify() -> None:
    cases = ["../skills/{{ name }}/SKILL.md", ".github/workflows/{{ name }}.yml", "tools/{{ name }}.py", "arbitrary/{{ name }}"]
    for case in cases:
        try:
            admitted_output(case)
        except Refusal:
            continue
        refuse("FALSIFIER_FAILED", case)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("source", "ontology", "snapshot", "falsify"))
    args = parser.parse_args()
    try:
        if args.phase == "source":
            verify_source(); print("PARTIAL_ALIVE: manufacturing source/admission contracts verified")
        elif args.phase == "ontology":
            verify_ontology(); print("PARTIAL_ALIVE: exported public-ontology semantic candidate verified")
        elif args.phase == "snapshot":
            print(snapshot())
        else:
            falsify(); print("PARTIAL_ALIVE: manufacturing falsifiers refused as designed")
        return 0
    except Refusal as exc:
        print(str(exc), file=sys.stderr); return 2
    except Exception as exc:
        print(f"BUILD_BROKEN[MANUFACTURING_VERIFIER]: {exc}", file=sys.stderr); return 3

if __name__ == "__main__":
    raise SystemExit(main())
