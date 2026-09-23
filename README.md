# Hippo — work brain

A work brain in markdown and git, run by an AI assistant. Two-layer pages (compiled truth on
top, append-only timeline below), a redaction stage that sees raw input before anything is
stored, a resolver that routes every fact to exactly one page, a board, and a "dream" run
that distills your filed captures into durable pages. No database, no embeddings, no daemon
— conventions and a linter.

This is the **work** variant of Hippo. It holds customers, projects, people, decisions,
events, and topics; keeps your personal life and HR matters about named people out by rule; and
ingests nothing you did not explicitly file. The personal variant is at
[github.com/smitche60/hippo](https://github.com/smitche60/hippo).

This repo is the **skeleton**: the rules, the design reasoning, the linter, the skills, and
empty directories. It holds no content and never will.

Credit: the conventions are adapted from Garry Tan's GBrain — two-layer pages, a resolver
you read before you write, brain-first lookup, date-hash capture ids, a dream. What Hippo
kept, dropped, and added — and why — is in `DESIGN.md`, along with Hippo's own additions:
decisions as first-class pages, the redactor, the ontology as one file, and — in this
variant — explicit-only intake.

## Rule zero

This repo never holds a page about anyone. Your brain is a **separate** clone with **no
remote**. If you push a brain with content in it, every fact in it is on the internet, and
git history keeps what you delete. The install puts four guards on it — no remote, a lint
check, and two git hooks — and makes the assistant prove both hooks work; a fifth forbids
the assistant from ever pushing, whoever asks. `DESIGN.md`, "This kit never holds content"
and "Five push guards, not one."

## Starting one

Hand your assistant the prompt in `INSTALL.md`. It clones this skeleton into your folder
with no history and no remote, reads the rules, fills in your page with you, walks you
through the types, installs the three skills, and lints. Scheduling the dream is optional;
the default is to run it by hand. If
you'd rather do it by hand, the prompt is also the checklist.

The rules say "the owner" throughout — that's you. They are the actual rules of an actual
brain, not an abstraction. `AGENTS.md`'s "Asking the owner" section in particular is how the
author wants to be asked questions; keep it or rewrite it, but keep the idea.

## What's here

- `INSTALL.md` — the prompt that sets this up.
- `AGENTS.md` — behaviour and operating rules. Start here. (`CLAUDE.md` is a pointer to
  it, for assistants that load that filename automatically.)
- `RESOLVER.md` — routing and page anatomy; read before any write.
- `ONTOLOGY.md` — the entity types, in precedence order. The customisation seam.
- `REDACTOR.md` — what may never be stored, and what happens to it instead.
- `CONTEXT.md` — the glossary.
- `WATCHED.md`, `RESEARCH.md`, `TODO.md` — watched folders (empty by default), the research
  queue, the board.
- `ME.md`, `VOICE.md` — the owner's page and voice profile, empty.
- `tools/lint.py` — strict lint; the gate on dream commits and multi-page filings.
- `skills/` — the three skills: file, dream, ask. (Shipped under `brain-*` names; the
  install renames them if those names are already taken on your account.)
- `DESIGN.md` — what Hippo borrows from GBrain, leaves out, and adds, and the reasoning
  behind every choice you might want to change. Read it second.
- `capture/` is deliberately absent; it's gitignored and gets created by the first filing.

## License

MIT — see `LICENSE`. Use it however you like, keep the notice, and nothing here comes with
a warranty.
