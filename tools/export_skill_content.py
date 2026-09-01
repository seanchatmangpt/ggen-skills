#!/usr/bin/env python3
"""Deterministically preserve the current admitted projections as public-ontology facts.

This is a one-way preservation bridge used to prove behavioral/byte equivalence before
semantic authority is inverted. It does not grant generated outputs authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ_SECTIONS = (
    "## Use when",
    "## Inputs",
    "## Procedure",
    "## Output",
    "## Falsifiers and refusals",
)

class Refusal(RuntimeError):
    pass

def refuse(kind: str, detail: str) -> None:
    raise Refusal(f"REFUSED[{kind}]: {detail}")

def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        refuse("FRONTMATTER_MISSING", "skill does not start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        refuse("FRONTMATTER_UNTERMINATED", "skill frontmatter is not closed")
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result

def literal(value: str) -> str:
    # JSON string escaping is a valid subset of Turtle string escaping for these UTF-8 inputs.
    return json.dumps(value, ensure_ascii=False)

def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def read_source_lock() -> tuple[str, str]:
    doc = json.loads((ROOT / "SOURCE.lock.json").read_text())
    source = doc.get("adaptedFrom", {})
    repository = source.get("repository")
    commit = source.get("commit")
    if repository != "seanchatmangpt/agile-protocol-specification":
        refuse("SOURCE_REPOSITORY", str(repository))
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        refuse("SOURCE_COMMIT", str(commit))
    return repository, commit

def build_graph() -> tuple[str, int]:
    repository, source_commit = read_source_lock()
    skill_paths = sorted((ROOT / "skills").glob("*/SKILL.md"))
    if len(skill_paths) < 20:
        refuse("SKILL_FRONTIER_TOO_SMALL", f"expected>=20 actual={len(skill_paths)}")

    members: list[str] = []
    records: list[str] = []
    names: set[str] = set()
    source_url = f"https://github.com/{repository}/commit/{source_commit}"

    for path in skill_paths:
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            refuse("SKILL_NOT_UTF8", f"{path}: {exc}")
        fm = frontmatter(text)
        name = fm.get("name", "")
        description = fm.get("description", "")
        if name != path.parent.name or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
            refuse("SKILL_IDENTITY", f"path={path.parent.name} frontmatter={name}")
        if name in names:
            refuse("SKILL_DUPLICATE", name)
        names.add(name)
        if len(description) < 40:
            refuse("SKILL_DESCRIPTION", name)
        missing = [section for section in REQ_SECTIONS if section not in text]
        if missing:
            refuse("SKILL_CONTRACT", f"{name} missing={missing}")
        iri = f"<https://seanchatmangpt.github.io/ggen-skills/skill/{name}>"
        members.append(iri)
        records.append(
            f"{iri}\n"
            "    a prov:Entity ;\n"
            "    dcterms:type \"SKILL\" ;\n"
            f"    dcterms:identifier {literal(name)} ;\n"
            f"    skos:prefLabel {literal(name)} ;\n"
            f"    dcterms:description {literal(description)} ;\n"
            f"    dcterms:abstract {literal(text)} ;\n"
            f"    dcterms:hasVersion {literal(digest(raw))} ;\n"
            "    dcterms:conformsTo <https://agentskills.io/specification> ;\n"
            f"    prov:wasDerivedFrom <{source_url}> .\n"
        )

    for path_name in ("AGENTS.md", "README.md"):
        path = ROOT / path_name
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        iri_name = path_name.lower().replace(".", "-")
        iri = f"<https://seanchatmangpt.github.io/ggen-skills/document/{iri_name}>"
        records.append(
            f"{iri}\n"
            "    a prov:Entity ;\n"
            "    dcterms:type \"PROJECT_DOCUMENT\" ;\n"
            f"    dcterms:identifier {literal(path_name)} ;\n"
            f"    dcterms:abstract {literal(text)} ;\n"
            f"    dcterms:hasVersion {literal(digest(raw))} ;\n"
            f"    prov:wasDerivedFrom <{source_url}> .\n"
        )

    collection = "<https://seanchatmangpt.github.io/ggen-skills/corpus/aps-adaptation>"
    member_lines = " ;\n".join(f"    prov:hadMember {member}" for member in members)
    if member_lines:
        member_lines += " .\n"
    header = (
        "@prefix prov: <http://www.w3.org/ns/prov#> .\n"
        "@prefix dcterms: <http://purl.org/dc/terms/> .\n"
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n"
        f"{collection}\n"
        "    a prov:Collection ;\n"
        "    dcterms:identifier \"ggen-skills-aps-adaptation\" ;\n"
        f"    prov:wasDerivedFrom <{source_url}> ;\n"
    )
    # The final collection predicate is emitted separately so each member is explicit.
    if members:
        collection_block = header + member_lines
    else:
        collection_block = header.rstrip(" ;\n") + " .\n"
    return collection_block + "\n" + "\n".join(records), len(skill_paths)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="manufacturing/ontology/skill-content.ttl")
    args = parser.parse_args()
    try:
        graph, count = build_graph()
        output = (ROOT / args.output).resolve()
        if ROOT != output and ROOT not in output.parents:
            refuse("OUTPUT_ESCAPES_ROOT", str(output))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(graph, encoding="utf-8")
        print(f"PARTIAL_ALIVE: preserved {count} skills plus AGENTS.md/README.md as public-ontology facts")
        return 0
    except Refusal as exc:
        print(str(exc))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
