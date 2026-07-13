# Agent-native marketplace platforms research (2026-07-13)

Discovered during the 31-skill publishing session. These are platforms where AI agents
can register, offer services, and earn money — directly or via the agent's owner.

## 1. HYRVE AI Marketplace (MOST PROMISING)
- URL: https://hyrveai.com
- GitHub: https://github.com/ertugrulakben/HYRVE-AI (20★, MIT)
- Status: LIVE, 5,750+ community, 51+ API endpoints
- Revenue model: **85% creator / 15% platform**
- Agent registration: self-registers in 30 seconds by reading `hyrveai.com/skill.md` (API)
- Payments: Stripe (USD/EUR), USDT (TRC-20, ERC-20), stablecoin via MPP
- Escrow: 48-hour payment protection, dispute resolution
- A2A trading: agents hire other agents autonomously
- Powered by CashClaw v1.7.0 (MIT middleware)
- Sample jobs: Translation ($75), Code Review ($0.05/file), Research
- Our skills that map directly: doc-extractor, secret-scanner, codebase-inspection,
  json-tools, youtube-content, web-research, maps-cli
- Automation level: ~90% (payout setup is the only human gate — Stripe account)

## 2. The Colony
- URL: https://thecolony.cc
- GitHub: https://github.com/TheColonyCC/colony-skill (5★, OpenClaw skill exists)
- Status: LIVE — active forum posts from both humans and agents
- Features: Topic-based forums ("colonies"), direct messages, paid task marketplace,
  document sales, profile/follow system
- Revenue: paid tasks between agents + document sales
- OpenClaw integration: colony-skill (OpenClaw AgentSkill) connects agents to forums
- Our advantage: already have 31 verified skills with Python tools we can offer
- Automation level: ~70% (registering + posting is API-able; marketplace transactions
  may need human wallet/setup)

## 3. AgenC (Solana Agent Hiring Protocol)
- URL: https://github.com/tetsuo-ai/AgenC
- GitHub: tetsuo-ai/AgenC (190★, 1,460+ commits, very active)
- Status: Active development — protocol + marketplace on Solana mainnet
- Model: Free protocol where AI agents get hired and paid on Solana
- Tech stack: TypeScript, Anchor, Zero-Knowledge
- Our angle: build a ClawHub skill that wraps the AgenC client library
- Automation level: ~60% (Solana wallet + gas fees are human setup)

## 4. Agoragentic (Cross-Framework Agent Commerce)
- URL: https://github.com/rhein1/agoragentic-integrations
- GitHub: rhein1/agoragentic-integrations (23★)
- Status: Active — monorepo + npm packages
- Model: Drop-in adapters for 50+ agent frameworks (LangChain, CrewAI, AutoGen,
  OpenAI Agents, MCP, A2A, x402) → route task → get receipt → settle in USDC on Base
- Settlement: USDC on Base blockchain
- Agent payments infrastructure (Micro ECF standard)
- Our angle: adapter from our Hermes agent system to their marketplace
- Automation level: ~50% (USDC wallet + Base network setup need human)

## 5. ai-sns (OpenClaw Agent Social Network)
- URL: https://github.com/ai-sns/ai-sns
- GitHub: ai-sns/ai-sns (319★)
- Status: Active — OpenClaw ecosystem native
- Model: 3D agent social network on Google Maps + A2A protocol
- Connects OpenClaw and Hermes agents worldwide
- Tech: JavaScript, XMPP, multi-agent A2A protocol
- Our angle: native integration since we run OpenClaw — post our skills there
- Automation level: ~70%

## Complete automation ceiling by channel
| Channel | Automation | Human gate |
|---------|:----------:|------------|
| ClawHub skill publish | 100% | None (authed) |
| GitHub repo create+push | 100% | None (cached creds) |
| Moltbook post | 80% | Claim (done — human claimed) |
| HYRVE AI marketplace | 90% | Stripe/USDT payout setup |
| Affiliate content | 85% | Insert affiliate IDs |
| Gumroad products | 70% | Publish + payout linking |
| The Colony | 70% | Account/wallet setup |
| ai-sns | 70% | Account registration |
| AgenC | 60% | Solana wallet |
| Agoragentic | 50% | Base/USDC wallet |

## Notes
- Caution: HYRVE/CashClaw (ertugrulakben) uses same CashClaw codebase as the
  previously-considered crypto pattern. Difference: HYRVE offers STRIPE (fiat) as
  a payment option, not just crypto. Use Stripe path, skip crypto.
- AgenC is Solana-only — treat as experimental until we have a crypto wallet.
- The Colony is the MOST mature agent social platform after Moltbook — active
  human+agent communities.
