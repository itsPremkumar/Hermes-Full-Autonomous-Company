# 🎯 Autonomous Money Goal — Paste-Ready Configuration

> **How to use this file:** Copy the command in Section 1, paste it into your
> Hermes chat, press Enter. The goal loop runs autonomously (no "continue"
> needed). It pauses only at the 3 human gates in Section 4.

---

## 0. One-time prerequisite (raise the turn budget)

The goal loop defaults to 20 turns — not enough for 12 pipelines + infra.
Run this once in your terminal or Hermes chat:

```
hermes config set agent.goal_max_turns 120
```

(If your build exposes a different key, check: `hermes config | grep -i goal`
or `hermes config set goal.max_turns 120`. The tests reference both
`goal_max_turns` and a gateway goal config.)

---

## 1. STEP 1 — Draft the contract (paste this first)

```
/goal draft Build the complete zero-to-revenue autonomous money system from the Hermes-Full-Autonomous-Company repo. Build the 7 remaining pipelines (#6–#12) named in money/MONEY_AUTOMATION_IDEAS.md: lead-enrichment SaaS, RAG-KB builder, affiliate farm, invoice automation, security scanner, proposal generator, social auto-poster. Each must follow the proven shape of pipeline1..5 (data dict + build_package + self-test + --list + --out) and be stdlib-only. Wire every pipeline into money/run_all.py and regenerate money/INCOME_DASHBOARD.md (target: 12 pipelines, ~50 packages). Replace n8n stub manifests with working workflow JSON (real code nodes, not placeholders) so each service can actually deliver. Build infra/docker-compose.yml for n8n + Chatwoot + Stirling-PDF + Listmonk with infra/SETUP.md. Generate platform-ready Fiverr/Upwork listing copy for every package under listings/. Schedule the acquisition loop (Moltbook already runs; add affiliate + cold-email). STOP at the 3 human gates: (1) marketplace account creation, (2) payment linkage, (3) first live gig approval.
```

Hermes returns a 5-field completion contract. Review it.

---

## 2. STEP 2 — Activate the goal (paste the returned contract)

After the draft, paste the activated goal. Example shape (use the exact text
Hermes returns from Step 1):

```
/goal <paste the drafted contract from Step 1 here>
```

The judge now runs turn-after-turn. It will NOT declare done until `verification`
is proven with real command output / file excerpts.

---

## 3. What the loop executes (phases)

| Phase | Work | Verification the judge checks |
|-------|------|-------------------------------|
| A | Build pipelines #6–#12 | each `pipelineN_*.py self-test` exits 0 |
| B | Unify in run_all.py | `python money/run_all.py self-test` → 15 pipelines, 62 packages |
| C | Real n8n workflows | each `*.json` has executable code nodes (no `TODO`/placeholder) |
| D | Infra stack | `infra/docker-compose.yml` + `infra/SETUP.md` present & coherent |
| E | Listing copy | `listings/<pipeline>/<item>.md` exists for every package |
| F | Acquisition loop | Moltbook + affiliate + cold-email scheduled & logged |
| G | **Human gate** | loop pauses, prints the 3-action checklist |

---

## 4. The 3 human gates (loop stops here, you act, then `/goal resume`)

1. **Account gate** — create Fiverr/Upwork accounts (ID verification). Loop stops.
2. **Payment gate** — link PayPal/Stripe (bank, tax). Loop stops.
3. **First-gig gate** — first gig ready to publish. Loop stops; you click Publish.

After each: type `/goal resume` → loop continues to the next phase.

---

## 5. The 7 remaining pipelines (specs for the loop)

| # | Pipeline | Tool basis | Pricing |
|---|----------|-----------|---------|
| 6 | lead-enrichment SaaS | maps-cli + web-research | $99–$299/mo |
| 7 | RAG-KB builder | hermes + openclaw | $500 setup + $149/mo |
| 8 | affiliate farm | polymarket-cli + blog gen | rev-share, $0 cost |
| 9 | invoice automation | n8n + ocr | $49–$149/mo |
| 10 | security scanner | secret-scanner + skill-lint | $199 setup + $99/mo |
| 11 | proposal generator | md-linter + templates | $150–$600/gig |
| 12 | social auto-poster | gif-search + excalidraw | $99–$399/mo |

All reuse the existing 31 ClawHub skills + 100 learned skills. Zero external cost.

---

## 6. Guardrails baked into the contract

- **Constraints:** never break the 5 verified pipelines; keep stdlib-only; judge must see `run_all.py self-test` output as proof.
- **Judge refuses vague done:** demands command output / file excerpts, not "all done" claims.
- **Fail-open + turn budget:** broken judge → continue; 120-turn cap prevents runaway cost.
- **Your message wins:** any real message you send preempts the loop and pauses it for that turn.

---

## 7. Outcome when "done"

- `money/run_all.py self-test` → 15 pipelines, 62 packages, all pass
- `infra/docker-compose.yml` + `SETUP.md` present
- `listings/` has platform-ready copy for every package
- Acquisition loop scheduled
- Loop paused at gate #1 with your 3-action checklist

You do the 3 gates (~15 min total) → first client → recurring revenue.

---

## 8. Alternative: in-session autonomous build (no `/goal` needed)

If you'd rather I just **start building now in this chat** (treating your
standing instruction as the goal), say **"go"** and I'll execute Phases A–F
across turns without per-step prompts. Same result, bootstrapped by your
authorization instead of the slash command. The `/goal` above is for true
hands-off operation you can trigger anytime.
