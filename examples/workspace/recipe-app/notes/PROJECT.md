# Project settings (recipe-app, example)

## Paths
Defaults for `notes/RESUME.md`, `notes/BACKLOG.md` and `notes/daily/`. Decisions and knowledge: see the maps below.

## Check
- Healthy when: `npm test && npm run build` passes.
- Quick check for `/resume`: `npm test -- --silent`

## Decisions (which decision goes where)
- Product and scope → `notes/decisions/product.md`
- Architecture and tools → `notes/decisions/tech.md`
- (split from a single DECISIONS.md on 2026-11-22)

## Knowledge map
- Competitors → `notes/knowledge/competitors/` (one file per competitor, see `_overview.md`)
- Customer interviews → `notes/knowledge/interviews/` (one file per interview: `YYYY-MM-DD-who.md`)
- Pricing research → `notes/knowledge/pricing.md`

## Structure rules
- Split a topic into a folder once it covers 4+ separate subjects.
- Competitor names in these examples are fictional.

## Project skills
- seed-test-data: rebuilds the local test database with 50 sample recipes (file: .claude/skills/seed-test-data/SKILL.md)

## Project agents
- none yet (test-log-reader: asked, answer "later")

## Working style
- Profile: local

## Obsidian
- Obsidian: on
- Links: markdown
- Canvas: off

## Suggestions
- Suggestions: on

## Commit / backup
- Handoff commits and pushes to `origin main`. Push: `yes`

## Never
- Never commit `.env` files.
- Never run the seed script against the production database.
