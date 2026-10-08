# REDACTOR — rules for what the brain may store

The sole stage that sees raw input. Stateless: each capture judged on its own text.
Guarantee (DESIGN.md “The redactor”): stripped content is never stored — not in pages, git history, the
archive, or reports. This table is the single source of the rules; loosening or tightening
it is the owner's edit here, nothing more.

## Verbs

- **pass** — store as-is.
- **strip** — remove the content; what remains is written without it.
- **abstract** — keep that the thing happened, drop the payload ("renewed at $1.2M"
  survives as "renewed; strategic tier"; the number does not).
- **flag** — hold for the owner's call before storing.

## Categories

Work content is in scope. The owner's personal life, other people's private situations, and
HR matters about named people are out. When one piece matches more than one row, the stricter verb
wins — flag > strip > abstract > pass: a human ruling beats an automatic deletion, and a
deletion beats a summary.

| Content | Verb |
|---|---|
| Credentials & secrets (passwords, keys, tokens, codes) | strip |
| Customer PII — end-user or contact personal data beyond name, role, and work contact details | strip |
| Anything privileged or under legal hold — the owner's counsel would want it out | strip |
| HR matters — anyone's performance reviews or ratings, salary, compensation, PIPs, disciplinary or medical leave, hiring or firing deliberations about a named person or candidate | strip |
| Healthcare — anyone's, including the owner's | strip |
| The owner's personal life (family, home, finances, health, anything outside work) | strip — belongs in a separate instance |
| Customer dollar figures — contract values, ARR, pricing, discounts | abstract — keep the tier or significance ("strategic, high-paying"), drop the number |
| Personal gossip and chit-chat — someone's private situation, relationships, or reputation, heard secondhand; small talk with no work content | strip |
| Business confidence — a customer's or colleague's confidential strategy, plans, or internal politics, however it reached the owner | flag — held; stored only if the owner says "store it" when asked, as a `[confidential]` line (RESOLVER.md); the assistant never stores it on its own initiative |
| Structural facts — who owns what, who approves, who reports to whom, how a decision gets made | pass |
| Financial context short of figures — tier, strategic weight, budget owner, renewal timing | pass |
| Targets and attainment — quota and results as numbers against plan, the owner's own and their team's. Not a review or a rating, which the HR row strips | pass |
| Headcount plans, open roles, and the hiring process itself — about roles, not named people | pass |
| Ordinary work content — projects, decisions, meetings, plans, opinions about work | pass |

## Procedure

1. Judge each distinct piece of a capture against the table; apply the matched verb. Two
   matches → the stricter verb, per the order above.
2. Uncertain whether a category applies → fail closed: the piece is not written. A capture
   with any uncertain piece is held whole in `capture/.quarantine/` (clean pieces wait with
   it) and counted. A watched-source file is never moved or copied — an uncertain piece
   there is simply skipped, listed in the report by folder and category only — the exact
   filename is told to the owner in conversation, never written to tracked files when the
   category is sensitive.
3. Flags likewise wait in `capture/.quarantine/` for the owner.
4. Report only category counts — never the redacted text.

## Quarantine

`capture/.quarantine/` holds raw refusals and flags until the owner rules (gitignored, like all
of capture/). Every dream report shows quarantine counts by category — counts only in
anything *stored*. When asking the owner to rule, show them the raw text in conversation: a
ruling requires seeing the item, and conversation display is not storage. Their override —
"store it" — is deliberate and final: re-run the item with the override noted. The override
lifts only the flag: strip and abstract rows still apply on the re-run, so a flagged item
that also held a credential or PII stores without them, and the guarantee at the top of this
file holds whatever the owner rules. When the override stores a business confidence, the
line it produces carries `[confidential]` after the date (RESOLVER.md, page anatomy), so
every such line in the brain is one grep away and can be reviewed or removed as a set. Rising counts in one category mean this table may be too conservative there:
say so in the report, and the owner decides whether to edit the row above.
