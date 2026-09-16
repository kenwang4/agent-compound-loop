# Contributing

Thanks for helping improve **agent-compound-loop**.

## Ground rules

Public brand/maintainer: **Aichill**. Do not commit personal legal names, private handles, personal emails, or private home paths.


1. Keep docs **host-agnostic** (Cursor, Claude Code, Codex, scripts, other).
2. Prefer **small, reversible** edits. One primary improvement per PR.
3. Do **not** commit secrets, absolute home paths, personal legal names / private handles / personal emails, private AppIDs, store credentials, finance data, or internal ops seat names.
4. Durable protocol changes need a short rationale in the PR: what future action changes?
5. Examples must use **fake** data only.

## How to propose a change

1. Open an issue describing the gap (protocol ambiguity, schema bug, gate wording).
2. Fork, branch from `main`, make the smallest fix.
3. Run a privacy scan before PR:

```bash
rg -n -i 'personal-email|home-path-leak|employer-name|portfolio-bio|resume-keyword' .
```

4. For schema/script changes, show a create/list round-trip with fake fields.

## Doc style

- English primary; short Chinese summaries OK where they help bilingual maintainers.
- Prefer checklists and tables over long narrative.
- Link to schemas instead of duplicating field lists.

## License

By contributing, you agree your contributions are licensed under the MIT License.
