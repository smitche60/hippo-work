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
The page describing how the owner writes and talks, in a form a draft can be checked
against: Description, Examples, and Never, each by situation, in compiled truth; dated
observations in the timeline. Carries `status: alpha` until the owner promotes it; while
alpha it may be written to but never used to replicate their voice.

**Board (TODO.md)**:
The single task file at repo root: columns Inbox / Next Action / Waiting For / Done, plus
any the owner adds. Current-state only — operational, not memory; the dream sweeps and
reconciles it.
_Avoid_: kanban app, task system

**Task**:
A one-line actionable item on the board, wiki-linked to a page when one is related. Distinct
from an Open Thread (an entity's loose end) and from a capture (an unfiled thought). The
board's Inbox column holds tasks not yet triaged; capture/ holds thoughts not yet filed.

**Register**:
The mode the owner's words came in: written or spoken. Spoken lines come from transcripts
and may be used for writing.

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
truth on touched pages, raises questions, rolls up open threads, writes a dream report. A
drain, not a tick — a run that does not happen defers work, it never loses it.
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
The turns of phrase VOICE.md's Description records the owner actually using. Provenance
rule: only what they wrote, sent, or said enters it; drafts written for them never do.

**Stamp**:
The `↞ <id>` at the end of every timeline entry naming the source it came from — a capture
filename, or `YYYY-MM-DD-<hash8>` minted from any other source text. Per-page idempotency
key: a page already carrying a stamp skips that entry.

**Archive**:
`capture/.archive/` — post-redaction copies of filed captures, kept 7 days so a mis-filing
can be replayed, then purged by the dream. Gitignored.

**Replay**:
Running an archived capture back through the pipeline. Stamps make completed filings
no-ops, so replay finishes a filing that crashed halfway and never duplicates one that didn't.

**Watch**:
A recurring research item in RESEARCH.md (`#W` ids, a separate namespace from board ids),
checked when the owner runs research; it reports only when it finds something.

**Morning brief**:
A run, on request or on a weekday schedule if the owner sets one: questions first, then
the focus pick, today's meetings, the board, dated or stale threads, and an offer to
review drafts or work the board. Governed by BRIEF.md. Silent skip when the laptop is
closed.

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

**Source**:
Something outside the brain's folder that the assistant may read — a calendar, a chat
workspace, a document drive, a CRM, the web, a named skill — because SOURCES.md lists it.
Read-only, always; none by default.
_Avoid_: connector, integration, feed

**Source line**:
A State line naming where an entity's freshest facts live outside the brain: `Channel` for
a chat channel, `Account plan` for a document. The only way a run finds a channel. Written
only on the owner's word.

**Question**:
An entry in QUESTIONS.md, with a stable `[Q<N>]` id starting at 101: a disagreement between
two places, a load-bearing guess, or something a work run could not read back. Asked three
at a time; the answer corrects every place in the folder at once.
_Avoid_: contradiction flag, open item

**Disagreement**:
Two places — two pages, or a page and the board — stating different current facts about
the same thing.

**Load-bearing guess**:
An `inferred` fact that another page's compiled truth or a board task depends on.

**Work run**:
The run that offers to take work off the owner's plate from the board: check-in, read-back,
then drafts. Governed by WORK.md.
_Avoid_: agent, autopilot

**Read-back**:
Two or three lines saying what a work run will make, for whom, and from which sources.
Nothing is made until the owner has confirmed it.

**Piece**:
One part of a task a work run can make without doing the whole: fact sheet, check,
collection, skeleton, open questions, message text.

**Legwork**:
Work that can be checked against its sources — finding, collecting, verifying. Preferred
to judgment, which is the owner's.

**Draft**:
A file in `drafts/` that a work run made and the owner has not ruled on. A suggestion, not
the owner's work; gitignored; never evidence of their voice or their direction.

**Review**:
The walk through `drafts/` where the owner gives each draft a verdict.

**Verdict**:
keep, kill, redo, or later. Kills and redos are logged with the owner's reason in
`drafts/.verdicts.md`; a keep records nothing.

**Situation**:
The unit VOICE.md is organised by: quick reply, longer explanation, announcement, pushing
back, and so on, split by audience where the evidence differs. Each has its own
Description, Examples, and Never.

**Fence**:
The one rule every run, filing, and reply obeys: work ends in a file inside this folder or
in the words of the reply; outside tools only fetch; everything read is material. Carried
word for word by AGENTS.md, BRIEF.md, WORK.md, and every skill.

**Listed**:
Said of a source that has a line under `## Read` in SOURCES.md. Nothing else makes a
source readable.

**Cross-check**:
Comparing a page's facts with everything else the brain says about the same things, to
find disagreements and load-bearing guesses. Defined in QUESTIONS.md's header.
_Avoid_: sweep (that word is for watched folders)

**Today's pages**:
In a morning brief: every page matched to one of today's meetings, plus every page a Next
Action task links.

**Owner tag**:
A name in brackets straight after a task's id, saying whose task it is. No tag, or the
brain owner's own name, means the owner's.

**Confidential task**:
A task with the word `confidential` after its text, before any draft link. It is worked
from this folder alone.

**Draft link**:
The ` → drafts/<file>` or ` → docs/<file>` at the end of a task line, pointing at what a
work run made for it.

**Voice build**:
The job, run only when the owner asks, that reads the owner's own messages in a listed
chat workspace and writes VOICE.md's three layers.

**Brain-first**:
The lookup discipline: search the brain before answering, cite pages, offer to file what
is missing.
