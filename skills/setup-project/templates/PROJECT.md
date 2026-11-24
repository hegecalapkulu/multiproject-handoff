# Project settings

> The handoff skills (`resume`, `handoff`, `daily-log`, `decision-log`) read this file first.
> Anything written here overrides their defaults. Remove the lines you don't need.

## Paths

| What | Where |
|---|---|
| Code | `.` <!-- the folder with the code; change it if your notes live apart from the code --> |
| Resume note | `notes/RESUME.md` |
| Daily logs | `notes/daily/YYYY-MM-DD.md` · template: `notes/daily/_template.md` |
| Backlog | `notes/BACKLOG.md` (open work only) |
| Decisions | `notes/DECISIONS.md` |

## Check
- Healthy when: `<your test / lint / build command>` passes.
- Quick check for `/resume` (optional, should take seconds): `<command>`

## Decisions (which decision goes where)
- Everything → `notes/DECISIONS.md`
- <!-- Bigger projects: e.g. pricing → notes/decisions/pricing.md, architecture → docs/architecture.md -->

## Resume note
- At most ~60 lines. Sections: Where we are · Tried, didn't work · Open questions · Next steps.
- Mark this project stale on the /resume dashboard after: `14` days

## Commit / backup
- Handoff commits `notes/` and finished work. Push: `no` <!-- yes / no -->

## Never
- <!-- e.g. "never touch the production database", "never edit generated files in dist/" -->
