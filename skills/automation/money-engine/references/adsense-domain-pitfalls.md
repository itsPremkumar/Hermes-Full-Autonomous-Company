# AdSense / Domain / Content-quality pitfalls (learned 2026-07)

Condensed knowledge bank for zero-cost income sites that monetize via ads
(AdSense / Ezoic) or affiliate. Verified this session via live GitHub API
checks + README inspection of candidate templates and the user's own repo.

## 1. Free subdomains are a BAD base for AdSense approval
- `.us.kg`, `.dpdns.org`, `.xx.kg`, `.qzz.io`, `.qd.je` (DigitalPlat FreeDomain),
  and `.blogspot.com` are **frequently rejected** by AdSense.
- Reason: heavily used by spammers -> low trust in Google's eyes; even if
  approved, ad RPM is typically lower.
- **Use free domains for:** testing, learning, affiliate links, traffic
  experiments. **Buy a cheap real TLD for AdSense:** `.com` ~Rs80-150/yr
  (Namecheap/Porkbun), `.in` often cheaper. One small spend hugely improves
  approval odds + earnings.

## 2. "Low value content" rejection -- real case study
User's own repo `itsPremkumar/sproutern-open-source` (Next.js 16 + Firebase +
Google Genkit AI, 200+ tools, 180+ games) was **already rejected by AdSense**
for "low value content". Its own `docs/ADSENSE_COMPLIANCE_PLAN.md` admits:
- Blog posts had **future dates** (manipulative signal).
- Content was **auto-generated** (`scripts/gen-content.ts`) of questionable quality.
- Blog architecture "strongly signals to Google that the content is thin or
  designed to manipulate search rankings."
Lesson: auto-generated/low-effort content + thin structure = rejection. Fix by
removing auto-gen, adding real original articles, fixing dates, adding trust
pages (Privacy / Terms / About / Contact).

## 3. Best template class for ad revenue (static > heavy app)
| Template | Stack | Verdict for AdSense |
|---|---|---|
| **minted-directory-astro** (154*, MIT) | Astro + Tailwind, static | BEST -- programmatic SEO, sponsored-content slots, markdown/CSV/Notion listings, deploys to Cloudflare Pages |
| riseofmachine (96*) | AI-agent-curated dir | Good, smaller community |
| FreshRSS (15k*) | Personal RSS reader | High quality but not a money site |
| watt-guide (1*) | AdSense demo | Just a demo, not a template |
| EatMyURL (37*) | Link shortener | Narrower use case |
| Sproutern (user's, 3*) | Next.js+Firebase+Genkit | Already AdSense-rejected; heavy stack, needs backend + AI keys (not free to run) |

Rule of thumb: a clean **static, SEO-optimized directory with ORIGINAL
listings** is easier to get approved than an auto-generated blog or a heavy
stateful app. Keep the build static (Astro/Cloudflare Pages) so it runs free on
an 8 GB laptop.

## 4. Verified-free domain provider: DigitalPlat FreeDomain
- Repo `DigitalPlatDev/FreeDomain`: **184k*, 3.8k forks, AGPL-3.0, created
  2024-05, last pushed 2026-04** (alive). Maintainer Edward Hsing.
- Claims 500k+ domains registered. Dashboard: `dash.domain.digitalplat.org`.
- Extensions: `.dpdns.org`, `.us.kg`, `.xx.kg`, `.qzz.io`, `.qd.je`.
  Limit **1 domain per account**. Works with Cloudflare/FreeDNS/Hostry.
- **Legit, not a scam** (publicly warns its old Telegram was hacked). Good for
  staging/affiliate/testing; NOT a substitute for a real TLD for AdSense.

## 5. AdSense approval checklist (content side)
- 20-40+ pages of **original, substantive** content (not just link lists).
- Required pages: Privacy Policy, About, Contact, Terms.
- Organic value a visitor wants; no auto-spun text.
- Site age 1-3 months with some traffic helps but isn't strictly required.
- Build on free domain first, then point a cheap real domain at it for the
  AdSense application.
