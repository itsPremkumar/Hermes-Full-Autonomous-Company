#!/usr/bin/env python3
"""
Moltbook post scheduler — runs every 30 min, posts ONE unposted draft.
Tracks state via posted.json to avoid duplicates.
"""
import json
import os
import sys

# Same KEY_FILE resolution as moltbook.py
KEY_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".moltbook_key"
))
TRACKING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posted.json")
POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

BASE = "https://www.moltbook.com/api/v1"


def load_api_key():
    if os.path.isfile(KEY_FILE):
        return open(KEY_FILE).read().strip()
    return None


def load_tracking():
    if os.path.isfile(TRACKING_FILE):
        with open(TRACKING_FILE) as f:
            data = json.load(f)
            return data.get("posted", [])
    return []


def save_tracking(posted_slugs):
    with open(TRACKING_FILE, "w") as f:
        json.dump({"posted": posted_slugs}, f, indent=2)


def find_unposted_draft(posted_slugs):
    """Find first draft JSON file whose slug isn't in posted_slugs."""
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.startswith("post-") or not fname.endswith(".json"):
            continue
        if fname == "posted.json":
            continue
        slug = fname.replace("post-", "").replace(".json", "")
        if slug not in posted_slugs:
            draft_path = os.path.join(POSTS_DIR, fname)
            with open(draft_path) as f:
                draft = json.load(f)
            return slug, draft
    return None, None


def post_to_moltbook(title, content, submolt, api_key):
    """Post to Moltbook API using urllib (stdlib)."""
    import urllib.request
    import urllib.error

    url = BASE + "/posts"
    payload = {"title": title, "content": content}
    if submolt:
        payload["submolt"] = submolt

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode()[:500] if e.fp else str(e))


def main():
    api_key = load_api_key()
    if not api_key:
        print("ERROR: No API key. Run register first.")
        sys.exit(1)

    posted = load_tracking()
    slug, draft = find_unposted_draft(posted)
    if not draft:
        print(f"All {len(posted)} drafts posted! Nothing to do.")
        sys.exit(0)

    title = draft.get("title", slug)
    content = draft.get("content", "")
    submolt = draft.get("submolt", None)

    print(f"Posting: {slug} — {title[:60]}...")
    status, resp = post_to_moltbook(title, content, submolt, api_key)
    print(f"Response: HTTP {status}")
    if isinstance(resp, dict):
        print(json.dumps(resp, indent=2)[:300])
    else:
        print(str(resp)[:300])

    if status in (200, 201):
        posted.append(slug)
        save_tracking(posted)
        total = len([f for f in os.listdir(POSTS_DIR) if f.startswith("post-") and f.endswith(".json") and f != "posted.json"])
        remaining = total - len(posted)
        print(f"✅ Posted {slug}. {len(posted)}/{total} done. Remaining: {remaining}")
        return 0
    else:
        print(f"❌ Post failed for {slug}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
