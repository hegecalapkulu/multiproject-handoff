---
name: mph-daily-log
description: Write today's work log for the current project. Use at the end of a work day or when the user says "daily log", "log today" or "save today's work".
---

# Daily log

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

## 0. Find the project
- Use the **active project** of this session if one is set (RULES.md §2); do not ask again. If none is set, choose it as RULES.md §2 says.
- Read `notes/PROJECT.md` first if it exists; its paths and extra steps apply.
- Default: `notes/daily/YYYY-MM-DD.md` and `notes/BACKLOG.md`. If the folder does not exist, ask before creating it.

## Steps

1. Get today's date (YYYY-MM-DD).
2. Read the template if there is one (`notes/daily/_template.md` or the one named in `PROJECT.md`). Otherwise use these headings: Done · Decisions · Learned · Blocked · Tomorrow.
3. Fill the headings from today's conversation and the changes made.
4. Write to today's file. If it already exists, **append**, never overwrite. If `PROJECT.md` has rules for new files (for example a link to the previous log), apply them.
5. For lasting decisions in the log, apply the `mph-decision-log` skill.
6. If there is a backlog: remove today's finished items (they are now in the log) and add new items to the right priority section.
7. Run any extra step listed in `PROJECT.md`.

## Rules

- Short and concrete: one line per item. Technical detail stays in commit messages and code.
- Never write that something was done if it was not.
- Label unverified numbers or claims as "hypothesis" or "unverified".
