# Using it in a team

[← back to README](../README.md)

multiproject-handoff is built for one person first, but the notes are plain files in the repo, so a team can share them. This page says what is shared, what stays personal, and what to agree on.

## What is shared, what stays yours

| File | In a team |
|---|---|
| `PROJECT.md` | **Shared.** One set of paths, checks and rules for everyone. Change it like code: in a pull request. |
| `DECISIONS.md` / `decisions/` | **Shared.** This is the part teams like most: every decision with its date and reason, next to the code. |
| `knowledge/` | **Shared.** Research, competitors, interviews. |
| `BACKLOG.md` | Shared, **if** the team has no issue tracker. If you use Jira, Linear or GitHub Issues, keep only a short personal "Now" list here, or point `Backlog` in `PROJECT.md` to a file each person keeps for themselves. |
| `RESUME.md` | Personal by nature ("where *I* stopped"): git-ignore it so each person has their own (see below). |
| `daily/` | Personal. Git-ignore it, or give each person a folder. |
| `working-style*.md` | **Personal and git-ignored** by default. In team projects use `working-style.<name>.md`. |

## One resume note per person

Everyone has their own working copy, so the simplest way is to keep the personal files out of git. Add to `.gitignore`:

```
notes/RESUME.md
notes/daily/
notes/working-style*.md
```

Each person's handoff then writes their own resume note and log, and nobody overwrites anyone else's. Decisions, knowledge and `PROJECT.md` stay shared. (If the notes folder has another name, use that.)

## Working alongside the tools you already have

- **ADRs or a `docs/decisions/` folder already?** `mph-setup-project` adopts it where it is: decisions keep going there, in your format.
- **Issue tracker?** Keep issues there. Let the handoff write only the resume note and decisions.
- **Confluence or Notion?** Keep long documents there; link them from `knowledge/` so the agent knows they exist.

## Things to agree on

1. Which files are committed (the table above is a good default).
2. Who changes `PROJECT.md` and how (a pull request is enough).
3. One AI tool at a time per working copy: two agents writing the same note at the same moment can overwrite each other. Separate clones or branches are fine.
4. If your company reviews tools before use, the [Security overview](security.md) is written for that.
