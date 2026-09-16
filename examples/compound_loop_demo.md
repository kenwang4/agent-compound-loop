# Compound loop demo (fake data)

This walkthrough uses **invented** paths and claims only.

## Scenario

An agent fixed a merge-game bug: delayed celebration SFX leaked after scene reset.
Maintainer confirmed: “Always cancel pending feedback timers in the single cleanup entry.”

## 1. Fast lane (session only)

```bash
python3 scripts/writeback_candidate.py create \
  --lane fast \
  --claim "SFX leak after reset — fixed locally for this session"
```

Expected: `{"status":"session_only","lane":"fast","writeback":false,...}`

## 2. Durable candidate

```bash
python3 scripts/writeback_candidate.py create \
  --lane durable \
  --claim "All delayed game feedback must cancel inside cleanupGameState on every exit path" \
  --source "examples/fake-test-log.txt" \
  --destination "docs/04-minigame-gates.md" \
  --owner maintainer \
  --scope "casual-merge-minigame" \
  --review-on "after-next-human-playtest" \
  --artifact "examples/fake-test-log.txt" \
  --task-id "demo-task-001" \
  --session-id "demo-session-001"
```

Absolute paths like `/Users/demo/...` are **rejected** by design.

## 3. Independent review

```bash
python3 scripts/writeback_candidate.py review \
  --candidate-id <id-from-create> \
  --verdict accepted \
  --reviewer "fresh-context-reviewer" \
  --evidence "examples/fake-review-notes.md"
```

Status becomes `accepted_pending_writeback`. The script still does **not** edit canonical docs — the main agent applies the smallest reversible patch and records evidence.

## 4. List inbox

```bash
python3 scripts/writeback_candidate.py list
```

## 5. What lands in DECISIONS (example text)

```markdown
### Decision: Single cleanup owns timer cancel

- Judgment: Every exit path calls one cleanup; delayed SFX/VFX must unregister there.
- Trigger: Celebration SFX played after reset in fake playtest.
- Evidence: examples/fake-test-log.txt
- Action: Document under minigame gates + game-quality-gates skill.
- Boundary: Does not authorize new platform SDK work.
```

## Fake evidence stubs

Create empty placeholders if you want a dry-run without committing noise:

```bash
printf 'fake pass\n' > examples/fake-test-log.txt
printf 'independent check: claim verifiable; changes future cleanup; no decision conflict\n' \
  > examples/fake-review-notes.md
```
