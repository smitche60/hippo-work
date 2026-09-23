---
name: brain-file
description: "File one item into the brain: redact, route, write pages or board lines, lint, commit. Use when the owner says 'file this' or accepts a filing suggestion."
---

# brain-file

Orchestrates one filing. Every rule — redaction categories and verbs, routing tests, page
anatomy, stamp minting, idempotency, board ids, crash-safety ordering, lock handling, the
lint gate — lives in the repo docs, not here. Read them and follow them exactly.

## Steps

1. Reach the repo (`<path to your brain>` — edit this to the path as your shell reaches it).
   Unreachable → hold the item in this conversation, tell the owner it's queued per
   AGENTS.md's queued-capture rule, and stop.
2. Read `AGENTS.md`, `RESOLVER.md`, `ONTOLOGY.md`, `REDACTOR.md` in the repo. They are the
   rulebook; this skill only sequences them.
3. Mint the id and redact FIRST — before any routing, board items included (TODO.md is
   git-tracked). Quarantine per REDACTOR.md stops the item here.
4. Route per RESOLVER.md, against ONTOLOGY.md's directory blocks in order: board items per
   AGENTS.md's board section; page content per AGENTS.md's crash-safety ordering, with
   RESOLVER.md's dedup and per-page idempotency.
5. Locks, lint, and commit message per AGENTS.md.
6. Tell the owner what landed where, citing paths; quarantine as category counts only. Any
   question for them goes in grill format per AGENTS.md's "Asking the owner".

## Verification

Re-running with the same source changes nothing; lint exits 0; `git status` clean; no raw
pre-redaction text in any tracked file.
