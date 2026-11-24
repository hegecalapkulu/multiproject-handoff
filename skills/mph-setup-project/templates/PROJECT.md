<!-- mph:project <name> -->
# Project settings: <name>

> Every mph-* skill reads this file first. The first line marks this folder as the project's notes folder; keep it.
> Paths below are relative to this folder. Anything written here overrides the skills' defaults. Remove the lines you don't need.

## About
<!-- What the project is, who it is for, where it stands. Written by setup from the files and your answers; edit freely. -->

## Language
- Language: English <!-- notes are written in it; replies too, unless the user writes in another language -->

## Modules
- knowledge: on <!-- research, competitors, interviews… filed into topics -->
- profile: on <!-- working-style notes; see "Working style" below -->
- suggestions: on <!-- one "want a skill for this?" question per handoff -->
- obsidian: off <!-- links, tags and _map.md for Obsidian -->

## Paths

| What | Where |
|---|---|
| Code | `..` <!-- the folder with the code; change it if your notes live apart from the code --> |
| Resume note | `RESUME.md` <!-- or an adopted file, e.g. `../docs/STATUS.md` --> |
| Daily logs | `daily/YYYY-MM-DD.md` · template: `daily/_template.md` |
| Backlog | `BACKLOG.md` (open work only) |
| Decisions | `DECISIONS.md` |

## Check
- Healthy when: `<your test / lint / build command>` passes.
- Quick check for `mph-resume` (optional, should take seconds): `<command>`

## Decisions (which decision goes where)
- Everything → `DECISIONS.md`
- <!-- Bigger projects: e.g. pricing → decisions/pricing.md, architecture → ../docs/architecture.md -->

## Knowledge map
<!-- Research, competitors, interviews, strategy… Topics are added here as the project grows
     (the knowledge skill proposes them; you approve). Any names, any language, any location. -->
- <!-- e.g. Competitors → knowledge/competitors.md -->

## Structure rules (optional)
<!-- How you like your notes organized. Every skill follows these. Examples:
- Number top-level folders: "01 Decisions", "02 Research", "03 Sales"
- Write notes in Turkish
- Split a topic into a folder at 100 lines instead of 150
- Interviews: one file per person, named YYYY-MM-DD-name.md -->

## Resume note
- At most ~60 lines. Sections: Where we are · Tried, didn't work · Open questions · Next steps.
- Mark this project stale on the mph-resume dashboard after: `14` days

## Project skills
<!-- Added by suggest-skill when you approve one. One line each. -->

## Project agents
<!-- Added by suggest-agent when you approve one. One line each, with the file path. -->

## Working style
- Profile: local <!-- local: working-style*.md is git-ignored (default) · committed: shared with the notes -->

## Obsidian
- Links: markdown <!-- markdown (also works on GitHub) | wikilinks -->
- Canvas: off <!-- on: also keep map.canvas up to date -->


## Commit / backup
- Handoff commits the notes and finished work. Push: `no` <!-- yes / no -->
- Git: <!-- only when the folder has no git: handoff writes on / not now (asked YYYY-MM-DD) / never -->

## Never
- <!-- e.g. "never touch the production database", "never edit generated files in dist/" -->
