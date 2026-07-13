---
name: notion-api
version: 1.0.0
description: Read, create, update, and search Notion pages and databases from the CLI. Manage your workspace programmatically.
tags: ["notion", "api", "database", "pages", "cli", "python"]
---

# Notion API Toolkit

## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/notion-api/main/notion_cli.py
```

## Usage
```bash
# Set your Notion API key
export NOTION_API_KEY=secret_xxxxx

python notion_cli.py search "meeting notes"
python notion_cli.py list-databases
python notion_cli.py query-database <database-id>
python notion_cli.py read-page <page-id>
python notion_cli.py create-page <database-id> --title "New Task" --status "In Progress"
python notion_cli.py update-page <page-id> --property "Status" --value "Done"
```

## Features
- **Search** — search across all pages and databases
- **Database query** — list and query Notion databases
- **Page CRUD** — read, create, and update pages
- **Property management** — update any page property
- **Markdown output** — pages rendered as readable markdown

## Why
Automate your Notion workspace from the terminal. Great for agent workflows.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
