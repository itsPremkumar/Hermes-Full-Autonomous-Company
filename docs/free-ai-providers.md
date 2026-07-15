# Free AI LLM Providers — Zero-Budget Company Stack

> **Purpose:** a detailed, source-verified catalog of **completely free AI providers and models**
> that the zero-budget autonomous company can route to with **no paid API key** — so LLM inference
> (normally the single biggest cost line) costs **$0**. Usable **with OmniRoute** (unified gateway)
> *or* **without OmniRoute** (directly, per provider).

---

## 🎯 Why this document exists (zero-budget money machine)

We are building a fully autonomous "money-earning machine" company under a **$0 budget** — no paid
API keys, no subscriptions. In the canonical stack:

```
Hermes  (first boss / self-improving orchestrator)
  └─ Paperclip  (ops company: budgets, agents, heartbeats)
       └─ OpenClaw  (channel: phone/Telegram, draft-only)
```

The largest recurring cost for any AI company is **LLM inference**. If every agent, every
automation, and every content pipeline bills a per-token paid model, the budget is dead on arrival.
**The fix:** route all non-critical and high-volume traffic through the **free providers documented
here**. They need no credit card and no paid key, so the company runs at net-zero inference cost.

> This list is a *sub-component* of the company's cost-avoidance strategy. It pairs with the
> `Hermes-Full-Autonomous-Company` repo (OS source of truth) and the OmniRoute gateway.

---

## 🔑 Golden rule — ALWAYS verify against the latest docs

Free tiers, rate limits, and provider Terms of Service **change constantly**. Before relying on any
provider or model below, re-check the two live sources of truth:

1. **OmniRoute's latest free catalog** (canonical, machine-readable):
   `open-sse/config/freeModelCatalog.data.ts` on
   [github.com/diegosouzapw/OmniRoute](https://github.com/diegosouzapw/OmniRoute) →
   `open-sse/config/freeModelCatalog.data.ts`
   and the human-readable `docs/reference/FREE_TIERS.md`.
2. **That specific provider's latest official documentation** (base URL, auth method, current limits,
   ToS). Provider endpoints and "free forever" status move without warning.

