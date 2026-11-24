#!/usr/bin/env python3
"""multiproject-handoff context hint: a Claude Code UserPromptSubmit hook.

Before each user message it reads how big the conversation has become
(from the usage Claude Code records in the session transcript). When the
size first crosses one of the thresholds, it shows the user a short note
and asks the agent to suggest `mph-handoff` + a new session once, at a
natural stopping point. Each threshold fires once per session.

Thresholds (tokens) come from `context_hint_tokens` in ~/.handoff/guard.conf,
default 120000,250000,500000. Set `context_hint=off` to disable.

Registered by the mph-guard skill (after asking) under hooks.UserPromptSubmit:
  { "hooks": [ { "type": "command", "command": "python3 ~/.handoff/mph-context.py" } ] }
"""
import json
import os
import sys

HOME = os.path.expanduser("~/.handoff")
CONF = os.environ.get("MPH_GUARD_CONF", os.path.join(HOME, "guard.conf"))
STATE = os.environ.get("MPH_CONTEXT_STATE", os.path.join(HOME, "context-state.json"))


def conf():
    c = {"context_hint": "on", "context_hint_tokens": "120000,250000,500000"}
    try:
        for line in open(CONF, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                c[k.strip()] = v.strip()
    except OSError:
        pass
    return c


def context_size(path):
    """Tokens in the context of the latest model call recorded in the transcript."""
    size = 0
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if '"usage"' not in line:
                    continue
                try:
                    msg = json.loads(line).get("message") or {}
                except ValueError:
                    continue
                u = msg.get("usage") if isinstance(msg, dict) else None
                if u:
                    size = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                            + u.get("cache_creation_input_tokens", 0))
    except OSError:
        pass
    return size


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    c = conf()
    if c["context_hint"] != "on":
        sys.exit(0)
    size = context_size(data.get("transcript_path", ""))
    try:
        limits = sorted(int(x) for x in c["context_hint_tokens"].split(",") if x.strip())
    except ValueError:
        limits = [120000, 250000, 500000]
    crossed = [t for t in limits if size >= t]
    if not crossed:
        sys.exit(0)
    sid = data.get("session_id", "unknown")
    try:
        state = json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    top = crossed[-1]
    if state.get(sid, 0) >= top:
        sys.exit(0)  # already told the user at this level
    state[sid] = top
    state = dict(list(state.items())[-50:])  # keep the file small
    try:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        json.dump(state, open(STATE, "w", encoding="utf-8"))
    except OSError:
        pass
    k = round(size / 1000)
    print(json.dumps({
        "systemMessage": f"🧭 This conversation is about {k}k tokens long. "
                         f"A fresh session after `mph-handoff` would be cheaper and sharper.",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"[multiproject-handoff] The conversation context is about {k}k tokens. "
                "Answer the user's message first. Then, once, at a natural stopping point "
                "(not in the middle of a task), suggest in one short sentence in the user's "
                "language: run mph-handoff and continue in a new session. Do not repeat it."),
        },
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
