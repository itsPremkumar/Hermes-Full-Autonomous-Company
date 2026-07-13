# 🎯 COMPLETE END-TO-END FREE MONEY AUTOMATION — GOAL PROMPT

Paste-ready `/goal draft` text (Section 1) + activation (Section 2).
This closes BOTH blockers from today: delivery is deployed, and a free
conversion path exists — so the loop runs on 100% free rails, no marketplace fees.

================================================================
## SECTION 1 — PASTE THIS AS A SLASH COMMAND
================================================================

/goal draft Build a COMPLETE end-to-end, 100%-free, autonomous money system inside the Hermes-Full-Autonomous-Company repo at C:\one\paperclip-company — no paid tools, no marketplace fees, no API keys required. The loop must run on free rails only:

(1) DELIVERY — make it real, not specs:
  - Write deploy.sh that runs `docker compose -f infra/docker-compose.yml up -d` and prints service URLs.
  - Emit REAL importable n8n workflow .json files (n8n export format: {nodes,connections,settings}) for the 3 highest-margin pipelines (SEO/Audit Reporter, Invoice Automation, Lead-Enrichment), each with executable code/function nodes (no TODO/placeholder), referencing only FREE env vars the user can set later ($env.GOOGLE_FORM_ID, $env.MAPS_KEY optional).
  - Build n8n import docs in infra/N8N_IMPORT.md (how to drag-drop each .json).

(2) CONVERSION — free path so prospects can actually buy:
  - Build a one-page static landing site (pure HTML/CSS, no framework) under site/ that lists the top 8 packages with price + a Google Forms intake link + UPI ID premkumar016555@oksbi displayed prominently.
  - Add GitHub Pages publish config (.nojekyll + instructions in site/README.md) so it hosts free at <user>.github.io.
  - Add the Google Forms intake URL field to GO_LIVE_CHECKLIST.md and PAYMENT.md.

(3) ACQUISITION — already partly done, finish it:
  - Keep the Moltbook 3-min scheduler; add 3 X/Threads cross-post drafts (free, no API key — user pastes manually or via free RSS) under revenue/moltbook/.
  - Ensure generate_moltbook_drafts.py + generate_listings.py stay in sync with run_all.py.

(4) VERIFY end-to-end with NO paid dependency:
  - python money/run_all.py self-test  -> 12 pipelines, 50 packages
  - bash infra/deploy.sh --check (validates compose file + lists URLs) — must not require Docker running
  - python -c to assert every emitted n8n .json parses and has nodes+connections
  - site/index.html exists and contains the UPI ID + a form link

STOP and pause only at the 3 human gates: (1) deploy infra on a free/cheap VPS or localhost, (2) create the free Google Form + GitHub Pages repo, (3) share the live site + UPI to first client.

================================================================
## SECTION 2 — AFTER DRAFT RETURNS A CONTRACT, PASTE:
================================================================

/goal <paste the exact contract text Hermes returned in Section 1>

================================================================
## ONE-TIME PREREQ (raise loop budget so it finishes):
================================================================

hermes config set agent.goal_max_turns 150

================================================================
## WHAT "FREE" MEANS HERE (no cost at any step):
================================================================

| Layer        | Free tool                        | Cost |
|--------------|----------------------------------|------|
| Landing      | GitHub Pages (static site/)      | $0   |
| Intake       | Google Forms                     | $0   |
| Delivery     | n8n self-hosted (docker-compose) | $0*  |
| PDF/render   | Stirling-PDF self-hosted         | $0*  |
| Email        | Listmonk self-hosted             | $0*  |
| Support      | Chatwoot self-hosted             | $0*  |
| Payment IN   | UPI premkumar016555@oksbi        | $0   |
| Marketing    | Moltbook + X/Threads (manual)    | $0   |
| Compute      | localhost OR free-tier VPS       | $0*  |

* $0 if run on your own machine. A 24/7 VPS is optional ($5-20/mo) but NOT
  required to prove the loop — localhost works for delivery + tests.

================================================================
## THE END-TO-END FREE LOOP (once gates cleared):
================================================================

  Client sees Moltbook/X post
        → clicks free GitHub Pages landing (site/index.html)
        → fills free Google Form (intake)
        → n8n (self-hosted) picks up form → runs free delivery
          (SEO scan via secret-scanner, invoice via Listmonk, lead enrich via maps)
        → delivers result (Stirling-PDF / email)
        → client pays via UPI premkumar016555@oksbi
        → money in bank. Zero platform fees. Zero API cost.

================================================================
## HUMAN GATES (loop pauses here, ~20 min total):
================================================================

  Gate 1: run infra/deploy.sh on localhost (or free VPS)  -> docker up
  Gate 2: create free Google Form + free GitHub Pages repo -> publish site
  Gate 3: paste live site URL + UPI to first prospect

After Gate 3 the loop is fully autonomous and free.
