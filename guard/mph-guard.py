#!/usr/bin/env python3
"""multiproject-handoff guard: a Claude Code PreToolUse hook.

Blocks (deny) or asks (ask) before risky tool calls, according to
~/.handoff/guard.conf. It never changes files itself.

Register it in ~/.claude/settings.json (the mph-guard skill does this
for you after asking):

  "hooks": { "PreToolUse": [ { "matcher": "Bash|Read|Edit|Write",
      "hooks": [ { "type": "command",
                   "command": "python3 ~/.handoff/mph-guard.py" } ] } ] }

Test it without Claude:
  echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf x"}}' | python3 ~/.handoff/mph-guard.py
"""
import json
import os
import re
import sys

CONF = os.path.expanduser(os.environ.get("MPH_GUARD_CONF", "~/.handoff/guard.conf"))

DEFAULTS = {
    "block_delete": "on",      # rm, rmdir, unlink, find -delete, git clean, delete from scripts
    "block_history": "on",     # force push, reset --hard, rebase, filter-branch, commit --amend
    "block_secrets": "on",     # reading .env files and dumping environment variables
    "ask_push": "off",         # ask before any git push
    "ask_commands": "",        # comma-separated words; ask before commands containing them (e.g. deploy.sh, npm publish)
    "protect_paths": "",       # comma-separated paths; never edit or write inside them
    "trash_folder": "",        # if set, the delete message suggests moving files here instead
}


def load_conf():
    conf = dict(DEFAULTS)
    try:
        with open(CONF, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    conf[k.strip()] = v.strip()
    except OSError:
        pass
    return conf


def decide(kind, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": kind,
        "permissionDecisionReason": "🧭 mph-guard: " + reason,
    }}))
    sys.exit(0)


def items(value):
    return [x.strip() for x in value.split(",") if x.strip()]


def expand(p):
    return os.path.realpath(os.path.expanduser(p))


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # never block because of our own parsing problem
    conf = load_conf()
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}

    if tool in ("Read", "Edit", "Write"):
        path = inp.get("file_path", "") or ""
        if conf["block_secrets"] == "on" and re.search(r"/\.env(\.[A-Za-z0-9_-]+)?$", path) \
                and not path.endswith(".example"):
            decide("deny", "secret file (.env). The guard keeps the agent out of it.")
        if tool in ("Edit", "Write") and path:
            real = expand(path)
            for p in items(conf["protect_paths"]):
                base = expand(p)
                if real == base or real.startswith(base.rstrip("/") + "/"):
                    decide("deny", f"{p} is protected in guard.conf; the agent may not change files there.")

    if tool == "Bash":
        cmd = inp.get("command", "") or ""
        if conf["block_delete"] == "on":
            if re.search(r"(^|[;&|(]|xargs)\s*(sudo\s+)?(rm|rmdir|unlink|shred|srm|trash)(\s|$)", cmd) \
                    or re.search(r"-delete(\s|$)|git\s+clean|os\.remove|os\.unlink|rmtree|unlinkSync|rmSync|fs\.rm|fs\.unlink|\.Trash", cmd):
                hint = f" Move it to {conf['trash_folder']} instead, or ask the user to delete it." \
                    if conf["trash_folder"] else " Tell the user what should be deleted and why; they delete it."
                decide("deny", "deleting files is blocked." + hint)
        if conf["block_history"] == "on" and re.search(
                r"git\s+push[^;&|]*(--force|\s-f(\s|$)|--force-with-lease)|git\s+reset[^;&|]*--hard"
                r"|git\s+rebase|git\s+filter-branch|git\s+commit[^;&|]*--amend", cmd):
            decide("deny", "rewriting git history (force push, reset --hard, rebase, amend) is blocked.")
        if conf["block_secrets"] == "on" and (
                re.search(r"(cat|less|more|head|tail|grep|rg|sed|awk|bat|open|cp|scp|curl|base64|strings|xxd)\s[^;&|]*\.env([.\s]|$)", cmd)
                or re.search(r"(^|[;&|]\s*)(env|printenv)(\s*$|\s*[;&|])", cmd)):
            decide("deny", "reading secrets (.env, environment variables) is blocked.")
        if conf["ask_push"] == "on" and re.search(r"git\s+push", cmd):
            decide("ask", "this pushes to a remote. Allow it?")
        for word in items(conf["ask_commands"]):
            if word in cmd:
                decide("ask", f"this runs '{word}', which you asked to confirm. Allow it?")
    sys.exit(0)


if __name__ == "__main__":
    main()
