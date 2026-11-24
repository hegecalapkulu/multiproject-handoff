#!/usr/bin/env python3
"""Uninstall multiproject-handoff. Run through:  ./install.sh --uninstall [options]

Nothing is deleted. Everything this tool installed is MOVED to
~/.handoff-removed/<date-time>/, so it can be restored; delete that folder
yourself once you are sure. Your project notes are never touched.

  --dry-run          show what would happen, change nothing
  --yes              do not ask before changing anything (for agents and scripts)
  --project DIR      also look in one project's skill folders
  --dir PATH         also look in a skills folder you name
  --agents-md DIR    also remove the multiproject-handoff block from DIR/AGENTS.md
"""
import argparse, json, os, shutil, sys, time

MARK = ".multiproject-handoff"
HOME = os.path.expanduser("~")
HANDOFF = os.path.join(HOME, ".handoff")
OUR_FILES = ["RULES.md", "mph-guard.py", "mph-scan.py", "mph-context.py", "guard.conf"]
HOOK_SCRIPTS = ("mph-guard.py", "mph-context.py")


def args():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--uninstall", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--project", action="append", default=[])
    p.add_argument("--dir", action="append", default=[])
    p.add_argument("--agents-md", action="append", default=[])
    p.add_argument("-h", "--help", action="store_true")
    a = p.parse_args()
    if a.help:
        print(__doc__.strip()); sys.exit(0)
    return a


def skill_folders(a):
    roots = [os.path.join(HOME, x) for x in (
        ".claude/skills", ".codex/skills", ".agents/skills", ".gemini/skills",
        ".gemini/antigravity/skills", ".handoff/skills")]
    for d in a.project:
        roots += [os.path.join(d, x) for x in (".claude/skills", ".agents/skills", ".gemini/skills")]
    roots += a.dir
    found = []
    for r in roots:
        if not os.path.isdir(r):
            continue
        for name in sorted(os.listdir(r)):
            f = os.path.join(r, name)
            if os.path.isfile(os.path.join(f, MARK)):   # only folders our installer marked
                found.append(f)
    return found


def handoff_files():
    ours, kept = [], []
    if not os.path.isdir(HANDOFF):
        return ours, kept
    for name in sorted(os.listdir(HANDOFF)):
        f = os.path.join(HANDOFF, name)
        if name == "RULES.md":
            with open(f, encoding="utf-8", errors="replace") as fh:
                (ours if "multiproject-handoff RULES" in fh.readline() else kept).append(f)
        elif name in OUR_FILES:
            ours.append(f)
        elif name != "skills":            # its marked skills are handled above
            kept.append(f)
    return ours, kept


def settings_plan():
    path = os.path.join(HOME, ".claude", "settings.json")
    if not os.path.isfile(path):
        return None, None, 0
    try:
        data = json.load(open(path, encoding="utf-8"))
    except ValueError:
        return path, None, -1
    removed = 0
    hooks = data.get("hooks", {})
    for event in list(hooks):
        groups = []
        for g in hooks[event]:
            inner = [h for h in g.get("hooks", [])
                     if not any(s in str(h.get("command", "")) and ".handoff" in str(h.get("command", ""))
                                for s in HOOK_SCRIPTS)]
            removed += len(g.get("hooks", [])) - len(inner)
            if inner:
                g = dict(g, hooks=inner); groups.append(g)
            elif not g.get("hooks"):
                groups.append(g)
        if groups:
            hooks[event] = groups
        else:
            del hooks[event]
    if "hooks" in data and not hooks:
        del data["hooks"]
    return path, data, removed


def agents_blocks(a):
    out = []
    for d in a.agents_md:
        f = os.path.join(d, "AGENTS.md")
        if os.path.isfile(f):
            s = open(f, encoding="utf-8").read()
            i, j = s.find("<!-- multiproject-handoff:start -->"), s.find("<!-- multiproject-handoff:end -->")
            if i != -1 and j > i:
                out.append((f, s[:i].rstrip("\n") + "\n" + s[j + len("<!-- multiproject-handoff:end -->"):].lstrip("\n")))
    return out


def main():
    a = args()
    skills = skill_folders(a)
    ours, kept = handoff_files()
    spath, sdata, nhooks = settings_plan()
    blocks = agents_blocks(a)
    backup = os.path.join(HOME, ".handoff-removed", time.strftime("%Y%m%d-%H%M%S"))
    short = lambda p: p.replace(HOME, "~", 1)

    print("multiproject-handoff uninstall\n")
    if not (skills or ours or nhooks > 0 or blocks):
        print("Nothing to remove: no installed skills, hooks or shared files found.")
        print("(Claude Code plugin? Type: /plugin uninstall multiproject-handoff)")
        return
    if skills:
        print(f"Move {len(skills)} skill folder(s):")
        by_root = {}
        for f in skills:
            by_root.setdefault(os.path.dirname(f), []).append(os.path.basename(f))
        for root, names in by_root.items():
            print(f"   {short(root)}/  {len(names)}: {', '.join(names)}")
    if ours:
        print("Move shared files:", ", ".join(short(f) for f in ours))
    if nhooks > 0:
        print(f"Remove {nhooks} hook entr{'y' if nhooks == 1 else 'ies'} (guard / long-conversation note) from {short(spath)}; a copy is kept")
    if nhooks == -1:
        print(f"Note: {short(spath)} is not valid JSON; left unchanged. Remove the .handoff hook entries by hand.")
    for f, _ in blocks:
        print(f"Remove the multiproject-handoff block from {short(f)}; a copy is kept")
    print(f"\nEverything goes to {short(backup)}/ (nothing is deleted).")
    print("Not touched: your project notes (PROJECT.md, resume notes, decisions, logs) stay as plain Markdown.")
    if kept:
        print("Kept, they are yours:", ", ".join(short(f) for f in kept))

    if a.dry_run:
        print("\n(dry run: nothing was changed)"); return
    if not a.yes:
        try:
            ans = input("\nProceed? [y/N] ").strip().lower()
        except EOFError:
            ans = ""
        if ans not in ("y", "yes"):
            print("Nothing changed."); return

    def keep_copy(src):
        dst = os.path.join(backup, os.path.relpath(src, HOME) if src.startswith(HOME) else src.lstrip("/"))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        return dst

    if nhooks > 0:   # hooks first, so no hook points at a moved script
        shutil.copy2(spath, keep_copy(spath))
        with open(spath, "w", encoding="utf-8") as fh:
            json.dump(sdata, fh, indent=2); fh.write("\n")
    for f, text in blocks:
        shutil.copy2(f, keep_copy(f))
        open(f, "w", encoding="utf-8").write(text)
    for f in skills + ours:
        shutil.move(f, keep_copy(f))

    print(f"\nDone. Moved to {short(backup)}/")
    print("Restart your AI tools. Delete that folder yourself once you are sure you won't need it.")
    print("Claude Code plugin installed too? Type: /plugin uninstall multiproject-handoff")


if __name__ == "__main__":
    main()
