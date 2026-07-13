# Windows Audit & Hardening Workflow (reference)

## Dependency audit command chain
```bash
npm audit --omit=dev            # real installed tree
npm audit fix                   # easy fixes
npm ls request                  # find what pulls in a critical
npm audit --json | python -c "..."   # list isDirect + fixAvailable per pkg
npm uninstall gtts              # remove dead direct dep dragging criticals
npm audit --omit=dev            # expect: found 0 vulnerabilities
npm run typecheck && npm run test:unit
```
Bump top-level:
```bash
npm install @remotion/cli@^4.0.487 @remotion/renderer@^4.0.487 @remotion/media-utils@^4.0.487
```

## Patch tool Windows path doubling (PITFALL)
Error seen:
```
Failed to read file: C:\c\one\Automated-Video-Generator\src\lib\voice-engine.ts
_resolved to 'C:\\c\\one\\...' which is OUTSIDE the active workspace ('C:\\Users\\PREM KUMAR')
```
Cause: MSYS path `/c/one/...` got a second `c:` prepended by the edit tool.
Fix: pass native Windows path `C:\one\Automated-Video-Generator\...` to `patch` / `write_file`.
Terminal `cd` and bash commands may still use `/c/one/...`.

## Git symlink disabled on this host
`git config core.symlinks` -> `false`. Do not rely on symlinks for dedup.
Use `.gitignore` for regenerable artifacts (e.g. `assets/tray-icon.png`, `assets/icon.ico`).

## Dead-code removal checklist (per removed dep)
- [ ] function definitions
- [ ] all caller sites
- [ ] type-union literals (e.g. 'gtts-fallback')
- [ ] import lines + now-unused imports
- [ ] doc-comment references
- [ ] re-run typecheck (catches `}/`->`;`, lost `return {`, leftover callers)

## Repo-hardening result on Automated-Video-Generator
- 29 vulns (2 critical / 6 high) -> 0 after removing dead `gtts` (only direct dep dragging `request`+`form-data`).
- Added `src/integration.pipeline.test.ts` (4 tests) -> 57/57 pass.
- Gitignored regenerable `tray-icon.png`/`icon.ico`; `public/logo.png` kept (served from public/).
- README hero/logo now point at real assets (`demo-thumbnail.png`, `logo.svg`).
