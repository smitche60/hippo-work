# Questions

next-id: 101

The brain asks instead of guessing. Everything above `## Open` is the rule for this file:
read it before cross-checking, writing an entry, asking, or applying an answer, and leave
it as it is — only `next-id:` and the two lists below ever change. The owner says "what
are you unsure about", answers by id ("Q102 b"), or says "leave it".

## What earns a question

- A **disagreement**: two places — two pages, or a page and the board — state different
  current facts about the same thing.
- A **load-bearing guess**: an `inferred` fact that another page's compiled truth or a
  board task depends on.
- A work run's question about a task it could not read back (WORK.md).

A fact that is merely missing is not a question; gaps never run out.

## Cross-checking

Pages are the `.md` files in the directories ONTOLOGY.md declares, plus ME.md; a page's
`updated:` line says when it last changed. To cross-check a set of pages, take them one at
a time and finish both passes on a page before opening the next.

**Pass A — disagreements.**

1. List every fact in the page's summary and State.
2. For each fact, find everywhere else the brain speaks about the same thing: the pages
   this page links, the pages that link it or name it (grep for its path and its name),
   its own timeline, and the TODO.md lines that link or name it.
3. Compare. Different current values for the same thing — an owner, a date, a status, who
   holds a role — are a disagreement, even when the field names differ (`Renewal date` on
   one page, `Renewal lands` on another). A newer timeline entry that contradicts the
   page's own State is a disagreement.

**Pass B — load-bearing guesses.** Pass A cannot find these: the other place agrees with
the guess and treats it as settled.

4. List every fact on the page labelled `inferred`.
5. For each, grep the other pages and TODO.md for the thing guessed: the name, the date,
   the value. It is load-bearing when another page's summary or State repeats it or builds
   on it, or a task acts on it. A page says `- **Buyer:** Jo`, labelled `inferred`, and a
   task says `Send Jo the renewal quote` → load-bearing: the task depends on the guess.
6. Note for each: `relied on by <path or #id>`, or `nothing relies on it`.

**Record.**

7. Add each disagreement and each load-bearing guess under Open, as "Writing an entry"
   says — unless it is already there, or is Settled as `left as is`, or is Settled as
   `unknown` and no page it names has changed since.

**Done when**, for every page in the set, you can state three things: how many facts went
through steps 2 and 3; each `inferred` label with its step-6 note; and the ids added, or
"none".

## Writing an entry

One line under Open, with the next id from `next-id:`, which is then incremented. Ids are
never reused. They start at 101 so that a stored question is never confused with a
question numbered Q1, Q2 in a single reply.

`- [Q107] Short label — the situation in a sentence. Places: customers/acme.md, people/jo.md, #12. (a) one choice (b) the other. ➡️ the recommendation and why.`

Places are paths in this folder and task ids, nothing else; name every one involved.
Entries are stored text, so REDACTOR.md applies: a question that cannot be written without
stripped content is asked in conversation and never stored. Commit `questions: YYYY-MM-DD`
once the new entries are in.

## Asking

1. If the owner asked "what are you unsure about" and fewer than three questions are
   open, first cross-check the pages updated in the last 30 days.
2. Take three open questions, the ones that touch the most places first. Ask them in grill
   format (AGENTS.md, "Asking the owner"), each under its own id. End the turn and wait.
3. Apply each answer as "Applying an answer" says, to its "Done when".
4. Re-read every entry still open against the corrected pages. One answer often settles
   others: an entry whose places now agree moves to Settled as `dissolved by Q<N>`.
5. Open is empty, or the owner stops → done. Otherwise back to 2.

**Done when** Open is empty or the owner has said stop, and step 4 was done after the last
answers.

## Applying an answer

The answer is the owner's statement and is filed like one. It changes pages and board
lines in this folder, and nothing anywhere else.

1. Mint its stamp (RESOLVER.md): today's date, a hyphen, and the first 8 hex characters
   of the sha256 of the answer's text — `printf '%s' '<the answer>' | sha256sum | cut -c1-8`.
2. Find every place that carried the other version: the places the entry lists, plus a
   grep for the old fact across all pages and TODO.md.
3. On each page: rewrite the summary and State to the answer, drop an `inferred` label the
   answer confirmed, add a timeline line that ends `↞ <stamp>`, and set `updated:` to
   today. Timeline entries already there are never edited. Fix board lines in place.
4. Move the entry to Settled with the date and the answer.
5. Run `python3 tools/lint.py` and fix what it reports until it prints `LINT: clean`.
   Only then commit `answer: Q<N>`, and show the owner the list of paths changed.

**Done when** a grep for the old version finds it in no summary, no State, and no board
line, and `git status` is clean.

Three answers change no page:

- "Leave it" or "both are true" → Settled as `left as is`. Kept for good, never re-asked.
- "Don't know" → Settled as `unknown`; both versions are labelled `inferred` where they
  stand. It returns only when a page it names changes.
- An answer to a work run's question (its Places is a task id) → Settled with the answer
  in the owner's words. The next work run reads it when it sorts that task. It stays until
  the task leaves the board.

Each commits as `answer: Q<N>`.

## Open

## Settled
