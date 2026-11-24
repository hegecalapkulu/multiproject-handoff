---
name: menu
description: Show every multiproject-handoff skill in one short screen, plus the active project and the most useful next command. Use when the user says "menu", "/menu", "what commands are there", "which skills do I have", "help with handoff" or seems to have forgotten what is available.
---

# Menu: what can I do here?

Read-only. Answer in one screen.

## Steps

1. **Active project.** If one is set in this session, name it. If not, say "no active project yet".
2. **Project-specific skills and agents.** If the active project's `notes/PROJECT.md` has a `## Project skills` or `## Project agents` section, read only those lines.
3. **Show this list** (adjust the last block to what step 2 found):

```
Session
  resume [project]     start: dashboard of all projects, or jump into one
  handoff [project]    end: check, log, decisions, knowledge, backlog, resume note, commit
  menu                 this screen

While working
  decision-log         record a decision and why
  knowledge            save research, competitors, interviews… · "organize notes"
  daily-log            today's log without a full handoff

Setup and growth
  setup-project        add the notes structure to a project
  suggest-skill        spot repeated work and suggest a skill for it
  suggest-agent        suggest a helper agent for heavy, noisy work

This project (from PROJECT.md)
  <project skills / agents, one line each, or "none yet">
```

4. **One suggestion**, in one line, based on the situation:
   - No active project → "Start with `resume`."
   - Active project, work was done and no handoff yet → "When you stop, run `handoff`."
   - A decision was made in the chat but not recorded → "Record it with `decision-log`."
   - Otherwise say nothing extra.

## Rules

- Changes no files.
- In tools without slash commands, show the names without `/`; the user can just say them.
