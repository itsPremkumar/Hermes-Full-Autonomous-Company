# PRE-52 — Gumroad Launch Runbook (human action required)

Status of the AI-agent portion: COMPLETE. All three products are built and packaged
as upload-ready folders under:

  income-engine/gumroad/products/
    ├── sales-prompts-pack/                (PRODUCT.md 68KB + LISTING.txt  -> $19)
    ├── ai-content-machine-blueprint/      (PRODUCT.md 74KB + LISTING.txt  -> $47)
    └── zero-to-10k-ai-agents/             (PRODUCT.md 96KB + LISTING.txt  -> $19)

Each folder contains:
  - PRODUCT.md  = the actual deliverable file the buyer downloads (full product)
  - LISTING.txt = copy-paste Title / Price / Description / Category + publish steps

The remaining steps (account creation, payout linking, and clicking "Publish") are
HUMAN-ONLY and cannot be performed by an AI agent or the Gumroad API without your
logged-in session and identity/tax verification.

────────────────────────────────────────────────────────────────────────────
STEP-BY-STEP (est. 30–45 min)

1. CREATE ACCOUNT
   - Go to https://gumroad.com and sign up with the business email.
   - Verify email. Gumroad may ask for identity (and, for payouts, tax info).

2. LINK PAYOUTS
   - Settings > Payouts. Connect a bank account or PayPal.
   - This is required before you can receive any sales revenue.

3. PRODUCT A — 100 Sales Prompts Pack ($19)
   - Products > New product.
   - Name:    copy from sales-prompts-pack/LISTING.txt (Title line)
   - Price:   $19
   - Category: Sales & Marketing Templates
   - Description: copy the Description block from LISTING.txt
   - Add file: upload PRODUCT.md (set access = "Software / File")
   - Publish.

4. PRODUCT B — AI Content Machine Blueprint ($47)
   - Repeat with ai-content-machine-blueprint/LISTING.txt (Price $47,
     Category: Business & Productivity), upload its PRODUCT.md.

5. PRODUCT C — Zero to $10k/mo ebook ($19)
   - Repeat with zero-to-10k-ai-agents/LISTING.txt (Price $19,
     Category: Technology & Business), upload its PRODUCT.md.

6. VERIFY
   - Open each product's public URL, confirm price + file download works.
   - Optional: set up a 30-day refund policy note (already in listing copy).

────────────────────────────────────────────────────────────────────────────
NOTES
- Gumroad fee is ~10% of each sale (you keep the rest). No listing cost.
- The source products live in revenue/digital-products/. These packages are
  faithful copies of those files (same byte content).
- If you want the agent to also generate cover images / preview thumbnails,
  ask in the issue thread and assign back to the agent.
- After you publish, paste the 3 product URLs into this issue so the agent can
  record them as `preview_url` work products and close PRE-52.

Unblock owner: Prem Kumar (human) — Gumroad account + payout + publish.
