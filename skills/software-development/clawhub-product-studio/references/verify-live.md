# Verify a ClawHub skill is actually live

## The trap
`clawhub.ai` is a client-side SPA. `curl -w "%{http_code}"` returns **200**
for BOTH a real skill page and the "We couldn't find that page" 404 view.
Never use curl status to claim a skill is deployed.

## Correct URL format (owner-namespaced)
- WRONG: `https://clawhub.ai/skills/skills/<slug>`  (404s, but returns 200)
- RIGHT: `https://clawhub.ai/itspremkumar/skills/<slug>`
- Slug collisions with other publishers (e.g. `cron-doctor` = `suryast/cron-doctor`
  too) make the bare path 404. Namespacing fixes it. Always namespace in links.

## Authoritative check: the CLI
```bash
clawhub inspect <slug>
# prints: Owner: itspremkumar / Created: ... / Latest: 1.0.0
#   "Owner: itspremkumar" present  -> YOUR live skill
#   AMBIGUOUS_SKILL_SLUG            -> deployed, but collides; use namespaced URL
#   "Skill not found"               -> not published (or wrong slug)
# NOTE: `clawhub inspect @itspremkumar/<slug>` is NOT accepted; use bare slug.
```

## Bulk liveness audit (all 31) — copy/paste
```bash
skills="agent-caps agent-sentinel dev-prompts company-ops agent-cost-tracker \
skill-lint prompt-lint agent-health agent-logger manifest-diff cron-doctor \
prompt-templates-cli agent-guardrails skill-benchmark airtable-cli arxiv-search \
ascii-art-creator ascii-video codebase-inspection doc-extractor excalidraw-cli \
file-watcher gif-search json-tools maps-cli md-linter notion-api polymarket-cli \
secret-scanner web-research youtube-content"
for s in $skills; do
  out=$(clawhub inspect "$s" 2>&1)
  if echo "$out" | grep -qi "Owner: itspremkumar"; then echo "OK    $s"
  elif echo "$out" | grep -qi "AMBIGUOUS";        then echo "AMB   $s"
  else echo "MISSING $s"; fi
done
```

## Browser confirmation (definitive for the user)
Navigate to `https://clawhub.ai/itspremkumar/skills/<slug>`. A real page has
the skill name as H1 + an "Install" panel + SKILL.md tabs. The 404 SPA shows
the lobster detective + "We couldn't find that page."

## Master list
`https://clawhub.ai/itspremkumar` -> profile badge "Skills N". This count can
exceed the documented 31 (companion skills like AVG docs also count) — verify
ownership per slug with `inspect`, don't assume every catalog card is yours.

## Bulk REPUBLISH (portfolio doc/SEO sweep)
- `clawhub sync --root clawhub-skills` **fails** on ambiguous slugs
  (`AMBIGUOUS_SKILL_SLUG` — other publishers share e.g. `cron-doctor`). It
  publishes nothing. **Loop `clawhub publish` per skill instead** (auth resolves
  owner):
  ```bash
  BASE="C:/one/paperclip-company/clawhub-skills"   # C:/ NOT /c/ — MSYS git -C needs it
  for slug in $(ls "$BASE"); do
    d="$BASE/$slug"; [ -f "$d/SKILL.md" ] || continue
    git -C "$d" add -A && git -C "$d" commit -m "docs: SEO/AEO/GEO" --no-verify
    git -C "$d" push origin HEAD --no-verify
    clawhub publish "$d" --slug "$slug" --version 2.0.1 --changelog "$MSG"
  done
  ```
- **Version bump required:** republishing the same version is rejected. Bump
  (2.0.1 → 2.0.2) if re-publishing.
- **Quick-start must be real:** derive subcommands from `add_parser("...")` ONLY,
  never from an `add_argument` inventory (that mixes positional args like `path`).
  Same for detecting `self-test`.
- After the sweep, re-run the liveness audit above; expect 31/31 `OK`/`AMB`.
