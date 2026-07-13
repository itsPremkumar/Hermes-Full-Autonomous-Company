#!/usr/bin/env python3
"""Scan a folder's .md files for github.com/owner/repo links, verify each via the
GitHub repo API, and print stars + license. Hard rate-limit (HTTP 403) is caught
and reported as RATELIMITED — this script NEVER invents star counts.

Usage:  python github_verify.py <folder>
"""
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

REPO_RE = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")
API = "https://api.github.com/repos/{}"
UA = {"User-Agent": "Mozilla/5.0"}


def verify(repo):
    try:
        req = urllib.request.Request(API.format(repo), headers=UA)
        with urllib.request.urlopen(req, timeout=12) as r:
            d = json.load(r)
        lic = (d.get("license") or {}).get("spdx_id") or "N/A"
        return f"  OK   {repo:34} | {str(d.get('stargazers_count')):>7} | {lic:12}"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            return f"  RATELIMITED {repo}  (canonical path only — re-verify next session)"
        return f"  ERR {e.code} {repo}"
    except Exception as e:  # noqa
        return f"  ERR {repo}: {e}"


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    seen = set()
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith(".md"):
                continue
            path = os.path.join(root, f)
            with open(path, encoding="utf-8", errors="ignore") as fh:
                for m in REPO_RE.findall(fh.read()):
                    m = m.rstrip(").,'")  # drop trailing punctuation
                    if m not in seen:
                        seen.add(m)
                        print(verify(m))
                        time.sleep(0.4)  # gentle; still 403 if IP already limited


if __name__ == "__main__":
    main()
