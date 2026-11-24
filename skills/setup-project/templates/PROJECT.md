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

## Knowledge map
<!-- Research, competitors, interviews, strategy… Topics are added here as the project grows
     (the knowledge skill proposes them; you approve). Any names, any language, any location. -->
- <!-- e.g. Competitors → notes/knowledge/competitors.md -->

## Structure rules (optional)
<!-- How you like your notes organized. Every skill follows these. Examples:
- Number top-level folders: "01 Decisions", "02 Research", "03 Sales"
- Write notes in Turkish
- Split a topic into a folder at 100 lines instead of 150
- Interviews: one file per person, named YYYY-MM-DD-name.md -->

## Resume note
- At most ~60 lines. Sections: Where we are · Tried, didn't work · Open questions · Next steps.
- Mark this project stale on the /resume dashboard after: `14` days

## Project skills
<!-- Added by suggest-skill when you approve one. One line each. -->

## Project agents
<!-- Added by suggest-agent when you approve one. One line each, with the file path. -->

## Suggestions
- Suggestions: on <!-- on / off: whether handoff may ask one short "want a skill for this?" question -->

## Commit / backup
- Handoff commits `notes/` and finished work. Push: `no` <!-- yes / no -->

## Never
- <!-- e.g. "never touch the production database", "never edit generated files in dist/" -->
