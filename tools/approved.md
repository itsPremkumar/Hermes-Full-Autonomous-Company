# Approved Tools

Validated tools the company actually runs. Each entry: what it's for, how to run it, license, footprint.

## Paperclip
- **Role:** Org chart, budgets, governance, ticketing (the "company" layer)
- **How to run:** `npx paperclipai onboard` → API on `http://127.0.0.1:3100`; data in `~/.paperclip/instances/default`
- **License:** OSS (paperclipai/paperclip)
- **Footprint:** embedded Postgres; keep only when company ops active
- **Status:** RUNNING — 7 agents, 7 heartbeats on

## Hermes Agent
- **Role:** Executive/growth agent (CEO hire)
- **How to run:** `hermes setup [--portal]`; hired into Paperclip via `hermes_local` (same machine) or `hermes_gateway` adapter
- **License:** OSS (Nous Research)
- **Footprint:** model-dependent; default to local model to save RAM
- **Status:** RUNNING

## OpenClaw
- **Role:** Comms + computer-use / GUI automation agent
- **How to run:** `openclaw onboard`; hired via `openclaw_gateway` adapter
- **License:** OSS
- **Footprint:** light when idle; close after task
- **Status:** installed, config at `~/.openclaw/openclaw.json`

## hermes-paperclip-adapter
- **Role:** Bridges Hermes into Paperclip (CEO↔company)
- **How to run:** `cd hermes-paperclip-adapter && npm i && npm run build` (source committed; `node_modules` excluded from repo)
- **License:** see `hermes-paperclip-adapter/LICENSE`
- **Status:** present in repo at `hermes-paperclip-adapter/`

## Automated-Video-Generator (AVG)
- **Role:** Remotion + Edge-TTS + stock-media text-to-video pipeline (product line)
- **Repo:** `itsPremkumar/Automated-Video-Generator` (separate, MIT)
- **Status:** referenced; PRs PRE-14..PRE-16 (CI, subtitle burn-in, batch queue)

## OmniRoute → OpenRouter
- **Role:** Free LLM routing across providers via one key
- **How to run:** `C:\one\omniroute\start-omniroute.bat`; key in `~/.openrouter_key` (never commit)
- **Status:** RUNNING (gateway on loopback :18789)

## Git (cached creds)
- **Role:** Push to GitHub (single source of truth)
- **How to run:** credential helper `manager`; token cached for `itsPremkumar`
- **Status:** working — no token typing needed
