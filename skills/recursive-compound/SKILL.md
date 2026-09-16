---
name: recursive-compound
description: >-
  Use when an agent should compound each real task into verified durable
  assets (recursive self-improvement) without building orchestration theater.
---

# recursive-compound

Public skill distilled for generic multi-host agents. Companion docs:
`docs/01-recursive-evolution.md`, `docs/02-writeback-protocol.md`,
`docs/03-operating-model.md`.

## When

- End of a non-trivial task
- Maintainer asks to “compound”, “write back”, “harden”, or “make next time shorter”
- A gate flipped FAIL→PASS, or the same task class hit a third time

## Daily / per-wake minimum (optional but powerful)

1. Learn **one** hard in-scope fact (not vibes).
2. Cite a source (URL, official docs, local skill path).
3. State one executable use in your role.
4. Harden into a skill/doc **or** explicitly skip (“not durable yet”).
5. Leave an evidence file on disk. No file = not done.

Refuse: directory theater, cross-role filler, learning meshes, auto-DM spam, claiming “recursion” without ≥3 weekday evidence files.

## Compound loop

```text
Identify intent → minimal context → one primary action → verify
→ four questions → writeback or explicit no-writeback
→ next round one step shorter
```

### Four questions

1. New maintainer decision / boundary / preference?
2. Reusable method or failure lesson?
3. State / blocker / next action changed?
4. Next run can read/ask/skip less?

All no → write nothing.

## Writeback rules

- Flow: Evidence → Candidate → Independent check → Accepted writeback
- Fast lane: session only
- Durable lane: `scripts/writeback_candidate.py` inbox; **no auto canonical edit**
- Doer ≠ Judge for durable claims
- Reject absolute paths and secret-like strings

## Musk 5-step (order fixed)

1. Question requirements (named owner)
2. Delete
3. Simplify
4. Accelerate
5. Automate **last**

## Output shape when reporting upward

1. Conclusion first (1–3 sentences)
2. Evidence path
3. Minimal deliverable path
4. Blocker + next deadline
5. No process noise without a gate pass
