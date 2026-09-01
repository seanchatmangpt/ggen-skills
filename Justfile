set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

doctor:
    python3 tools/verify.py
    python3 tools/verify_manufacturing.py source
    python3 tools/verify_manufacturing.py falsify
    python3 -m unittest discover -s tests -v

preserve:
    python3 tools/export_skill_content.py --output manufacturing/ontology/skill-content.ttl
    python3 tools/verify_manufacturing.py ontology

chicago: doctor preserve
    before="$(python3 tools/verify_manufacturing.py snapshot)"; \
      ggen sync run; \
      ggen receipt verify --format json; \
      after="$(python3 tools/verify_manufacturing.py snapshot)"; \
      test "$before" = "$after"; \
      git diff --exit-code -- skills AGENTS.md README.md; \
      python3 tools/verify.py; \
      ggen sync run; \
      ggen receipt verify --format json; \
      replay="$(python3 tools/verify_manufacturing.py snapshot)"; \
      test "$after" = "$replay"; \
      git diff --exit-code -- skills AGENTS.md README.md; \
      printf 'PARTIAL_ALIVE: equivalence rail proved %s\n' "$replay"

replay: chicago

dod: chicago
