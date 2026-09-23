# Hippo

A work brain: markdown-in-git knowledge system run by an AI assistant that turns
explicit captures into a compounding, queryable model of the owner's work — the entity
types ONTOLOGY.md declares. Work scope only; the owner's personal life belongs in a
separate instance. Never connects to email.

## Language

**Brain**:
The git repo of markdown pages plus the conventions that govern reading and writing it. The
system of record — not any other app's memory.
_Avoid_: knowledge base, vault, second brain

**Page**:
One markdown file representing one entity, with two layers: compiled truth above the `---`
separator, append-only timeline below.
_Avoid_: note, document

**Compiled truth**:
The always-current layer of a page: summary, State fields, Open Threads. Rewritten whenever
new information arrives.
_Avoid_: header, summary section

**Timeline**:
The append-only, dated, never-rewritten history layer of a page, below the separator.
_Avoid_: log, history, journal

**State**:
The structured current-fact fields inside compiled truth (the queryable "as of now" facts).

**Open Thread**:
An active, unresolved item on a page. Lives in compiled truth; on resolution it moves to the
timeline with its resolution.
_Avoid_: todo, task

**Capture**:
A raw unsorted input landed in `capture/` awaiting the dream run. Date-hash filename.
Captures are pre-redaction by definition; `capture/` is never tracked by git.
_Avoid_: inbox item (email connotation), note

**ME.md**:
The entity page for the brain's protagonist. Holds facts and preferences about the owner that
have no other page to live on. Not a journal, not the agent's personality.

**Voice profile (VOICE.md)**:
The two-layer page modeling how the owner writes and talks: style guide and registers in
compiled truth, dated observations in the timeline. Carries `status: alpha` until the owner
promotes it; while alpha it may be written to but never used to replicate their voice.

**Board (TODO.md)**:
The single task file at repo root: columns Inbox / Next Action / Waiting For / Done.
Current-state only — operational, not memory; the dream sweeps and reconciles it.
_Avoid_: kanban app, task system

**Task**:
A one-line actionable item on the board, wiki-linked to a page when one is related. Distinct
from an Open Thread (an entity's loose end) and from a capture (an unfiled thought). The
board's Inbox column holds tasks not yet triaged; capture/ holds thoughts not yet filed.

**Register**:
A context-specific mode of the owner's voice inside the voice profile (friend-text,
professional, formal), each with rules for when it applies.

**Resolver**:
The decision tree (RESOLVER.md) that routes content to its one correct directory.
Read-before-write is mandatory.

**Redactor**:
The mandatory pipeline stage ahead of the resolver — the sole stage that sees raw input.
Stateless; verbs are pass / strip / abstract / flag; fails closed. Its guarantee is
never-stored (see DESIGN.md “The redactor”), not never-transits.

**Dream run**:
The consolidation run, on request or on a schedule if the owner sets one: drains capture
(and sweeps watched sources, if any are listed) through the resolver, refreshes compiled
truth on touched pages, rolls up open threads, writes a dream report. A drain, not a tick —
a run that does not happen defers work, it never loses it.
_Avoid_: cron, maintenance job (as user-facing terms)

**Watched source**:
A folder listed in WATCHED.md that every dream sweeps for new or changed files, distilling
durable material and storing none of the raw. None by default; the owner adds one
deliberately.
_Avoid_: ingestion source, feed

**Stated**:
Sourcing label: the owner said it. Unlabeled content is stated; the explicit label is for pages
where the two kinds sit side by side.

**Inferred**:
Sourcing label: concluded from patterns rather than said by the owner — by the dream or by a hand
filing. A guess until the owner confirms; must never silently harden into compiled truth.

**Dream report**:
The file the dream run writes to `reports/YYYY-MM-DD-dream.md`: what got filed, stale
threads, patterns, what the brain noticed unprompted.

**Ontology**:
The set of entity types this brain holds, with the routing test and allowed `status:` values
for each. Declared once in ONTOLOGY.md, in precedence order; RESOLVER.md routes against it
and tools/lint.py reads it. Changing the set: ONTOLOGY.md, "How to change this".

**Entity**:
Anything that gets a page — one of the types declared in ONTOLOGY.md. Canonical slug =
filename = identity; frontmatter `aliases` handle variants.

**Residue**:
A capture that no ONTOLOGY.md test claims. It stays in capture/ and the dream report nags
about it; persistent residue is the signal to add a type.

**Quarantine**:
`capture/.quarantine/` — where the redactor holds a capture it refused or flagged until
the owner rules on it. Gitignored. Reports show counts by category, never the text.

**Phrase bank**:
VOICE.md's list of turns of phrase the owner actually uses. Provenance rule: only text they wrote
or sent enters it; drafts written for them never do.

**Stamp**:
The `↞ <id>` at the end of every timeline entry naming the source it came from — a capture
filename, or `YYYY-MM-DD-<hash8>` minted from any other source text. Per-page idempotency
key: a page already carrying a stamp skips that entry.

**Archive**:
`capture/.archive/` — post-redaction copies of filed captures, kept 30 days so a mis-filing
can be replayed, then purged by the dream. Gitignored.

**Replay**:
Running an archived capture back through the pipeline. Stamps make completed filings
no-ops, so replay finishes a filing that crashed halfway and never duplicates one that didn't.

**Watch**:
A recurring research item in RESEARCH.md (`#W` ids, a separate namespace from board ids),
checked by the morning brief; it reports only when it finds something.

**Morning brief**:
A run, on request or on a weekday schedule if the owner sets one: research digest, decisions
needing the owner in grill format, the board, dated or stale threads. Silent skip when the
laptop is closed.

**Entry bar**:
The condition a thing must clear before it earns its own page — stated as the `entry:` line
of a type in ONTOLOGY.md. Below the bar it lives as timeline lines on the pages it touched.
Frequency alone never clears it; the owner's call overrides it in both directions.

**Confidential line**:
A timeline line that stores a flagged business confidence on the owner's explicit "store
it". Marked `[confidential]` immediately after the date (RESOLVER.md, page anatomy) so every
such line is one grep away.

**Grill format**:
How every open question reaches the owner: numbered Qs, lettered options, an explicit
recommendation to argue with. Shape and rules in AGENTS.md; named after the grilling
session that designed the brain.

**Brain-first**:
The lookup discipline: search the brain before answering, cite pages, offer write-back.
