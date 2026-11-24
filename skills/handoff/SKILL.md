---
name: handoff
description: Close the current Claude Code session cleanly so the next session can pick up in seconds. Runs checks, appends to the daily log, records decisions, updates the backlog, rewrites a short resume note and commits. Use when the user says "handoff", "/handoff", "wrap up", "let's start a new session" or "save where we are".
---

# Handoff: end this session, prepare the next one

The goal: a fresh session should understand where the project stands by reading **one short file** (`RESUME.md`), not by replaying this conversation.

## 0. Find the project and its settings

- The project is the folder this session is working in. If the working folder holds several projects, use the one this conversation was about. If that is unclear, ask the user in one sentence. Never guess.
- If the project has `notes/PROJECT.md`, **read it first**. Paths, check commands and extra steps written there override every default below.
- Defaults when there is no `PROJECT.md`:
  - Resume note: `notes/RESUME.md`
  - Daily log: `notes/daily/YYYY-MM-DD.md`
  - Backlog: `notes/BACKLOG.md`
  - Decisions: `notes/DECISIONS.md`
- If the project has no `notes/` folder yet, do not create it silently. Ask: "This project has no notes setup yet. Shall I run setup-project?"
- If the session belonged to no project (a one-off question), say so and stop.

## Steps

1. **Check.** If code changed in this session, run the project's check command (from `PROJECT.md`; otherwise the test suite if there is one). If it fails, stop and fix it first, or tell the user clearly that it is failing.
2. **Daily log.** Append a short entry to today's log (at most ~8 bullets: what was done, what was decided, what is blocked). Use the template if the project has one. Only append, never rewrite earlier entries. If nothing was done in this session, skip this step.
3. **Decisions.** If a decision was made, record it with the `decision-log` skill rules (read the target file first).
4. **Backlog.** Remove finished items (make sure they are in the daily log first) and add new requests to the right section. The backlog only holds open work.
5. **Resume note.** Read `RESUME.md` and rewrite it short (limit and sections come from `PROJECT.md`; default at most ~60 lines with: Where we are · Open questions · Next steps). Put "Last updated: YYYY-MM-DD" at the top. Finished details do not stay in the note; if they are not in the daily log yet, move them there first.
6. **Commit.** If `PROJECT.md` names a backup command, run it. Otherwise, if the project is a git repo, `git add` the notes (and any finished work) and commit with a short message. Push only if `PROJECT.md` says the project pushes routinely.
7. **Report.** Tell the user in a few lines what was saved, and how to start next time: "In the new session, run `/resume`."

## Rules

- **Nothing gets lost.** Shortening the resume note means moving information to the daily log or decision file first, then removing it from the note.
- **Never delete files.** Edit, append, or move. Old versions live in git history.
- **Never claim work that did not happen.** If tests are failing or work is unfinished, the resume note says so plainly.
- **Never rewrite git history.** No force push, no reset, no rebase. If a push fails, report it.
