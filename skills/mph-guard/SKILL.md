---
name: mph-guard
description: Set up or adjust the optional safety guard and the long-conversation hint, a Claude Code hook that really blocks risky actions (deleting files, rewriting git history, reading .env secrets) and asks before others the user names (push, deploy, publish), with personal choices kept in ~/.handoff/guard.conf. Shows a short checklist with defaults, changes settings only after an explicit yes, and tests itself. Use when the user says "mph-guard", "/mph-guard", "set up the guard", "protect this folder", or when mph-setup-project offers it.
---

# mph-guard: a real safety net, set up your way

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

The rules in RULES.md are **instructions**: the agent follows them, but nothing stops a mistake. The guard is a **hook**: it runs before every command and file change, and blocks what the user chose to block, whatever the agent intends.

It works in **Claude Code** (hooks in `~/.claude/settings.json`). Other tools have their own safety settings (approval or sandbox modes); in those, say so and point the user to that tool's settings instead.

## 1. Look first

- Is `~/.handoff/mph-guard.py` there? (The installer puts it there; if missing, copy it after saying so from the `guard/` folder two levels above this skill's folder (`../../guard/`, where it is when installed as a Claude Code plugin) or from the repo's `guard/` folder. Copy `mph-context.py` from the same place if it is missing too.)
- Read `~/.handoff/guard.conf` if it exists: these are the user's current choices.
- Read the `hooks` section of `~/.claude/settings.json` (read-only for now). If another safety hook is already registered (any `PreToolUse` hook), **say which one** and ask whether to add the guard next to it or leave it. Never remove or change someone else's hook.
- Read the active project's `## Never` list: lines that name a folder or file can become protected paths.

## 2. One short checklist

Adapt it to what you found, with the current values pre-selected:

```
🧭 Safety guard: what should be blocked for real?

  1. [x] Deleting files (rm, find -delete, git clean, deleting from scripts)
  2. [x] Rewriting git history (force push, reset --hard, rebase, amend)
  3. [x] Reading secrets (.env files, environment variables)
  4. [ ] Ask before every git push
  5. Ask before these commands: (e.g. deploy.sh, npm publish)      ______
  6. Never edit inside these folders: (from your Never list: dist/)  ______
  7. When a delete is blocked, suggest moving to: (e.g. ~/Desktop/To-delete/) ______
  8. [x] Tell me when the conversation gets long (at 150k, 300k, 600k tokens) and suggest a handoff
  9. [x] Before a clearly simple task on a large model, offer once to switch to a lighter one (I decide)

Enter keeps the marks as shown.
```

## 3. Apply (only after an explicit yes)

1. Write `~/.handoff/guard.conf` (create the folder if needed):
   ```
   block_delete=on
   block_history=on
   block_secrets=on
   ask_push=off
   ask_commands=deploy.sh,npm publish
   protect_paths=~/code/recipe-app/dist
   trash_folder=~/Desktop/To-delete
   context_hint=on
   context_hint_tokens=150000,300000,600000
   context_hint_command=mph-handoff   # or the user's own handoff command
   model_advice=on
   ```
2. **Registering the hook changes Claude Code's security settings, so show the exact change first** and wait for a clear yes:
   ```json
   { "matcher": "Bash|Read|Edit|Write",
     "hooks": [ { "type": "command", "command": "python3 ~/.handoff/mph-guard.py" } ] }
   ```
   added to `hooks.PreToolUse` in `~/.claude/settings.json`, and, if item 8 is on,
   ```json
   { "hooks": [ { "type": "command", "command": "python3 ~/.handoff/mph-context.py" } ] }
   ```
   added to `hooks.UserPromptSubmit` (items 8 and 9 share this one entry). On Windows use `python` and the full path (`python %USERPROFILE%\\.handoff\\mph-guard.py`), since `~` and `python3` may not exist there. Read the file, add only this entry (skip if it is already there), keep everything else exactly as it was, and check the result is valid JSON.
3. **Test it** without risk, by piping sample calls into the script:
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf demo"}}' | python3 ~/.handoff/mph-guard.py
   echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | python3 ~/.handoff/mph-guard.py
   ```
   The first must print a `deny`, the second nothing. Report both results.
4. Tell the user: changes take effect in new sessions; "mph-guard" again to change the choices; to switch it off, remove the entry from `settings.json` (the agent can do this too, after a yes).

### About the long-conversation hint

The model cannot reliably feel how long its own conversation is, but Claude Code records the size after every reply. `mph-context.py` reads that before each user message; when a threshold is first crossed it shows a one-line note and asks the agent to suggest `mph-handoff` once, at a natural stopping point. Thresholds are in tokens, not percent, because context windows differ between models (200k, 1M); the defaults suit both. Change them in `guard.conf`.

### About the model advice

On the first message of each session, the same hook leaves the agent one short instruction: if it knows which model it is running on, and that model is a large one, then before starting a **clearly simple, mechanical task that is also large** (many files, long texts, dozens of repeated edits) it offers once (for a small task, asking would cost more than it saves, so it just does it): switch to a lighter model (with the exact command for this tool), continue, or don't ask again. It never switches or delegates silently, never offers for planning, architecture, hard debugging or security, and stays quiet if it cannot tell which model it is. "Don't ask again" sets `model_advice=off`.

## Rules

- Changing `settings.json` or `guard.conf` always needs the user's explicit yes in this conversation, every time.
- Never weaken a protection the user did not ask to weaken. Never remove another hook.
- Changing choices later: edit `guard.conf` only; the registration stays.
