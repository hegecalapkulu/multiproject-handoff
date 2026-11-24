<!-- mph:project landing-page -->
# Project settings: landing-page (example of an adopted project)

> This project already had its own notes before multiproject-handoff was set up.
> `mph-setup-project` adopted them where they were: nothing was moved or renamed.
> `notes/` was already used for meeting notes, so these settings live in `.mph/`.

## Language
- Language: English

## Modules
- knowledge: off
- profile: off
- suggestions: on
- obsidian: off

## Paths

| What | Where |
|---|---|
| Code | `..` |
| Resume note | `../docs/STATUS.md` (adopted) |
| Backlog | `../TODO.md` (adopted) |
| Decisions | `../docs/decisions.md` (adopted) |
| Daily logs | `daily/YYYY-MM-DD.md` (new) |

## Check
- Healthy when: `npm run build` passes.

## Never
- Never edit files in `../notes/` (the client's meeting notes).
