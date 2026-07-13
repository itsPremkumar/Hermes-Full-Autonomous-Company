---
name: airtable-cli
version: 1.0.0
description: Read, create, update, delete, and search Airtable records. List bases and tables, filter records, and batch upsert.
tags: ["airtable", "database", "api", "cli", "python", "no-code"]
---

# Airtable API CLI

## Install
```bash
# Requires Python 3.8+. No pip install needed.
curl -O https://raw.githubusercontent.com/itsPremkumar/airtable-cli/main/airtable_cli.py
```

## Usage
```bash
# Set your Airtable API key
export AIRTABLE_API_KEY=keyxxxxx

python airtable_cli.py list-bases
python airtable_cli.py list-tables <base-id>
python airtable_cli.py list-records <base-id> <table-name> --limit 10
python airtable_cli.py get-record <base-id> <table-name> <record-id>
python airtable_cli.py create-record <base-id> <table-name> --data '{"Name":"Test","Status":"Active"}'
python airtable_cli.py update-record <base-id> <table-name> <record-id> --data '{"Status":"Done"}'
python airtable_cli.py delete-record <base-id> <table-name> <record-id>
python airtable_cli.py search <base-id> <table-name> <field> <value>
```

## Features
- **Browse bases/tables** — list all accessible bases and their tables
- **Record CRUD** — create, read, update, delete records
- **Search & filter** — find records by field value
- **JSON output** — machine-readable for pipeline integration
- **Rate-limit handling** — automatic retry on Airtable API limits

## Why
Manage your no-code database from the CLI. Automate Airtable workflows.

## Support
Free + MIT. Sponsor if useful:
- GitHub Sponsors: https://github.com/sponsors/itsPremkumar
- Buy Me a Coffee: https://buymeacoffee.com/itsPremkumar
