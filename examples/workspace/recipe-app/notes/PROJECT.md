# Project settings (recipe-app, example)

## Paths
Defaults (`notes/RESUME.md`, `notes/BACKLOG.md`, `notes/DECISIONS.md`, `notes/daily/`).

## Check
- Healthy when: `npm test && npm run build` passes.
- Quick check for `/resume`: `npm test -- --silent`

## Decisions (which decision goes where)
- Product and scope → `notes/DECISIONS.md` under "Product"
- Architecture → `notes/DECISIONS.md` under "Tech"

## Commit / backup
- Handoff commits and pushes to `origin main`. Push: `yes`

## Never
- Never commit `.env` files.
- Never run the seed script against the production database.
