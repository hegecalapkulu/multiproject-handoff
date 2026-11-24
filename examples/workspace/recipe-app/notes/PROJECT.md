<!-- mph:project recipe-app -->
# Project settings: recipe-app (example)

## Language
- Language: English

## Modules
- knowledge: on
- profile: on
- suggestions: on
- obsidian: on

## Paths
Defaults: `RESUME.md`, `BACKLOG.md` and `daily/` in this folder. Decisions and knowledge: see the maps below.

## Check
- Healthy when: `npm test && npm run build` passes.
- Quick check for `mph-resume`: `npm test -- --silent`

## Decisions (which decision goes where)
- Product and scope → `decisions/product.md`
- Architecture and tools → `decisions/tech.md`
- (split from a single DECISIONS.md on 2026-11-22)

## Knowledge map
- Competitors → `knowledge/competitors/` (one file per competitor, see `_overview.md`)
- Customer interviews → `knowledge/interviews/` (one file per interview: `YYYY-MM-DD-who.md`)
- Pricing research → `knowledge/pricing.md`

## Structure rules
- Split a topic into a folder once it covers 4+ separate subjects.
- Competitor names in these examples are fictional.

## Project skills
- seed-test-data: rebuilds the local test database with 50 sample recipes (file: ../.claude/skills/seed-test-data/SKILL.md)

## Project agents
- none yet (test-log-reader: asked, answer "later")

## Working style
- Profile: local

## Obsidian
- Links: markdown
- Canvas: off

## Commit / backup
- Handoff commits and pushes to `origin main`. Push: `yes`

## Never
- Never commit `.env` files.
- Never run the seed script against the production database.
