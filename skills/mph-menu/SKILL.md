---
name: mph-menu
description: Show every multiproject-handoff skill in one short screen, plus the active project and the most useful next command. Use when the user says "menu", "/mph-menu", "what commands are there", "which skills do I have", "help with handoff" or seems to have forgotten what is available.
---

# Menu: what can I do here?

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` in this skill's own folder;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

Read-only. Answer in one screen.

## Steps

1. **Active project** (RULES.md §2). If none is set, say "none yet".
2. **Project details.** From the active project's `notes/PROJECT.md` read only `## Modules`, `## Project skills` and `## Project agents`.
3. **Show this list** (adjust the last block to what step 2 found):

```
🧭 multiproject-handoff · active project: <name or "none yet">

Session
  mph-resume [project]    start: dashboard of all projects, or jump into one
  mph-handoff [quick]     end: save what this session produced, commit
  mph-menu                this screen

While working
  mph-decision-log        record a decision and why
  mph-knowledge           save research, competitors, interviews… · "organize notes"   (module)
  mph-daily-log           today's log without a full handoff
  mph-profile             how I work with you: show, fix, "in this project I want…"   (module)
  mph-obsidian-map        link the notes, update the map, draw a canvas               (module)

Setup and growth
  mph-setup-project       add the notes structure to a project
  mph-suggest-skill       spot repeated work, suggest a skill                         (module)
  mph-suggest-agent       suggest a helper agent for heavy, noisy work                (module)

This project (from PROJECT.md)
  modules: <on/off list> · skills: <list or "none yet"> · agents: <list or "none yet">
```

4. **One suggestion**, in one line, based on the situation:
   - No active project → "Start with `mph-resume`."
   - Active project, work was done and no handoff yet → "When you stop, run `mph-handoff`."
   - A decision was made in the chat but not recorded → "Record it with `mph-decision-log`."
   - Otherwise say nothing extra.

## Rules

- Changes no files.
- In tools without slash commands, show the names without `/`; the user can just say them.
