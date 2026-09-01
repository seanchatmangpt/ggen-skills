#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from rdflib import Graph, Namespace, RDF

GSK = Namespace("https://w3id.org/chatman/ggen-skills#")
REQUIRED = (
    "skillName", "title", "description", "whenToUse", "law", "procedure",
    "authorityClass", "authorityBoundary", "evidence", "falsifiers",
    "composition", "standingRule", "sourceCoordinate", "sourcePath",
)
SECTIONS = (
    "## When to use", "## Law", "## Procedure", "## Authority boundary",
    "## Evidence", "## Falsifiers", "## Composition", "## Standing", "## Source",
)
ALLOWED_AUTHORITY = {"SELECT", "CONSTRUCT", "VERIFY", "GOVERN"}


def git_blob_sha(path: Path) -> str:
    body = path.read_bytes()
    header = f"blob {len(body)}\0".encode()
    return hashlib.sha1(header + body).hexdigest()


def one(graph: Graph, subject, predicate, errors: list[str]) -> str:
    values = list(graph.objects(subject, predicate))
    if len(values) != 1:
        errors.append(f"{subject}: expected exactly one {predicate}, got {len(values)}")
        return ""
    return str(values[0])


def validate_repo(root: Path) -> list[str]:
    errors: list[str] = []
    lock = json.loads((root / "SOURCE.lock.json").read_text())
    source = lock["source"]
    source_coordinate = f'{source["repository"]}@{source["commit"]}'

    readme = (root / "README.md").read_text()
    if source_coordinate not in readme:
        errors.append("README source authority pin does not match SOURCE.lock.json")

    aps_core = root / "ontology" / "aps-core.ttl"
    expected_core_blob = source["blobs"]["ontology/aps-core.ttl"]
    if git_blob_sha(aps_core) != expected_core_blob:
        errors.append("ontology/aps-core.ttl is not byte-identical to the admitted APS blob")

    graph = Graph()
    try:
        graph.parse(root / "ontology" / "skills.ttl", format="turtle")
        graph.parse(aps_core, format="turtle")
        for rel in (
            "skills-protocol-kernel.ttl",
            "skills-manufacture-actuation.ttl",
            "skills-epistemics-governance.ttl",
            "skills-meta.ttl",
        ):
            graph.parse(root / "ontology" / rel, format="turtle")
    except Exception as exc:
        return errors + [f"ontology parse failed: {exc}"]

    subjects = sorted(set(graph.subjects(RDF.type, GSK.Skill)), key=str)
    if len(subjects) != 25:
        errors.append(f"expected 25 gsk:Skill entities, got {len(subjects)}")

    rows: dict[str, dict[str, str]] = {}
    for subject in subjects:
        row = {}
        for name in REQUIRED:
            row[name] = one(graph, subject, GSK[name], errors)
        skill_name = row["skillName"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name):
            errors.append(f"{subject}: invalid portable skill name {skill_name!r}")
        if skill_name in rows:
            errors.append(f"duplicate skillName {skill_name}")
        rows[skill_name] = row

        if row["authorityClass"] not in ALLOWED_AUTHORITY:
            errors.append(
                f"{skill_name}: authorityClass {row['authorityClass']!r} is not one of "
                f"{sorted(ALLOWED_AUTHORITY)}"
            )
        if row["sourceCoordinate"] != source_coordinate:
            errors.append(f"{skill_name}: source coordinate drift")
        if row["standingRule"].strip() == "":
            errors.append(f"{skill_name}: empty standing rule")

    skills_root = root / "skills"
    disk_names = (
        sorted(p.name for p in skills_root.iterdir() if p.is_dir())
        if skills_root.exists()
        else []
    )
    if disk_names != sorted(rows):
        errors.append(
            f"generated skill directory set differs from ontology: disk={disk_names}, "
            f"ontology={sorted(rows)}"
        )

    for skill_name, row in sorted(rows.items()):
        path = skills_root / skill_name / "SKILL.md"
        if not path.exists():
            errors.append(f"{skill_name}: missing generated SKILL.md")
            continue
        text = path.read_text()
        if not text.startswith("---\n"):
            errors.append(f"{skill_name}: missing YAML frontmatter")
        front_parts = text.split("---", 2)
        if len(front_parts) < 3:
            errors.append(f"{skill_name}: malformed YAML frontmatter")
        else:
            front = front_parts[1]
            if f"name: {skill_name}\n" not in front:
                errors.append(f"{skill_name}: frontmatter name drift")
            if f"description: {row['description']}\n" not in front:
                errors.append(f"{skill_name}: frontmatter description drift")

        if f"# {row['title']}\n" not in text:
            errors.append(f"{skill_name}: title drift")
        for section in SECTIONS:
            if section not in text:
                errors.append(f"{skill_name}: missing section {section}")
        expected_authority = f"Authority class: `{row['authorityClass']}`"
        if expected_authority not in text:
            errors.append(f"{skill_name}: authority projection drift")
        for field in (
            "whenToUse", "law", "procedure", "authorityBoundary", "evidence",
            "falsifiers", "composition", "standingRule",
        ):
            if row[field] not in text:
                errors.append(f"{skill_name}: projection omitted ontology field {field}")
        source_line = f"Adapted from `{row['sourceCoordinate']}` at `{row['sourcePath']}`."
        if source_line not in text:
            errors.append(f"{skill_name}: source projection drift")
        if "This file is a GGen projection." not in text:
            errors.append(f"{skill_name}: generated-surface warning missing")
        if re.search(r"Authority class:\s*`DO`", text):
            errors.append(f"{skill_name}: ambient DO authority projected")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    errors = validate_repo(root)
    result = {
        "schema": "ggen-skills.verification.v1",
        "root": str(root),
        "status": "ALIVE" if not errors else "BUILD_BROKEN",
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
