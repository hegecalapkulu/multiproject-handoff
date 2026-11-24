Last updated: 2026-11-23

# Resume note

## Where we are
- Search by ingredient works (SQLite full-text search), 41 tests pass; shopping list half done.
- Shopping list: items can be added, not yet removed.
- Deployed preview works; production not deployed yet.

## Tried, didn't work
- Plain `LIKE '%tomato%'` search: too slow above 20k recipes and misses plurals. Replaced by FTS5.

## Open questions
- Do we need user accounts for v1, or is a local-only list enough? (user to decide)

## Next steps
1. Finish "remove item" on the shopping list and add its test.
2. Decide the accounts question, then record it with `decision-log`.
3. First production deploy.
