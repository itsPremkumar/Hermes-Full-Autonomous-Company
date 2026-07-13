# prompt-executor

A tiny, **dependency-free** command-line tool that takes a prompt category and
prints a polished, expert-crafted prompt for it. Great for kick-starting
ChatGPT / Claude / any LLM session without re-inventing the wheel.

Sells for **$9**. Zero install friction — just Node.js (v14+).

## Why

You know you should use a good prompt, but typing one from scratch every time is
tedious. `prompt-executor` gives you a curated library of high-quality prompt
templates at your fingertips:

```bash
$ prompt-executor coding
# Code Helper

You are a senior software engineer. Given a code snippet or problem description,
produce correct, idiomatic, well-tested code...
```

Copy the output into your AI chat and you are ready to go.

## Install

No dependencies, no build step.

```bash
# From the project folder
npm link           # makes `prompt-executor` available globally
# or just run it directly:
node bin/prompt-executor.js coding
```

## Usage

```bash
prompt-executor <category>     Print the prompt for a category
prompt-executor list           List all available categories
prompt-executor search <term>  Search categories by keyword
prompt-executor --help         Show help
prompt-executor --version      Print version
```

### Examples

```bash
prompt-executor coding
prompt-executor marketing
prompt-executor email
prompt-executor list
prompt-executor search social
```

## Available categories

Run `prompt-executor list` to see the full, always-current list. Ships with
12 categories including: writing, coding, marketing, email, social-media, seo,
product-naming, blog-outline, cold-outreach, meeting-agenda, resume, and
customer-support.

## Extending the library

All prompts live in `src/prompts.js` as a plain array of objects:

```js
{
  key: 'my-category',          // used on the command line
  title: 'My Category',        // shown in output header
  description: 'Short summary',// shown by `list`
  prompt: 'You are an expert...' // the prompt text
}
```

Add an object and it is immediately available — no registration needed.

## License

MIT
