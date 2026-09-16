# Security Policy

## Supported versions

This repository is documentation + schemas + a small Python helper. Treat the latest `main` as the supported surface.

## What this project will never store

- Secrets, API keys, passwords, private keys
- Absolute machine paths (`/Users/...`, `~/...`)
- Personal contact data, finance ledgers, or private chat dumps
- Platform AppIDs, ad unit IDs, or store credentials
- Full model prompts / chain-of-thought as “memory”

`scripts/writeback_candidate.py` rejects absolute / home-directory path refs in candidate fields for this reason.

## Reporting a vulnerability

If you find a privacy leak, path leak, or script issue that could cause unsafe writes:

1. **Do not** open a public issue with the sensitive payload.
2. Open a private GitHub security advisory on this repository, or contact the maintainer through the profile linked on this repo.
3. Include: affected file, reproduction without secrets, and suggested fix.

We aim to acknowledge reports within 7 days and ship a scrub/fix promptly.
