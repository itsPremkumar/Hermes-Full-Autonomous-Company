# Making noindexed thin pages indexable (editorial-content rollout)

Sites often **deliberately noindex thin pages** (bare calculators/tools with no prose) to
avoid Google's thin/duplicate-content penalty. Un-noindexing them WITHOUT adding content
just re-creates thin pages. The correct free-plan growth move: add real per-page editorial
content FIRST, then clear the noindex list. This is a large but high-ROI organic lever.

## 0. Diagnose: is the sitemap gap intentional?

A sitemap that lists fewer URLs than route dirs is often NOT a bug. Check for an explicit
noindex policy before "fixing" it:

```bash
curl -s "https://site/sitemap.xml" | grep -oE "<loc>[^<]+</loc>" | grep -c "/tools/"   # e.g. 52
ls src/app/tools | wc -l                                                                # e.g. 100
# find the policy that filters them:
grep -rn "noindex\|NOINDEX\|shouldIndexPath\|shouldNoindex" src/lib/seo src/app 2>/dev/null
```

sproutern (2026-07-11): `src/lib/seo/indexing-policy.ts` held `NOINDEX_TOOL_SLUGS = new Set([...])`
with 49 slugs + comment "temporarily excluded until editorial long-form sections are added".
Sitemap auto-walks `src/app` for `page.tsx` but `dedupeSitemapEntries` filters via
`shouldIndexPath()`. So 52 = 100 − 48-ish. **The gap was intentional, not a bug.** The real
opportunity was to earn indexation by adding content, and to notice several HIGH-VALUE tools
(currency-converter, gpa-calculator, tax-calculator) were suppressed and likely never revisited.

## 1. Build ONE reusable editorial component (not N inline blocks)

Create a server component that takes a `slug` and renders intro + use-cases + FAQ, using the
`.key-takeaway` / `.faq-answer` classes the root JSON-LD `speakable` selector points at — so
this ALSO reconnects the dead speakable/AEO signal (see geo-structured-data-audit.md §2).

```tsx
// src/components/seo/tool-editorial.tsx  (server component, static, no client JS)
import { ToolEditorialContent } from '@/lib/seo/tool-editorial-content';
export function ToolEditorial({ slug }: { slug: string }) {
  const d = ToolEditorialContent[slug];
  if (!d) return null;                       // safe fallback — never crashes a page
  return (<section aria-label={`${d.name} guide`}>
    <div className="key-takeaway"><h2>{d.name}: What it does</h2><p>{d.intro}</p></div>
    {/* use-cases <ul>, FAQ list with <p className="faq-answer"> */}
  </section>);
}
```

Content lives in a data file `tool-editorial-content.ts` = `Record<slug, {name, intro, useCases[], faqs:{q,a}[]}>`.
Write UNIQUE, tool-specific content per slug (name is self-describing → derive accurate copy).
Generic/templated filler = duplicate-content risk. 3 use-cases + 3 FAQs per tool is a good floor.

## 2. Reconcile slug lists BEFORE wiring (prevents thin re-creation)

The noindex set and your content file MUST match. Diff them:
```bash
grep -oE "^  '[a-z0-9-]+': \{" tool-editorial-content.ts | tr -d "': {" | sort -u > /tmp/content.txt
sed -n '/NOINDEX_TOOL_SLUGS/,/^]);/p' indexing-policy.ts | grep -oE "'[a-z0-9-]+'" | tr -d "'" | sort -u > /tmp/noindex.txt
comm -23 /tmp/noindex.txt /tmp/content.txt   # in noindex but NO content -> would become thin. ADD content.
```

## 3. Wire the component per tool (handle BOTH client and server pages)

Client tool pages have a sibling `layout.tsx`; server tool pages may have NONE. A robust
scripted rollout that handles every return form + creates missing layouts:

```bash
while read s; do
  IMP="import { ToolEditorial } from '@/components/seo/tool-editorial';"
  F="src/app/tools/$s/layout.tsx"
  if [ -f "$F" ]; then
    grep -q ToolEditorial "$F" && continue                              # idempotent guard
    # 'use client' MUST stay line 1 -> insert import at line 2 if present, else line 1:
    head -1 "$F" | grep -q "use client" && sed -i "2i $IMP" "$F" || sed -i "1i $IMP" "$F"
    if grep -q "return children;" "$F"; then
      sed -i "s#return children;#return (<>\n<ToolEditorial slug=\"$s\" \/>\n{children}\n<\/>);#" "$F"
    elif grep -q "{children}" "$F"; then
      sed -i "s#{children}#<ToolEditorial slug=\"$s\" \/>\n{children}#" "$F"
    fi
  else                                                                  # server page, no layout -> create one
    printf '%s\n\nexport default function Layout({ children }: { children: React.ReactNode }) {\n  return (\n    <>\n      <ToolEditorial slug="%s" />\n      {children}\n    </>\n  );\n}\n' "$IMP" "$s" > "$F"
  fi
done < /tmp/noindex.txt
```

Pitfalls baked in above:
- `'use client'` must remain the first line — inserting an import at line 1 breaks the build.
- A tool's layout `return children;` (variable) vs `<>{children}</>` (JSX) need different edits.
- Guard on `grep -q ToolEditorial` so re-runs don't double-insert.

## 4. Clear the noindex list

Empty the set (keep the export + type so imports don't break):
`const NOINDEX_TOOL_SLUGS = new Set<string>([]);` with a dated comment explaining why.

## 5. Verify live (deploy READY → prove indexable + content + sitemap)

```bash
# sitemap grew:
curl -s "https://site/sitemap.xml?cb=$(date +%s)" | grep -oE "<loc>[^<]+</loc>" | grep -c "/tools/"   # 52 -> 101
# each page now index,follow (NOT noindex) + renders editorial + speakable classes:
for t in currency-converter tax-calculator qr-code-generator; do
  h=$(curl -s "https://site/tools/$t?cb=$(date +%s)")
  echo "$t: $(echo "$h" | grep -oiE 'name=\"robots\" content=\"[^\"]*\"' | head -1) | faq-answer=$(echo "$h" | grep -oc faq-answer)"
done
```
Expect `content="index, follow"` and `faq-answer` ≥ 1. Suggest the user resubmit the sitemap
in Google Search Console to speed re-crawl.

sproutern result: sitemap tool URLs 52 → 101; 49 tools flipped noindex → index,follow with
unique FAQ/intro content; speakable signal reconnected. All: tsc exit 0, ESLint exit 0.
