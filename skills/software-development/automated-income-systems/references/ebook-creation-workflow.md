# Ebook Creation Workflow (Zero-Cost, Agent-Powered)

Used when creating a $19-29 ebook for Gumroad as part of the automated income system. This reference captures the proven 15K-word ebook creation process developed during the "Zero to $10k/mo" build.

## When to Use
- You're creating an ebook/gumroad product listed in the revenue table ("Ebooks | 'Zero to $10k/mo' style guides | $19-$29")
- User asks for a complete ebook, guide, whitepaper, or comprehensive tutorial
- Product goes to `revenue/digital-products/ebooks/<slug>.md`

## The Two-Pass Workflow

### Pass 1: Write the Full Draft
Write the complete ebook in a single `write_file` call. Include:
- **All chapters** — don't leave placeholders. Every section gets real content.
- **Foreword + Author bio** — personal story establishes credibility.
- **Actionable steps** at end of each chapter (Your Turn sections).
- **Cost breakdowns** showing $0 — this is the core selling point.
- **Real numbers** — revenue tables, download counts, pricing evolution.
- **Case studies** — the running example (e.g. Prem Autonomous Co).
- **Country-specific guidance** — India, Nigeria, Philippines, Brazil.
- **Appendices** — command references, product idea lists, config templates.

**Target length**: 15,000+ words (~40 pages). Write longer than needed in Pass 1 — it's easier to trim than to expand.

### Pass 2: Check Word Count and Iteratively Expand

After the first write, ALWAYS verify word count:

```bash
wc -w "<path-to-file>.md"
```

If below 15,000 words, identify the thinnest chapters and expand them with `patch`:

1. **Read thin sections** — open the file at the chapter that needs expansion
2. **Identify what's missing** compared to other chapters: less detail, fewer examples, no real numbers, short action steps
3. **Write the expansion** using `patch` with a unique `old_string` anchor (several surrounding lines for uniqueness)
4. **Re-check word count** after each expansion
5. **Target remaining gaps** — aim each patch to add 200-500 words until you hit 15K+

Sections that typically need the most expansion:
- Foreword/author story
- "Your Turn" action steps (these are often too terse on first pass)
- Country-specific guidance (India tax rules, Nigeria CAC, etc.)
- Scaling pitfalls / lessons learned
- Final Words / inspirational closing
- Case studies with specific numbers

## Path Pitfall (Windows/MSYS)

`write_file` does NOT understand MSYS path translation. `/c/one/...` will resolve relative to the workspace, NOT to `C:\one\...`. Always use absolute Windows paths:

```bash
# ✅ Correct — write_file will land here:
C:\one\paperclip-company\revenue\digital-products\ebooks\zero-to-10k-ai-agents.md

# ❌ Wrong — resolves relative to workspace:
/c/one/paperclip-company/...  # goes to C:\Users\<user>\c\one\...
```

After writing, verify with `wc -w "C:\\path\\to\\file.md"` via terminal (which DOES understand MSYS paths).

## Chapter Structure Template

Each chapter in a $19-29 ebook should follow this structure:

```
## Chapter Title

### Section Headline
- Problem statement (1-2 paragraphs)
- Solution explanation (2-3 paragraphs)
- Real data, numbers, tables

### Sub-section (deeper dive)
- Detailed walkthrough
- Code/config examples in fenced blocks
- Platform-specific guidance

### Your Turn: Action Steps
1. **Specific action** — description
2. **Specific action** — description
```

For the target audience (developers in developing countries), emphasize:
- Exchange rate math ($50/hr in local currency)
- Country-specific tax/legal registration info
- Free alternatives to every paid tool
- Mindset shifts specific to their context (underpricing fear, English concerns)

## Product Packaging

After the ebook `.md` is finalized:

```bash
mkdir -p revenue/digital-products/ebooks/<slug>-pack/
cp revenue/digital-products/ebooks/<slug>.md revenue/digital-products/ebooks/<slug>-pack/
# Add bonus files: cheatsheet, reference card, cover image
cd revenue/digital-products/ebooks/
zip -r <slug>-pack.zip <slug>-pack/
```

The ZIP goes on Gumroad at $19-29. The `.md` source stays in version control.
