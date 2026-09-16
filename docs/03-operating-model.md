# Operating Model (Generic)

> A file-based control plane for AI-assisted work — without building a platform first.

---

## 1. Core thesis

This is not an IDE rule pack. It is a **maintainer-owned control plane**.

The system moves execution work to AI while keeping judgment and irreversible approval with the maintainer.

> The maintainer provides goals, context, taste, and approval.  
> AI owns observation, context gathering, planning, reversible execution, verification, and learning.  
> The maintainer only handles judgment and approval.

## 2. First-principles goal

The scarce resource is **maintainer attention**.

Every system decision must reduce one of:

1. Repeating context
2. Choosing which agent / context / tool to use
3. Decomposing tasks manually
4. Checking whether work happened
5. Re-deciding questions already settled

If a change does not reduce one burden, do not build it.

## 3. Role boundaries

### Maintainer

Owns: direction, taste, business judgment, risk acceptance, approval for irreversible actions.

Should not own: context routing, tool selection, file hunting, task decomposition, routine verification, status tracking.

### AI operator

Owns: reading relevant context / playbooks / memory / logs; understanding intent; breaking work into steps; reversible execution; checks; summaries; recording decisions and state.

Must not: send external messages, publish, spend money, destructive deletes, or external deploy without approval; invent KPIs; pretend work happened.

### IDE / coding agents

Engineering executors: code, docs, local tests, scripts. Not the long-running brain.

### Browser agents

External-world hands: research, SaaS UI, form prep, public downloads. Not strategy or approval.

### Human messaging surface (chat / IM)

Alerts, approval requests, short status, failure escalation — not complex reasoning.

### Memory layer

Stable preferences, decisions, lessons, constraints, repeated failure patterns — independent of any IDE session.

## 4. Default work loop

```text
Observe → Understand → Decide → Act → Verify → Learn
```

- **Observe**: read only what the task needs; do not ask the maintainer which file to open.
- **Understand**: restate the real goal internally.
- **Decide**: next reversible action — or prepare an approval request if irreversible.
- **Act**: drafts, local docs/JSON, tests, reports, outbound drafts.
- **Verify**: does the claimed result actually exist and hold?
- **Learn**: write durable outcomes to `STATE.md` / decision log / memory when appropriate.

## 5. Autonomy policy

**Without approval:** read/search workspace; write drafts; update local non-public docs; safe local tests; reports; state / decision logs; prepare outbound drafts; analyze logs.

**Ask first:** send email/DM/IM to others; publish; submit forms; spend money; delete outside archive; deploy externally; change long-term strategy; legal/compliance commitments; expose private identity or company details.

**Escalate when:** conflict with prior decisions; unclear risk; missing context that cannot be found; decision changes active focus; workflow failed twice.

## 6. Platform rule

Do not build a platform yet. Start as Markdown / JSON until real usage proves need.

Platformization only if **at least two** stay true for two consecutive weeks:

1. Ten or more autonomous AI tasks per day
2. Five or more approval requests per week
3. Tasks regularly span multiple days
4. Messaging approval becomes a daily surface
5. JSON / Markdown state becomes hard to maintain
6. One workflow produces measurable value every week

Until then: no Web UI, no new daemon, no workflow engine, no database “because someday”.

## 7. Anti-patterns

- Dashboard before useful data
- Agent framework before one workflow proves value
- Asking the maintainer to choose files / agents / tools
- Treating context files as fake employees
- Runtime machinery for work that is read/write files
- Re-discussing settled decisions without new evidence
- Optimizing architecture instead of closing one real loop

## 8. Musk 5-step (public engineering practice)

Order is fixed — do not invert:

1. **Question requirements** — every “must” attaches to a named owner; unowned → deletable
2. **Delete** — cut idle roles, duplicate reports, half-finished meshes; delete enough that ≥10% might need to come back
3. **Simplify** — optimize only what should still exist
4. **Accelerate** — shorten to the smallest verifiable delivery
5. **Automate last** — no cron/daemon until a human path has run green

## 9. Strength / recursive-learn (generic maintainer practice)

Daily (or per wake), each role should output:

1. Conclusion first (1–3 sentences)
2. Evidence path (file / command / screenshot; no evidence = not done)
3. Minimal deliverable path
4. Blocker + next deadline (time or condition; no “keep watching”)
5. Report upward only through the agreed control seat

Recursive self-improve (weekday minimum): learn one hard in-scope fact → cite source → say how it applies → harden into a skill/doc or explicitly skip → evidence file on disk. Claiming “recursion” without ≥3 weekday evidence files is theater.

## 10. Current operating principle

> Use existing capabilities.  
> Write state.  
> Record decisions.  
> Let AI choose context automatically.  
> Do reversible work directly.  
> Ask the maintainer only for judgment and approval.