> Treat every model ID, base URL, and limit in this file as a **snapshot taken 2026-06-17**
> (OmniRoute's last research refresh, shipped v3.8.40+). Re-verify before production use.

---

## Two ways to use these free models

### Path 1 — WITH OmniRoute (recommended for the company)

OmniRoute unifies 250+ providers behind one OpenAI-compatible endpoint
(`http://localhost:20128/v1`). Connect the Tier-A providers below in the dashboard, point every tool
at the single endpoint, and let smart auto-routing (`model: auto`) spread load across free pools.
This keeps the company's code provider-agnostic and makes swapping a dead free tier a one-line config
change.

### Path 2 — WITHOUT OmniRoute (direct per-provider)

Each free provider also exposes its own API. Use this when you want zero extra infrastructure, or when
a specific provider's direct endpoint is simpler for a single-purpose agent. You still need the
provider's **free** access method (some need a free account/key, others are fully anonymous).

Examples of direct (no OmniRoute) access for the key Tier-A providers:

| Provider | Direct base URL (verify in latest docs!) | Auth for free use |
| --- | --- | --- |
| **Pollinations** | `https://text.pollinations.ai/v1/chat/completions` (OpenAI-compatible) | none (anonymous) |
| **Puter** | `https://api.puter.com/...` (Puter AI chat) | free Puter account |
| **Z.AI / GLM-CN** | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | free BigModel key |
| **SiliconFlow** | `https://api.siliconflow.cn/v1/chat/completions` | free SiliconFlow key |
| **OpenCode Zen / Kilo-gateway** | accessed via their gateway / OmniRoute | free, no key |

> ⚠️ Direct endpoints above are **examples to verify**, not guaranteed-current URLs. Always confirm
> against the provider's latest docs before wiring them into an agent.

---

# 🟢 Tier A — Truly no sign-up, no API key (anonymous)

Works with **zero account**. Connect in the OmniRoute dashboard (Path 1) or call the provider's
free endpoint directly (Path 2).

## Pollinations (keyless · `tos: caution` · ~24 models)

Multimodal (text, image, audio). Anonymous, rate-limited (~1 req / 6–15s).

| Model ID | Notes |
| --- | --- |
| `openai` | OpenAI (Pollinations) |
| `openai-fast` | OpenAI Fast |
| `openai-large` | OpenAI Large |
| `qwen-coder` | Qwen Coder |
| `mistral` | Mistral |
| `gemini-flash-lite-3.1` | Gemini Flash Lite 3.1 |
| `deepseek` | DeepSeek |
| `grok` | Grok |
| `grok-large` | Grok Large |
| `gemini-search` | Gemini Search |
| `perplexity-fast` | Perplexity Fast |
| `perplexity-reasoning` | Perplexity Reasoning |
| `kimi` | Kimi |
| `gemini-large` | Gemini Large |
| `nova-fast` | Nova Fast |
| `nova` | Nova |
| `glm` | GLM |
| `minimax` | MiniMax |
| `mistral-large` | Mistral Large |
| `polly` | Polly (TTS) |
| `qwen-coder-large` | Qwen Coder Large |
| `qwen-large` | Qwen Large |
| `qwen-vision` | Qwen Vision |
| `qwen-safety` | Qwen Safety |

## Puter (keyless · `tos: caution` · 33 models)

OpenAI, Claude, Gemini, DeepSeek, Grok, Llama, Mistral, Qwen, Perplexity.

| Model ID | Notes |
| --- | --- |
| `gpt-5.5` | GPT-5.5 |
| `gpt-5.4` | GPT-5.4 |
| `gpt-5.4-mini` | GPT-5.4 Mini |
| `gpt-5.4-nano` | GPT-5.4 Nano |
| `gpt-4o` | GPT-4o |
| `gpt-4o-mini` | GPT-4o Mini |
| `o3` | OpenAI o3 |
| `claude-haiku-4-5` | Claude Haiku 4.5 |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 |
| `claude-opus-4-7` | Claude Opus 4.7 |
| `google/gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash Lite |
| `google/gemini-3-flash` | Gemini 3 Flash |
| `google/gemini-3.1-pro-preview` | Gemini 3.1 Pro |
| `deepseek/deepseek-v4-pro` | DeepSeek V4 Pro |
| `deepseek/deepseek-v4-flash` | DeepSeek V4 Flash |
| `x-ai/grok-4.3` | Grok 4.3 |
| `x-ai/grok-4.20` | Grok 4.20 |
| `llama-4-scout` | Llama 4 Scout |
| `llama-4-maverick` | Llama 4 Maverick |
| `llama-3.3-70b-instruct` | Llama 3.3 70B |
| `mistral-small-2603` | Mistral Small 4 |
| `mistral-medium-3-5` | Mistral Medium 3.5 |
| `mistral-large-2512` | Mistral Large |
| `devstral-2512` | Devstral 2 |
| `codestral-2508` | Codestral |
| `mistral-nemo` | Mistral Nemo |
| `qwen/qwen3.6-plus` | Qwen 3.6 Plus |
| `qwen/qwen3.5-397b-a17b` | Qwen 3.5 397B |
| `perplexity/sonar` | Perplexity Sonar |
| `perplexity/sonar-pro` | Perplexity Sonar Pro |
| `perplexity/sonar-reasoning-pro` | Perplexity Sonar Reasoning Pro |
| `perplexity/sonar-deep-research` | Perplexity Sonar Deep Research |
| `perplexity/sonar-pro-search` | Perplexity Sonar Pro Search |

## Z.AI / GLM-CN (recurring-uncapped · `tos: ok` · 3 models)

Cleanest free-forever set — terms explicitly permit personal use.

| Model ID | Notes |
| --- | --- |
| `glm-4-flash` | GLM-4-Flash |
| `glm-4.5-flash` | GLM-4.5-Flash |
| `glm-4.7-flash` | GLM-4.7-Flash |

## OpenCode Zen (recurring-uncapped · `tos: caution` · 6 models)

Best free *coding* models, no auth.

| Model ID | Notes |
| --- | --- |
| `opencode/big-pickle` | Big Pickle (stealth) |
| `opencode/deepseek-v4-flash-free` | DeepSeek V4 Flash (free) |
| `opencode/nemotron-3-super-free` | Nemotron 3 Super (free) |
| `opencode/mimo-v2.5-free` | MiMo V2.5 (free) |
| `opencode/north-mini-code-free` | North Mini Code (free) |
| `opencode/nemotron-3-ultra-free` | Nemotron 3 Ultra (free) |

## Kilo-gateway "free" (recurring-uncapped · `tos: caution` · 7 models)

Rotating auto free set (NVIDIA Nemotron, StepFun, Poolside, Nex).

| Model ID | Notes |
| --- | --- |
| `kilo-auto/free` | Kilo Auto Free (auto-router) |
| `stepfun/step-3.7-flash:free` | StepFun Step 3.7 Flash (free) |
| `poolside/laguna-m.1:free` | Poolside Laguna M.1 (free) |
| `poolside/laguna-xs.2:free` | Poolside Laguna XS.2 (free) |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | NVIDIA Nemotron 3 Ultra (free) |
| `nvidia/nemotron-3-super-120b-a12b:free` | NVIDIA Nemotron 3 Super (free) |
| `nex-agi/nex-n2-pro:free` | Nex-N2-Pro (free) |

## SiliconFlow (recurring-uncapped · `tos: caution` · 10 models)

Permanently free `$0` models (free account, no paid key).

| Model ID | Notes |
| --- | --- |
| `deepseek-ai/DeepSeek-V3.2` | DeepSeek V3.2 |
| `deepseek-ai/DeepSeek-V3.1` | DeepSeek V3.1 |
| `deepseek-ai/DeepSeek-R1` | DeepSeek R1 |
| `Qwen/Qwen3-235B-A22B-Instruct-2507` | Qwen3 235B |
| `Qwen/Qwen3-Coder-480B-A35B-Instruct` | Qwen3 Coder 480B |
| `Qwen/Qwen3-32B` | Qwen3 32B |
| `moonshotai/Kimi-K2.5` | Kimi K2.5 |
| `zai-org/GLM-4.7` | GLM 4.7 |
| `openai/gpt-oss-120b` | GPT OSS 120B |
| `baidu/ERNIE-4.5-300B-A47B` | ERNIE 4.5 300B |

## Tencent Hunyuan (recurring-uncapped · `tos: caution` · 1 model)

| Model ID | Notes |
| --- | --- |
| `hunyuan-pro` | Hunyuan Pro (permanently free since 2024) |

## Baidu ERNIE (recurring-uncapped · `tos: caution` · 1 model)

| Model ID | Notes |
| --- | --- |
| `ernie-4.0-8k` | ERNIE 4.0 8K |

## Smaller anonymous / keyless Tier-A providers

| Provider | `tos` | Model count | Example model IDs |
| --- | --- | --- | --- |
| `uncloseai` | caution | 3 | `adamo1139/Hermes-3-Llama-3.1-8B-FP8-Dynamic`, `qwen3.6:27b`, `gemma4:31b` |
| `liquid` | unknown | 1 | `liquid-lfm-40b` |
| `reka` | caution | 2 | Reka family (2 models) |
| `stepfun` | ok | 1 | StepFun free model |
| `sensenova` | caution | 1 | SenseTime public-beta model |

**Tier A total:** ~80+ distinct free models across **12 provider families**, zero API key, zero (or free-only) sign-up.

---

# 🟡 Tier B — Keyless but REQUIRES a login / session cookie (not "no sign-in")

Marked `keyless` by OmniRoute, but you **must be signed in to the host service** (OAuth token or
session cookie). Not usable with a truly anonymous setup.

| Provider | `tos` | Model count | Notable models |
| --- | --- | --- | --- |
| `agy` (Google Antigravity) | **avoid** | 16 | `claude-opus-4-6-thinking`, `claude-sonnet-4-6`, `gemini-3.1-pro-*`, `gemini-3-flash`, `gpt-oss-120b-medium`, `gemini-2.5-flash` |
| `qwen-web` | **avoid** | 3 | `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-plus` |
| `muse-spark-web` (Meta) | **avoid** | 3 | `muse-spark`, `muse-spark-thinking`, `muse-spark-contemplating` |
| `duckduckgo-web` | **avoid** | 6 | `gpt-4o-mini`, `gpt-5-mini`, `claude-3-5-haiku-20241022`, `llama-4-scout`, `mistral-small-2501`, `o3-mini` |
| `blackbox` | **avoid** | 6 | `gpt-4o`, `gemini-2.5-flash`, `claude-sonnet-4`, `deepseek-v3`, `blackboxai`, `blackboxai-pro` |
| `opencode` (GitHub login) | **avoid** | 7 | `big-pickle`, `deepseek-v4-flash-free`, `minimax-m2.5-free`, `ling-2.6-1t-free`, `trinity-large-preview-free`, `nemotron-3-super-free`, `qwen3.6-plus-free` |
| `friendliai` | avoid | 2 | `meta-llama-3.1-70b-instruct`, `meta-llama-3.1-8b-instruct` |
| `iflytek` | avoid | 1 | `generalv3.5` |
| `coze` | avoid | 1 | ByteDance agent platform model |
| `nlpcloud` | avoid | 1 | NLP Cloud free plan model |
| `baichuan` | ambiguous | 1 | Baichuan free model |
| `freemodel-dev` | unknown | 4 | FreeModel dev models |
| `monsterapi` | ambiguous | 1 | MonsterAPI trial model |
| `publicai` | caution | 3 | PublicAI community models |
| `inference-net` | caution | 3 | Inference.net models |
| `sparkdesk` (iFlytek) | caution | 1 | `general` (Spark Lite, free but rate-capped) |
| `t3-web` | avoid | 23 | T3 web free model set |

> **Why "avoid"?** Antigravity, Qwen, Meta (Muse), DuckDuckGo, Blackbox, OpenCode, etc. explicitly
> prohibit accessing their service through third-party/proxy software in their Terms of Service.
> OmniRoute *can* technically route to them if you supply your own logged-in cookie, but doing so
> violates the host's ToS. Use only for personal experimentation, at your own risk — **not** in the
> company's production money-earning pipeline.

---

# ✅ Recommended zero-cost setup for the company

For **genuinely anonymous, low-friction, production-safe** use, connect these Tier-A providers:

1. **Pollinations** — multimodal / quick experiments (anonymous, rate-limited).
2. **Puter** — widest free menu (GPT-5.x, Claude Opus/Sonnet, Gemini, Grok, Perplexity).
3. **GLM-CN / Z.AI** — cleanest terms (`tos: ok`), free forever, solid general quality.
4. **OpenCode Zen** + **Kilo-gateway free** — best free *coding* models (DeepSeek V4 Flash, Nemotron 3, MiMo V2.5).
5. **SiliconFlow** — big open models (DeepSeek R1/V3, Qwen3, Kimi K2.5) if a free account is acceptable.

**Architecture fit:** point every company agent/tool at the single OmniRoute endpoint and set
`model: auto`. OmniRoute's smart routing + the RTK/Caveman compression (~15–95% token savings) stretch
the free quotas further, keeping the whole pipeline at **$0 inference cost**.

### Caveats

- These are **rate-limited** (no published token ceiling) → suited to dev / light / personal + early
  production use, not heavy 24/7 bursts on a single model. Spread load across the pool.
- Stick to `tos: ok` / `caution` entries; skip `avoid` ones for the company pipeline.
- **Re-verify against the latest OmniRoute catalog + each provider's latest docs before shipping.**

---

# 🔧 Quick-start

## With OmniRoute (Path 1)

```bash
# Install & run OmniRoute — single endpoint http://localhost:20128/v1
# https://github.com/diegosouzapw/OmniRoute
# Dashboard → Providers → connect the Tier-A providers above.

curl http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.7-flash",
    "messages": [{ "role": "user", "content": "Hello from a $0 model!" }]
  }'
```

## Without OmniRoute (Path 2 — direct, example)

```bash
# Pollinations — fully anonymous, OpenAI-compatible
curl https://text.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai",
    "messages": [{ "role": "user", "content": "Hello from a free model, no gateway!" }]
  }'
```

> The Pollinations URL above is an example — confirm the current endpoint in Pollinations' latest docs.

---

## Source & license

- Data sourced from **OmniRoute** `open-sse/config/freeModelCatalog.data.ts` (main branch, refreshed
  2026-06-17, shipped v3.8.40+). Re-check the live file for current data.
- OmniRoute is MIT licensed: https://github.com/diegosouzapw/OmniRoute
- This document is a component of the **zero-budget autonomous company** stack
  (see `Hermes-Full-Autonomous-Company`). Provided for reference only; model availability, rate
  limits, and provider Terms of Service change frequently. Always verify against the live catalog and
  the provider's official terms before building on top of it. Not legal advice.
- This catalog document is MIT licensed.
