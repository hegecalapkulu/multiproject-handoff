#!/usr/bin/env python3
"""multiproject-handoff context hint: a Claude Code UserPromptSubmit hook.

Before each user message it reads how big the conversation has become
(from the usage Claude Code records in the session transcript). When the
size first crosses one of the thresholds, it shows the user a short note
and asks the agent to suggest `mph-handoff` + a new session once, at a
natural stopping point. Each threshold fires once per session.

It also carries the optional **model advice**: on the first message of each
session it leaves the agent one short instruction: before starting a clearly
simple, mechanical task on a large model, offer once to switch to a lighter
one (the user decides; nothing happens silently). `model_advice=off` disables it.

Thresholds: once Claude Code has auto-compacted a conversation on this
computer, the size it compacted at is remembered per model (the first run also
looks through recent transcripts for past compactions), and the note fires at
50% and 80% of it. This adapts to each model, plan and setting by itself.
Only real "window is full" compactions count (not the app's precomputed early
ones), and a learned size never stays below the longest conversation already
seen for that model. `context_window=<tokens>` in guard.conf states the window
outright and wins. `context_hint_auto=off` turns the learning off. Until a model's size is known,
the fixed `context_hint_tokens` from ~/.handoff/guard.conf are used, default
500000,800000. Set `context_hint=off` to disable.
`context_hint_command` sets the command it suggests (default mph-handoff;
use your own, e.g. /devir, if you hand off differently).

**Handoff reminder:** it also counts the file edits (Edit, Write, MultiEdit,
NotebookEdit) since the last handoff in this session. When they reach
`handoff_reminder_edits` (default 20), it asks the agent once to suggest a
handoff at a natural stopping point, so a long working session is not lost
when the window is simply closed. `handoff_reminder=off` disables it.

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
    c = {"context_hint": "on", "context_hint_tokens": "500000,800000", "model_advice": "on",
         "context_hint_command": "mph-handoff", "context_hint_auto": "on",
         "handoff_reminder": "on", "handoff_reminder_edits": "20"}
    try:
        for line in open(CONF, encoding="utf-8"):
            line = line.split("#", 1)[0].strip()
            if "=" in line:
                k, v = line.split("=", 1)
                c[k.strip()] = v.strip()
    except OSError:
        pass
    return c


EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def is_handoff(item, cmd):
    """A user message naming the handoff command, or the agent starting it as a skill."""
    name = cmd.lstrip("/")
    if item.get("type") == "tool_use" and item.get("name") == "Skill":
        return name in str((item.get("input") or {}).get("skill", ""))
    if item.get("type") == "text":
        return name in item.get("text", "")
    return False


def read_transcript(path, cmd="mph-handoff"):
    """One pass over a transcript: the context size of the latest model call, the
    latest model name, the auto-compactions seen ({model: tokens before it}) and
    the file edits since the last handoff."""
    size, model, compactions, edits = 0, "", {}, 0
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if '"compact_boundary"' in line:
                    try:
                        meta = json.loads(line).get("compactMetadata") or {}
                    except ValueError:
                        continue
                    pre = meta.get("preTokens")
                    # only a real "window is full" compaction tells us the size; the app's own
                    # precomputed (early) compactions do not
                    if (meta.get("trigger") == "auto" and not meta.get("precomputed")
                            and isinstance(pre, int) and pre > 20000 and model):
                        compactions[model] = pre
                    continue
                if '"usage"' not in line and '"type":"user"' not in line.replace(" ", ""):
                    continue
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                msg = entry.get("message") or {}
                if not isinstance(msg, dict):
                    continue
                content = msg.get("content")
                if isinstance(content, str):
                    content = [{"type": "text", "text": content}]
                if isinstance(content, list):
                    for item in content:
                        if not isinstance(item, dict):
                            continue
                        # only what the user typed counts as a handoff request, not hook notes
                        if is_handoff(item, cmd) and (entry.get("type") == "user" or item.get("type") == "tool_use"):
                            edits = 0
                        elif item.get("type") == "tool_use" and item.get("name") in EDIT_TOOLS:
                            edits += 1
                if msg.get("model") and not str(msg["model"]).startswith("<"):
                    model = msg["model"]
                u = msg.get("usage")
                if u:
                    size = (u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                            + u.get("cache_creation_input_tokens", 0))
    except OSError:
        pass
    return size, model, compactions, edits


def context_size(path):
    """Tokens in the context of the latest model call recorded in the transcript."""
    return read_transcript(path)[0]


def learn_once(state, transcript):
    """First run only: look through recent transcripts (same folder tree) for
    auto-compactions, so the sizes are known before this session ever compacts."""
    if state.get("learned_scan"):
        return
    state["learned_scan"] = 1
    root = os.path.dirname(os.path.dirname(transcript)) if transcript else ""
    files = []
    try:
        for d in os.listdir(root):
            full = os.path.join(root, d)
            if os.path.isdir(full):
                for n in os.listdir(full):
                    if n.endswith(".jsonl"):
                        fp = os.path.join(full, n)
                        files.append((os.path.getmtime(fp), fp))
    except OSError:
        return
    for _, fp in sorted(files)[-200:]:  # oldest first, so the newest result wins
        try:
            with open(fp, encoding="utf-8", errors="replace") as f:
                if '"compact_boundary"' not in f.read():
                    continue
        except OSError:
            continue
        for m, pre in read_transcript(fp)[2].items():
            state["window:" + m] = pre


MODEL_ADVICE = (
    "[multiproject-handoff · model advice, applies to this whole session] "
    "Only if you know which model you are running on and it is a large one: when the user asks for a task "
    "that is clearly simple and mechanical (renaming, formatting, short summaries, simple text edits, "
    "repetitive changes) AND large enough that a lighter model saves meaningfully (many files, long texts, "
    "dozens of repeated edits, or a long run of such work), then BEFORE starting, offer once, in a short block in the user's language: "
    "1) switch to a lighter model (give the exact command or setting for this tool, e.g. `/model sonnet`), "
    "2) continue with the current model, 3) don't ask again. Then wait for the answer. "
    "For a small task that takes a moment, just do it: asking would cost more than it saves. "
    "Never offer it for planning, architecture, hard debugging, security, anything the user called important, "
    "or when you are unsure; never switch models or delegate to a smaller model silently. "
    "Ask at most once per session, and not again after the user chose 2. If the user chooses 3, set "
    "`model_advice=off` in ~/.handoff/guard.conf (their choice is the permission). "
    "If you cannot tell which model you are, ignore this entirely.")


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(state):
    keep = {k: v for k, v in state.items() if k.startswith(("window:", "seen:")) or k == "learned_scan"}
    rest = [(k, v) for k, v in state.items() if k not in keep]
    state = dict(rest[-100:], **keep)  # keep the file small, but never forget learned sizes
    try:
        os.makedirs(os.path.dirname(STATE), exist_ok=True)
        json.dump(state, open(STATE, "w", encoding="utf-8"))
    except OSError:
        pass


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    c = conf()
    sid = data.get("session_id", "unknown")
    state = load_state()
    out = {}
    if c["model_advice"] == "on" and not state.get("advice:" + sid):
        state["advice:" + sid] = 1
        save_state(state)
        out = {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": MODEL_ADVICE}}
    path = data.get("transcript_path", "")
    size, model, compactions, edits = read_transcript(path, c["context_hint_command"])
    try:
        need = int(c["handoff_reminder_edits"])
    except ValueError:
        need = 20
    if c["handoff_reminder"] == "on" and edits >= need and not state.get("work:" + sid):
        state["work:" + sid] = 1
        save_state(state)
        cmd = c["context_hint_command"]
        note = {
            "systemMessage": f"🧭 {edits} file edits since the last handoff. Before you close this window, `{cmd}` saves where you are.",
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"[multiproject-handoff] {edits} file edits since the last handoff in this session. "
                    "Answer the user's message first. Then, once, at a natural stopping point "
                    "(not in the middle of a task), say in one short sentence in the user's language "
                    f"that a lot was done and {cmd} would save it for the next session. Do not repeat it.")}}
        if out:
            note["hookSpecificOutput"]["additionalContext"] += "\n\n" + MODEL_ADVICE
        print(json.dumps(note))
        sys.exit(0)
    if c["context_hint"] != "on":
        if out:
            print(json.dumps(out))
        sys.exit(0)
    learned = None
    try:
        stated = int(c.get("context_window", "0") or 0)
    except ValueError:
        stated = 0
    if stated:
        learned = stated  # the user said how big their window is: trust that
    elif c["context_hint_auto"] == "on":
        learn_once(state, path)
        for m, pre in compactions.items():
            state["window:" + m] = pre
        if model:
            # a conversation already ran this long without being compacted, so the
            # window is at least this big: a learned size can only go up from here
            seen = max(size, state.get("seen:" + model, 0))
            state["seen:" + model] = seen
            if state.get("window:" + model, 0) and state["window:" + model] < seen:
                state["window:" + model] = seen
        learned = state.get("window:" + model) if model else None
        save_state(state)
    if learned:
        # This model was auto-compacted at about `learned` tokens on this computer:
        # warn at half of that, and again at 80%.
        limits = [learned // 2, learned * 4 // 5]
    else:
        try:
            limits = sorted(int(x) for x in c["context_hint_tokens"].split(",") if x.strip())
        except ValueError:
            limits = [500000, 800000]
    crossed = [t for t in limits if size >= t]
    top = crossed[-1] if crossed else 0
    if not crossed or state.get(sid, 0) >= top:  # below the thresholds, or already told at this level
        if out:
            print(json.dumps(out))
        sys.exit(0)
    state[sid] = top
    save_state(state)
    k = round(size / 1000)
    cmd = c["context_hint_command"]
    hint = {
        "systemMessage": f"🧭 This conversation is about {k}k tokens long"
                         + (f" (half of {model}'s ~{round(learned / 1000)}k window)" if learned and top == limits[0] else "")
                         + f". A fresh session after `{cmd}` would be cheaper and sharper.",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                f"[multiproject-handoff] The conversation context is about {k}k tokens. "
                "Answer the user's message first. Then, once, at a natural stopping point "
                "(not in the middle of a task), suggest in one short sentence in the user's "
                f"language: run {cmd} and continue in a new session. Do not repeat it."),
        },
    }
    if out:  # both on the same message: join the two instructions
        hint["hookSpecificOutput"]["additionalContext"] += "\n\n" + MODEL_ADVICE
    print(json.dumps(hint))
    sys.exit(0)


if __name__ == "__main__":
    main()
