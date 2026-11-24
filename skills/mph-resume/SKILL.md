---
name: mph-resume
description: Start an AI coding session (any agent) from the project notes instead of from scratch. With several projects it first shows a one-screen dashboard of all of them and asks which one; with one project, or "mph-resume <name>", it goes straight in and loads the resume note, the top of the backlog and the user's working style. Use when the user says "mph-resume", "/mph-resume", "resume", "continue", "where were we" or opens a session to keep working.
---

# mph-resume: start a session from the notes, not from memory

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` in this skill's own folder;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

Read as little as possible, but the right things. This skill changes no files.

## 1. Which project?

- **`mph-resume <name>`** → the project whose name matches (case-insensitive; a unique prefix is enough). No match → show the dashboard.
- **An active project is already set** in this session → use it (RULES.md §2). Show the dashboard again only if the user asks.
- **Otherwise**, find projects (RULES.md §1):
  - the working folder is a project, or exactly one project is found → use it, and name it in one line;
  - several → show the **dashboard** and wait for the pick;
  - none → "No project notes found here." and offer `mph-setup-project` (it can also adopt notes you already have).

### The dashboard

For each project read **only**: the marker line and the `## Paths` table of its `PROJECT.md` (to find its resume note and backlog, which may have any name), the first ~15 lines of the resume note, and the first item under `## Now` (or the first open section) of the backlog. Nothing else yet. The name shown is the one in the marker. Sort by "Last updated", newest first:

```
🧭 3 projects

1. recipe-app      updated 1 day ago
   Search works, 41 tests pass; shopping list half done. Now: finish "remove item".
2. landing-page    updated 6 days ago
   Waiting on headline copy from the client. Now: hero section.
3. cli-tool        updated 23 days ago  ⚠ stale
   v0.2 released; next is Windows support. Now: Windows CI runner.

Which one? (number or name)
```

- One line of state, one line of "Now".
- **⚠ stale** when the note is older than 14 days (or the number in that project's `PROJECT.md`).
- No "Last updated" line → "date unknown".

The chosen project becomes the active project.

## 2. Load the project

1. `notes/PROJECT.md` (settings, maps, modules).
2. The resume note in full (path from `PROJECT.md`; default `RESUME.md` in the notes folder).
3. Only the `## Now` section of `BACKLOG.md`.
4. If the **profile** module is on: `~/.handoff/working-style.md` and the project's `notes/working-style*.md`. Apply them quietly; do not recite them.
5. Note the **knowledge map** in `PROJECT.md` (topic names only). Open a topic file later, only when the work needs it.
6. Quick health check, only if `PROJECT.md` defines one.
7. **Drift check:** in a git repo, if there are commits newer than the note's "Last updated", say so in one line.

Do **not** read daily logs, decision files, topic files or code now.

## 3. Answer in at most 8 lines

```
🧭 [recipe-app]
Where we are: <1-2 lines>
Tried, didn't work: <if listed>
Open questions: <if any>
Next step: <from the notes>
Continue with that, or something else?
```

**Hard limit: 8 lines, no extra paragraphs.** Each field is one line; drop empty fields. If the health check could not run, add at most one short line saying so. Do not explain which files you read or that the working style was loaded; just apply it.
