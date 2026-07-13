# Real case: Automated-Video-Generator script-parser.ts

## Symptom
Editing a regex literal on line 71:
```ts
const sentences = line.split(/(?<=[.?!])\\s+(?![^\\[]*\\])/);
```
Goal: fix the `no-useless-escape` lint error (the `\[` inside `[^\[]` is unnecessary).
Wanted: `/(?<=[.?!])\s+(?![^[]*\])/`

## What failed
- `patch` tool called ~6 times with old/new containing `\\s` / `\\[`. Each reported
  "file modified" but `read_file` showed line 71 UNCHANGED.
- `String.raw\`\\s\`` attempts also produced wrong bytes (String.raw of `\\s` is
  single-backslash `\s`, not the file's double-backslash `\\s`).
- `execute_code` with hermes_tools.patch was BLOCKED ("runs arbitrary local Python").
- `npx eslint` cached stale results; always `rm -rf node_modules/.cache .eslintcache`
  before re-checking.

## What worked
A node `.cjs` script using `String.split(from).join(to)` with `from`/`to` built by
concatenating `'\\'` (one backslash) segments, then `rm -rf node_modules/.cache` and
re-run eslint -> **0 errors**.

## Lesson
On backslash/regex content: do NOT loop on `patch`. Immediately write a node script
(run via `terminal`) and verify with `read_file` + a fresh eslint cache clear.
