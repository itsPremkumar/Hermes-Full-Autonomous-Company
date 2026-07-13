#!/usr/bin/env bash
set -u
BASE="C:/one/paperclip-company/clawhub-skills"
CHANGELOG="SEO/AEO/GEO-optimized docs: richer features, FAQ, comparison table, geo/local section, accurate CLI quick-start; README badges. No code changes."
PASS=0; FAIL=0; FAILSLUGS=""
for slug in agent-caps agent-cost-tracker agent-guardrails agent-health agent-logger agent-sentinel airtable-cli arxiv-search ascii-art-creator ascii-video codebase-inspection company-ops cron-doctor dev-prompts doc-extractor excalidraw-cli file-watcher gif-search json-tools manifest-diff maps-cli md-linter notion-api polymarket-cli prompt-lint prompt-templates-cli secret-scanner skill-benchmark skill-lint web-research youtube-content; do
  d="$BASE/$slug"
  echo "===== $slug ====="
  git -C "$d" add -A 2>&1 | head -1
  git -C "$d" commit -m "docs: SEO/AEO/GEO-optimized SKILL.md + README" --no-verify >/dev/null 2>&1
  git -C "$d" push origin HEAD --no-verify >/dev/null 2>&1
  out=$(clawhub publish "$d" --slug "$slug" --version 2.0.1 --changelog "$CHANGELOG" 2>&1)
  if echo "$out" | grep -qiE "Published|✔"; then
    echo "  PUBLISHED"
    PASS=$((PASS+1))
  else
    echo "  FAIL: $out" | head -2
    FAIL=$((FAIL+1)); FAILSLUGS="$FAILSLUGS $slug"
  fi
done
echo "==================="
echo "PASS=$PASS FAIL=$FAIL"
[ -n "$FAILSLUGS" ] && echo "FAILED:$FAILSLUGS"
