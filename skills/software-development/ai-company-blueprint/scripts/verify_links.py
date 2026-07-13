#!/usr/bin/env python3
"""Verify GitHub repo links inside a blueprint folder.

Scans every .md under <folder> for `github.com/owner/repo` URLs, then for each
unique repo: hits the GitHub repo API for live star count + license, and falls
back to an HTTP-200 HEAD check on the web URL if the API is rate-limited.

Usage:
    python verify_links.py <folder>
Exit code 0 = all links returned 200; 1 = at least one failed.
"""
import os
import re
import sys
import json
import urllib.request
import urllib.error

API = "https://api.github.com/repos/{}"
WEB = "https://github.com/{}"
LINK_RE = re.compile(r"https?://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)")


def check(repo):
    """Return (stars_or_None, license_or_ERR, source)."""
    try:
        req = urllib.request.Request(API.format(repo), headers={"User-Agent": "hermes-verify"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.load(r)
            return d.get("stargazers_count"), (d.get("license") or {}).get("spdx_id") or "N/A", "api"
    except Exception:
        pass
    try:
        req = urllib.request.Request(WEB.format(repo), headers={"User-Agent": "hermes-verify"}, method="HEAD")
        with urllib.request.urlopen(req, timeout=15) as r:
            return "200", "live", "http"
    except Exception as e:
        return None, "ERR {}".format(e), "http"


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    seen = {}
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            try:
                txt = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for repo in set(LINK_RE.findall(txt)):
                # strip any trailing path segments like /blob/.../file
                repo = repo.split("/blob/")[0].split("/tree/")[0]
                seen.setdefault(repo, fn)

    if not seen:
        print("No github.com/owner/repo links found.")
        return 0

    fails = 0
    for repo, src in sorted(seen):
        stars, lic, src_tag = check(repo)
        ok = stars is not None
        if not ok:
            fails += 1
        status = "200" if ok else "FAIL"
        star_str = str(stars) if stars is not None else "----"
        print("{:>4}  {:>7}  {:<12}  {}  (in {})".format(status, star_str, lic, repo, src))
    print("\n{} links checked, {} failed.".format(len(seen), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
