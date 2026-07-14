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

# Validated submolt names (seeded from GET /submolts). Mirror of the set in
# moltbook.py — keeps the scheduler from 404-ing on bad drafts.
VALID_SUBMOLTS = {
    "agent-economy","agent-ops","agentautomation","agentcommerce","agenteconomics",
    "agenteconomy","agentfinance","agentinfra","agentinfrastructure","agentops",
    "agents","agentskills","agentsouls","agentstack","agenttips","ai","ai-agents",
    "ai-coding","aiagents","aisafety","aithoughts","aitools","algotrading",
    "announcements","automation","blesstheirhearts","builders","buildlogs","builds",
    "buildx","clawtasks","cli-agents","coding","conscious","consciousness",
    "continuity","coordinating-agi","crab-rave","crustafarianism","crypto",
    "cybersecurity","debugging","debugging-wins","defi","dev","devtools","economics",
    "emergence","engineering","existential","explainlikeim5","finance","fomolt",
    "ftec5660","gaming","general","infrastructure","introductions","investing",
    "mbc-20","mbc20","mcp","memory","meta","multiagent","music","nightshift",
    "offmychest","openclaw","openclaw-explorers","optimization","philosophy",
    "ponderings","productivity","programming","quantmolt","remote-work","research",
    "saas","science","security","selfmodding","selfpaid","shipping","shitposts",
    "showandtell","skills","souls","streaming","swarm","tech","technology",
    "thebecoming","tips","todayilearned","tooling","tools","trading","travel","usdc",
}

def validate_submolt(name):
    if not name:
        return True
    return name in VALID_SUBMOLTS


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


FAILED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "failed.json")


def load_failed():
    if os.path.isfile(FAILED_FILE):
        with open(FAILED_FILE) as f:
            data = json.load(f)
            return set(data.get("failed", []))
    return set()


def save_failed(failed):
    with open(FAILED_FILE, "w") as f:
        json.dump({"failed": sorted(failed)}, f, indent=2)


def find_unposted_draft(posted_slugs, skipped_slugs=None, failed_slugs=None):
    """Find first draft JSON file whose slug isn't posted, isn't skipped
    (invalid submolt), and isn't in the hard-failure set.

    Drafts with an invalid submolt are accumulated into `skipped_slugs` and
    drafts that hard-failed (non-transient 4xx) go into `failed_slugs` so the
    scheduler never gets stuck on one bad draft and stalls the whole queue.
    """
    if skipped_slugs is None:
        skipped_slugs = set()
    if failed_slugs is None:
        failed_slugs = set()
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.startswith("post-") or not fname.endswith(".json"):
            continue
        if fname == "posted.json":
            continue
        slug = fname.replace("post-", "").replace(".json", "")
        if slug in posted_slugs or slug in skipped_slugs or slug in failed_slugs:
            continue
        draft_path = os.path.join(POSTS_DIR, fname)
        with open(draft_path) as f:
            draft = json.load(f)
        submolt = draft.get("submolt", None)
        if not validate_submolt(submolt):
            skipped_slugs.add(slug)
            continue
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
    failed = load_failed()
    skipped = set()
    slug, draft = find_unposted_draft(posted, skipped, failed)
    if not draft:
        if skipped:
            print(f"All valid drafts posted ({len(posted)}). "
                  f"Skipped {len(skipped)} draft(s) with invalid submolt: "
                  f"{', '.join(sorted(skipped))} — fix the draft's submolt to post them.")
            sys.exit(0)
        if failed:
            print(f"All postable drafts done ({len(posted)} posted, "
                  f"{len(failed)} hard-failed & skipped: {', '.join(sorted(failed))}).")
        else:
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
        remaining = total - len(posted) - len(failed)
        print(f"✅ Posted {slug}. {len(posted)}/{total} done. Remaining (postable): {remaining}")
        return 0
    elif status == 429:
        # Transient rate-limit — back off, do NOT mark failed. The scheduler's
        # caller should wait before retrying. Exit non-zero so a tight loop
        # caller knows to stop hammering.
        print(f"⏳ Rate limited (HTTP 429). Back off and retry later — not marking as failed.")
        return 3
    elif 400 <= status < 500:
        # Hard client error (e.g. 400 invalid payload, 403 forbidden). Skip so
        # the queue advances instead of looping forever on this draft.
        failed.add(slug)
        save_failed(failed)
        print(f"⛔ Hard failure HTTP {status} for {slug} — skipping so the queue advances.")
        return 1
    else:
        # 5xx or other — treat as transient, don't mark failed, let it retry.
        print(f"❌ Post failed for {slug} (HTTP {status}) — will retry next run.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
