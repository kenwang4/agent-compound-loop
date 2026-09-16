# Writeback Protocol

> Purpose: define the only durable writeback path shared by Cursor, Claude Code, Codex, and future hosts.

> Review trigger: on major model upgrade — ask which rule is now redundant before adding new ones. Harnesses expire; they should not only grow.

---

## Core principle

Do not remember everything. Preserve only what **changes future action**.

A good writeback is:

- durable;
- verified or explicitly marked unverified;
- useful to future AI sessions;
- stored in a tool-agnostic file;
- small enough to be read again.

Host-native memory, chat history, subagent transcripts, and model summaries are caches or evidence — **not** canonical memory.

## High-integrity reload surface

These files (or your equivalents) are re-injected at cold start. An unverified sentence that lands here is reloaded as truth next session. Treat them as poisonable persistent memory:

- `CONTEXT_PACK.md`
- `AGENTS.md` (or host agent instructions)
- `STATE.md`
- `DECISIONS.md`

Do not append model speculation, raw web/tool text, or unverified subagent output. Maintainer-verified decisions and independently checked writebacks only. Raw evidence stays in `logs/`. Retire stale claims; do not leave them to steer the next session.

This is a **file-layer** rule. Do not copy host startup classifiers, sandboxes, or auto-mode into this repo.

## The only writeback flow

```text
Evidence → Candidate → Independent check → Accepted writeback
```

Every durable candidate must include:

```yaml
candidate:
  claim: <what should change future action>
  source: <file, test, decision, or external evidence>
  verified_by: <independent check or maintainer decision>
  owner: <who maintains it>
  scope: <where it applies>
  review_on: <date, trigger, or reopen condition>
  destination: <canonical file>
```

Machine-checkable shape: [`schemas/writeback_candidate.schema.json`](../schemas/writeback_candidate.schema.json). Helper: [`scripts/writeback_candidate.py`](../scripts/writeback_candidate.py).

## Proactive decision capture

The current host should inspect the conversation and verified artifacts for the **maintainer’s** explicit decisions, preferences, and vetoes. The maintainer does not need a separate “please write this back” command.

An unambiguous statement made directly by the maintainer is evidence with `verified_by: maintainer`. After scope / destination / duplication / secret checks, write to the matching layer:

- current focus, blocker, or next action → `STATE.md`;
- settled decision or veto → `DECISIONS.md`;
- stable preference → taste / identity asset;
- project-specific checkpoint → project state file (e.g. YAML).

Report briefly after writing. Ambiguous, contradictory, high-risk, or externally consequential decisions still need focused confirmation.

The host must **not** treat its own inference as the maintainer’s decision. Model-inferred preferences and generalized lessons stay candidate-only until independently checked. Direct model output must not auto-append to playbooks, agent cards, boards, or compound indexes.

### Session-close default

At session end, ask internally: did the maintainer make or confirm something that changes future action? If no → write nothing. If yes → write the smallest verified change to the matching layer. This is a semantic host action — not a required hook, telemetry loop, or sync workflow.

Before the write lands, run one independent minimal self-check from a fresh vantage:

1. Is the claim verifiable (not opinion or hope)?
2. Does it actually change a future action?
3. Does it contradict `DECISIONS.md`?

Fail any → downgrade to a `writeback_candidates/` candidate instead of a direct canonical write. **Doer ≠ Judge** also applies to this common path.

## Two-speed execution

| Lane | Use for | Durable writeback | Gate |
|------|---------|-------------------|------|
| Fast | Tunables, local bugs, temporary exploration, same-session trial | No long-lived candidate; session / project checkpoint only | Deterministic local check |
| Durable | Rules, decisions, reusable methods that change future action | Candidate under `writeback_candidates/` | Independent review + owner acceptance |

The durable inbox is bounded (default **20** pending, **12 KiB** each, **30-day** TTL). Overdue open candidates become `expired`. The inbox is **optional overflow**, not the default path: preferred flow is `evidence → independent check → direct canonical write by the current host`. Use the inbox for multi-writer handoffs or async reviewers.

