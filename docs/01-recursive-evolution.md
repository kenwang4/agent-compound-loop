# Recursive Evolution Protocol

> Goal: every real task should improve the starting point of the next task — without growing system complexity.

> Review trigger: on major model upgrades, ask “which constraint here is now redundant because the model got stronger?” before “what should we add?”. Direction is periodic simplification, not thickening.

## One line

The current AI session owns understanding, judgment, and execution. The durable workspace owns **verified assets that change future behavior**.

## Standard loop

```text
Identify intent → load minimal context → execute one primary action → local verify
→ decide whether a new pattern exists → writeback to the correct layer
→ next round needs one fewer step
```

## Continuous execution contract

When the user asks to execute / continue / “finish end-to-end”, **or** a task has started and the next safe step is clear, enter continuous mode:

```text
Set overall goal + done criteria
→ keep doing locally safe actions
→ verify and write progress each turn
→ re-read state
→ auto-continue until done
→ pause only at risk boundaries
→ report once at the end
```

Finishing a small turn is **not** a reason to stop and ask. Stop only when:

- delete, publish, outbound message, payment, deploy, or other irreversible action;
- a maintainer-only judgment call is required;
- secret, privacy, compliance, or safety risk appears;
- done criteria are met;
- the environment truly cannot continue.

## Four questions (end of non-trivial tasks)

1. Did this produce a new maintainer decision, boundary, or preference?
2. Did this produce a reusable method or failure lesson?
3. Did this change project state, blockers, or next action?
4. Can the next run read less, ask less, or skip a step because of this?

If all four are no → **do not write back**.

## Writeback destinations (generic)

| Change | Destination |
|--------|-------------|
| Current focus, blocker, next action | `STATE.md` |
| Settled decision still affecting behavior | `DECISIONS.md` (keep short; archive history separately) |
| Reusable method / failure lesson | `assets/compound/` + index |
| Run evidence | `logs/` (not default context) |
| Stable preference / brand boundary | `CONTEXT_PACK.md` / `assets/identity/` |

Names are conventions — adapt to your repo layout; keep the **roles** fixed.

## Loop, harness, agent, hook

- **Loop**: which single primary action to push now.
- **Agent**: specialist viewpoint when needed.
- **Harness**: constraints / evaluation for multi-path or high-risk work.
- **Hook**: remind or block at critical nodes.

All are on-demand tools, not a default runtime. No real consumer → no new daemon, dashboard, or orchestration layer.

## Anti-bloat

- Do not promote raw logs, model speculation, or duplicate daily digests into long-term knowledge.
- Do not add files to hide overlapping responsibilities.
- Fixed rules live in protocols/assets; one-off process lives in logs.
- One primary improvement per round; escalate harness only after three stalled rounds.
- Continuous mode may include many small turns but stays one overall goal — not an unbounded backlog.

## Done criteria

A recursive-evolution turn is complete only when **all** hold:

- the primary action has a clear result;
- the result was locally or factually verified;
- unverified speculation was not written as fact;
- reusable change was written to the right place, or “no writeback” was explicit;
- the next round’s starting point is clearer, shorter, or more reliable.
