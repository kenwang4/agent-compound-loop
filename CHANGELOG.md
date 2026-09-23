# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CLI `--version` reports package `__version__` (packaging verification).

### Fixed

- TTL auto-expire `review_evidence` now points at `writeback_candidate/cli.py:ttl` (was a stale module path).
- Reject Windows drive-letter and UNC absolute path refs in `_safe_ref`.
- Also reject Linux `/home/...` absolute path refs in `_safe_ref`.
- Default CLI `--destination` now points at existing `docs/02-writeback-protocol.md` (removed missing `docs/DECISIONS.md`).
- Keep `VERSION` / `pyproject.toml` / package `__version__` aligned via pytest.

### Tests

- Cover overdue candidate expiry on inbox touch.
- Cover privacy heuristic rejection of email addresses in candidate text.

### Changed

- `pyproject.toml` uses SPDX `license = "MIT"` + `license-files` (drops deprecated License classifier) for cleaner PyPI metadata.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) still pending: maintainer token needs `workflow` scope (`gh auth refresh -s workflow`).

## [0.1.0] - 2026-09-16

### Added

- Initial public release under maintainer brand **Aichill** (brand Aichill).
- Docs: recursive compound loop, writeback protocol, operating model, minigame quality gates.
- JSON Schemas for writeback candidates and task envelopes.
- Python package `writeback_candidate` with CLI entry point `writeback-candidate`
  (also `python -m writeback_candidate` and `scripts/writeback_candidate.py` shim).
- Bounded durable candidate inbox (`writeback_candidates/`) with privacy path heuristics.
- Drop-in agent skills under `skills/`.
- Pytest suite (`tests/`) covering schema load, absolute-path rejection, happy-path create.
- Local pytest suite runnable via `pip install -e ".[dev]" && pytest -q`.
- MIT license, SECURITY, CONTRIBUTING, CHANGELOG.

### Planned (tracked in issues)

- CI: pytest on push/PR (Python 3.11+)
- Optional PyPI publish once CI is green and a maintainer PyPI token exists

## Verify locally

```bash
pip install -e ".[dev]"
pytest -q
```
