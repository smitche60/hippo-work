---
name: brain-dream
description: "Run the dream: drain capture, sweep any watched folders, refresh pages, reconcile the board, report. Use when the owner says 'run the dream' or on a scheduled run if one exists."
---

# brain-dream

Executes AGENTS.md's "Dream duties" list — the single canonical spec for what a dream
does, in what order, with what ordering guarantees, and what the report contains. This
skill adds only session mechanics; every rule and parameter lives in the repo docs.

## Steps

1. Reach the repo (`<path to your brain>` — edit this to the path as your shell reaches it).
   Unreachable → stop silently; the dream is a drain, not a tick — the next run catches up.
2. Read `AGENTS.md`, `RESOLVER.md`, `ONTOLOGY.md`, `REDACTOR.md`. AGENTS.md's Dream duties
   section is the checklist for this run: execute it top to bottom, under its crash-safety
   ordering, its lint gate, and its lock rule.
3. Apply RESOLVER.md, routing against ONTOLOGY.md's directory blocks in order, for all
   routing, anatomy, stamps, and idempotency; REDACTOR.md for all redaction, quarantine,
   and watched-source refusal handling; WATCHED.md and `.dream-state.json` (gitignored —
   never `git add` it) for the sweep.
4. Report and final commit per the duties list. Anything the report asks the owner to
   decide goes in grill format per AGENTS.md's "Asking the owner".

## Verification

Run the drain and sweep logic a second time: a no-op. This run's commits contain no raw
quarantined text, no sensitive watched filenames, and no `.dream-state.json`.