The helper may validate or record a review verdict; it **never** edits canonical state, playbooks, or the compound index. After `accepted_pending_writeback`, the current main agent owns the last mile: whitelist destination, preview diff, smallest reversible edit, relevant check, record evidence. Until applied, accepted ≠ durable truth.

## Minimal task telemetry

Only record telemetry when a consumer already exists. Portable envelope (see [`schemas/task_envelope.schema.json`](../schemas/task_envelope.schema.json)):

```json
{
  "schema_version": "1.0",
  "task_id": "stable task identifier",
  "risk": "low|medium|high|unknown",
  "owner": "decision owner",
  "host": "cursor|claude|codex|other",
  "machine": "handoff machine label",
  "session_id": "host session identifier",
  "agent_id": "main or subagent identifier",
  "agent_type": "planner|implementer|reviewer|script|other",
  "artifact": "relative path or durable URI",
  "acceptance": "acceptance criteria reference",
  "verdict": "pass|revise|fail|unknown"
}
```

Identity and contract only — not a prompt archive. High-risk completed envelopes with explicit verdicts should include non-empty `evidence_refs`. Do not build a dashboard. Do not store prompts, chain-of-thought, secrets, or full model responses.

## Load principle

Do not reload everything. Default cold start:

1. `CONTEXT_PACK.md`
2. `STATE.md`
3. One task asset only when the current action needs it

Load decision files only when a prior decision affects the action. Do not reload the whole workspace unless the maintainer asks for a full audit / migration / refactor sweep.

## Writeback decision test

1. Did the maintainer make or confirm a decision?
2. Did system / product state change?
3. Did we discover a reusable workflow, rule, or failure mode?
4. Did a stable preference or boundary appear?
5. Did a pipeline, content loop, or project status change?
6. Did an external action happen or require follow-up?

All no → do not write back.

### Mandatory compound signals

These enter a review queue deterministically (LLM may not skip):

- a test or gate goes FAIL → PASS;
- the maintainer corrects or rejects output;
- the same task class is handled a third time;
- an asset is proven useful or misleading;
- an explicit `review_on` or 30/60/90 date arrives.

A queue signal is not durable truth. Only Evidence → Candidate → Independent check → Accepted writeback may change canonical assets.

## Destination map (adapt names)

| Durable information | Write to | Notes |
|---------------------|----------|-------|
| Stable preference | context pack / taste asset | Concise; no transient mood |
| Settled decision | `DECISIONS.md` | Short active set; boundary + reopen |
| Historical decision | decision log | Archive when inactive |
| Operating state | `STATE.md` | Focus, watchlist, blockers |
| Daily factual summary | `logs/eod/YYYYMMDD.md` | Optional; not ritual |
| Handoff | section inside `STATE.md` | Avoid standalone handoff dumps |
| Reusable pattern | compound assets + index | Only if reusable |
| New workflow | host-discovered `SKILL.md` | After proven reusable |
| Secrets | **do not write** | Approved secret store only |

## Do not write back

- raw chain-of-thought;
- unverified web claims as facts;
- temporary search results;
- one-off chat phrasing;
- secrets / tokens / passwords / keys;
- unapproved drafts;
- screenshots or local absolute paths unless part of a real deliverable;
- duplicate memories already in context pack or decision log;
- host-native summaries without durable evidence;
- telemetry merely because it exists;
- model-generated patterns without independent check.

## Value evidence and exit

When a durable asset demonstrably avoids repeated explanation, prevents a repeated mistake, or removes a workflow step, log one concise row at the **point of use** (not from memory at session end).

If no such row is added for 90 consecutive days, or maintenance time exceeds saved time, review whether the workspace should become a read-only archive.

## Close-out

A task is not fully closed until the AI either (1) wrote durable changes to the correct file, or (2) explicitly concluded nothing durable to write.

For external/public actions also verify: compliance gate, maintainer approval, ledger/status update, follow-up owner.

## One-line rule

**If it should help the next AI act better, write it to the durable workspace. If it only explains this moment, leave it in chat.**
