#!/usr/bin/env python3
"""Hippo strict lint. Exit 0 = clean. Run from repo root.

The directory set is NOT stated here — it is read from ONTOLOGY.md, which is the single
source. Adding or renaming a type is an edit to that file plus a git mv.
"""
import os, re, sys, subprocess
errs = []

ONTOLOGY = "ONTOLOGY.md"

def load_ontology(path=ONTOLOGY):
    """-> (dirs: {name: {type,test,status?,entry?,not?}}, roots: {file: {type,status?}}, noncontent: set)

    Insertion order of `dirs` is RESOLVER's precedence order.
    """
    dirs, roots, noncontent = {}, {}, set()
    seen_sections = set()
    if not os.path.exists(path):
        errs.append(f"{path} missing — it is the source of the directory set")
        return dirs, roots, noncontent
    block = None       # current ## directory block
    section = None     # current # top-level section, by title
    for lineno, line in enumerate(open(path), 1):
        top = re.match(r"^#\s+(\S.*?)\s*$", line)
        if top:                                    # a top-level section ends any block
            section, block = top.group(1), None
            seen_sections.add(section.lower())
            continue
        head = re.match(r"^##\s+([a-z][a-z0-9_-]*)\s*$", line)
        if head:
            block = head.group(1)
            dirs.setdefault(block, {})
            continue
        field = re.match(r"^-\s+\*\*(type|status|test|entry|not):\*\*\s*(.+?)\s*$", line)
        if field and block:
            dirs[block][field.group(1)] = field.group(2)
            continue
        if block is None and section and line.startswith("- "):
            # The two sections lint reads have a fixed line shape; anything else is an error,
            # so a reworded line cannot silently drop a page or a directory from linting.
            if section.lower().startswith("root pages"):
                root = re.match(r"^-\s+`([A-Za-z0-9_.-]+\.md)`\s+—\s+type\s+`([a-z0-9_-]+)`\s+—\s+status\s+`([^`]+)`\s*$", line)
                if root: roots[root.group(1)] = {"type": root.group(2), "status": root.group(3)}
                else: errs.append(f"{path}:{lineno}: Root pages line not in the form - `FILE.md` — type `value` — status `a | b`")
            elif section.lower().startswith("non-content"):
                nc = re.match(r"^-\s+`([a-z0-9_-]+)/`(?:\s+—.*)?\s*$", line)
                if nc: noncontent.add(nc.group(1))
                else: errs.append(f"{path}:{lineno}: Non-content line not in the form - `name/` — note")
    for needed in ("root pages", "non-content directories"):
        if not any(s.startswith(needed) for s in seen_sections):
            errs.append(f"{path}: required section '# {needed[0].upper() + needed[1:]}' is missing — pages there would silently go unlinted")
    for d in [d for d, v in dirs.items() if "type" not in v or "test" not in v]:
        errs.append(f"{path}: directory block '{d}' is missing type: or test:")
        dirs.pop(d)
    return dirs, roots, noncontent

ONT, ROOTS, NONCONTENT = load_ontology()
CONTENT_DIRS = list(ONT)
ROOT_PAGES = list(ROOTS)

# a declared type with no directory is the mirror failure: pages routed there have nowhere
# to land, and a clean lint on an empty brain would never say so
for d in CONTENT_DIRS:
    if not os.path.isdir(d):
        errs.append(f"{ONTOLOGY} declares '{d}' but the directory '{d}/' does not exist")

# a content directory on disk that ONTOLOGY.md doesn't declare is silent drift
for entry in sorted(os.listdir(".")):
    if not os.path.isdir(entry) or entry.startswith("."):
        continue
    if entry in CONTENT_DIRS or entry in NONCONTENT:
        continue
    if any(f.endswith(".md") for _, _, fs in os.walk(entry) for f in fs):
        errs.append(f"directory '{entry}/' holds pages but is not declared in {ONTOLOGY}")

pages = [os.path.join(r, f) for d in CONTENT_DIRS if os.path.isdir(d)
         for r, _, fs in os.walk(d) for f in fs if f.endswith(".md")] + [p for p in ROOT_PAGES if os.path.exists(p)]
FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
STAMP = re.compile(r"↞ (\d{4}-\d{2}-\d{2}-[0-9a-f]{8}|v1-build)")
all_aliases, slugs = {}, {}
for p in pages:
    t = open(p).read()
    m = FM.match(t)
    if not m: errs.append(f"{p}: no frontmatter"); continue
    fm = m.group(1); body = t[m.end():]
    for field in ("type:", "status:", "aliases:", "updated:"):
        if field not in fm: errs.append(f"{p}: frontmatter missing {field[:-1]}")
    mu = re.search(r"updated:\s*(\S+)", fm)
    if mu and not DATE.fullmatch(mu.group(1)): errs.append(f"{p}: bad updated date '{mu.group(1)}'")
    # type must match what ONTOLOGY.md declares for this page's home
    mt = re.search(r"type:\s*(\S+)", fm)
    d = p.split(os.sep)[0] if os.sep in p else ""      # the declaring directory, however deep the page sits
    want = ONT.get(d, {}).get("type") if d else ROOTS.get(os.path.basename(p), {}).get("type")
    if mt and want and mt.group(1) != want:
        errs.append(f"{p}: type '{mt.group(1)}' but {ONTOLOGY} declares '{want}' for {d or 'root'}")
    # status must be one of the values ONTOLOGY.md allows, when it constrains them
    allowed = ONT.get(d, {}).get("status") if d else ROOTS.get(os.path.basename(p), {}).get("status")
    if allowed:
        ok = [v.strip() for v in allowed.split("|")]
        ms = re.search(r"status:\s*(\S+)", fm)
        if ms and ms.group(1) not in ok:
            errs.append(f"{p}: status '{ms.group(1)}' not in {' | '.join(ok)} (per {ONTOLOGY})")
    sep = body.find("\n---\n"); tlpos = body.find("## Timeline")
    if sep < 0: errs.append(f"{p}: no truth/timeline separator")
    if tlpos < 0: errs.append(f"{p}: no Timeline section")
    if sep >= 0 and tlpos >= 0 and tlpos < sep: errs.append(f"{p}: Timeline must come after the --- separator")
    if not re.search(r"^# \S", body[:sep if sep >= 0 else len(body)], re.M):
        errs.append(f"{p}: no `# Name` heading above the separator")
    tl = body.split("## Timeline", 1)[-1]
    if tlpos >= 0 and not re.search(r"^- \d{4}-\d{2}-\d{2}", tl, re.M):
        errs.append(f"{p}: empty section '## Timeline' (a page needs its creation entry)")
    for line in tl.splitlines():
        if line.startswith("- ") and not re.match(r"- \d{4}-\d{2}-\d{2}", line):
            errs.append(f"{p}: timeline entry without leading date: {line[:50]}")
    dates = re.findall(r"^- (\d{4}-\d{2}-\d{2})", tl, re.M)
    if dates != sorted(dates, reverse=True):
        errs.append(f"{p}: timeline not reverse-chronological: {dates}")
    entries = re.split(r"\n(?=- \d{4})", tl.strip())
    for e in entries:
        if e.startswith("- ") and "↞ " not in e:
            errs.append(f"{p}: unstamped timeline entry: {e[:60]}")
    if mu and dates and mu.group(1) < max(dates):
        errs.append(f"{p}: updated {mu.group(1)} older than newest timeline entry")
    for s in re.findall(r"↞ \S+", body):
        if not STAMP.match(s): errs.append(f"{p}: malformed stamp '{s[:40]}'")
    lines = [l for l in body.splitlines() if l.strip()]
    for i, l in enumerate(lines[:-1]):
        if l.startswith("## ") and (lines[i+1].startswith("## ") or lines[i+1] == "---"):
            errs.append(f"{p}: empty section '{l.strip()}' (omit empty sections)")
    for link in ([] if p == "VOICE.md" else re.findall(r"\[\[([^\]|]+)(?:\|[^\]]*)?\]\]", t)):   # VOICE.md quotes real messages
        tgt = link if link.endswith(".md") else link + ".md"
        if not os.path.exists(tgt): errs.append(f"{p}: dangling wikilink [[{link}]]")
    base = os.path.basename(p)
    slugs.setdefault(base, []).append(p)
    am = re.search(r"aliases:\s*\[(.*?)\]", fm, re.S)
    for a in re.findall(r'[\'"]([^\'"]+)[\'"]', am.group(1) if am else ""):
        all_aliases.setdefault(a.lower(), []).append(p)
for base, ps in slugs.items():
    if len(ps) > 1: errs.append(f"duplicate slug {base}: {ps}")
for a, ps in all_aliases.items():
    if len(set(ps)) > 1: errs.append(f"alias '{a}' on multiple pages: {sorted(set(ps))}")
def tracked(pathspec):
    return subprocess.run(["git", "ls-files", pathspec], capture_output=True, text=True).stdout.strip()
remotes = subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.split()
has_content = any(p.split(os.sep)[0] in CONTENT_DIRS for p in pages if os.sep in p)
if remotes and has_content:
    errs.append(f"this repo holds pages and has a remote configured ({', '.join(remotes)}) — "
                "a brain is never pushed; see the no-remote rule in the operating rules")
