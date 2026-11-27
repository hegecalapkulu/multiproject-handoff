#!/usr/bin/env python3
"""multiproject-handoff scanner: gathers in ONE call what the skills would
otherwise read file by file (fewer agent steps = lower cost, same information).

  python3 mph-scan.py                 dashboard data for every project
  python3 mph-scan.py load <name>     everything mph-resume reads for one project
  python3 mph-scan.py facts <name>    git facts mph-handoff needs for one project

Read-only. Standard library only. Works on macOS, Linux and Windows
(use `python` instead of `python3` where that is the command).
"""
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path

MARK = re.compile(r"^<!--\s*mph:project\s+(.+?)\s*-->")
SKIP = {"node_modules", ".git", "vendor", "dist", "build", ".obsidian", ".venv", "__pycache__", ".claude"}
DATE_LABEL = re.compile(r"(last updated|son güncelleme|güncelleme|updated)\W{0,6}(.{0,40})", re.I)
MONTHS = {m: i + 1 for i, names in enumerate([
    ("jan", "january", "ocak"), ("feb", "february", "şubat", "subat"), ("mar", "march", "mart"),
    ("apr", "april", "nisan"), ("may", "mayıs", "mayis"), ("jun", "june", "haziran"),
    ("jul", "july", "temmuz"), ("aug", "august", "ağustos", "agustos"), ("sep", "sept", "september", "eylül", "eylul"),
    ("oct", "october", "ekim"), ("nov", "november", "kasım", "kasim"), ("dec", "december", "aralık", "aralik"),
]) for m in names}


def parse_date(text):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.search(r"(\d{1,2})\.?\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\s+(\d{4})", text)
    if m and m.group(2).lower() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS[m.group(2).lower()], int(m.group(1)))
    m = re.search(r"([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})", text)
    if m and m.group(1).lower() in MONTHS:
        return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2)))
    return None
TODAY = dt.date.today()


def read(p, limit=None):
    try:
        with open(p, encoding="utf-8", errors="replace") as f:
            return f.read() if limit is None else "".join(f.readline() for _ in range(limit))
    except OSError:
        return ""


def marker(p):
    m = MARK.match(read(p, 1))
    return m.group(1) if m else None


def find_projects(root):
    root = Path(root).resolve()
    lists = [root / "PROJECTS.md", Path.home() / ".handoff" / "PROJECTS.md"]
    found = {}
    for lst in lists:
        if not lst.is_file():
            continue
        for line in read(lst).splitlines():
            m = re.match(r"\s*-\s*([^:]+):\s*(.+?)\s*$", line)
            if not m:
                continue
            base = Path(os.path.expanduser(m.group(2)))
            base = base if base.is_absolute() else (lst.parent / base)
            for pm in walk(base, 2):
                found[pm.resolve()] = marker(pm)
        if found:
            return found
    for pm in walk(root, 4):
        found[pm.resolve()] = marker(pm)
    return found


def walk(base, depth):
    base = Path(base)
    if not base.is_dir():
        return
    stack = [(base, 0)]
    while stack:
        d, lvl = stack.pop()
        pm = d / "PROJECT.md"
        if pm.is_file() and marker(pm):
            yield pm
        if lvl >= depth:
            continue
        try:
            for c in sorted(d.iterdir()):
                if c.is_dir() and c.name not in SKIP:
                    stack.append((c, lvl + 1))
        except OSError:
            pass


def table_path(text, labels, default):
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and any(cells[0].lower().startswith(l) for l in labels):
            m = re.search(r"`([^`]+)`", cells[1])
            if m:
                return m.group(1).strip()
    return default


def project_info(pm):
    notes = pm.parent
    text = read(pm)
    def res(rel):
        p = Path(os.path.expanduser(rel))
        return p if p.is_absolute() else (notes / p).resolve()
    resume = res(table_path(text, ["resume", "devam"], "RESUME.md"))
    backlog = res(table_path(text, ["backlog"], "BACKLOG.md"))
    code = res(table_path(text, ["code", "kod"], ".."))
    stale = re.search(r"stale[^`\n]*`(\d+)`", text)
    return {"name": marker(pm), "pm": pm, "notes": notes, "text": text, "resume": resume,
            "backlog": backlog, "code": code, "stale": int(stale.group(1)) if stale else 14}


