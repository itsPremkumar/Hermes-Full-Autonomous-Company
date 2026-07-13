# Sproutern clone / rebrand — concrete intel (2026-07)

## Source repo
- `itsPremkumar/sproutern-open-source` — the user's OWN repo (they own "Sproutern").
- Stack: **Next.js 16 + Firebase + Google Genkit AI**.
- Features: 200+ career tools, 180+ games, AI resume builder, career roadmaps.
- License: MIT. Version 5.6.8. Deployed (original) on a `.vercel.app` preview URL.
- 3 GitHub stars — NOT high traffic. (Cloning does not transfer traffic.)
- **AdSense history: REJECTED for "low-value content"** — auto-generated blog
  (`scripts/gen-content.ts`), future-dated posts (`src/lib/blog-data.ts`), thin
  blog architecture. This rejection carries to any clone unless content is cleaned.

## Required backend keys (`.env.example`)
Needed ONLY if keeping Firebase/Genkit (Path B):
```
NEXT_PUBLIC_FIREBASE_API_KEY
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN
NEXT_PUBLIC_FIREBASE_PROJECT_ID
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID
NEXT_PUBLIC_FIREBASE_APP_ID
NEXT_PUBLIC_FIREBASE_VAPID_KEY
```
+ a Gemini API key for Genkit AI. All are user-supplied; the agent cannot create them.
For Path A (recommended), strip these deps so no keys are needed.

## Rebrand checklist (MIT-safe)
1. Keep `LICENSE` `Copyright (c) 2026 Sproutern` line — do NOT remove.
2. `rm` the original owner's GSC verify file `googlec26fda405340f88f.html`.
3. Replace product name in: `package.json` (name), `README.md`, UI strings,
   `src/` metadata, SEO titles/descriptions, `vercel.json`/`.github/` templates.
4. Add trust pages: Privacy Policy, About, Contact, Terms.
5. If re-applying for AdSense: remove auto-generated blog, fix future dates,
   add 20–40+ original substantive pages.

## Clone locations this session
- Started: `C:\Users\PREM KUMAR\money-engine\careerspark`
- Moved to: `C:\Users\PREM KUMAR\Downloads\careerspark`  (user's chosen final location)

## Clean static alternative (better for AdSense)
`masterkram/minted-directory-astro` — https://github.com/masterkram/minted-directory-astro
- 154*, MIT, Astro + TailwindCSS, SEO-optimized, programmatic SEO out of the box.
- Built-in **Sponsored Content** slots; tags + search; dark/light; add listings via
  Markdown / CSV / JSON / Google Sheets / Notion / Airtable (automation-friendly).
- Demo: https://minteddirectory.com. Deploys free to Cloudflare Pages.
- For ad revenue this is easier to get approved than the Next.js/Sproutern app and
  runs free on an 8 GB laptop.

## Income streams mapped to a career-tools site
Affiliate (courses/SaaS) · sponsored listings · lead-gen (privacy-compliant) ·
freemium AI · display ads (only AFTER content cleaned + real traffic) · donations.
Start with affiliate + sponsored + donations (no approval needed); pursue ads last.
