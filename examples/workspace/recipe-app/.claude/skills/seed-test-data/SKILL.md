---
name: seed-test-data
description: Rebuild the local test database with 50 sample recipes. Use when the user says "reset test data", "seed", or tests fail because of stale local data. (Example of a project skill created by suggest-skill.)
---

# Seed test data

1. Make sure the target is the **local** database (`DATABASE_URL` points to `./dev.db`). If not, stop and ask.
2. Run `npm run db:reset && npm run db:seed`.
3. Run `npm test -- --silent` and report the result in one line.

Never run this against production.
