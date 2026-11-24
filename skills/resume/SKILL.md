---
name: resume
description: Start an AI coding session (any agent) from the project notes instead of from scratch. In a single project it loads the resume note and the top of the backlog; in a folder with several projects it first shows a short dashboard of all of them and asks which one. Use when the user says "resume", "/resume", "/resume <project>", "continue", "where were we" or opens a session to keep working.
---

# Resume: start a session from the notes, not from memory

Read as little as possible, but the right things.

## Finding projects (shared by all skills)

A **project** is any folder that contains `notes/RESUME.md`. Projects are found in this order:

1. **A `PROJECTS.md` file** in the working folder, or else in `~/.handoff/PROJECTS.md`. It lists projects that live anywhere on disk:
   ```markdown
   - recipe-app: ~/code/recipe-app
   - landing-page: ~/clients/acme/landing-page
   ```
   Each path is the folder that holds `notes/`. Relative paths are relative to the `PROJECTS.md` file. Use the listed name, not the folder name.
2. **Otherwise, scan below the working folder:** `*/notes/RESUME.md` and `*/*/notes/RESUME.md` (skip `node_modules`, `.git`, `vendor`, `dist`, `build`).
3. **The working folder itself** counts as a project if it has `notes/RESUME.md`.

A project's code does not have to sit next to its notes: if `notes/PROJECT.md` has a `Code` entry (table row or `Code:` line), that folder is where the code lives (run checks and git commands there).

## The active project (shared by all skills)

Once a project is chosen in a session, it becomes the **active project**, and every skill uses it **without asking again**:

- It is set by `resume`, by the first skill that had to ask, or by the user naming a project ("let's work on cli-tool").
- It changes only when the user says so: "switch to landing-page", `resume landing-page`, or clearly starts talking about another project. In that last case confirm once: "Switching to **landing-page**?"
- Every skill that writes notes starts its report with the project name in brackets, e.g. `[recipe-app] daily log updated`, so a wrong project is visible at once.
- If work in the session clearly touches a second project, the active project does not silently change; `handoff` sorts it out at the end.

## 1. Which project?

- **`/resume <name>`** → use the project whose folder name matches `<name>` (case-insensitive; a unique prefix is enough). If nothing matches, show the dashboard below.
- **The working folder itself has `notes/RESUME.md`** → that is the project. Go to step 2.
- **Otherwise, collect projects** as described in "Finding projects" (`PROJECTS.md` first, then the scan).
  - **Exactly one found** → use it, and say which one in one line.
  - **More than one** → show the **dashboard** and wait for the user's pick.
  - **None** → say "No project notes found here." and offer `setup-project`.

### The dashboard

For each project read **only the first ~15 lines** of its `RESUME.md` (enough for "Last updated" and "Where we are") and **only the first item** under `## Now` in its `BACKLOG.md`. Do not read anything else yet.

Sort by "Last updated", newest first. Show it like this:

```
You have 3 projects with notes:

1. recipe-app      updated 1 day ago
   Search works, 41 tests pass. Now: finish "remove item".
2. landing-page    updated 6 days ago
   Waiting on copy from the client. Now: hero section.
3. cli-tool        updated 23 days ago  ⚠ stale
   v0.2 released. Now: Windows support.

Which one? (number or name)
```

- One line of state, one line of "Now". No more.
- Mark a project **⚠ stale** when its note is older than 14 days (or the number in that project's `PROJECT.md`).
- If a note has no "Last updated" line, show "date unknown".

## 2. Load the chosen project

1. **Read `notes/PROJECT.md`** if it exists. It may change the paths below or add a step.
2. **Read the full resume note** (`notes/RESUME.md` by default).
3. **Read only the `## Now` section of the backlog.**
4. **Read the working-style profiles** (`profile` skill): `~/.handoff/working-style.md` and the project's `notes/working-style*.md`, if they exist. Apply them quietly; do not recite them.
5. **Note the knowledge map** in `PROJECT.md` (topic names only). Do not open topic files now; open one later only when the work needs it ("let's price this" → the pricing topic).
6. **Quick health check**, only if `PROJECT.md` defines one. Run it and note the result.
7. **Drift check:** if the project is a git repo, compare `git log -1 --format=%cs` with the note's "Last updated". If there are commits newer than the note, say so in one line ("3 commits since the last handoff; the note may be behind").
8. **Do not read** daily logs, decision files, topic files or code unless the resume note points to them for the next step.

## 3. Answer in at most 8 lines

- Project name and where we are (1-2 lines)
- What was tried and did not work, if the note lists it
- Open questions, if any
- The next step the notes suggest
- Then ask: "Continue with that, or something else?"

## Rules

- Read-only: this skill changes no files.
- Never invent a status. If a note is missing or empty, say so.
- The chosen project becomes the active project (see above). Do not show the dashboard again in this session unless the user asks for it.
