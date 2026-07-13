# Windows build pitfalls — Paperclip + Hermes (verified repro)

All observed on Windows 10/11 with the MSYS git-bash that Hermes's `terminal` tool uses.

## 1. pnpm install "hangs" during linking
Symptom: `node_modules` size freezes (~891M), store has ~1248 packages, `ls node_modules/@paperclipai`
returns 0 links, yet `netstat` shows ~90 ESTABLISHED connections and 1 node process alive for 10+ min.
No `.modules.yaml` is ever written.
Root cause: default `isolated` linker does slow/hung hardlink+symlink resolution under MSYS.
Repro fix that works:
```
pnpm install --ignore-scripts --config.node-linker=hoisted
```
Hoisted links in ~1 min. `--ignore-scripts` skips `scripts/link-plugin-dev-sdk.mjs` (harmless symlink
postinstall). After install, run `pnpm build` explicitly to compile workspace packages.
Note: the very first run may have already populated the pnpm store (1248 pkgs reused), so a retry is fast.

## 2. `node dist/index.js` → ERR_MODULE_NOT_FOUND
Symptom: server exits with `Cannot find module '...\packages\db\src\client.js' imported from ...\packages\db\src\index.ts`.
Root cause: Paperclip workspace packages set `"exports": { ".": "./src/index.ts" }` — they resolve to
**source TypeScript**, not the built `dist`. Plain `node` can't load `.ts`.
Fix: run the server via tsx instead of node:
```
cd server
../node_modules/.bin/tsx src/index.ts
```
`pnpm build` still required first (it compiles adapters/server to `dist/` and copies onboarding-assets +
built-ins). If the build's `tsc && copy` chain stops at tsc, manually:
```
mkdir -p dist/onboarding-assets dist/built-ins
cp -R src/onboarding-assets/. dist/onboarding-assets/
cp -R src/built-ins/. dist/built-ins/
```

## 3. MSYS path rewrites break absolute tsx path
Symptom: `node /c/one/.../node_modules/.pnpm/tsx@4.22.4/.../cli.mjs src/index.ts` →
`Cannot find module 'C:\c\one\...'` (note doubled `c`).
Root cause: the bash shell prepends an extra `c` to `C:\` paths passed to native node.
Fix: use the relative shim `../node_modules/.bin/tsx` (MSYS resolves it correctly), OR invoke from a
`.bat` that uses the native `C:\one\...` path (see templates/run-server.bat). The `.bin/tsx` shim itself
works: `../node_modules/.bin/tsx probe.ts` prints output fine.

## 4. Embedded Postgres refuses admin account
Symptom: server starts, embedded Postgres initializes the cluster, then fails:
`Execution of PostgreSQL by a user with administrative permissions is not permitted. The server must be
started under an unprivileged user ID...`
Root cause: interactive user is a Windows admin; PostgreSQL on Windows blocks this.
Fix A (preferred): external Postgres. Set `DATABASE_URL=postgres://user:pass@localhost:5432/paperclip`.
A full PostgreSQL is frequently already installed as a Windows service (check `sc query postgresql-x64-17`
and `netstat -an | grep :5432`). Create the db (`createdb paperclip` or let Paperclip migrate).
Fix B: run the server under a non-admin user via `runas /user:paperclipuser "cmd /c run-server.bat"`
(requires creating the user first; interactive password prompt makes this awkward headless).

## 5. Adapter is already bundled
Do not patch `server/src/adapters/registry.ts` or add entries to `ui/src/adapters/`. `hermes_local` and
`hermes_gateway` ship in `main`. Just create a `hermes_local` agent after first run.

## 6. Docker daemon off
`docker compose up` fails with "open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file
specified." Launch Docker Desktop GUI first, or use the native tsx run (no Docker needed).
