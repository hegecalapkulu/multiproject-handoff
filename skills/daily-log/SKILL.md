---
name: daily-log
description: Write today's work log for the current project. Use at the end of a work day or when the user says "daily log", "log today" or "save today's work".
---

# Daily log

## 0. Find the project
- The project is the folder this session is working in. If unclear, ask.
- Read `notes/PROJECT.md` first if it exists; its paths and extra steps apply.
- Default: `notes/daily/YYYY-MM-DD.md` and `notes/BACKLOG.md`. If the folder does not exist, ask before creating it.

## Steps

1. Get today's date (YYYY-MM-DD).
2. Read the template if there is one (`notes/daily/_template.md` or the one named in `PROJECT.md`). Otherwise use these headings: Done · Decisions · Learned · Blocked · Tomorrow.
3. Fill the headings from today's conversation and the changes made.
4. Write to today's file. If it already exists, **append**, never overwrite. If `PROJECT.md` has rules for new files (for example a link to the previous log), apply them.
5. For lasting decisions in the log, apply the `decision-log` skill.
6. If there is a backlog: remove today's finished items (they are now in the log) and add new items to the right priority section.
7. Run any extra step listed in `PROJECT.md`.

## Rules

- Short and concrete: one line per item. Technical detail stays in commit messages and code.
- Never write that something was done if it was not.
- Label unverified numbers or claims as "hypothesis" or "unverified".
