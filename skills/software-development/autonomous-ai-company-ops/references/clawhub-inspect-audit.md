# ClawHub Inspect / Audit — Avoiding False Negatives

## Problem (hit during 2026-07-13 full audit)

A naive loop `for slug in $SLUGS; do clawhub inspect "@$slug"; done` reported
**22/31 MISSING** — but all 31 were actually live. The "missing" results were
false negatives from THREE separate inspect quirks, not real gaps.

## The three traps

### Trap 1 — `@` prefix is rejected
`clawhub inspect @codebase-inspection` → errors. Use the **bare slug**:
```bash
clawhub inspect codebase-inspection        # ✅ works
```
Even this form fails when Trap 2 fires.

### Trap 2 — `AMBIGUOUS_SKILL_SLUG` looks like "not found"
When another user published a skill with the same slug, `clawhub inspect <slug>`
returns:
```json
{"code":"AMBIGUOUS_SKILL_SLUG","message":"Found multiple skills with the slug \"polymarket-cli\"...","matches":[{"ownerHandle":"ivangdavila",...},{"ownerHandle":"itspremkumar",...}]}
```
This is NOT "your skill is missing" — it means the slug collides. Our
`@itspremkumar/<slug>` version is still live. 9/31 of our skills hit this
(polymarket-cli, youtube-content, arxiv-search, notion-api, web-research,
agent-sentinel, cron-doctor, agent-guardrails, skill-lint).

### Trap 3 — grep on `head -2` misses the "Owner:" line
A loop that does `clawhub inspect "$slug" 2>&1 | head -2 | grep "Owner:"` can
miss because the output has a `- Fetching skill` banner line before `Owner:`.
Always grep the FULL output, or just check exit code + web page.

## The reliable audit pattern (verified 31/31)

```bash
# 1. Web-page HTTP check per slug — unambiguous, no ambiguity errors
for slug in agent-caps codebase-inspection secret-scanner ... ; do
  code=$(curl -sS -o /dev/null -w "%{http_code}" "https://clawhub.ai/itspremkumar/skills/$slug")
  echo "$slug => HTTP $code"          # 200 = live, 404 = missing
  sleep 0.3                            # be polite to the API
done

# 2. Or: grep clawhub explore for your slug
clawhub explore --sort newest 2>&1 | grep -i "itspremkumar" | head -40
```

## Version confirmation

`clawhub inspect <slug>` (bare) prints `Latest: 2.0.1` etc. on success.
To confirm a specific version is live, the web page is authoritative:
`https://clawhub.ai/itspremkumar/skills/<slug>` → look for the version badge.

## Lesson

Never conclude "skill missing on ClawHub" from a failing `clawhub inspect`.
Confirm with the **web-page HTTP 200** check. The inspect command is useful for
fetching metadata once you know the slug is unambiguous, but it is NOT a reliable
presence probe when slugs collide.
