# GEO / Structured-Data Coverage Audit (Next.js App Router)

AI-search visibility (GEO: ChatGPT/Gemini/Perplexity citing your tools) depends on
JSON-LD + clean extractable content. Before ADDING schema, AUDIT existing coverage —
most "GEO gaps" are pages that never got wired into the SEO system, not missing schema types.

## 1. Quantify the coverage gap (grep-based, no browser)

Many Next.js apps keep SEO in a centralized module (e.g. `lib/seo/complete-page-seo.ts`
with `getPageSEO(pageKey)` / `getPageSchema(pageKey)`). Find how many pages actually use it:

```bash
cd /path/to/app
# pages that call the SEO system
grep -rl "getPageSEO\|getPageSchema" src/app 2>/dev/null \
  | sed 's#src/app/##; s#/page.tsx##; s#/layout.tsx##' | sort -u > /tmp/using_seo.txt
wc -l /tmp/using_seo.txt
# all route directories (e.g. tool pages)
ls src/app/tools | sort -u > /tmp/all_tools.txt
wc -l /tmp/all_tools.txt
# routes NOT using the system = the real GEO gap (no metadata + no schema)
comm -23 /tmp/all_tools.txt /tmp/using_seo.txt | tee /tmp/gap.txt | wc -l
```

Real case (sproutern 2026-07-11): 100 tool dirs, only 22 used the system → **78 uncovered**.
Those 78 had no `<title>`/description/canonical AND no JSON-LD → invisible to AI search.

Caveat: `comm` compares raw dir names vs SEO keys (camelCase vs kebab-case), so treat the
number as a floor. Confirm a few manually (e.g. `grep -n "gpaConverter:" complete-page-seo.ts`).

## 2. The `speakable` trap

Global JSON-LD often declares `speakable: { cssSelector: ['.faq-answer', '.key-takeaway', '.tldr-summary'] }`
(voice-search / answer-extraction hints). These only help IF pages actually render those
classes. Check:

```bash
grep -rln "key-takeaway\|tldr-summary\|faq-answer" src/app/tools src/app/blog 2>/dev/null | wc -l
# 0 = the speakable signal points at nothing -> AI extracts no clean answer
```

If 0, the GEO signal is wired but disconnected. Fix: use the existing AEO component
(`aeo-content-blocks.tsx` or similar) on tool/blog pages so the selectors resolve to content.

## 3. Do NOT create a parallel JSON-LD component

When you find a page missing schema, resist writing a new `<ToolJsonLd>` helper — a
centralized system usually already owns schema. Adding a parallel component duplicates
logic and can emit conflicting `@graph` nodes. Instead:
- Add the page's entry to the central SEO module, OR
- Reuse the system's `getPageSchema(pageKey)` in that page.

(We created `tool-json-ld.tsx` then DELETED it once we found `complete-page-seo.ts` already
covered schema — that detour is the lesson.)

## 4. Editorial-scale decision gate

Closing a 78-page gap means writing real titles/descriptions per tool. Auto-generating
78 guessed descriptions risks low-quality/spammy metadata that HURTS GEO. At scale, use
`clarify` to pick scope: top-traffic subset first / all-now / homepage+blog / report-only.
Quality per page > coverage of guessed pages.

## 5. Verify schema is live

After wiring a page into the system:
```bash
curl -s "https://www.site.com/tools/<page>?cb=$(date +%s%N)" \
  | grep -o '"@type":"SoftwareApplication"\|"@type":"WebApplication"' | head
# present = schema renders
```
