# Resilient large `yarn install` (generic)

For huge Node trees (Next 16, React 19, Firebase, Monaco, Lighthouse, Playwright, sharp)
on slow/flaky networks, the default `yarn install --frozen-lockfile` intermittently dies with:
`AggregateError [ENETUNREACH]` while fetching platform binaries
(`@next/swc-linux-x64-gnu`, `@img/sharp-linux-x64`, etc.). The registry IS reachable
(curl → HTTP 200) — it's transient parallel-connect drops, not a config problem.

## Fix
```bash
yarn config set network-concurrency 4          # default is higher → more parallel drops
yarn install --frozen-lockfile --network-concurrency 4 --network-timeout 600000
```
Background it so it isn't killed by a foreground timeout; set `notify_on_complete: true`.

## Monitoring (because output is buffered by `| tail` and progress is invisible)
- **Downloading phase:** `du -sh "$(yarn cache dir)"` (e.g. `~/.yarn/cache/v6`). Grows 1.5→2.3 GB for this size. Healthy sign = cache size increasing.
- **node_modules stays ABSENT for 10–30 min even when healthy.** It materializes only at the link/extract phase. Do NOT treat absence as failure.
- **Alive?** `ps -ef | grep "yarn install" | grep -v grep`.
- A stalled cache size for several minutes usually means downloads finished and linking started — keep waiting a few more min for `node_modules` to appear.
