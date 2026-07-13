---
name: File System Watcher
version: 1.0.0
description: Watch, monitor, and diff file system changes with a polling-based file watcher. Detect creates, modifications, and deletions — no external dependencies. Zero deps (Python stdlib).
tags: file, watch, monitor, fsnotify, python, devtools
---

# File System Watcher

A polling-based file system watcher that detects creates, modifications, and deletions. No external dependencies, no inotify, no OS-specific APIs — pure Python stdlib.

Ideal for build pipelines, development servers, log monitoring, and CI environments where `watchdog` or `inotifywait` isn't available.

## Install

```bash
# No dependencies needed — Python 3.8+ stdlib only
python file_watcher.py --help

# Make it a system command
chmod +x file_watcher.py
sudo cp file_watcher.py /usr/local/bin/file-watcher
```

## Commands

| Command | Description |
|---------|-------------|
| `watch` | Continuously watch a path for changes (polling loop) |
| `once` | Take a one-time snapshot of a path's state |
| `diff` | Compare two snapshots and show changes |

## Usage

```bash
# Watch a directory continuously (poll every 1s, show events)
python file_watcher.py watch ./src --poll-interval 1

# Watch a specific file
python file_watcher.py watch config.json

# Take a one-time snapshot (saves to stdout or file)
python file_watcher.py once ./src > snapshot1.json
python file_watcher.py once ./src --output snapshot2.json

# Diff two snapshots
python file_watcher.py diff snapshot1.json snapshot2.json
```

## Features

- **Zero dependencies** — pure Python stdlib, runs on any Python 3.8+ install
- **Polling-based** — works on every OS (Windows, macOS, Linux) without kernel-specific APIs
- **Event filtering** — watch for create, modify, or delete events separately
- **Snapshot diff** — take snapshots and compare them offline
- **Glob/regex filtering** — ignore noise like `__pycache__`, `.git`, and `node_modules`
- **Quiet mode** — only report changes, no banner
- **JSON snapshots** — machine-readable state captures for CI integration

## Examples

```bash
# Watch a project directory, ignoring common noise
python file_watcher.py watch . --ignore "**/node_modules" --ignore "**/.git" --ignore "**/__pycache__"

# Watch only Python files
python file_watcher.py watch . --glob "*.py"

# Take a snapshot before and after a build
python file_watcher.py once ./src --output pre-build.json
# ... run build ...
python file_watcher.py once ./dist --output post-build.json
python file_watcher.py diff pre-build.json post-build.json

# Watch a config directory for changes and exit after 5 events
python file_watcher.py watch /etc/myapp --max-events 5
```

## Why File System Watcher?

Most file watchers depend on OS-specific APIs — `inotify` on Linux, `FSEvents` on macOS, `ReadDirectoryChangesW` on Windows — or the `watchdog` Python package which wraps these. In CI, Docker, serverless, or locked-down environments, you often can't install additional packages or rely on kernel APIs. This tool uses simple polling (like `make`'s `-w` flag or `entr`'s polling mode) and works everywhere Python runs. The snapshot/diff model is also CI-native: capture state before and after a step and compare offline.

## Support

- File an issue on the [ClawHub registry](https://clawhub.nousresearch.com)
- MIT License — free to use, modify, and share
