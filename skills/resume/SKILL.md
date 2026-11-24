---
name: resume
description: Start a new Claude Code session on a project with minimal reading. Loads the project settings, the resume note and the top of the backlog, then states where things stand and asks what to do. Use when the user says "resume", "/resume", "continue the project", "where were we" or opens a session to keep working.
---

# Resume: start a session from the notes, not from memory

Read as little as possible, but the right things.

## Steps

1. **Find the project** (the folder this session is working in). If there are several and it is unclear which one, ask.
2. **Read `notes/PROJECT.md`** if it exists. It may change the paths below or add a step.
3. **Read the resume note** (`notes/RESUME.md` by default). This is the main source.
4. **Read only the top section of the backlog** (`notes/BACKLOG.md` → the `## Now` section, or the first open section). Do not read the whole backlog.
5. **Quick health check** (only if `PROJECT.md` defines one, for example a fast test command). Run it and note the result.
6. **Do not read** daily logs, decision files or old code unless the resume note points to them for the next step.
7. **Answer in at most 8 lines:**
   - Where we are (1-2 lines)
   - Open questions, if any
   - The next step the notes suggest
   - Then ask: "Continue with that, or something else?"

## Rules

- If `RESUME.md` is missing, say so and offer to run `setup-project`. Do not invent a status.
- If the resume note is older than the latest commit by days and things look out of sync, mention it in one line.
- Read-only: this skill changes no files.
