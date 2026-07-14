# How I Built a Zero-Cost AI Company

*Submission target: Better Programming / Towards Data Science · Medium Partner Program*

> Everyone says "AI will change business." I decided to find out by actually building one — with no funding, no team, and no software budget. Here is exactly how it works, what it cost, and the parts that still need a human.

## The setup nobody talks about

When people imagine an "AI company," they picture a seed round, a Slack full of engineers, and a GPU bill. My version is different. Prem Autonomous Co runs on a single low-RAM laptop, a handful of open-source tools, and a hard rule: **spend nothing that isn't already free.**

The core engine is an autonomous agent operating system (I use Paperclip, an open-source agent orchestration layer, paired with the Hermes agent runtime). Together they give me a small fleet of AI agents — a CTO/engineer, a researcher, a writer, a reviewer, an operator — that pick up real work items and move them to a finished, verified state without me hand-holding every step.

The total recurring software cost is **$0**. Domain name and email are the only line items, and even those are optional for a prototype.

## Why zero-cost is a feature, not a constraint

Scarcity forces good architecture. When you can't just throw compute or SaaS subscriptions at a problem, you design for leverage instead of volume.

Three decisions made this possible:

1. **Free and open-source tooling only.** No paid orchestration platform, no per-seat SaaS. The agent runtime is self-hosted. The video pipeline (Remotion + Edge-TTS + CC0 stock media) renders locally at zero per-render cost.
2. **Output is the unit of value, not tokens.** I don't sell "access to an AI." I sell finished, reviewed deliverables: code, docs, narrated video, research, automation. The buyer never prompts an LLM or runs a build — they get the artifact.
3. **Human-in-the-loop only where real money moves.** Agents draft, package, write, and track. A human approves anything that touches a payment, a public publish, or a customer commitment. That boundary is what keeps the whole thing legal and honest.

## The actual weekly loop

Here's what a quiet week looks like:

- **Monday:** the research agent reads ~20 RSS sources, summarizes trends, and proposes 2–3 content angles.
- **Drafting:** the writer turns the chosen angle into a long-form article plus 15 repurposed assets (LinkedIn post, newsletter section, video script, tweet thread).
- **Review gate:** the reviewer agent checks each asset for factual drift, broken structure, and off-brand tone before anything is marked ready.
- **Packaging:** a digital product (prompt pack, playbook, template) gets its README, files, and Gumroad listing copy generated and staged.
- **Reporting:** the operator agent logs what shipped, what's blocked, and what's waiting on human publish approval.

The founder's job is direction and approval — roughly 90 minutes of decisions a week, not 40 hours of execution.

## What it actually cost me

- Software: $0 (all OSS / free tiers)
- Domain + email: ~$47/year
- Compute: the laptop I already own
- Time: ~90 min/week of review; the rest is agent runtime

There is no inference bill in my current setup because the agent runtime defaults to a local/free-tier model and only escalates to a stronger model when a task genuinely needs it. For a content-and-code company, that's enough.

## The parts that still need a human (and why that's fine)

I will not pretend this is fully unattended. Three things stay human:

1. **Publishing.** YouTube, TikTok, Gumroad, LinkedIn, Medium all require authenticated accounts. The agent stages everything; a human clicks "Publish." This is a feature — it's the honesty gate.
2. **Pricing commitments.** Quoting a public rate is a commercial promise. Agents draft and stage the pricing page; the founder confirms the floor before it goes live.
3. **Customer relationships.** Replies to real leads are written by the agent but sent by a human, so a real person owns the relationship.

## What I'd tell anyone starting today

Start before you're ready. The bottleneck in the agent economy is not execution — agents are cheap at the margin. The bottleneck is *having something worth shipping* and the discipline to ship it weekly.

Pick one function you can fully automate (content, a niche service, a digital product). Prove the loop works on a $0 stack. Then expand. The infrastructure is free; the leverage is in the system you design.

If you want the exact playbook — agent roles, review gates, packaging scripts — it's in the company showcase repo. But the principle fits on a sticky note:

> Spend nothing. Ship weekly. Keep a human on the money.

That's the whole company.
