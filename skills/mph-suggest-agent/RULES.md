<!-- multiproject-handoff RULES v0.1.0 -->
# multiproject-handoff: shared rules

Every `mph-*` skill follows these rules. They are kept in one file so every skill, in every tool, applies them the same way.

## 1. Finding projects

A **project** is any folder that contains `notes/RESUME.md`. Find projects in this order:

1. **A `PROJECTS.md` list**, in the working folder or else in `~/.handoff/PROJECTS.md`. It lists projects that live anywhere on disk:
   ```markdown
   - recipe-app: ~/code/recipe-app
   - landing-page: ~/clients/acme/landing-page
   ```
   Each path is the folder that holds `notes/`. Relative paths are relative to the `PROJECTS.md` file. Use the listed name.
2. **Otherwise, scan below the working folder:** `*/notes/RESUME.md` and `*/*/notes/RESUME.md` (skip `node_modules`, `.git`, `vendor`, `dist`, `build`).
3. **The working folder itself** is a project if it has `notes/RESUME.md`.

A project's code does not have to sit next to its notes: the `Code` row in `notes/PROJECT.md` says where the code is. Run checks and git commands there.

## 2. The active project

Once a project is chosen in a session, it is the **active project**, and every skill uses it **without asking again**.

- It is set by `mph-resume`, by the first skill that had to ask, or by the user naming a project ("let's work on cli-tool").
- It changes only when the user says so ("switch to landing-page", `mph-resume landing-page`) or clearly starts working on another project; then confirm once: "Switching to **landing-page**?"
- If no project is active and one is needed: use the working folder if it is a project; otherwise, if exactly one project was touched in this session, confirm it in one sentence; otherwise ask, listing the projects found.
- Work that touches a second project does not silently change the active project; `mph-handoff` sorts it out.

## 3. Project settings

Read `notes/PROJECT.md` of the active project before writing anything. Paths, checks, maps, structure rules and switches written there **override every default** in the skills.

**Modules.** The core skills always work. The optional modules run only when switched on in `PROJECT.md`:

```markdown
## Modules
- knowledge: on      # research, competitors, interviews… filed into topics
- profile: on        # working-style notes (local by default)
- suggestions: on    # one "want a skill for this?" question per handoff
- obsidian: off      # links, tags and map notes for Obsidian
```

A missing line means the default above. A user can still call a module skill by name when it is off; it then works once without switching itself on.

## 4. Reports

- Every skill that writes notes starts its report with **`🧭 [project-name]`**, for example `🧭 [recipe-app] decision recorded`. A wrong project is then visible at once.
- Keep reports short: what changed, where, and anything unfinished or failing.

## 5. Safety (never broken, in any mode)

- **Never delete files.** Edit, append, move (`git mv` in git repos) or archive. Old versions live in git.
- **Never rewrite git history.** No force push, no reset, no rebase. A failed push is reported, not "fixed".
- **Never claim work that did not happen.** "Tests pass" is written only if they passed in this session.
- **The user decides.** A suggestion is not a decision; structure changes (new topics, splits, merges, archives) and new skills or agents happen only after a yes.
- **No secrets** in notes: no passwords, keys, tokens or real customer data.
- **Look before writing:** read a file before changing it; never overwrite a file you have not read.
