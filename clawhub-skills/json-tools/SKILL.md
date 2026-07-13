---
name: JSON Power Tools
version: 1.0.0
description: A Swiss-army-knife CLI for JSON files — validate, format, query, diff, filter, stats, flatten, and merge. Zero dependencies (Python stdlib).
tags: json, data, cli, devtools, python
---

# JSON Power Tools

A Swiss-army-knife CLI for JSON files. Validate, format, query (jq-like), diff, filter, stats, flatten, and merge — all with **zero dependencies** beyond Python's stdlib.

Perfect for CI pipelines, data engineering workflows, configuration file management, and any environment where installing `jq` or `yq` is impractical.

## Install

```bash
# No dependencies needed — Python 3.8+ stdlib only
# Copy the script anywhere
cp json_tools.py /usr/local/bin/json-tools
chmod +x /usr/local/bin/json-tools

# Or run directly
python json_tools.py --help
```

## Commands

| Command | Description |
|---------|-------------|
| `validate` | Check if a JSON file is well-formed |
| `format` | Pretty-print JSON with configurable indentation |
| `query` | Extract values using dot-notation paths (e.g., `users.0.name`) |
| `diff` | Show structural differences between two JSON files |
| `filter` | Filter arrays by a key-value condition |
| `stats` | Compute statistics: key count, depth, array sizes, types |
| `flatten` | Convert nested JSON to flat key-value pairs |
| `merge` | Deep-merge two or more JSON files |

## Usage

```bash
# Validate a file
python json_tools.py validate data.json

# Pretty-print with 4-space indent
python json_tools.py format data.json --indent 4

# Query a nested value
python json_tools.py query config.json --path "database.host"

# Diff two files
python json_tools.py diff old.json new.json

# Filter an array
python json_tools.py filter users.json --key role --value admin

# Stats overview
python json_tools.py stats large.json

# Flatten nested JSON
python json_tools.py flatten nested.json --separator "."

# Merge multiple files
python json_tools.py merge base.json patch1.json patch2.json --output merged.json
```

## Features

- **Zero dependencies** — nothing to install beyond Python itself
- **Stdin support** — pipe data through commands
- **Colorized diff output** — red/green for removed/added lines
- **Dot-notation queries** — traverse deep structures intuitively
- **Deep merge** — recursive dictionary merging preserves nested data
- **Type-aware stats** — counts strings, numbers, arrays, objects, nulls

## Examples

```bash
# Validate then pretty-print
python json_tools.py validate package.json && python json_tools.py format package.json

# Query a specific user's email
python json_tools.py query users.json --path "users.0.email"

# Filter active users and format
python json_tools.py filter users.json --key active --value true | python json_tools.py format

# Merge config overrides
python json_tools.py merge defaults.json production.json --output config.json

# Check diff exits 1 on differences (CI-friendly)
python json_tools.py diff expected.json actual.json
```

## Why JSON Power Tools?

Most JSON CLI tools require installing `jq` (a C binary) or npm packages. JSON Power Tools runs anywhere Python runs — that includes Docker scratch images with Python, locked-down enterprise environments, and Windows machines where compiling C tools is painful. Every command is a single file you can audit, copy, or vendor.

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
