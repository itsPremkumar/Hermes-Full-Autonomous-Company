# Pushing the local Paperclip company to GitHub (verified procedure)

The company runs locally at `/c/one/paperclip-company`. To make GitHub the single source of truth
(a local-only company drifts and is fragile), use this verified push procedure.

## 1. Create repos via GitHub API (cached creds — no token typing)
```bash
TOK=$(printf 'protocol=https\nhost=github.com\n\n' | git credential fill 2>/dev/null | sed -n 's/^password=//p')
# NEVER echo $TOK. It is a live PAT for itsPremkumar.
curl -s -m 15 -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" \
  -d '{"name":"Hermes-Full-Autonomous-Company","private":false,"auto_init":false}' \
  https://api.github.com/user/repos
# mirror for prompts: {"name":"Hermes-Prompt-Library", ...}
```

## 2. Curated copy (EXCLUDE node_modules — `find` over it hangs ~60s on this box)
```bash
STAGE=/c/one/_stage_master
rm -rf "$STAGE"; mkdir -p "$STAGE"
cp -r digital-products income-engine finance COMPANY_PLAN.md company-status.json "$STAGE/"
cp -r hermes-paperclip-adapter "$STAGE/hermes-paperclip-adapter"
rm -rf "$STAGE/hermes-paperclip-adapter/node_modules" "$STAGE/hermes-paperclip-adapter/.git"
find "$STAGE" -name '.git' -type d -prune -exec rm -rf {} +   # no nested repos
```

## 3. .gitignore (keep repo lean / secret-free)
```
node_modules/ dist/ .env .env.* *.key secrets/ *.zip *.mp4 *.png *.log
```

## 4. Init + commit + push
```bash
cd "$STAGE"
git init -q
git config user.name prem; git config user.email premkumar016555@gmail.com
git remote add origin https://github.com/itsPremkumar/Hermes-Full-Autonomous-Company.git
git add -A; git commit -q -m "..."
git branch -M master          # repo default branch is MASTER, not main
git push -u origin master
```

## 5. Verify via API (don't trust the local exit code alone)
```bash
curl -s -H "Authorization: Bearer $TOK" \
  https://api.github.com/repos/itsPremkumar/Hermes-Full-Autonomous-Company/contents/ \
  | sed -n 's/.*"name": "\([^"]*\)".*/\1/p'
```

## 6. Cleanup staging (memory discipline — this box is RAM-starved)
```bash
rm -rf "$STAGE"
# if "Device or resource busy", `cd` to a neutral dir first, then retry rm -rf
```

## Pitfalls hit this session
- Default branch is `master` → `git push -u origin main` fails with `src refspec main does not match any`. Use `git branch -M master`.
- **write_file tool path bug:** pass the NATIVE Windows path `C:\one\...`, NOT MSYS `/c/one/...`. The tool prepends `C:\` to MSYS-style paths, producing a phantom `C:\c\one\...` so the file "writes" somewhere wrong. The terminal `cd` is fine with `/c/one/...`; only the write_file `path` argument needs the native form.
- `find . -path ./x/node_modules` re-scans node_modules and hangs (60s timeout). Copy a curated subset excluding node_modules instead of scanning.
- Cached creds: `git credential fill` returns `password=<token>` for itsPremkumar; filter it out, never print it.

## Prompt-consolidation rules (apply before any push)
- ONE constitution, versioned — not five overlapping drafts. Consolidate into `CONSTITUTION.md`
  (master operating prompt v2.0), keep the best structure, archive superseded drafts in
  `prompts/archive/` (never delete — they're the version history).
- **Reality-match the stack.** Drafts often list tools you DON'T run (n8n, Mem0, CrewAI, AutoGen,
  standalone "OmniRouter", "Claude Fable 5 leaked prompts"). The real stack is Paperclip + Hermes +
  OpenClaw + `hermes-paperclip-adapter` + OmniRoute→OpenRouter + Automated-Video-Generator. Adopt the
  draft whose structure matches reality as the spine; drop fictional assumptions.
- Never build on unverified "leaked system prompts" — prefer officially-published guidance.
