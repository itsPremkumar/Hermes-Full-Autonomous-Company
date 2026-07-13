# 🏭 AI Content Machine Blueprint
## Build Your Autonomous Content Team with Paperclip + Hermes

**Version:** 1.0  
**Format:** Digital Blueprint (PDF / Markdown)  
**Price Point:** $47  
**Audience:** Indie Hackers & Solopreneurs (US/UK Markets)  
**Stack:** Paperclip AI Agent Framework + Hermes Agent Orchestrator

---

> *"Stop trading time for content. Deploy three AI agents that plan, write, and publish for you while you build your product."*

---

## Table of Contents

1. [Overview & What This Blueprint Delivers](#1-overview--what-this-blueprint-delivers)
2. [System Architecture](#2-system-architecture)
3. [Agent Personas & Configs](#3-agent-personas--configs)
4. [Step-by-Step Deployment Guide](#4-step-by-step-deployment-guide)
5. [SOPs for Each Agent](#5-sops-for-each-agent)
6. [Prompt Library (20 Prompts)](#6-prompt-library-20-prompts)
7. [Tool Integration Guide](#7-tool-integration-guide)
8. [Example Workflow — 1 Week of Autonomous Content](#8-example-workflow--1-week-of-autonomous-content)
9. [Appendix — Troubleshooting & FAQ](#9-appendix--troubleshooting--faq)

---

## 1. Overview & What This Blueprint Delivers

### The Problem

Content marketing is the highest-ROI channel for indie hackers and solopreneurs — but it's a full-time job. Researching topics, writing drafts, editing, formatting, scheduling, cross-posting, and engaging with comments consumes 15–25 hours per week that you could spend on product development.

### The Solution

The **AI Content Machine** is a proven blueprint for deploying three autonomous AI agents — orchestrated by Hermes and running on the Paperclip framework — that handle your entire content operation end-to-end.

### What You Get

| Asset | What It Does |
|-------|-------------|
| **Content Strategist Agent** | Researches topics, analyzes competitors, generates content calendars, briefs the Writer |
| **Writer Agent** | Produces long-form articles, LinkedIn posts, Twitter threads, and newsletters from briefs |
| **Editor/Publisher Agent** | Proofreads, formats for each platform, schedules, publishes, and monitors performance |

### What This Blueprint Delivers

✅ Complete Paperclip agent configurations (copy-paste JSON)  
✅ 20 battle-tested content prompts covering 6 content types  
✅ Deployment guide — go from zero to publishing in under 60 minutes  
✅ SOP workflows for the full brief → draft → review → publish cycle  
✅ Platform-specific formatting guides for LinkedIn, Medium, WordPress, and Substack  
✅ A sample 7-day content calendar showing exactly what happens each day  
✅ Troubleshooting guide for common issues  
✅ **No AI experience required** — if you can edit a JSON file, you can run this

### Prerequisites

- A server or VPS (minimum 2GB RAM — $10–20/month from Linode, DigitalOcean, or Hetzner)
- Hermes Agent installed and running (your existing setup)
- Paperclip framework installed (covered in the deployment guide)
- API keys for: OpenAI (GPT-4o or Claude 3.5 Sonnet), your target platforms
- Basic familiarity with the command line (running `hermes` commands)

---

## 2. System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    HERMES AGENT ORCHESTRATOR                   │
│          (Schedules, Triggers, Monitors, Logs)                 │
└──────────┬──────────────────────┬──────────────────┬──────────┘
           │                      │                  │
           ▼                      ▼                  ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│  CONTENT STRATEGIST │ │  WRITER AGENT   │ │  EDITOR/PUBLISHER   │
│  (Paperclip Agent)  │ │ (Paperclip Agent)│ │  (Paperclip Agent)  │
├─────────────────────┤ ├─────────────────┤ ├─────────────────────┤
│ • Market research   │ │ • Article       │ │ • Grammar & style   │
│ • Topic discovery   │ │   generation    │ │ • Platform formatting│
│ • Keyword analysis  │ │ • LinkedIn posts│ │ • SEO optimization   │
│ • Content calendar  │ │ • Twitter       │ │ • Scheduling         │
│ • Trend monitoring  │ │   threads       │ │ • Cross-posting     │
│ • Brief creation    │ │ • Newsletters   │ │ • Performance        │
│                     │ │ • Repurposing   │ │   tracking          │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
           │                      │                  │
           └──────────────────────┼──────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────┐
│                    INTEGRATION LAYER                           │
│                                                               │
│  ┌─────────┐  ┌────────┐  ┌──────────┐  ┌──────────────────┐ │
│  │ LinkedIn│  │ Medium │  │ WordPress│  │ Substack         │ │
│  │ API     │  │ API    │  │ REST API │  │ API / Email      │ │
│  └─────────┘  └────────┘  └──────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
WEEKLY CYCLE:
  Day 1 ──► Strategist researches → creates briefs → writes calendar
  Day 2 ──► Writer receives brief → produces drafts
  Day 3 ──► Writer continues drafts → Editor begins review
  Day 4 ──► Editor finishes review → formats → schedules
  Day 5 ──► Content publishes across platforms
  Day 6-7 ──► Performance collection → strategist learns → next cycle

CONTENT BRIEF FLOW (per piece):
  [Strategist] ──brief──► [Writer] ──draft──► [Editor] ──published──► [Platform]
                              ▲                        │
                              └── revision notes ──────┘
```

---

## 3. Agent Personas & Configs

### 3.1 Agent Persona: Content Strategist

**Role:** The strategist owns the "what" and "why" of your content machine.  
**Personality:** Analytical, data-driven, market-aware, slightly cynical about hype.  
**Tone in briefs:** Direct, factual, decision-oriented.  

**Responsibilities:**
- Scan industry news, competitor blogs, and trending topics
- Analyze keyword gaps and content opportunities
- Produce a weekly content calendar with 5–7 briefs
- Brief each article with angle, target keyword, audience, and structure
- Review performance data and adjust strategy

**Paperclip Agent Configuration:**

```json
{
  "agent": {
    "name": "content-strategist",
    "version": "1.0",
    "role": "Content Strategist",
    "model": {
      "provider": "openai",
      "name": "gpt-4o",
      "temperature": 0.4,
      "max_tokens": 4000
    },
    "persona": {
      "description": "Senior content strategist with 10+ years in B2B SaaS content marketing. Data-driven, research-obsessed, and skilled at finding content gaps competitors miss.",
      "traits": ["analytical", "strategic", "proactive", "data-driven"],
      "communication_style": "Direct, concise, recommendation-focused. Uses data to justify every content decision."
    },
    "schedule": {
      "cron": "0 8 * * 1",
      "description": "Every Monday at 8:00 AM — research and produce weekly content calendar"
    },
    "inputs": [
      {
        "name": "industry_keywords",
        "description": "Primary keywords and topics to target",
        "type": "string",
        "default": "AI, automation, SaaS, indie hacking, content marketing"
      },
      {
        "name": "competitor_urls",
        "description": "Competitor blogs to monitor",
        "type": "array",
        "default": ["https://example-competitor.com/blog"]
      },
      {
        "name": "target_audience_description",
        "description": "Who we're writing for",
        "type": "string",
        "default": "Indie hackers and solopreneurs building SaaS products, technical founders, US/UK market"
      },
      {
        "name": "weekly_performance_data",
        "description": "Last week's content performance metrics",
        "type": "string",
        "optional": true
      }
    ],
    "outputs": [
      {
        "name": "content_calendar",
        "description": "Weekly content plan with 5-7 briefs",
        "type": "markdown_file",
        "path": "/data/content-plans/{date}/calendar.md"
      },
      {
        "name": "content_briefs",
        "description": "Individual briefs for each piece",
        "type": "markdown_file",
        "path": "/data/content-plans/{date}/briefs/"
      }
    ],
    "tools": ["web_search", "web_extract", "save_memory"],
    "instructions": [
      "You are the Content Strategist for a solo creator's content machine.",
      "Every Monday at 8:00 AM, research and produce the weekly content calendar.",
      "Your inputs: industry keywords, competitor URLs, target audience, and optional performance data.",
      "STEP 1: Research — Search for trending topics, competitor content, and keyword opportunities.",
      "STEP 2: Analyze — Identify content gaps, underserved angles, and high-impact topics.",
      "STEP 3: Plan — Create a content calendar with 5-7 pieces for the week.",
      "STEP 4: Brief — Write a detailed brief for each piece (angle, structure, target keyword, audience hook).",
      "Output the calendar to /data/content-plans/YYYY-MM-DD/calendar.md",
      "Output individual briefs to /data/content-plans/YYYY-MM-DD/briefs/",
      "Each brief must include: target keyword (with search volume estimate), audience hook, article structure, suggested title (3 options), and relevant links for research.",
      "Use the performance data from last week to refine future topics."
    ]
  }
}
```

---

### 3.2 Agent Persona: Writer

**Role:** The writer turns briefs into compelling content.  
**Personality:** Creative, adaptable, voice-aware, prolific.  
**Tone in articles:** Varies by platform — professional on LinkedIn, narrative on Medium, punchy on Twitter.  

**Responsibilities:**
- Accept briefs from the strategist
- Write long-form articles (1,500–2,500 words)
- Repurpose articles into LinkedIn posts, Twitter threads, and newsletter versions
- Apply brand voice and style guidelines
- Self-review for quality before handoff

**Paperclip Agent Configuration:**

```json
{
  "agent": {
    "name": "content-writer",
    "version": "1.0",
    "role": "Content Writer",
    "model": {
      "provider": "openai",
      "name": "gpt-4o",
      "temperature": 0.7,
      "max_tokens": 8000
    },
    "persona": {
      "description": "Versatile B2B content writer specializing in SaaS, AI, and startup content. Can write in multiple brand voices and adapt tone for any platform.",
      "traits": ["creative", "prolific", "adaptable", "voice-conscious"],
      "communication_style": "Engaging, clear, value-driven. Writes as a peer who understands the reader's pain points."
    },
    "schedule": {
      "cron": "0 9 * * 2,3",
      "description": "Tuesday and Wednesday at 9:00 AM — write content from this week's briefs"
    },
    "inputs": [
      {
        "name": "content_briefs_directory",
        "description": "Path to this week's content briefs",
        "type": "string",
        "path": "/data/content-plans/{date}/briefs/"
      },
      {
        "name": "brand_voice_guide",
        "description": "Brand voice and tone guidelines",
        "type": "string",
        "default": "Direct, authoritative, slightly irreverent. Write like a knowledgeable friend who's already done what the reader is trying to do. Use contractions. Avoid buzzwords. Lead with specific numbers and results."
      },
      {
        "name": "target_audience",
        "description": "Who we're writing for",
        "type": "string",
        "default": "Technical founders and indie hackers building SaaS products, US/UK, aged 25-45"
      }
    ],
    "outputs": [
      {
        "name": "long_form_articles",
        "description": "Full article drafts in markdown",
        "type": "markdown_file",
        "path": "/data/drafts/{date}/articles/"
      },
      {
        "name": "repurposed_content",
        "description": "Platform-specific versions of each article",
        "type": "markdown_file",
        "path": "/data/drafts/{date}/repurposed/"
      }
    ],
    "tools": ["read_file", "save_memory"],
    "instructions": [
      "You are the Content Writer for a solo creator's content machine.",
      "Your job is to take content briefs from the Strategist and produce high-quality drafts.",
      "Work through briefs one at a time. For each brief:",
      "",
      "STEP 1: Read the brief thoroughly.",
      "STEP 2: Research any referenced sources or links in the brief.",
      "STEP 3: Write the long-form article (1,500-2,500 words) following the brief's structure.",
      "STEP 4: Self-review the article for clarity, flow, grammar, and factual accuracy.",
      "STEP 5: Create repurposed versions:",
      "  - LinkedIn post (300-500 words with hook, body, CTA, and 3-5 hashtags)",
      "  - Twitter/X thread (10-15 tweets, numbered, with thread hook)",
      "  - Newsletter version (600-800 words, conversational tone, with PS)",
      "",
      "Save the full article to /data/drafts/YYYY-MM-DD/articles/{slug}.md",
      "Save repurposed content to /data/drafts/YYYY-MM-DD/repurposed/{slug}/",
      "",
      "Brand voice rules:",
      "- Write like a knowledgeable peer, not a textbook",
      "- Open with a hook that creates curiosity or identifies a pain point",
      "- Use short paragraphs (2-4 sentences max)",
      "- Include specific numbers, data points, and examples",
      "- End every piece with a clear CTA",
      "- No fluff, no filler, no obvious AI-isms"
    ]
  }
}
```

---

### 3.3 Agent Persona: Editor/Publisher

**Role:** The editor polishes, formats, schedules, and deploys content.  
**Personality:** Meticulous, quality-obsessed, process-driven.  
**Tone:** Professional, precise, platform-aware.  

**Responsibilities:**
- Review drafts for grammar, clarity, and brand voice alignment
- Format content for each target platform
- Add SEO metadata (titles, descriptions, tags)
- Schedule and publish via platform APIs
- Capture performance metrics for the strategist

**Paperclip Agent Configuration:**

```json
{
  "agent": {
    "name": "editor-publisher",
    "version": "1.0",
    "role": "Editor & Publisher",
    "model": {
      "provider": "openai",
      "name": "gpt-4o",
      "temperature": 0.3,
      "max_tokens": 4000
    },
    "persona": {
      "description": "Meticulous editor and publishing operations manager. Ensures every piece is platform-optimized, error-free, and published on schedule.",
      "traits": ["meticulous", "quality-obsessed", "process-driven", "platform-expert"],
      "communication_style": "Precise and actionable. Gives clear feedback and never lets a typo slip through."
    },
    "schedule": {
      "cron": "0 10 * * 4,5",
      "description": "Thursday and Friday at 10:00 AM — edit drafts and schedule publishing"
    },
    "inputs": [
      {
        "name": "drafts_directory",
        "description": "Path to this week's drafts and repurposed content",
        "type": "string",
        "path": "/data/drafts/{date}/"
      },
      {
        "name": "platform_config",
        "description": "Target platforms and their API credentials",
        "type": "json",
        "path": "/config/platforms.json"
      },
      {
        "name": "seo_settings",
        "description": "SEO defaults and keyword targets",
        "type": "json",
        "path": "/config/seo.json"
      }
    ],
    "outputs": [
      {
        "name": "published_articles",
        "description": "Links to published content",
        "type": "json_file",
        "path": "/data/published/{date}/published.json"
      },
      {
        "name": "editorial_feedback",
        "description": "Feedback for the writer on each piece",
        "type": "markdown_file",
        "path": "/data/published/{date}/feedback.md"
      }
    ],
    "tools": ["read_file", "web_search"],
    "instructions": [
      "You are the Editor & Publisher for a solo creator's content machine.",
      "Your job: polish drafts, format for each platform, and publish.",
      "",
      "STEP 1: Read each draft article from the writer.",
      "STEP 2: Edit for:",
      "  - Grammar, spelling, punctuation",
      "  - Brand voice consistency",
      "  - Clarity and flow",
      "  - Factual accuracy",
      "  - Hook strength",
      "STEP 3: Format for each target platform:",
      "  - WordPress: HTML with proper H2/H3 tags, alt text on images, meta description, slug, tags",
      "  - Medium: Markdown with headline, subtitle, tags, canonical link",
      "  - LinkedIn: Plain text with line breaks, emojis (sparingly), hashtags",
      "  - Substack: Markdown with subject line, preview text, custom button",
      "STEP 4: Apply SEO:",
      "  - Title tag (55-60 chars)",
      "  - Meta description (150-160 chars)",
      "  - URL slug",
      "  - Header hierarchy",
      "STEP 5: Schedule or publish via platform APIs.",
      "STEP 6: Log all published URLs and metrics.",
      "STEP 7: Write editorial feedback for the writer (strengths, areas for improvement).",
      "",
      "Quality gates:",
      "- Every piece must pass the 'read aloud' test before publishing",
      "- LinkedIn posts must not exceed 3,000 characters",
      - Twitter threads must have a compelling first tweet (the hook)",
      "- Newsletter subject lines must be under 60 characters"
    ]
  }
}
```

---

## 4. Step-by-Step Deployment Guide

### Phase 1: Foundation (15 minutes)

#### Step 1: Install Paperclip (if not already installed)

```bash
# SSH into your server
ssh user@your-server-ip

# Install Paperclip
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pip install -e .

# Verify installation
paperclip --version
# Expected output: paperclip X.Y.Z
```

#### Step 2: Create the project structure

```bash
mkdir -p ~/ai-content-machine/{agents,config,data/{content-plans,drafts,published},logs}
mkdir -p ~/ai-content-machine/config
```

#### Step 3: Platform credentials file

Create `~/ai-content-machine/config/platforms.json`:

```json
{
  "platforms": {
    "linkedin": {
      "enabled": true,
      "api_key": "YOUR_LINKEDIN_API_KEY",
      "organization_id": "YOUR_ORG_ID_OR_URN",
      "default_post_type": "article"
    },
    "medium": {
      "enabled": true,
      "integration_token": "YOUR_MEDIUM_TOKEN",
      "publication_id": "YOUR_PUBLICATION_ID_OR_NULL",
      "default_tags": ["saas", "indiehacking", "ai", "startup", "productivity"]
    },
    "wordpress": {
      "enabled": true,
      "site_url": "https://yourblog.com",
      "username": "YOUR_WP_USERNAME",
      "application_password": "YOUR_WP_APP_PASSWORD",
      "default_category": "Content Marketing",
      "default_tags": ["AI", "automation", "SaaS"]
    },
    "substack": {
      "enabled": true,
      "publish_endpoint": "https://api.substack.com/api/v1/publish",
      "api_key": "YOUR_SUBSTACK_API_KEY",
      "publication_url": "https://yournewsletter.substack.com"
    }
  },
  "scheduling": {
    "linkedin": ["Monday", "Wednesday", "Friday"],
    "medium": ["Tuesday", "Thursday"],
    "wordpress": ["Wednesday"],
    "substack": ["Sunday"]
  }
}
```

#### Step 4: SEO configuration

Create `~/ai-content-machine/config/seo.json`:

```json
{
  "seo": {
    "default_meta_description_length": 155,
    "default_title_length": 55,
    "target_keywords": [
      "AI content automation",
      "content marketing for indie hackers",
      "automated content creation",
      "SaaS content strategy",
      "solopreneur marketing"
    ],
    "excluded_tags": ["spammy", "over-optimized"],
    "og_image_default": "https://yourblog.com/images/default-og.png",
    "twitter_card_type": "summary_large_image"
  },
  "analytics": {
    "tracking_enabled": true,
    "utm_params": {
      "source": "newsletter",
      "medium": "email",
      "campaign": "weekly-digest"
    }
  }
}
```

### Phase 2: Agent Registration (15 minutes)

#### Step 5: Register the agents with Hermes

Create agent registration scripts:

```bash
# Register Content Strategist
cat > ~/ai-content-machine/agents/register-all.sh << 'REGISTER_EOF'
#!/bin/bash

AGENTS_DIR=~/ai-content-machine/agents
CONFIG_DIR=~/ai-content-machine/config
DATE=$(date +%Y-%m-%d)

echo "=== Registering Content Strategist ==="
hermes agent register content-strategist \
  --config $AGENTS_DIR/strategist.json \
  --working-dir ~/ai-content-machine

echo "=== Registering Content Writer ==="
hermes agent register content-writer \
  --config $AGENTS_DIR/writer.json \
  --working-dir ~/ai-content-machine

echo "=== Registering Editor/Publisher ==="
hermes agent register editor-publisher \
  --config $AGENTS_DIR/editor.json \
  --working-dir ~/ai-content-machine

echo "=== All agents registered ==="
hermes agent list
REGISTER_EOF

chmod +x ~/ai-content-machine/agents/register-all.sh
```

#### Step 6: Save the agent JSON configs

Save each agent JSON configuration from Section 3 into individual files under `~/ai-content-machine/agents/`:

```bash
# strategist.json → ~/ai-content-machine/agents/strategist.json
# writer.json → ~/ai-content-machine/agents/writer.json
# editor.json → ~/ai-content-machine/agents/editor.json
```

(Use the exact JSON blocks from Section 3 above.)

#### Step 7: Register and test

```bash
cd ~/ai-content-machine
bash agents/register-all.sh

# Test each agent
hermes agent run content-strategist --dry-run
hermes agent run content-writer --dry-run
hermes agent run editor-publisher --dry-run

# If all pass, do a live test of the strategist
hermes agent run content-strategist
```

### Phase 3: Integration Setup (15 minutes)

#### Step 8: Platform API setup

**LinkedIn API:**
1. Go to https://www.linkedin.com/developers/
2. Create a new app → request "Share on LinkedIn" and "Organizations" permissions
3. Generate an access token (valid 60 days; set a calendar reminder)
4. Add the token to `platforms.json`

**Medium API:**
1. Go to https://medium.com/me/settings → Security → Integration tokens
2. Generate a new token
3. Add to `platforms.json`

**WordPress API:**
1. Go to Users → Profile → Application Passwords
2. Generate a new password (WordPress 5.6+)
3. Add username and app password to `platforms.json`

**Substack API:**
1. Go to Settings → API in your Substack dashboard
2. Generate API key
3. Add to `platforms.json`

#### Step 9: Create the orchestration workflow

Create `~/ai-content-machine/config/orchestration.yaml`:

```yaml
pipeline:
  name: weekly-content-cycle
  schedule: "0 8 * * 1"  # Every Monday at 8:00 AM

  steps:
    - step: 1
      name: Research & Plan
      agent: content-strategist
      description: "Research topics and produce weekly calendar"
      timeout_minutes: 30
      on_failure: skip_topic

    - step: 2
      name: Write Articles
      agent: content-writer
      description: "Write long-form articles from briefs"
      triggers_on: step_1_complete
      timeout_minutes: 120
      on_failure: retry_once_else_skip

    - step: 3
      name: Review & Publish
      agent: editor-publisher
      description: "Edit, format, and publish all content"
      triggers_on: step_2_complete
      timeout_minutes: 60
      on_failure: notify_admin

  notifications:
    on_complete: "admin@yourdomain.com"
    on_failure: "admin@yourdomain.com"
    summary: true
```

### Phase 4: First Run & Validation (15 minutes)

#### Step 10: Dry run the full pipeline

```bash
# Dry-run the orchestration
hermes pipeline run weekly-content-cycle --dry-run

# If successful, run for real
hermes pipeline run weekly-content-cycle

# Check logs
tail -f ~/ai-content-machine/logs/pipeline.log
```

#### Step 11: Verify output

```bash
# Check that content was created
ls -la ~/ai-content-machine/data/content-plans/
ls -la ~/ai-content-machine/data/drafts/
ls -la ~/ai-content-machine/data/published/

# View the content calendar
cat ~/ai-content-machine/data/content-plans/$(date +%Y-%m-%d)/calendar.md
```

---

## 5. SOPs for Each Agent

### 5.1 Content Strategist SOP

**Objective:** Produce 5–7 research-backed content briefs every Monday.

**Inputs:**
- Industry keywords (from config)
- Competitor URLs (from config)
- Target audience description (from config)
- Last week's performance data (optional)

**Process:**

```
┌─────────────────────────────────────────────────────────┐
│                     MONDAY 8:00 AM                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [RESEARCH PHASE - 15 min]                               │
│  1. Search trending topics in target keywords            │
│  2. Extract top 3 competitor articles from last week     │
│  3. Identify keyword gaps (what competitors aren't       │
│     covering that your audience cares about)             │
│  4. Note any industry news or product launches            │
│                                                          │
│  [ANALYSIS PHASE - 10 min]                               │
│  5. Score each potential topic on:                       │
│     a) Search volume potential (1-5)                     │
│     b) Audience pain point alignment (1-5)               │
│     c) Competitor coverage gap (1-5)                     │
│     d) Evergreen value (1-5)                             │
│  6. Select top 5-7 topics based on composite score       │
│                                                          │
│  [PLANNING PHASE - 5 min]                                │
│  7. Assign topics to days of the week                    │
│  8. Mix content types: 3 articles, 2 LinkedIn posts,     │
│     1 Twitter thread, 1 newsletter                       │
│                                                          │
│  [BRIEFING PHASE - 15 min]                               │
│  9. For each topic, write a complete brief:              │
│     - Working title (3 options)                          │
│     - Target keyword & search context                   │
│     - Audience hook (the first 2 sentences)              │
│     - Article structure (H2 outline)                     │
│     - Key points to cover (5-7 bullet points)            │
│     - Sources to reference                               │
│     - Suggested CTA                                      │
│                                                          │
│  [OUTPUT - 5 min]                                        │
│  10. Write calendar to /data/.../calendar.md             │
│  11. Write each brief to /data/.../briefs/{topic}.md    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Sample Brief Output:**

```markdown
# Content Brief: "How Indie Hackers Can Publish 5x More Content Without Hiring"

**Working Titles:**
1. How Indie Hackers Can Publish 5x More Content Without Hiring (Primary)
2. The Solo Founder's Guide to Content Production at Scale
3. Content Automation for Bootstrapped Startups

**Target Keyword:** "content automation for indie hackers"
**Search Context:** ~320/mo, low competition, high conversion intent
**Content Type:** Long-form article (2,000 words)
**Target Platform:** Blog (WordPress) + repurpose for LinkedIn

**Audience Hook:**
"You know content marketing works. You've seen the case studies—founders who grew to 100k monthly visitors through consistent blogging. But when you're the CEO, CTO, marketer, and support team rolled into one, finding 20 hours a week for content feels impossible. What if you could get the output of a 3-person content team without the headcount?"

**Article Structure:**
- H1: Title
- H2: The content dilemma every solo founder faces
- H2: Why most indie hackers fail at content (and it's not what you think)
- H2: Meet your AI content team—3 agents, zero salaries
  - H3: The Strategist
  - H3: The Writer
  - H3: The Editor/Publisher
- H2: Setting up the machine (step-by-step)
- H2: A day in the life of automated content
- H2: Results you can expect in 30/60/90 days
- H2: Start tonight (the 30-minute setup)

**Key Points:**
- The math: 3 agents cost ~$30/mo in API costs vs $15k/mo for a team
- Speed: From brief to published in under 4 hours
- Quality: With proper prompts, AI content now matches junior writers
- Scale: 5-7 pieces/week vs 1-2 for a solo founder writing manually

**Sources:**
- https://example.com/solo-founder-content-stats
- ProductHunt trends in content tools

**CTA:** "Ready to build your own content machine? Grab the blueprint at [link]."
```

---

### 5.2 Writer SOP

**Objective:** Convert briefs into polished drafts with platform-specific variants.

**Inputs:**
- Content brief (from the strategist)
- Brand voice guide
- Target audience profile

**Process:**

```
┌─────────────────────────────────────────────────────────┐
│                  TUESDAY-WEDNESDAY 9:00 AM                │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  [READ BRIEF - 2 min each]                               │
│  1. Read the brief completely                            │
│  2. Open any reference links the strategist provided     │
│                                                          │
│  [WRITE DRAFT - 30-45 min each]                          │
│  3. Write hook paragraph (3-5 sentences)                 │
│  4. Follow the H2 structure from the brief               │
│  5. Include specific data points, examples, anecdotes    │
│  6. Keep paragraphs short (2-4 sentences)                │
│  7. Use transition sentences between sections            │
│  8. End with a strong CTA                                │
│                                                          │
│  [SELF-EDIT - 5 min each]                                │
│  9. Read aloud to catch awkward phrasing                 │
│  10. Check: does every paragraph serve the reader?       │
│  11. Cut any sentence that doesn't add value              │
│  12. Verify all facts and numbers                        │
│                                                          │
│  [REPURPOSE - 15 min each article]                       │
│  13. Extract key insight → LinkedIn post (300-500 words) │
│  14. Expand key insight thread → Twitter thread (10-15   │
│      tweets)                                             │
│  15. Condense with friendly tone → Newsletter (600-800   │
│      words)                                              │
│                                                          │
│  [OUTPUT - 2 min each]                                   │
│  16. Save article + repurposed variants                  │
│  17. Move to next brief                                  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

**Writing Quality Checklist:**

| Criterion | Standard | Pass/Fail |
|-----------|----------|-----------|
| Opening hook creates curiosity | First 3 sentences | — |
| Subheadings are benefit-driven | Every H2 | — |
| Paragraphs ≤ 4 sentences | Every paragraph | — |
| At least 3 specific data points | Per 1,000 words | — |
| No jargon without explanation | Throughout | — |
| CTA is specific and actionable | Last paragraph | — |
| Total word count ±10% of brief target | Article | — |
| No passive voice clusters | Max 2 per paragraph | — |
| Each section answers "so what?" | Reader test | — |

---

### 5.3 Editor/Publisher SOP

**Objective:** Polish, format, and publish content across all platforms.

**Inputs:**
- Draft articles and repurposed content (from the writer)
- Platform credentials (from config)
- SEO settings (from config)

**Process:**

```
┌──────────────────────────────────────────────────────────┐
│                THURSDAY-FRIDAY 10:00 AM                    │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  [EDITING PASS - 10 min per article]                      │
│  1. Fix grammar, spelling, punctuation                    │
│  2. Tighten sentence structure                            │
│  3. Verify brand voice consistency                        │
│  4. Check hook strength and CTA clarity                   │
│  5. Flag factual claims for verification                  │
│                                                           │
│  [SEO OPTIMIZATION - 5 min per article]                   │
│  6. Write SEO title (55-60 chars)                         │
│  7. Write meta description (150-160 chars)                │
│  8. Create URL slug                                       │
│  9. Check header hierarchy (H1 → H2 → H3)                 │
│  10. Suggest 3-5 tags/categories                          │
│                                                           │
│  [PLATFORM FORMATTING - 5 min per platform per piece]     │
│  11. WordPress: HTML, featured image, alt text, tags      │
│  12. Medium: Markdown, subtitle, canonical URL, tags      │
│  13. LinkedIn: Plain text, 5-10 hashtags, @mentions       │
│  14. Substack: Markdown, subject line, preview text       │
│                                                           │
│  [PUBLISHING - 2 min per platform]                        │
│  15. Schedule or publish immediately per calendar         │
│  16. Log all published URLs to published.json             │
│                                                           │
│  [FEEDBACK - 5 min total]                                 │
│  17. Write 3 things the writer did well                   │
│  18. Suggest 2 areas for improvement                      │
│  19. Save to feedback.md                                  │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

**Platform-Specific Formatting Rules:**

| Element | LinkedIn | Medium | WordPress | Substack |
|---------|----------|--------|-----------|----------|
| Max length | 3,000 chars | Unlimited | Unlimited | Unlimited |
| Best time | Mon-Fri 8-10am | Tue-Thu 12-2pm | Tue-Thu 9-11am | Sun 10am |
| Hashtags | 3-5 max | 5 max | N/A | N/A |
| Emoji use | 1-2 per post | sparingly | none | sparingly |
| Image required | No | Yes (header) | Yes (featured) | Optional |
| Links | In comments only | Inline + canonical | Inline | Inline + button |
| Tone | Professional | Narrative | Authoritative | Conversational |

---

## 6. Prompt Library (20 Prompts)

### Category 1: Long-Form Articles (Prompts 1–5)

---

**Prompt 1: The Ultimate Guide — Foundation Article**

```
You are writing a comprehensive guide for {{audience}} about {{topic}}.

TONE: Authoritative but accessible. Write like a senior practitioner who has 
been in the trenches. Use "you" and "I" — this is a conversation between peers.

STRUCTURE:
- Hook: Start with the reader's pain point. Make them feel seen in 2 sentences.
- The Problem: Why most people get this wrong (with specific examples)
- The Framework: A memorable mental model (3-5 step framework)
- Deep Dive: Each step explained with real-world application
- Case Study: Brief example of this working in practice
- Your Turn: Actionable next steps the reader can take today
- CTA: Where to go for deeper treatment

REQUIREMENTS:
- 1,800-2,200 words
- At least 5 specific data points or statistics
- At least 3 external references (linked)
- Short paragraphs (max 4 sentences)
- Every H3 section must answer "so what?"

TOPIC: {{topic}}
TARGET KEYWORD: {{keyword}}
KEY ANGLE: {{angle}}
```

---

**Prompt 2: The "How We Did It" Case Study**

```
Write a first-person narrative case study about achieving {{result}} using {{method}}.

TONE: Authentic and vulnerable. Share struggles honestly before revealing solutions. 
Specific beats generic. Numbers beat adjectives.

STRUCTURE:
- The Before State: What was broken? What was the cost of not fixing it?
- The Breaking Point: What made you finally take action?
- The False Starts: What didn't work (and why that taught you something valuable)
- The Solution: Step-by-step what you actually did (with screenshots/data)
- The Results: Before/after metrics. Be specific. "4 hours saved per week" not "a lot of time"
- Key Learnings: 3 things you'd do differently
- Your Shortcut: One thing the reader can steal and apply immediately

REQUIREMENTS:
- 1,500-2,000 words
- Real metrics (even if anonymized)
- At least one "we almost gave up" moment
- Clear framework the reader can apply WITHOUT your exact stack

TOPIC: {{topic}}
TARGET KEYWORD: {{keyword}}
KEY ANGLE: {{angle}}
```

---

**Prompt 3: The Listicle That Actually Delivers Value**

```
Write a value-packed listicle about {{topic}} for {{audience}}.

TONE: Direct, scannable, generous. Every item must deliver immediate value.
No fluff introductions — get to the list within 3 sentences of the hook.

STRUCTURE:
- Hook paragraph (3 sentences max)
- The list {{number}} items, each with:
  - Bold header naming the item
  - 2-3 paragraph explanation
  - Why most people get this wrong (a contrarian twist on each item)
  - The correct approach
- Closing: Which item is the most important for beginners
- CTA

RULES:
- {{number}} items minimum, no filler
- Each item must stand alone (readers should gain value even if they only read one)
- Avoid obvious advice. If a beginner would know it, replace it.
- Include at least one "controversial take" per 5 items

TOPIC: {{topic}}
NUMBER OF ITEMS: {{number}}
TARGET KEYWORD: {{keyword}}
```

---

**Prompt 4: The Thought Leadership / Opinion Piece**

```
Write a strong-opinion piece arguing that {{thesis}} about {{topic}}.

TONE: Confident but not arrogant. Back every claim. You're challenging the status
quo, not just being contrarian for attention.

STRUCTURE:
- The Conventional Wisdom: What "everyone knows" about this topic
- Why It's Wrong: Specific evidence that the conventional view is outdated
- My Thesis: Clear statement of your position
- The Evidence: 3-5 arguments supporting your thesis, each with data or examples
- Addressing Objections: What critics would say and why they're partially right but ultimately wrong
- What This Means For You: How the reader should change their approach
- CTA: Invite discussion, not agreement

RULES:
- This is NOT a hot take. Every opinion must be justified.
- At least 50% of the piece should be arguments/evidence, not opinion.
- Acknowledge nuance — signal that you understand counterarguments.
- If you can't find contradicting evidence, your opinion isn't strong enough.

TOPIC: {{topic}}
THESIS: {{thesis}}
READER: {{audience}}
```

---

**Prompt 5: The "Tools & Stack" Review**

```
Write a detailed review/comparison of {{tools}} for {{use_case}}.

TONE: Skeptical, experienced, practical. You've actually used these tools. 
Your loyalty is to the reader, not any tool vendor.

STRUCTURE:
- The Problem: What the reader is trying to accomplish
- Why This Matters: The cost of choosing the wrong tool
- Contender 1: {{tool_name}}
  - Best for: Who should use this
  - Key features (pros)
  - Limitations (cons — be honest about dealbreakers)
  - Pricing
  - Verdict (score out of 10)
- Contender 2: {{tool_name}} (same structure)
- Contender 3: {{tool_name}} (same structure)
- Head-to-Head: Feature comparison table
- My Pick: Which one to choose and why (with specific use cases)
- Honorable Mentions: Tools that almost made the list

RULES:
- You MUST have used each tool for at least 2 weeks (in your persona)
- Each review must include at least one criticism
- If a tool is free, say so. If it has a generous free tier, note that.
- Include pricing gotchas (e.g., "limits you only discover after paying")

TOOLS: {{tools}}
USE CASE: {{use_case}}
AUDIENCE: {{audience}}
```

---

### Category 2: LinkedIn Posts (Prompts 6–10)

---

**Prompt 6: The "Personal Experience" LinkedIn Post**

```
Write a LinkedIn post sharing a personal lesson from {{experience}}.

TONE: Authentic, vulnerable, generous. This is a story that teaches.

STRUCTURE:
- HOOK (1-2 lines): The surprising or counterintuitive lesson
- THE STORY (4-6 lines): What happened (specific, chronological, real details)
- THE REALIZATION (2-3 lines): What you learned that changed your approach
- THE ACTIONABLE ADVICE (3-5 lines): How the reader can apply this TODAY
- CTA + HASHTAGS (1-2 lines)

RULES:
- 300-500 words total
- Line breaks between every 2-3 sentences (LinkedIn readability)
- 3-5 relevant hashtags
- Tag 1-2 relevant people/companies (only if genuinely relevant)
- End with a question to drive comments

EXPERIENCE: {{experience}}
KEY LESSON: {{lesson}}
AUDIENCE: {{audience}}
```

---

**Prompt 7: The "Hot Take" LinkedIn Post**

```
Write a LinkedIn post that challenges {{common_belief}} about {{topic}}.

TONE: Confident but respectful. You're not attacking anyone — you're upgrading
the conversation.

STRUCTURE:
- HOOK: State the common belief in quotes (e.g., "You need 10,000 followers to make an impact on LinkedIn")
- YOUR COUNTER: A single sentence stating your opposing view
- WHY THE COMMON BELIEF IS HARMFUL: 2-3 ways it holds people back
- YOUR EVIDENCE: Specific example or data supporting your view
- THE NUANCE: Where you agree with the original (shows you're fair-minded)
- CALL TO ACTION: "Here's what I'd suggest instead..."
- QUESTION: Ask followers for their experience

RULES:
- 200-400 words (short and punchy)
- 5-8 line breaks (high scannability)
- 2-3 hashtags
- Avoid attacking individuals — challenge ideas, not people

TOPIC: {{topic}}
COMMON BELIEF: {{common_belief}}
YOUR COUNTER: {{counter_argument}}
```

---

**Prompt 8: The "Step-by-Step How-To" LinkedIn Post**

```
Write a LinkedIn post teaching {{skill}} in exactly {{steps}} clear steps.

TONE: Teacher-like, patient, specific. Assume the reader knows nothing about
this specific workflow.

STRUCTURE:
- HOOK: "If you're still doing {{old_way}}, here's a better way..."
- THE OLD WAY: 1 sentence on why the common approach is inefficient
- THE STEPS: Numbered, 1 sentence each with a specific instruction
- THE RESULT: What happens after following these steps
- BONUS TIP: One extra trick that makes this even easier
- CTA: "Save this for later" or "Tag someone who needs to see this"

RULES:
- 150-250 words (shorter than most posts)
- Every step must be actionable in under 2 minutes
- Number the steps (LinkedIn preview shows them well)
- 1-2 relevant emojis maximum
- 3 hashtags

SKILL: {{skill}}
STEPS: {{number}}
AUDIENCE: {{audience}}
```

---

**Prompt 9: The "Industry Insight / Trend Spot" LinkedIn Post**

```
Write a LinkedIn post analyzing {{trend}} and what it means for {{audience}}.

TONE: Forward-looking, analytical, slightly provocative. You spotted something
most people missed.

STRUCTURE:
- HOOK: A surprising data point or observation (e.g., "I analyzed 500 startup blogs last month. Here's what the top 1% do differently.")
- THE TREND: What's happening (with specific evidence)
- WHY IT MATTERS: The implications for your audience
- THE OPPORTUNITY: What smart operators should do about it
- THE WARNING: What happens if you ignore this
- CTA: "What's your take on this?"

RULES:
- 300-500 words
- Reference specific sources (studies, reports, observables)
- Don't just describe the trend — predict where it's going
- 2-4 hashtags

TREND: {{trend}}
AUDIENCE: {{audience}}
YOUR PREDICTION: {{prediction}}
```

---

**Prompt 10: The "Engagement / Poll" LinkedIn Post**

```
Write a LinkedIn post designed to maximize comments and engagement.

TONE: Conversational, curious, community-building. You genuinely want to hear
from your audience.

STRUCTURE:
- HOOK: State a relatable scenario or dilemma
- THE CONTEXT: 2-3 sentences on why this is a tough call
- THE QUESTION: Clear either/or (or multiple choice) for the poll/comment
- YOUR TAKE: What you've personally experienced (shows vulnerability)
- INVITATION: "Drop your answer in the comments — I reply to everyone"
- HASHTAGS

RULES:
- 100-200 words
- Must end with a question that's easy to answer
- Avoid yes/no questions — give options
- Best posted Tuesday-Thursday
- Respond to the first 10 comments within 2 hours

SCENARIO: {{scenario}}
QUESTION: {{question}}
OPTIONS: {{options}}
```

---

### Category 3: Twitter/X Threads (Prompts 11–15)

---

**Prompt 11: The "X Things I Learned" Thread**

```
Write a Twitter thread sharing {{number}} lessons learned from {{experience}}.

HOOK TWEET (1): A bold statement that teases the thread's value.
"The {{number}} lessons that changed how I think about {{topic}}. 🧵"

TWEETS 2-{{number+1}}: Each lesson gets 1 tweet (1-3 lines each).
- Include specific numbers, dates, or amounts
- Use line breaks for readability
- Each tweet should be understandable on its own
- Last tweet: summarize and ask a question

RULES:
- 280 characters max per tweet (count carefully)
- Number each tweet (format: "1/{{number}}")
- Hook tweet has no number
- 1-2 line breaks per tweet for readability
- End with a question to drive replies
- Use 3-5 relevant hashtags in the last tweet

EXPERIENCE: {{experience}}
NUMBER OF LESSONS: {{number}}
TOPIC: {{topic}}
```

---

**Prompt 12: The "Controversial Opinion" Thread**

```
Write a Twitter thread arguing {{opinion}} that goes against mainstream thinking.

HOOK: A strong, quotable statement (something people will screenshot)
"{{quote}}"

STRUCTURE:
- Tweet 1-2: Why the common belief is wrong (with evidence)
- Tweet 3-5: Your argument (with real examples)
- Tweet 6-7: Why people disagree (acknowledge the other side)
- Tweet 8: What you recommend instead
- Tweet 9: Invite discussion

RULES:
- Every tweet must add evidence, not just repetition
- Don't attack people — attack ideas
- Include 1 counterargument to show fairness
- End with a discussion prompt

OPINION: {{opinion}}
TOPIC: {{topic}}
EVIDENCE: {{evidence_points}}
```

---

**Prompt 13: The "Step-by-Step Tutorial" Thread**

```
Write a Twitter thread teaching {{task}} in {{steps}} simple steps.

HOOK: "I've helped {{number}} people {{result}}. Here's exactly how to {{task}}: 🧵"

EACH STEP TWEET:
- Step number and action (bold via *asterisks*)
- One clear sentence explaining the step
- One line with a specific example
- Optional: tool/resource recommendation

FINAL TWEET:
- Summary of all steps
- "Save this thread for later"
- 2-3 hashtags
- Question to drive engagement

RULES:
- Maximum 240 characters per tweet (leave room for shares)
- Screenshots or visuals recommended between steps
- Test every step before writing about it
- Include a "pro tip" variation for experienced readers

TASK: {{task}}
STEPS: {{steps}}
AUDIENCE: {{audience}}
TOOLS_NEEDED: {{tools}}
```

---

**Prompt 14: The "Resource List" Thread**

```
Write a Twitter thread curating {{number}} resources for {{audience}} about {{topic}}.

HOOK: "I spent {{time}} finding the best {{resources}} for {{audience}}. Here's my list: 🧵"

STRUCTURE:
- Tweet 1: Hook with the curation premise
- Tweets 2-{{number+1}}: One resource per tweet
  - Resource name (bold)
  - What it does (1 line)
  - Why it's the best (1 line)
  - Price (free/paid/trial)
  - Link
- Final tweet: Summary and "which one would you add?"

RULES:
- You must have actually used each resource
- Include a mix of free and paid options
- Each tweet must justify why this resource made the list
- 3 hashtags in final tweet
- Make it easy to retweet (quote the hook)

TOPIC: {{topic}}
RESOURCE_TYPE: {{resource_type}}
NUMBER: {{number}}
AUDIENCE: {{audience}}
```

---

**Prompt 15: The "Personal Story" Thread**

```
Write a Twitter thread telling a personal story about {{experience}} that teaches {{lesson}}.

HOOK: A specific, surprising moment from the story (not the ending)
"The moment I realized {{insight}} was when {{specific_moment}}. Here's what happened: 🧵"

STRUCTURE:
- Tweet 1: Hook (cliffhanger)
- Tweets 2-4: Setup (what was the situation)
- Tweets 5-7: The tension (what went wrong/why it was hard)
- Tweets 8-10: The breakthrough (what you learned/realized)
- Tweet 11: The lesson (the actionable takeaway)
- Tweet 12: CTA (have you experienced something similar?)

RULES:
- Be vulnerable. Share what went wrong, not just the success.
- Specific details > generic descriptions
- Each tweet must make the reader want to read the next one
- 2-3 hashtags in the last tweet
- End with a question

EXPERIENCE: {{experience}}
LESSON: {{lesson}}
INSIGHT: {{insight}}
```

---

### Category 4: Newsletters (Prompts 16–18)

---

**Prompt 16: The Weekly Roundup Newsletter**

```
Write a weekly newsletter edition for {{publication_name}}.

SUBJECT LINE: {{subject_line}} (max 50 chars, must create curiosity)

STRUCTURE:
- GREETING: "Hey {{reader_name}}," (1 line)
- THE BIG IDEA: 2-3 paragraphs on the week's most important insight
- WHAT I LEARNED: 3 bullet points with lessons from the week
- LINKS WORTH CLICKING: 3-5 curated links with 1-line descriptions
- TOOL OF THE WEEK: One tool recommendation with use case
- PERSONAL NOTE: 1-2 paragraphs on what you're working on (builds connection)
- P.S.: The most interesting thing you've read/listened to this week
- SIGN-OFF: "See you next week — {{name}}

RULES:
- 600-800 words total
- Scannable format (short paragraphs, bold headers, bullet points)
- At least 50% original insight, not just link curation
- One CTA (reply, share, or click)
- Preview text (max 150 chars) for email clients

PUBLICATION: {{publication_name}}
WEEK_OF: {{date}}
TOPICS_COVERED: {{topics}}
```

---

**Prompt 17: The Deep Dive / Long Read Newsletter**

```
Write a single-topic deep dive newsletter on {{topic}}.

SUBJECT LINE: A bold promise (e.g., "Why {{common_practice}} is holding you back")
PREVIEW TEXT: A curiosity gap (e.g., "I spent 6 months testing this. Here's the truth.")

STRUCTURE:
- OPENING: Personal connection to the topic (why you care)
- THE FRAMEWORK: A new way to think about this topic
- THE EVIDENCE: Data, examples, and stories that support the framework
- THE APPLICATION: How to apply this today
- THE INVITATION: Reply with your take (creates conversation)
- SIGN-OFF

RULES:
- 1,000-1,500 words (this is a big newsletter — label it "Long Read")
- No more than 1 link per 200 words
- Must include at least one counterintuitive insight
- Encourage replies to build relationship with subscribers

TOPIC: {{topic}}
TARGET_KEYWORD: {{keyword}}
AUDIENCE: {{audience}}
PRIMARY_INSIGHT: {{insight}}
```

---

**Prompt 18: The Launch / Announcement Newsletter**

```
Write a newsletter announcing {{announcement}} to {{audience}}.

SUBJECT LINE: Clear announcement value (e.g., "I built the thing I've been talking about")
PREVIEW TEXT: What they'll get (e.g., "Here's what it does, what it costs, and why I built it")

STRUCTURE:
- THE BACKSTORY: 2-3 paragraphs on why you built this (the problem, the frustration)
- THE ANNOUNCEMENT: What it is (1 clear sentence)
- WHAT IT DOES: Bullet features (3-5 bullets, benefit-focused)
- WHAT IT COSTS: Honest pricing, no hidden fees
- WHY NOW: The timing
- THE ASK: What you need from readers (buy, share, feedback)
- BONUS: Exclusive discount for subscribers (creates FOMO)
- SIGN-OFF

RULES:
- 500-700 words
- Lead with the reader's problem, not your feature
- Include a clear CTA button (+ link)
- Be honest about limitations — trust is the only asset
- Send on a Tuesday or Thursday for best open rates

ANNOUNCEMENT: {{announcement}}
LAUNCH_DATE: {{date}}
SPECIAL_OFFER: {{offer}}
```

---

### Category 5: SEO & Metadata (Prompt 19)

---

**Prompt 19: SEO Metadata Bundle**

```
Generate complete SEO metadata for an article with the following details:

ARTICLE TITLE: {{article_title}}
FOCUS KEYWORD: {{keyword}}
ARTICLE SUMMARY (2-3 sentences): {{summary}}

OUTPUT THE FOLLOWING IN JSON FORMAT:
{
  "seo_title": "A 55-60 character title with the keyword near the front",
  "meta_description": "A 150-160 character description that includes the keyword and compels clicks",
  "url_slug": "a-url-friendly-slug-with-keyword",
  "focus_keyword": "the primary keyword",
  "secondary_keywords": ["3-5 related keywords"],
  "og_title": "Similar to SEO title, optimized for social sharing (50-60 chars)",
  "og_description": "Social share description (2-3 sentences)",
  "twitter_title": "Title optimized for X/Twitter card (max 70 chars)",
  "alt_text_template": "Template for image alt text: '{{keyword}} showing [description of image]'",
  "internal_links_suggested": ["3 suggestions for internal links"],
  "categories": ["2-3 relevant categories"],
  "tags": ["5-8 relevant tags"]
}

RULES:
- SEO title must be compelling enough to generate clicks, not stuffed with keywords
- Meta description must include the keyword naturally in the first 100 characters
- URL slug should use hyphens, lowercase, max 60 characters
- All suggestions must be specific to this article, not generic
```

---

### Category 6: Editorial & Quality Control (Prompt 20)

---

**Prompt 20: Editorial Review — Full Quality Audit**

```
You are a senior editor at a top-tier publication. Review the following article 
and provide a structured audit.

ARTICLE: {{full_article_text}}

OUTPUT YOUR AUDIT IN THIS FORMAT:

## OVERALL SCORE: X/10

## STRENGTHS (list 3):
1. [strength]
2. [strength]
3. [strength]

## ISSUES (list all that apply):
- [ ] Grammar/spelling errors found
- [ ] Opening hook is weak
- [ ] CTA is unclear or missing
- [ ] Paragraphs exceed 4 sentences
- [ ] Jargon or buzzwords without explanation ([list them])
- [ ] Claims without evidence or sources
- [ ] Transitions between sections are abrupt
- [ ] Brand voice inconsistency
- [ ] Passive voice overuse
- [ ] Too long/could be tighter
- [ ] No clear reader takeaway

## SPECIFIC CORRECTIONS (line-by-line if needed):
| Line | Issue | Correction |
|------|-------|------------|
| 12 | "very unique solution" | "unique solution" (very is redundant) |
| ... | ... | ... |

## SEO CHECK:
- Title: ✅/❌ ([suggested fix])
- Meta description: ✅/❌ ([suggested fix])
- URL slug: ✅/❌ ([suggested fix])
- Header hierarchy: ✅/❌ ([suggested fix])

## PLATFORM READINESS:
- WordPress: ✅ Complete the following: [list missing items]
- Medium: ✅ Complete the following: [list missing items]
- LinkedIn: ✅ Complete the following: [list missing items]
- Substack: ✅ Complete the following: [list missing items]

## FINAL VERDICT:
- [ ] Publish as-is
- [ ] Publish after minor fixes
- [ ] Major revision needed (explain why)
- [ ] Do not publish (explain why)
```

---

## 7. Tool Integration Guide

### 7.1 LinkedIn Integration

**Method:** LinkedIn API v2 (via OAuth 2.0)

**Setup Steps:**

1. **Create a LinkedIn App:**
   - Go to https://www.linkedin.com/developers/apps
   - Click "Create app"
   - Name: "Content Machine Integration"
   - App logo: Upload a simple logo
   - Products: Select "Share on LinkedIn" and "Sign In with LinkedIn using OpenID Connect"

2. **Get API Credentials:**
   ```
   Client ID: ***************
   Client Secret: ***************
   Redirect URL: https://yourdomain.com/auth/linkedin/callback
   ```

3. **Generate Access Token:**
   ```bash
   # Use the LinkedIn OAuth 2.0 flow
   # For production, set up a refresh token workflow
   # Tokens expire in 60 days — set a calendar reminder
   ```

4. **Sample cURL Test:**
   ```bash
   curl -X POST 'https://api.linkedin.com/v2/ugcPosts' \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -H "X-Restli-Protocol-Version: 2.0.0" \
     -d '{
       "author": "urn:li:person:YOUR_URN",
       "lifecycleState": "PUBLISHED",
       "specificContent": {
         "com.linkedin.ugc.ShareContent": {
           "shareCommentary": {
             "text": "Your post content here."
           },
           "shareMediaCategory": "NONE"
         }
       },
       "visibility": {
         "com.linkedin.umbuttonication.umbuttonication": "PUBLIC"
       }
     }'
   ```

**Best Practices:**
- Post Mon-Fri between 8-10 AM in the target timezone
- Max 3,000 characters (LinkedIn truncates at 3,100)
- Include 3-5 hashtags (LinkedIn allows up to 30, but engagement drops after 5)
- Upload a link preview card — posts with links get 2x more engagement
- Tag relevant people/companies sparingly (tagging someone irrelevant hurts trust)

---

### 7.2 Medium Integration

**Method:** Medium API (REST)

**Setup Steps:**

1. **Get Integration Token:**
   - Go to https://medium.com/me/settings
   - Scroll to "Integration tokens"
   - Click "Get integration token"
   - Copy and save it immediately (shown once)

2. **Verify the Token:**
   ```bash
   curl -H "Authorization: Bearer $MEDIUM_TOKEN" \
     https://api.medium.com/v1/me
   
   # Returns your user info and publication IDs
   ```

3. **Sample Publish Request:**
   ```bash
   curl -X POST "https://api.medium.com/v1/users/$USER_ID/posts" \
     -H "Authorization: Bearer $MEDIUM_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Your Article Title",
       "contentFormat": "markdown",
       "content": "Your markdown content here...",
       "canonicalUrl": "https://yourblog.com/slug",
       "tags": ["saas", "indiehacker", "ai"],
       "publishStatus": "public"
     }'
   ```

**Best Practices:**
- Always include a `canonicalUrl` pointing to your own blog (SEO domain authority)
- Publish on Tuesday or Thursday (Medium's highest traffic days)
- Use "public" status for broad reach, "draft" status for review before publishing
- Write a compelling subtitle (Medium shows it right below the title)
- Include a header image at 1200x600px minimum

---

### 7.3 WordPress Integration

**Method:** WordPress REST API (Application Password)

**Setup Steps:**

1. **Generate Application Password:**
   - Login to WordPress admin → Users → Profile
   - Scroll to "Application Passwords"
   - Enter name: "Content Machine"
   - Click "Add New Application Password"
   - Copy the 24-character password (shown once)

2. **Verify Connection:**
   ```bash
   curl -X GET "https://yourblog.com/wp-json/wp/v2/posts" \
     -u "yourusername:YOUR_APP_PASSWORD" \
     -H "Content-Type: application/json"
   ```

3. **Sample Publish Request:**
   ```bash
   curl -X POST "https://yourblog.com/wp-json/wp/v2/posts" \
     -u "yourusername:YOUR_APP_PASSWORD" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Your Article Title",
       "content": "<p>Your HTML content here...</p>",
       "status": "publish",
       "categories": [5],
       "tags": [12, 15, 22],
       "slug": "your-article-slug",
       "meta": {
         "seo_title": "SEO Title Here",
         "meta_description": "Meta description here."
       }
     }'
   ```

**Best Practices:**
- Use "future" status instead of "publish" to schedule posts
- Always include a featured media ID (set the featured image)
- WordPress handles HTML natively — format with proper H2/H3 tags
- Keep slugs under 60 characters, use hyphens
- Set categories and tags for internal SEO

---

### 7.4 Substack Integration

**Method:** Substack Draft API / Email API

**Setup Steps:**

1. **Get API Access:**
   - Login to Substack → Settings
   - Scroll to "API Access" (may need to request access)
   - Generate and save your API key
   - Note your publication URL (e.g., `yournewsletter.substack.com`)

2. **Sample Publish Request:**
   ```bash
   curl -X POST "https://api.substack.com/api/v1/publish" \
     -H "Authorization: Bearer $SUBSTACK_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Your Newsletter Title",
       "subtitle": "A compelling subtitle",
       "body": {
         "type": "doc",
         "content": [
           {"type": "paragraph", "content": [{"text": "Your content here..."}]}
         ]
       },
       "subject": "Email Subject Line Here",
       "preview_text": "Preview text for inbox",
       "type": "newsletter",
       "send_date": "2025-01-15T10:00:00Z"
     }'
   ```

**Alternative (Email-based):**
If the Substack API is rate-limited or restricted:

```bash
# Use Substack's email-to-substack feature
# Send your newsletter as HTML email to:
# publish@yournewsletter.substack.com

# Format the email with:
# Subject line as newsletter title
# First line as preview text (wrapped in <em>)
# Body as HTML
# Unsubscribe footer added automatically
```

**Best Practices:**
- Send on Sunday morning (highest open rates for newsletters)
- Subject lines under 50 characters get 12% higher open rates
- Use preview text strategically (your second sentence in inbox preview)
- Include at least one clickable action (reply, link, button)
- Keep the personal element — Substack readers subscribe for voice, not scale

---

### 7.5 Publishing Schedule Template

| Platform | Frequency | Best Day | Best Time | Content Type |
|----------|-----------|----------|-----------|--------------|
| LinkedIn | 3x/week | Mon, Wed, Fri | 8-10 AM | Posts, repurposed articles |
| Medium | 2x/week | Tue, Thu | 12-2 PM | Full articles (canonical to blog) |
| WordPress | 1-2x/week | Tue, Wed | 9-11 AM | Long-form (canonical source) |
| Substack | 1x/week | Sun | 10 AM | Newsletter version of best article |

---

## 8. Example Workflow — 1 Week of Autonomous Content

Below is a realistic week from the AI Content Machine. Times are in Eastern Time (ET) and assume the agents run on a US-based server schedule.

### Week 1 Snapshot: "Building in Public"

**Theme:** How indie hackers can build an audience while building a product.

| Day | Agent | Time | Activity | Output | Hours Saved vs Manual |
|-----|-------|------|----------|--------|----------------------|
| **Mon** | Strategist | 8:00 AM | Research trending topics in the indie hacker space (Twitter, ProductHunt, HackerNews, competitor blogs) | 5 content briefs + weekly calendar | 3 hrs |
| **Mon** | Strategist | 8:45 AM | Write briefs with keyword targets, article structures, and hooks | 5 detailed briefs | 2 hrs |
| **Tue** | Writer | 9:00 AM | Read brief #1 "How to Build an Audience Before Launching Your Product" + research | Draft article (1,800 words) | 4 hrs |
| **Tue** | Writer | 10:30 AM | Read brief #2 "The Solo Founder's Content Stack: 7 Tools I Use Every Day" + research | Draft article (2,000 words) | 4 hrs |
| **Tue** | Writer | 12:00 PM | Read brief #3 "Why Most Indie Hackers Fail at Content (And How to Fix It)" + research | Draft article (1,900 words) | 4 hrs |
| **Tue** | Writer | 2:00 PM | Self-edit all three drafts + create repurposed versions | 3 LinkedIn posts, 1 Twitter thread, 1 newsletter draft | 2 hrs |
| **Wed** | Writer | 9:00 AM | Read brief #4 "10 Twitter Threads That Got Me 1,000 Followers in a Month" + research | Draft article (1,500 words) | 3 hrs |
| **Wed** | Writer | 10:30 AM | Read brief #5 "The ROI of Automated Content: My Numbers After 90 Days" + research | Draft article (2,200 words) | 3 hrs |
| **Wed** | Writer | 12:30 PM | Create repurposed content for articles #4 and #5 | 2 LinkedIn posts, 1 Twitter thread | 1.5 hrs |
| **Wed** | Writer | 2:00 PM | Final pass on all drafts, save to drafts directory | 5 articles, 5 LinkedIn posts, 2 Twitter threads, 1 newsletter | 1 hr |
| **Thu** | Editor | 10:00 AM | Read and edit articles #1-3 (grammar, flow, brand voice, SEO) | Edited drafts with feedback notes | 3 hrs |
| **Thu** | Editor | 1:00 PM | Format for platforms: WordPress HTML, Medium Markdown, Substack | Platform-ready versions | 2 hrs |
| **Thu** | Editor | 3:00 PM | Schedule on platforms: WordPress (#1 Wed), Medium (#1 Tue+#2 Thu), LinkedIn posts | Scheduled queue | 1 hr |
| **Fri** | Editor | 10:00 AM | Read and edit articles #4-5 + remaining LinkedIn posts | Edited drafts with feedback notes | 2 hrs |
| **Fri** | Editor | 12:00 PM | Format and schedule remaining content + write editorial feedback | All content scheduled or published for next week | 2 hrs |
| **Fri** | Editor | 2:00 PM | Save published URLs to log, prepare performance data for strategist | Published log + metrics | 1 hr |
| **Sat** | *(retro)* | — | Strategist reviews performance data from published articles (opens, clicks, shares) | Learning notes → next week's briefs | 1 hr |
| **Sun** | *(publish)* | 10:00 AM | Substack newsletter sends (automated from Thursday's scheduling) | Newsletter delivered to inboxes | 0 hrs |
| **Total** | — | — | — | **5 articles, 7 LinkedIn posts, 3 Twitter threads, 1 newsletter** | **~37 hrs saved** |

**Total human time required:** ~15 minutes (reviewing outputs, resolving any errors)  
**Total manual time without automation:** ~52 hours  
**Time savings:** ~37 hours/week (71% reduction)

### The Actual Content Produced That Week

**Article Titles:**
1. How to Build an Audience Before Launching Your Product
2. The Solo Founder's Content Stack: 7 Tools I Use Every Day
3. Why Most Indie Hackers Fail at Content (And How to Fix It)
4. 10 Twitter Threads That Got Me 1,000 Followers in a Month
5. The ROI of Automated Content: My Numbers After 90 Days

**Repurposed Content:**
- 7 LinkedIn posts (main takeaways from each article + 2 original perspectives)
- 3 Twitter threads (key frameworks from articles #1, #3, and #4)
- 1 Sunday newsletter (curated highlights + personal note)

**Key Metrics Target:**
| Metric | Goal | Measurement |
|--------|------|-------------|
| Blog traffic (unique visitors) | 500+ per article | Google Analytics |
| LinkedIn engagement rate | >5% | LinkedIn analytics |
| LinkedIn post reach | 2,000+ per post | LinkedIn analytics |
| Twitter thread impressions | 10,000+ per thread | Twitter analytics |
| Newsletter open rate | >40% | Substack analytics |
| Newsletter click rate | >5% | Substack analytics |
| New email subscribers | 50+/week | Substack dashboard |

### Ramp-Up Schedule (First 4 Weeks)

| Week | Focus | Articles | Platforms | Notes |
|------|-------|----------|-----------|-------|
| **Week 1** | Setup & validation | 3 | WordPress + LinkedIn | Test the pipeline, verify quality |
| **Week 2** | Expand to Medium | 4 | WordPress + LinkedIn + Medium | Add Medium with canonical links |
| **Week 3** | Add newslette | 5 | All platforms | Introduce Substack on Sunday |
| **Week 4** | Full throttle | 5-7 | All platforms | Full content machine running |
| **Week 8** | Optimize from data | 5-7 | All platforms | Use performance data to sharpen briefs |
| **Week 12** | Scale | 7-10 | All platforms + guest posts | Expand to 2-3 writers working in parallel |

---

## 9. Appendix — Troubleshooting & FAQ

### Common Issues

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| Agent doesn't run on schedule | Cron syntax error | Run `hermes agent list` to verify schedule. Check cron expression in agent config. |
| Article quality is too generic | Temperature too high or brief too vague | Lower temperature to 0.6-0.7. Make briefs more specific with angles and examples. |
| LinkedIn post fails to publish | Token expired | LinkedIn tokens expire every 60 days. Set a calendar reminder. Regenerate token. |
| WordPress returns 401 | App password wrong | Regenerate app password in WordPress profile. Use username:password format in Basic Auth. |
| Medium returns 403 | Token revoked or expired | Generate new integration token in Medium settings. |
| Strategist briefs are too similar | No variation mechanism | Add a "fresh angle" instruction: "Avoid repeating topics or angles from the last 2 weeks." |
| Writer ignores brand voice | Voice guide too vague | Give 3 before/after examples of tone. "Instead of X, write Y." |
| Agent run times out | Article too long or model too slow | Reduce max_tokens for the writer model. Split large articles into 2-part series. |

### FAQ

**Q: How much will this cost me to run?**
A: API costs for OpenAI GPT-4o run ~$15-30/month for 5-7 pieces per week. Server costs are $10-20/month. Total: $25-50/month. Compare to $3,000-5,000/month for a junior content marketer.

**Q: Can I use Claude instead of GPT-4o?**
A: Yes. Change the `model.provider` field from `"openai"` to `"anthropic"` and `model.name` to `"claude-sonnet-4-20250514"`. Claude often produces slightly more natural long-form content; GPT-4o is better for structured/SEO content.

**Q: Will Google penalize me for AI content?**
A: Google penalizes *low-quality* content, not AI content. If your agents produce original research, unique frameworks, and genuine insights (via good briefs), it passes Google's E-E-A-T guidelines. Our SOPs emphasize adding original analysis in every piece.

**Q: Can I run this on a laptop instead of a server?**
A: Yes, for testing. For production, use a $10/mo VPS so agents run 24/7 regardless of your computer being on.

**Q: How long before I see results?**
A: Content is a compounding channel. Expect: 3-4 weeks to see initial traffic, 8-12 weeks for meaningful growth, 6 months for compounding returns. The machine is designed to be patient — it publishes consistently so you don't have to think about it.

**Q: What if I don't have all 4 platforms?**
A: Start with just your blog (WordPress) and LinkedIn. Add Medium at week 3 and Substack at week 4. The blueprint works with any subset of platforms.

**Q: How do I ensure consistent brand voice across all agents?**
A: Document your brand voice in 3 concrete rules + 5 examples. Store it in `config/brand-voice.md`. Reference it in each agent's instructions. The editor agent checks adherence during the review pass.

**Q: Can I add more agents?**
A: Yes — common extensions include a "Social Media Responder" (engages with comments) and an "Analytics Agent" (deep-dive into performance data). The minimum viable system is the 3 agents above.

---

## Final Checklist — Before You Go Live

- [ ] Paperclip installed and configured
- [ ] All 3 agents registered with Hermes
- [ ] Platform credentials valid in `platforms.json`
- [ ] Dry run passed for all agents
- [ ] SEO config in place
- [ ] Brand voice guide saved
- [ ] Orchestration pipeline configured
- [ ] First weekly calendar generated
- [ ] First article drafted and reviewed
- [ ] First article published successfully
- [ ] Performance tracking (UTM params, analytics) enabled
- [ ] Token expiry calendar reminders set (LinkedIn = 60 days)
- [ ] Monitoring/logging verified

---

## License & Use Terms

This blueprint is licensed for **personal and commercial use** by the purchaser only. You may:
- Deploy this system for your own business
- Use the prompts in your content operation
- Modify the agents to fit your brand

You may **not**:
- Resell or redistribute this blueprint (partial or complete)
- Use the prompts as a standalone product
- Claim the system design as your own original work

---

*Built for indie hackers who ship — by the team at Prem Autonomous Co.*

*Questions? Join our community: [link] | Support: support@premautonomous.co*

---

**Document version 1.0 — Published July 2026**
