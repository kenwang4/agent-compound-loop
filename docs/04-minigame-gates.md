# Casual Merge Minigame — Production Gates

> Public methodology distilled from a mini-game host / short-video host–class casual merge minigame.  
> **No AppIDs, store credentials, private paths, or product secrets.**  
> Platforms named only in the abstract.

## Thesis

**Automation green ≠ fun ≠ ship.**  
Ship gates are human-blind playtests plus thin platform adapters around a shared native core.

Recommended progression:

| Gate | Question | Pass signal |
|------|----------|-------------|
| **G1** | First-minute understandability | New player merges once in ~30s without a tutorial |
| **G2** | Vertical slice (3–5 min) | One business cycle: understand + choose + scene gets better |
| **G3** | Replayable short sessions | 60–90s continuous flow without teaching; willing to continue |
| **Human playtest** | “Do I want minute 6?” | Blind 5-minute session; yes/no + one sentence each |
| **Platform** | Adapter + compliance | Shared rules; mini-game host/short-video host/browser differences stay thin |

Until the human gate passes: **do not expand systems** (NPC, currencies, social, ads-as-content).

---

## Human 5-minute blind playtest

1. Build to a local / preview package (platform tools as needed).
2. Play **5 minutes only** — no docs, no AI coaching. First impression = product verdict.
3. Answer yes/no + one sentence:

| # | Question | Maps to |
|---|----------|---------|
| 1 | First 30s: know what to do without a tutorial? | G1 understandability |
| 2 | First “clear → reward → scene lights up”: any delight? | Core juice |
| 3 | Want minute 6? | Retention intuition |
| 4 | Any stuck / no-feedback / “where do I tap” moment? | Blockers |

Record `verdict: pass|fail` with date + one-line evidence in project state.  
**Fail is cheap** — it produces a fix list. Pass is required before AppID / filing / compliance talk.

---

## G2 vertical slice (one question)

> Can a 3–5 minute cycle make the player feel: “I know what I’m doing”, “I’m choosing”, and “the cafe/board got better because of me”?

### Keep in slice

- One scene area with a visible unfinished reward (e.g. unlit lamp).
- Two short merge chains (e.g. drink / dessert), levels L1–L3 only.
- Current order + next-order preview (no order list page).
- Small board with a readable set of active cells.
- One free recover (undo last merge) — no currency, no ads.
- Completing N orders lights a scene change + character response.

### Keep out of G2

- Stamina, ads, login, payment, chapter select, remote config.
- NPC, social, leaderboards, events, complex codex, multi-currency.
- Long chains, random procedural levels, one-off scripted exceptions.

### Experience beats (illustrative)

| Time | Player | Feedback intent |
|------|--------|-----------------|
| 0–5s | See matching L1 + order goal | Soft hint, no long tutorial |
| 5–20s | First merge | Snap + SFX + character glance |
| 20–60s | Choose next merge across two chains | Current order primary; next preview secondary |
| ~1–2m | First order complete | Scene micro-change, not only numbers |
| ~3–5m | Third order / cycle complete | Clear “day done” + reason to replay |

### Acceptance (player)

- First merge ≤30s without tutorial.
- First order ≤90s; player can state merge↔order link.
- 3–5 minutes: N orders + one scene payoff.
- At least one real “now vs next” choice.
- Stuck → can name cause and recover with one undo.
- Some players voluntarily restart (ratio decided later by broader playtests).

### Engineering boundary

- Prove in an isolated slice before merging to production entry.
- No real platform SDKs in the slice; adapters later.
- All delayed feedback must cancel on reset / exit (no leaked timers).

---

## G3 replayability (one question)

> Can inbound items, merges, combos, and scene feedback sustain 60–90s without teaching — and invite the next order?

### Beat contract (“flat-fast, snackable, small joys”)

Each action closes a short loop **in-session**, not only on a settlement screen:

1. **Catch** — place inbound item; land bounce + SFX + character beat.
2. **Stack** — same-column same-type auto-merge or half-second manual merge feedback.
3. **Upgrade** — L2→L3 / combo gets a stronger burst without changing the next input.
4. **Serve** — one clear tap to deliver; instant tip/progress feedback.
5. **Advance** — next order, scene stage, or inbound pace changes immediately.

Automation proves **states exist**. Humans prove **flow**.

### Content grammar

Prefer one new decision per short session, expressed as **data**, not `if (levelId === …)` branches. Shared fields example:

```js
{
  id: "session-01",
  title: "First lamp",
  focus: "now vs next",
  orders: [/* item ids */],
  initialBoard: [/* cells */],
  lockedSlots: [/* geometry only */],
  deliveryPlan: [/* refill after orders */],
  capacity: 8,
  sceneStage: [0, 1, 2],
  recoveryHint: "point at the choice that blocked the board"
}
```

If a session only works via new currency, stamina, ads, or special scripts → delete or rewrite the grammar.

### Soft vs hard pressure

- Soft: near-full board hint (“merge a pair first”).
- Hard spatial fail / heavy guest-patience: **only after** human gate says soft pressure is insufficient.
- One undo per cycle max in early gates.

---

## Verified lessons (sanitized)

1. **Validate the main loop before expanding systems.** Fix reproducible blockers only.
2. **Shared native core; thin platform adapters** for mini-game host / short-video host / browser.
3. **Project checkpoint > chat handoff.** Record task / session / artifact / acceptance / verdict in a state file before switching machines or IDEs.
4. **Negative decisions:** do not restore rejected prototypes as mainline without new human evidence; do not mark platform publish ready without entity / filing / rights / IDs / device evidence; do not add NPC/currency/social/ads to hide a weak loop; do not grow a second control plane of nested agent instruction files.

---

## Pre-ship checklist (pair with skill)

Use [`skills/game-quality-gates/SKILL.md`](../skills/game-quality-gates/SKILL.md) for lifecycle/bug-class gates (cleanup entry, buffs, timers, delta time, audio, input mutex, saves, network timeouts, assets, anti-cheat baseline).

Then require:

- [ ] Human 5-minute blind playtest recorded
- [ ] G2 slice acceptance met (or explicitly deferred with reason)
- [ ] G3 data-driven sessions without per-level script forks
- [ ] No private AppID / credential material in repo
- [ ] Platform adapter diffs reviewed as *thin*
