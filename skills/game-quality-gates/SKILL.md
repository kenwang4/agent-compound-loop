---
name: game-quality-gates
description: >-
  Run game lifecycle/quality gates when building, reviewing, or debugging
  a game project. Do not load for ordinary non-game web pages.
---

# Game Quality Gates

Mandatory quality standards for game projects. Distilled from many real cross-state bugs and common industry practice.

## Core principle

> Bugs come from **cross-state interactions**, not individual features.
> Each feature works alone; they break in combination.

## 12 universal rules

### 1. Single cleanup entry point

All exit paths (death / level-complete / quit / pause / scene-switch) call **one** cleanup method with options.

```js
cleanupGameState(opts) {
  // Fixed order: sub-objects → buffs+timers → UI → projectiles → (optional) enemies/controls/events
}
```

New feature = add one line here. Never scatter cleanup across exits.

### 2. Respect active buffs

Any code modifying attributes (speed / attack / size / defense) must check active temporary effects first.

### 3. Cache before destroy

Extract needed data before `destroy()` / `dispose()` / `remove()`.

### 4. Timers follow lifecycle

Track all `setTimeout` / `setInterval` / `delayedCall` / `rAF`. Cancel in cleanup.

### 5. Frame-rate independent logic

Multiply time-dependent logic by delta. Never assume 60fps.

### 6. Scene transition = full cleanup

Clean listeners, timers, rAF, audio nodes, pools, GPU resources, global state, pending network. Verify with heap snapshots when unsure.

### 7. Audio lifecycle

- iOS: resume `AudioContext` inside a user gesture
- `visibilitychange` → pause when hidden
- mini-game host WebView: unlock audio via platform bridge patterns before autoplay
- Pool SFX; manage BGM separately

### 8. Input safety

- Purchase / consume: mutex + visual disable
- Attack / fire: cooldown
- Pause toggles: state-machine guard

### 9. Save state persistence

- Include `version` for migrations
- Persist meaningful state only
- Auto-save on level end, manual save, and hide
- Prefer platform storage APIs on mini-program hosts

### 10. Network fault tolerance

Leaderboard / share / ads / sync: timeout (e.g. 5s) + local fallback + never block the core loop on failure.

### 11. Asset loading strategy

Critical (<2s) → level (loading screen) → deferred. Fatal only for critical failures.

### 12. Anti-cheat baseline

Client is untrusted. Server validates tokens, play-duration sanity, and score ranges for consequential actions.

## Pre-deploy checklist

- [ ] New objects cleaned in single cleanup?
- [ ] New timers cancelled?
- [ ] Attribute changes respect buffs?
- [ ] Data cached before destroy?
- [ ] Movement uses delta?
- [ ] No leak across scene transitions?
- [ ] Audio pauses on background?
- [ ] Spend/consume has duplicate-click prevention?
- [ ] Save has version + migration?
- [ ] Network has timeout + fallback?
- [ ] Asset failure degrades gracefully?
- [ ] Critical settle/spend server-validated?

### Mobile extras

- [ ] Multi-touch fingers tracked independently?
- [ ] iOS AudioContext after first interaction?
- [ ] Mini-program WebView CSS constraints respected?
- [ ] Controls do not obscure the playfield?
- [ ] Orientation change handled?

Pair with production methodology: `docs/04-minigame-gates.md`.