# A brain must carry both push guards. "Brain" here means: this is a git repo, it has no
# remote, and ME.md has been filled in (the kit ships ME.md with installer prose, and the
# install replaces it before the first commit). A kit, or a tarball copy with no .git, is
# not checked. Fix text is addressed to the owner: the assistant never touches .git/hooks/.
def _me_is_template():
    try: return "Replace this paragraph" in open("ME.md").read()
    except OSError: return True
is_brain = os.path.isdir(".git") and not remotes and not _me_is_template()
if is_brain:
    for hook in ("pre-push", "pre-commit"):
        hp = os.path.join(".git", "hooks", hook)
        if not (os.path.isfile(hp) and os.access(hp, os.X_OK)):
            errs.append(f".git/hooks/{hook} missing or not executable — a push guard from "
                        f"INSTALL.md's guards step is gone. Owner: `cp tools/hooks/{hook} .git/hooks/ "
                        f"&& chmod +x .git/hooks/{hook}`. The assistant stops here and does not do this.")
if tracked("capture/"): errs.append(f"capture/ files tracked by git: {tracked('capture/').splitlines()[:3]}")
if tracked("drafts/"): errs.append(f"drafts/ files tracked by git (must be gitignored — unreviewed work-run output): {tracked('drafts/').splitlines()[:3]}")
# drafts/ must be ignored, not merely untracked: an unignored folder is one `git add -A` from history
if os.path.isdir(".git") and subprocess.run(["git", "check-ignore", "-q", "drafts/x.md"]).returncode != 0:
    errs.append("drafts/ is not gitignored — add `drafts/` to .gitignore before the next commit")

def lint_questions(p="QUESTIONS.md"):
    """The header of QUESTIONS.md is the rule for the file; check it is whole and the ids are sane."""
    if not os.path.exists(p):
        if os.path.exists("WORK.md") or os.path.exists("BRIEF.md"):
            errs.append(f"{p} missing — BRIEF.md and WORK.md depend on it; restore it from the kit")
        return
    lines = open(p).read().splitlines()
    heads = [l.strip() for l in lines if l.startswith("## ")]
    want = ["## What earns a question", "## Cross-checking", "## Writing an entry", "## Asking",
            "## Applying an answer", "## Open", "## Settled"]
    if heads != want:
        errs.append(f"{p}: headings are {heads}; expected {want} — the header is the rule for the file, restore it from the kit")
        return
    nid = [m for m in (re.fullmatch(r"next-id:\s*(\d+)\s*", l) for l in lines) if m]
    if len(nid) != 1:
        errs.append(f"{p}: needs exactly one `next-id: <number>` line")
        return
    nxt = int(nid[0].group(1))
    ids = [int(m.group(1)) for l in lines[lines.index("## Open"):] for m in [re.match(r"- \[Q(\d+)\]", l)] if m]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup: errs.append(f"{p}: ids used more than once: {dup}")
    if ids and max(ids) >= nxt: errs.append(f"{p}: next-id {nxt} is not above the highest id in use ({max(ids)})")
lint_questions()

def fence_of(path):
    """The fence block as one normalised line, or None."""
    try: ls = open(path).read().splitlines()
    except OSError: return None
    out, on = [], False
    for l in ls:
        if l.startswith("> **The fence.**"): on = True
        if on:
            if l.startswith(">"): out.append(l[1:])
            else: break
    return " ".join(" ".join(out).split()) or None
# The fence is the one rule stated in more than one file; every copy must match AGENTS.md's.
if os.path.exists("WORK.md") or os.path.exists("BRIEF.md"):
    ref = fence_of("AGENTS.md")
    if ref is None:
        errs.append("AGENTS.md has no fence block (`> **The fence.** …`) — restore it from the kit")
    else:
        carriers = [p for p in ("BRIEF.md", "WORK.md") if os.path.exists(p)]
        if os.path.isdir("skills"):
            carriers += sorted(os.path.join("skills", d, "SKILL.md") for d in os.listdir("skills")
                               if os.path.isfile(os.path.join("skills", d, "SKILL.md")))
        for p in carriers:
            if fence_of(p) != ref:
                errs.append(f"{p}: the fence block is missing or differs from AGENTS.md's — copy it across word for word")
if tracked(".dream-state.json"): errs.append(".dream-state.json is tracked by git (must be gitignored)")
if errs:
    print(f"LINT: {len(errs)} finding(s)")
    for e in errs: print(" -", e)
    sys.exit(1)
print(f"LINT: clean ({len(pages)} pages, {len(CONTENT_DIRS)} types from {ONTOLOGY})")
