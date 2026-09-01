set shell := ["bash", "-euo", "pipefail", "-c"]

default:
    @just --list

doctor:
    python3 scripts/verify_repo.py source

falsify:
    python3 scripts/verify_repo.py falsify

chicago:
    python3 scripts/verify_repo.py source
    ggen sync run
    ggen receipt verify --format json
    python3 scripts/verify_repo.py generated
    before="$(python3 scripts/verify_repo.py snapshot)"; \
      ggen sync run; \
      ggen receipt verify --format json; \
      after="$(python3 scripts/verify_repo.py snapshot)"; \
      test "$before" = "$after"; \
      printf 'ALIVE_CANDIDATE: deterministic replay %s\n' "$after"
    python3 scripts/verify_repo.py generated

replay: chicago

dod: doctor falsify chicago
