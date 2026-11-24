---
name: setup-project
description: Set up the handoff notes structure (PROJECT.md, RESUME.md, BACKLOG.md, DECISIONS.md, daily logs) in the current project, filled from what is already known. Use when the user says "set up notes", "setup-project", or when handoff/resume finds no notes folder.
---

# Setup project notes

## Steps

1. **Find the project** (the folder this session is working in). Confirm the folder with the user in one sentence before writing anything.
2. **Look before writing.** If `notes/` already exists, list what is there and only add what is missing. Never overwrite an existing file.
3. **Learn the project quickly:** read the README, the package/build files and `git log --oneline -15` if it is a git repo. Find the check command (tests, lint, build).
4. **Create** (from the `templates/` folder next to this SKILL.md, adapted to the project):
   - `notes/PROJECT.md`: paths, check command, backup/commit habit, decision map, an empty knowledge map. Keep only the lines that apply. If the project already has notes or docs folders (research, specs, meeting notes), **map them as they are** instead of creating new ones.
   - `notes/RESUME.md`: "Where we are" filled from what you learned; "Next steps" left for the user to confirm.
   - `notes/BACKLOG.md`: sections `## Now`, `## Next`, `## Later`, empty unless the user names work.
   - `notes/DECISIONS.md`: empty heading list.
   - `notes/daily/_template.md` (from `daily-template.md`).
5. **Ask the user three questions (plus one optional)** (in one message) and write the answers into `PROJECT.md`:
   - What command tells us the project is healthy?
   - Should handoff push to the remote, or only commit?
   - Anything the assistant must never do in this project?
   - (Optional) Any way you like notes organized? (folder names, language, numbering) → written under "Structure rules".
6. **Register it** if the user keeps a project list: if a `PROJECTS.md` exists in the parent folder or in `~/.handoff/`, add a line `- <name>: <path>` (append only). If the notes live apart from the code, write the code folder in the `Code` row of `PROJECT.md`.
7. Commit the new `notes/` folder if the project is a git repo.
8. Tell the user: "From now on: `/resume` to start a session, `/handoff` to end one."

## Rules

- Never delete or overwrite. Only create missing files.
- No secrets in notes (passwords, keys, tokens, real customer data).