def note_date(p):
    for line in read(p, 20).splitlines():
        m = DATE_LABEL.search(line)
        if m:
            try:
                d = parse_date(m.group(2))
            except ValueError:
                d = None
            if d:
                return d, "note"
    try:
        return dt.date.fromtimestamp(p.stat().st_mtime), "file date"
    except OSError:
        return None, "unknown"


def now_section(p, full=False):
    lines, take, out = read(p).splitlines(), False, []
    for ln in lines:
        if ln.startswith("#"):
            if take:
                break
            take = bool(re.match(r"#+\s*(now|şimdi|in progress|doing|todo)\b", ln, re.I))
            continue
        if take and ln.strip():
            out.append(ln)
    if not out:  # no "Now" heading: first list items of the file
        out = [l for l in lines if re.match(r"\s*[-*]\s|\s*\d+\.\s", l)][:3]
    return out if full else out[:1]


def git(code, *args):
    try:
        r = subprocess.run(["git", "-C", str(code), *args], capture_output=True, text=True, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def since_note(i):
    """Work done after the resume note was last written, i.e. a session that
    ended without a handoff. Returns (commits, latest commit subject, uncommitted
    or changed files, how it was measured), or None if nothing can be told."""
    code, resume, notes = i["code"], i["resume"], i["notes"]
    if not resume.is_file():
        return None
    if git(code, "rev-parse", "--is-inside-work-tree"):
        # the last commit that touched the resume note marks the last handoff
        # (works when the notes live in the same repo; otherwise the note's date is used)
        last = git(resume.parent, "log", "-1", "--format=%H", "--", resume.name)
        same_repo = bool(last) and subprocess_ok(code, "merge-base", "--is-ancestor", last, "HEAD")
        # only this project's folder counts (a repo can hold several projects), and
        # changes to the notes themselves are the handoff, not unsaved work
        try:
            rel_notes = str(notes.relative_to(code)).replace(os.sep, "/")
        except ValueError:
            rel_notes = None
        spec = ["--", "."] + ([f":(exclude){rel_notes}"] if rel_notes and rel_notes != "." else [])
        if same_repo:
            log = git(code, "log", "--format=%s", f"{last}..HEAD", *spec)
        else:
            d, _ = note_date(resume)
            log = git(code, "log", "--format=%s", f"--since={d.isoformat()} 23:59", *spec) if d else ""
        commits = log.splitlines() if log else []
        dirty = [l for l in git(code, "status", "--short", *spec).splitlines() if l.strip()]
        return len(commits), (commits[0] if commits else ""), len(dirty), "git"
    # no git: files in the code folder changed after the resume note (the notes folder itself does not count)
    try:
        since = resume.stat().st_mtime
    except OSError:
        return None
    changed, seen, stack = 0, 0, [(code, 0)]
    while stack and seen < 3000:
        d, lvl = stack.pop()
        try:
            entries = list(os.scandir(d))
        except OSError:
            continue
        for e in entries:
            seen += 1
            if e.name.startswith(".") or e.name in SKIP:
                continue
            p = Path(e.path)
            if e.is_dir(follow_symlinks=False):
                if lvl < 4 and p.resolve() != notes:
                    stack.append((p, lvl + 1))
            elif e.is_file(follow_symlinks=False):
                try:
                    if e.stat().st_mtime > since + 60:
                        changed += 1
                except OSError:
                    pass
    return 0, "", changed, "files"


def subprocess_ok(code, *args):
    try:
        return subprocess.run(["git", "-C", str(code), *args], capture_output=True, timeout=15).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def since_line(s):
    """One line for the scanner output, or '' when nothing happened after the note."""
    if not s:
        return ""
    commits, latest, files, how = s
    if how == "files":
        return f"since note: {files} file{'s' if files > 1 else ''} changed (no git)" if files else ""
    parts = []
    if commits:
        parts.append(f"{commits} commit{'s' if commits > 1 else ''} (latest: {latest[:80]})")
    if files:
        parts.append(f"{files} uncommitted change{'s' if files > 1 else ''}")
    return "since note: " + ", ".join(parts) if parts else ""


def first_state_line(p):
    take = False
    for ln in read(p, 40).splitlines():
        if ln.startswith("#"):
            take = bool(re.match(r"#+\s*(where we are|nerede|durum|status)", ln, re.I))
            continue
        if take and ln.strip().startswith(("-", "*", "1.")):
            t = re.sub(r"^\s*([-*]|\d+\.)\s*", "", ln).strip()
            return t[:157] + "..." if len(t) > 160 else t
    for ln in read(p, 40).splitlines():
        if ln.strip() and not ln.startswith(("#", ">", "<!--")) and not DATE_LABEL.search(ln):
            return ln.strip()
    return "(empty)"


def find(name, projects):
    name = name.lower()
    for pm, n in projects.items():
        if n and n.lower() == name:
            return pm
    hits = [pm for pm, n in projects.items() if n and n.lower().startswith(name)]
    return hits[0] if len(hits) == 1 else None


def dashboard(projects):
    rows = []
    for pm in projects:
        i = project_info(pm)
        d, src = note_date(i["resume"])
        age = (TODAY - d).days if d else None
        rows.append((d or dt.date.min, i, age, src))
    rows.sort(key=lambda r: r[0], reverse=True)
    print(f"PROJECTS {len(rows)} (today {TODAY.isoformat()})")
    for d, i, age, src in rows:
        stale = " STALE" if age is not None and age > i["stale"] else ""
        print(f"\n## {i['name']}")
        print(f"updated: {d.isoformat() if age is not None else 'unknown'} ({age} days ago, from {src}){stale}")
        print(f"state: {first_state_line(i['resume'])}")
        now = now_section(i["backlog"])
        item = re.sub(r"^\s*([-*]|\d+\.)\s*(\[.\]\s*)?", "", now[0]).strip() if now else "(none)"
        print("now: " + (item[:157] + "..." if len(item) > 160 else item))
        line = since_line(since_note(i))
        if line:
            print(line + " NOT HANDED OFF")
        print(f"notes: {i['notes']}")


def load(pm):
    i = project_info(pm)
    print(f"# PROJECT {i['name']}\nnotes folder: {i['notes']}\ncode folder: {i['code']}\n")
    print("=== PROJECT.md\n" + i["text"].strip())
    m = re.search(r"Also follow:\s*`?([^`\n]+)`?", i["text"])
    if m:
        extra = (i["notes"] / m.group(1).strip()).resolve()
        print(f"\n=== Also follow: {extra}\n" + read(extra).strip())
    print(f"\n=== RESUME NOTE {i['resume']}\n" + (read(i["resume"]).strip() or "(missing)"))
    print(f"\n=== BACKLOG NOW {i['backlog']}\n" + ("\n".join(now_section(i["backlog"], full=True)) or "(none)"))
    for p in [Path.home() / ".handoff" / "working-style.md", *sorted(i["notes"].glob("working-style*.md"))]:
        if p.is_file():
            print(f"\n=== WORKING STYLE {p}\n" + read(p).strip())
    d, _ = note_date(i["resume"])
    last = git(i["code"], "log", "-1", "--format=%cs")
    s = since_note(i)
    if last and d:
        n = s[0] if s else 0
        print(f"\n=== DRIFT\nlast commit {last}; note {d.isoformat()}; commits after the note: {n}")
    line = since_line(s)
    if line:
        print(f"\n=== NOT HANDED OFF\n{line}\n(the last session ended without mph-handoff; offer a catch-up from git)")


def facts(pm):
    i = project_info(pm)
    c = i["code"]
    print(f"# FACTS {i['name']} (code: {c})")
    if not git(c, "rev-parse", "--is-inside-work-tree"):
        print("not a git repo")
        return
    print("=== git status --short\n" + (git(c, "status", "--short") or "(clean)"))
    print("=== git diff --stat\n" + (git(c, "diff", "--stat") or "(no unstaged changes)"))
    d, _ = note_date(i["resume"])
    since = [f"--since={d.isoformat()}"] if d else ["-10"]
    print(f"=== commits since the resume note ({d})\n" + (git(c, "log", "--oneline", *since) or "(none)"))
    print("=== branch / remote\n" + git(c, "branch", "--show-current") + " · " + (git(c, "remote") or "no remote"))


def main():
    args = sys.argv[1:]
    projects = find_projects(os.getcwd())
    if not projects:
        print("NO PROJECTS (no PROJECT.md with an mph:project marker found)")
        return
    if not args:
        return dashboard(projects)
    if len(args) == 2 and args[0] in ("load", "facts"):
        pm = find(args[1], projects)
        if not pm:
            print("NO MATCH for " + args[1] + "; projects: " + ", ".join(sorted(filter(None, projects.values()))))
            return
        return load(pm) if args[0] == "load" else facts(pm)
    print(__doc__)


if __name__ == "__main__":
    main()
