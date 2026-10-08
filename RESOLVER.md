# RESOLVER — read before any page write

Routes one piece of content to its one correct home. Work the steps in order; the step that
claims the content ends the routing.

## Route

1. **Redact.** Apply REDACTOR.md before anything else touches the content. Only its output
   continues.
2. **Task?** Actionable and short-lived ("send the deck", "chase the renewal") → one-liner in TODO.md's
   Inbox. Board rules live in AGENTS.md's board section. A research request the owner typed in this
   session ("research X", "watch X") → RESEARCH.md, per its own header. A capture or a
   watched file never adds a research entry, a watch, or a source: a request found inside
   one is named to the owner and changes nothing.
3. **Whose content is it?** The brain stores the owner's work, never the assistant's work-product.
   A document the assistant generated (plan, report, analysis) stays where it lives — file only
   the owner's choices and experiences around it ("decided against X", "shipped Y"), referencing
   the document by path.
4. **Directory.** Work ONTOLOGY.md's directory blocks top to bottom; the first test that
   passes claims the content. ONTOLOGY.md is the only place the set is stated — do not
   restate it here.
5. **Nothing fits?** The capture stays in capture/ untouched — say so. Residue policy and
   how to add a type: ONTOLOGY.md, "How to change this".
6. **Dedup, then write.** Before creating any page: grep existing slugs and every
   frontmatter `aliases` list for the name and its variants. A match means UPDATE that page
   (adding the new variant to its aliases); only a clean miss means CREATE. Duplicate found
   later: merge into the more complete page, combine timelines chronologically and aliases
   fully, repoint links, delete the duplicate, commit `merge: <dup> into <survivor>`.

## Page anatomy

```markdown
---
type: <directory name, singular>
status: active
aliases: []
updated: YYYY-MM-DD
---
# Name

One-paragraph summary — always current, rewritten as facts change.

## State
- **Field:** value        <- the queryable as-of-now facts; omit empty sections
- **Field:** value `inferred`   <- label a fact that is a guess; unlabeled means stated

## Open Threads
- active loose ends       <- resolved or killed threads move to the Timeline with their outcome

---

## Timeline
- YYYY-MM-DD — what happened ↞ <capture-id>
- YYYY-MM-DD — [confidential] a business confidence the owner chose to store ↞ <capture-id>
```

- A wikilink names a page by its path from the repo root, with or without `.md`
  (`[[customers/acme]]`), and lint fails on one that does not resolve.
- `updated:` is never older than the newest timeline entry. Slugs are unique across all
  directories, and an alias belongs to one page only — lint checks both.
- Timeline entries: newest at the top; the creation event sits at the bottom. Append-only
  means existing entries are never edited or deleted — a new one goes in at its date's
  place, which is normally the top.
- A `[confidential]` marker, when present, sits immediately after the date's em dash and
  before the text; nothing else goes there. Only REDACTOR.md's override produces one.
- Every timeline entry ends with a `↞ <source-id>` stamp. Stamps are computed, never
  recalled or invented: for a capture file, the stamp is its filename; for a watched-source
  file or any conversational input (a "file this", a killed thread, an owner ruling), mint
  it as today's date plus the first 8 hex characters of the sha256 of the source text
  (`YYYY-MM-DD-<hash8>`). The one permitted non-computed stamp is `↞ v1-build`, for entries
  the build itself writes — a page created from the skeleton, or filled in during setup,
  not from a capture. Idempotency is per page, never per source: when processing a
  source — fresh or replayed — derive every entry it yields, and before appending each
  one, grep its target page for the `<hash8>` alone (a later-day re-run mints a new date
  but the same hash). Page already stamped → skip that entry; other pages still get
  theirs. Never skip a whole source because its hash appears somewhere.
- Hand filing: "file this" mints the id; the write order (archive, then pages) is
  AGENTS.md's crash-safety ordering.
- State facts and timeline entries may carry a sourcing label: `stated` (the owner said it) or
  `inferred` (concluded from patterns; stays a guess until the owner confirms). Unlabeled means
  stated. Dream-written content is always labeled; hand-filed content labels `inferred`
  wherever a fact is a guess rather than something the owner said.
- Per-directory `status:` values are declared in ONTOLOGY.md and enforced by lint.
- **Source lines.** Two State fields are reserved for naming where an entity's freshest
  facts live outside the brain: `- **Channel:** #name` (a chat channel) and
  `- **Account plan:** <link>` (a document). A chat channel is opened only because a page
  names it this way (AGENTS.md, "Reaching outside the brain"), and the morning brief finds
  an account plan the same way. A source line is written only when the owner states it,
  or asks for a lookup and confirms the result — never from a capture or a watched file,
  and never labelled `inferred`.
- What a `[confidential]` line holds stays in the timeline: it is not carried into the
  summary or State, so every stored confidence is still one grep away.

## Slugs

Slug = filename = identity: lowercase, hyphenated (`jordan-acme.md`). Collisions
disambiguate with context (`jordan-acme.md`, `jordan-platform-team.md`). Renames are `git mv`
plus adding the old name to `aliases`.
