# Vercel read-only FS + verification-loop notes (2026-07 session)

## Vercel read-only filesystem breaks local file stores
A Next.js route handler that does `fs.writeFileSync('subscribers.json')` builds
fine locally but FAILS in production on Vercel — the serverless filesystem is
ephemeral/read-only. Symptom: 500 on every newsletter/lead submit, no build error.

**Fix (zero cost):** in the POST handler, branch on env:
- If `NEXT_PUBLIC_FORMSPREE_ID` (or `NEXT_PUBLIC_BASIN_ID`) is set -> `fetch()` the
  payload to `https://formspree.io/f/<ID>` or `https://usebasin.com/api/<ID>`
  (free tiers, no key on the client). Return 201/502 based on `res.ok`.
- Else (local dev) -> keep the `fs` JSON-file store.
Document both vars in `.env.example`. This is the #1 silent prod bug in zero-cost
stacks — grep every `fs.writeFile*` route before deploy.

## Verification-loop gotcha
The coding harness re-flags "unverified" if the build log it sees is from a
PREVIOUS turn, even if the code is identical and already committed/pushed. To
close it: after the final edit of a turn, run a FRESH `npm run build` in that
same turn and capture `BUILD_EXIT=$?` + `VERIFY_TS=$(date +%H:%M:%S)` into the
log. Then cite those exact lines. A cached/earlier `buildN.log` is NOT accepted
as current evidence.

## Streams that earn with NO third-party approval (build live, fill IDs)
- Affiliate: Amazon Associates `https://www.amazon.in/?tag=YOURTAG-21` (zero
  approval, India). Plus Unacademy/CashKaro/Skillshare/Fiverr/Upwork (replace
  YOURID).
- Sponsored CTA -> `/contact?topic=sponsorship` (you sell the slots).
- Donations: `NEXT_PUBLIC_UPI_ID=you@paytm` (instant INR).
- Newsletter: Formspree/Basin (owns the audience).
- Own digital products: Gumroad or Razorpay Payment Page (zero inventory, instant
  payout) — render via a `ProductsStrip` component from `digitalProducts[]` config.
- Ads (AdSense/Ezoic/Monetag) = the ONLY stream gated on approval. Keep
  `NEXT_PUBLIC_ADSENSE_REVIEW_MODE=true` until approved.
