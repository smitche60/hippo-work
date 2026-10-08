# ONTOLOGY — the entity types this brain holds

The single source of the directory set. RESOLVER.md routes against the tests below;
`tools/lint.py` reads this file for the directory list, the expected `type:` value, and any
allowed `status:` values. Nothing else states the set — change it here and the rest follows.

**Order is precedence.** RESOLVER works the blocks top to bottom and the first test that
passes claims the content.

A directory block is a `##` heading naming the directory, followed by its fields, each on
one line in the shape `` - **field:** value ``. `type:`
and `test:` are required; `status:`, `entry:` and `not:` are optional. `not:` names the nearest
neighbours and the boundary — the half of a resolver that says what does not go here.

## decisions
- **type:** decision
- **status:** active | superseded | reversed
- **test:** Someone — the owner or anyone else — chose between real alternatives, and the choice binds the owner's or their team's work. ("We went with the second vendor", "leadership chose not to fund the redesign" — yes. "The customer moved offices" — no; nobody chose between alternatives, that's a timeline line on the customer page.)
- **not:** A choice with no real alternative — a timeline line on the page it affected. A plan or a build is a project, even when it embeds choices. Who approved a decision is a State line on its page, not a reason to make a page for the approver.

## customers
- **type:** customer
- **status:** prospect | active | former
- **entry:** A page when there is something to say about the account beyond its contract — who the people are, what they are trying to do, how the relationship has moved, what is open. Until then the account lives as timeline lines on the pages it touched, however large the contract. The owner's call overrides the test in both directions.
- **test:** An external organisation the owner's team does business with, or is working to win, that clears the entry bar.
- **not:** A single interaction with an account — a timeline line. The work being done for the account — a project. A person at the account — a person, if they clear their own bar; otherwise a line on the customer page. A vendor or partner known only through one project — that project page carries them. The owner's own employer is never a customer; facts about it live on ME.md, projects, decisions, and topics.

## projects
- **type:** project
- **status:** active | complete | abandoned
- **test:** Ends by producing an outcome — a launch shipped, a migration finished, a renewal landed, a deal closed. A finished one keeps its page with `status: complete`.
- **not:** Something with no end — a topic. An occasion that ends by happening — an event. The account it is for — a customer. The choices made inside it that bind later work — decisions, each with its own page.

## people
- **type:** person
- **status:** active | archived
- **entry:** A page when there is something to say about the person beyond their title and the account or project they turned up in — how they work, what they care about, history with the owner, open threads. Until then they live as text in other pages' timelines, however often they appear or however senior they are. The owner's call overrides the test in both directions.
- **test:** A named human — colleague, customer contact, or anyone else — who clears the entry bar above.
- **not:** Anyone who fails the entry bar — a timeline line on the page they appeared in. Anything REDACTOR.md strips — never here either. The owner's direct reports — never a page, whatever they clear; they appear only as lines on the project, customer, and decision pages they touch (DESIGN.md, "Smaller choices").

## events
- **type:** event
- **status:** upcoming | held
- **entry:** A page only when preparing for it generates substantial context of its own — an agenda built, materials produced, positions worked out, follow-ups owed. An occasion that simply happens and is over is a timeline line on the pages it touched.
- **test:** Ends by occurring: a dated occasion the owner prepares for, attends, and refers back to as a unit (a business review, an offsite, a conference, a launch day) that clears the entry bar.
- **not:** A recurring meeting with no end date — a topic if it carries a line of thinking, otherwise a timeline line on the pages it touched. The account or project it was for — those pages carry the outcome. The decisions made there — decisions.

## topics
- **type:** topic
- **status:** active | archived
- **test:** An ongoing line of thinking with no end date — a market shift, a recurring internal debate, how the owner thinks a process should work, a competitor's trajectory. The current take above the line, how it evolved below.
- **not:** Anything with an end date — a project or an event. A single fact or opinion — a State line on the page it belongs to. An organisation — a customer.

# Root pages

Single pages outside the directory set, linted like any other page but exempt from the
directory/type match. lint reads this section: every list item must be exactly
`` - `FILE.md` — type `value` — status `a | b` `` (backticked filename, em dash, the word type,
backticked value, em dash, the word status, backticked allowed values). All three parts are
required. Directory names and type values are lowercase, and may contain digits, hyphens and
underscores. Both this section and
the next must exist; lint errors if either heading is missing. A list item here in any other shape is a lint error, so a reworded line can't
silently drop a page from linting.

- `ME.md` — type `me` — status `active | archived`
- `VOICE.md` — type `voice` — status `alpha | active`

# Non-content directories

Not part of the ontology; never linted as pages. lint reads this section too: every list
item must start `` - `name/` `` (backticked directory name with trailing slash). A
directory holding pages that appears in neither section is a lint error.

- `capture/` — pre-redaction landing pad, gitignored
- `drafts/` — what the work run made and the owner has not yet ruled on, gitignored
- `reports/` — dream reports, research digests, audits
- `docs/` — your own documents and notes, and the drafts you chose to keep
- `tools/` — lint and any other scripts
- `skills/` — the assistant's skills, when a kit ships them

# How to change this

Adding, removing, or renaming a type is an edit to this file plus a `git mv` of the
directory: RESOLVER.md points here rather than restating the set, and lint.py derives its
list from here. Three things inside a rename are easy to miss — the block's own `type:`
value, the singular name where other blocks' `not:` lines cross-reference it, and any prose
elsewhere that lists the set. Lint catches a wrong `type:` only once a page of that type
exists, so on an empty brain, check it by eye or write a throwaway page and lint that. Write down why — the set is a design
decision, and the reasons matter more than the list.

No catch-all directory. What fits nowhere stays in `capture/`, and persistent residue is
the signal to add a type rather than to force a bad fit.
