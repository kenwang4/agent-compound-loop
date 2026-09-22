# PyPI release draft — agent-compound-loop 0.1.0

Status: **draft only**. Do not upload until maintainer authorizes a PyPI account/token.

## Intended package

- Name: `agent-compound-loop`
- Version: `0.1.0` — keep root `VERSION` identical to `pyproject.toml` `[project].version`
- Install (after publish): `pip install agent-compound-loop`
- Entry point: `writeback-candidate`

## Build locally (verified path)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip build
pip install -e ".[dev]"
pytest -q
python -m build
# artifacts under dist/: *.whl and *.tar.gz
```

## Twine upload (blocked until authorized)

```bash
# NOT run in automation without explicit authorization
# twine upload dist/*
```

## Checklist before first upload

- [ ] CI workflow green on `main` (GitHub token needs `workflow` scope to land `.github/workflows/ci.yml`)
- [ ] `VERSION` matches tag and `pyproject.toml`
- [ ] Changelog `[0.1.0]` section accurate
- [ ] No private identity strings in package metadata or packaged files
- [x] `pyproject.toml` SPDX `license = "MIT"` (no deprecated License classifier)
- [ ] PyPI project name available / owned by maintainer brand **Aichill**

Issue tracker: https://github.com/kenwang4/agent-compound-loop/issues/3
