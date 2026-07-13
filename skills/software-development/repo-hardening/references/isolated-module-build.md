# Isolated sub-module build + verify-before-merge (YouTube adapter case)

Pattern used to add a brand-new capability (YouTube upload) to an existing
project WITHOUT destabilizing it: build in a sibling folder, verify offline,
then wire in later.

## User ask that triggered this
"build it in a separate new folder, after training everything works then we can
connect with the main project" — i.e. isolate risk, prove it, then merge.

## Folder shape (standalone, own package.json)
```
youtube-upload/
  package.json        # own deps; googleapis listed but lazily imported
  tsconfig.json       # NodeNext + .js extensions, rootDir src
  src/
    types.ts  auth.ts  uploader.ts  token-store.ts  cli.ts  index.ts
    adapter.test.ts    # offline tests, no network/credentials
  README.md            # setup + explicit merge plan into main project
```

## Key techniques that worked
1. **Lazy import the heavy SDK** so dry-run needs zero external deps and is
   fully verifiable offline:
   ```ts
   const { google } = await import('googleapis');   // inside live branch only
   ```
   - Import from the **package root** (`'googleapis'`), NOT a deep internal path
     (`'googleapis/build/src/auth/oauth2client.js'`). The deep path fails
     `tsc` module-resolution (TS2307) even though tsx/esbuild run it fine.
   - Dry-run/sandbox modes never hit the `await import`, so `npm test` passes
     with NO googleapis installed at all.

2. **Make OAuth methods async and update EVERY caller.** When `buildAuthUrl`
   changed from `: string` to `: Promise<string>`, three sites broke silently
   until fixed: the unit test (`await auth.buildAuthUrl(...)`), the CLI
   (`await auth.buildAuthUrl()`), and the live branch (`await loadClient()`).
   Grep for all callers before changing a signature.

3. **Tests run with only tsx + typescript installed** (no googleapis):
   ```bash
   npx tsx --test "src/adapter.test.ts"   # 6 tests, all green, no network
   ```

4. **MSYS /tmp path quirk (Windows):** `fs.existsSync('/tmp/x.mp4')` resolves
   wrong under MSYS Node — the file "isn't found" even after `printf > /tmp/x.mp4`.
   Use a CWD-relative path (`demo_test.mp4`) in scripts/tests instead.

## Verification gate (run after EVERY edit batch)
The agent is re-prompted for "fresh passing verification evidence" after code
edits. Satisfy it with real commands, not claims:
```bash
npx tsx --test "src/adapter.test.ts"     # 6/6 pass
npx tsc -p tsconfig.json --noEmit        # clean (filter dom-webcodecs/lib.dom noise)
node src/cli.ts auth                     # prints valid accounts.google.com URL
node src/cli.ts upload demo.mp4 --dry-run  # returns mocked watch?v= URL
```
Only flag `--live` as "blocked: needs real OAuth credentials" — never claim it
was tested.

## Merge plan (documented in sub-module README)
Move `auth.ts`/`uploader.ts` -> `src/adapters/http/social-upload/`,
reuse the main project's `job-store.ts` for tokens, add a
`POST /api/social/youtube` route guarded by `requireLocalAccess` + a
`YOUTUBE_ENABLED` env flag, and a "Publish to YouTube" button in `src/views/home/`.
