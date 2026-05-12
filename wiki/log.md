# Wiki log

Append-only, chronological. Every entry: `## [YYYY-MM-DD] <ingest|query|lint|note> | <title>`.
This is the resume state — `grep "^## \[" wiki/log.md | tail` shows recent activity.

## [2026-05-11] note | wiki bootstrapped

Created the `wiki/` skeleton (`index.md`, `log.md`, `overview.md`, 8 methodology
stubs, 3 playbook stubs, 2 history stubs, `_templates/`) and the `CLAUDE.md`
schema. No posts ingested yet — `raw/posts.jsonl` has ~4,655 rows, all
`ingested == false`. Next: Plan 2.5 (timeline parser), then Plan 3 (the Ingest loop).
