[![ClawHub](https://img.shields.io/badge/ClawHub-notion-api-red)](../..) [![License](https://img.shields.io/badge/license-MIT--0-blue)](../..) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB)](../..)

---
name: notion-api
version: 2.0.0
description: Complete Notion API client: pages, databases, blocks, search with config file and dry-run mode
tags: ["notion", "api", "notes", "database", "cli", "productivity", "python", "open-source", "agent", "automation", "MIT"]
---

# Notion API CLI

**Complete Notion client: pages, databases, blocks, and search with config file and dry-run mode.**

> *Keywords: notion, api, notes, database, cli, productivity, python, open-source, agent, automation, MIT*  
>
> Part of the [itsPremkumar](https://github.com/itsPremkumar) Hermes / OpenClaw / Paperclip agent stack — 31 free, MIT-licensed, CI-tested agent-native tools.

## What it does

Notion's API is capable but verbose; every operation is many REST calls. Notion API CLI solves this: Complete Notion client: pages, databases, blocks, and search with config file and dry-run mode.

**Best for:** Notion power users, ops, and agents automating notes/databases.

## Features

- **Create/read/update pages**
- **Manage databases**
- **Append blocks**
- **Search across workspace**
- **Dry-run before writing**

## Install

```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/notion-api/main/notion_api.py
# Or copy the file anywhere — it's self-contained.
```

## Quick start

```bash
python notion_api.py search --help   # search subcommand
python notion_api.py list-databases --help   # list-databases subcommand
python notion_api.py query-database --help   # query-database subcommand
python notion_api.py read-page --help   # read-page subcommand
python notion_api.py read-page-md --help   # read-page-md subcommand
python notion_api.py read-blocks --help   # read-blocks subcommand
python notion_api.py create-page --help   # create-page subcommand
python notion_api.py create-page-md --help   # create-page-md subcommand
python notion_api.py update-page --help   # update-page subcommand
python notion_api.py update-page-md --help   # update-page-md subcommand
python notion_api.py append-blocks --help   # append-blocks subcommand
python notion_api.py archive-page --help   # archive-page subcommand
python notion_api.py create-database --help   # create-database subcommand
python notion_api.py list-users --help   # list-users subcommand
python notion_api.py get-user --help   # get-user subcommand
python notion_api.py list-property-types --help   # list-property-types subcommand
python notion_api.py block-template --help   # block-template subcommand
```

## Use cases

1. Create/read/update pages
1. Manage databases
1. Append blocks
1. Search across workspace
1. Dry-run before writing

## Why choose this over alternatives

| Alternative | Why this skill is better |
|---|---|
| Raw Notion API | Subcommands wrap pages/DBs/blocks/search. |
| Copy-paste | Dry-run safety + Markdown page support. |
| Manual blocks | Block templates. |

## FAQ (SEO / AEO)

**Q: Dry-run?**  
A: Yes — preview changes without writing.

**Q: Auth?**  
A: Config file / env token; no secrets in repo.

**Q: Blocks?**  
A: Create and read blocks, including Markdown pages.

**Q: Offline?**  
A: No — live Notion API.

## Geo / local reach

Built and maintained by [@itsPremkumar](https://github.com/itsPremkumar) (Chennai, India · serving developers worldwide). 
Free for individuals and teams everywhere. Documentation in English; tool output is locale-neutral.

## CI integration

```yaml
# .github/workflows/verify.yml
name: Verify
on: [push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Self-test notion-api
        run: python notion_api.py --help
```

## Support

Free + MIT-0 (free, modifiable, no attribution required). Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar

⭐ Star on [GitHub](https://github.com/itsPremkumar/notion-api)
