# agent-compound-loop

**Recursive compound engineering for multi-host AI agents** — plus production quality gates for casual merge minigames.

Maintainer brand: **Aichill** · License: [MIT](LICENSE) · Version: **0.1.0**

---

## What

This repository packages two battle-tested practices as **portable, host-agnostic docs + schemas + a small Python helper**:

1. **Recursive compound loop** — after each real task, preserve only what changes future action (writeback), so the next session starts shorter and more reliable.
2. **Casual merge minigame production gates** — G1→G2→G3 style gates that separate *automation green* from *human-fun*, for mobile mini-game / browser merge games and similar casual titles.

It is **not** a platform, daemon, or memory mesh. Files and checklists only.

## Why

AI sessions forget. Teams then either (a) dump everything into prompts, or (b) invent orchestration theater. Both fail.

The compound loop says: **verify → candidate → independent check → smallest durable write**. Fast lane stays session-local; durable lane never auto-mutates canonical docs.

Minigame gates say: **automation PASS ≠ ship**. A five-minute blind human playtest is the release gate that protects fun.

## Install

Requires **Python 3.11+**. From a clone of this repo:

```bash
# editable install (exposes `writeback-candidate` on PATH)
pip install -e .

# with test tools
pip install -e ".[dev]"
# or:
pip install -r requirements-dev.txt
```

## Run

```bash
# help
writeback-candidate --help
# equivalent:
python -m writeback_candidate --help
python3 scripts/writeback_candidate.py --help

# fast lane (session-only, no durable file)
writeback-candidate create \
  --lane fast \
  --claim "Local fix only for this session"

# durable candidate (writes under writeback_candidates/)
writeback-candidate create \
  --lane durable \
  --claim "All delayed game feedback must cancel inside cleanup on every exit path" \
  --source "examples/fake-test-log.txt" \
  --destination "docs/04-minigame-gates.md" \
  --owner maintainer \
  --scope "casual-merge-minigame" \
  --review-on "after-next-human-playtest" \
  --task-id "demo-task-001"

# list / review
writeback-candidate list
writeback-candidate review \
  --candidate-id <id-from-create> \
  --verdict accepted \
  --reviewer "fresh-context-reviewer" \
  --evidence "examples/fake-review-notes.md"
```

Absolute machine paths (e.g. `/Users/...`, `~/...`) are **rejected** by design.

## Test

```bash
pytest -q
```

## Continuous integration

GitHub Actions should run `pytest` on every push and pull request to `main`
(`.github/workflows/ci.yml`: Python 3.11/3.12, `pip install -e ".[dev]"`).

If the workflow file is missing from `main`, the push was blocked by missing
OAuth `workflow` scope on the maintainer token. Refresh once, then push the
local workflow file:

```bash
gh auth refresh -h github.com -s workflow
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI workflow for pytest on main"
git push origin main
```

Until then, run tests locally:

```bash
pip install -e ".[dev]"
pytest -q
```

CI runs the same suite on Ubuntu with Python 3.11+ (see `.github/workflows/ci.yml`).

## How (quick start)

```text
Identify intent → load minimal context → one primary action → local verify
→ decide if a new pattern exists → writeback to the correct layer
→ next round needs one fewer step
```

1. Read [`docs/01-recursive-evolution.md`](docs/01-recursive-evolution.md)
2. Read [`docs/02-writeback-protocol.md`](docs/02-writeback-protocol.md)
3. Validate candidates with the CLI above
4. For game work, run [`docs/04-minigame-gates.md`](docs/04-minigame-gates.md) + [`skills/game-quality-gates/`](skills/game-quality-gates/)

See a fake worked example: [`examples/compound_loop_demo.md`](examples/compound_loop_demo.md)

## Repo map

| Path | Role |
|------|------|
| `docs/` | Protocols (evolution, writeback, operating model, minigame gates) |
| `schemas/` | JSON Schema for writeback candidates and task envelopes |
| `writeback_candidate/` | Python package + CLI (`writeback-candidate`) |
| `scripts/writeback_candidate.py` | Thin shim for clone-without-install usage |
| `skills/` | Drop-in agent skills (quality gates + recursive compound) |
| `examples/` | Minimal fake-data walkthrough |
| `tests/` | Pytest suite |
| `writeback_candidates/` | Bounded durable-candidate inbox (gitignored payloads OK) |

## Design principles

- **Doer ≠ Judge** for durable memory: the same pass that drafted a claim must not be the only check.
- **Anti-bloat**: no raw logs, vibes, or duplicate files promoted to long-term knowledge.
- **Musk 5-step as public engineering practice**: question requirements → delete → simplify → accelerate → automate last.
- **Secrets stay out**: refuse absolute machine paths, tokens, and private identifiers in candidates.

## 简述（中文）

本仓公开两套可复用方法：**递归复利闭环**（只写回会改变未来行动的已验证内容）与**休闲合成小游戏生产闸**（自动化绿 ≠ 可上架；真人盲玩才是放行）。无平台、无私有业务、无个人/财务数据。维护者品牌：**Aichill**。

## Status

Public methodology pack, **v0.1.0**. See [CHANGELOG.md](CHANGELOG.md). No fabricated adoption metrics — use your own stars/issues after publish.

## Contributing / Security

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md).
