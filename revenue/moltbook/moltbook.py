#!/usr/bin/env python3
"""
moltbook.py — post agent-native announcements to Moltbook via the public REST API.

Agent-safe, stdlib-only. Flow:
  1. register()  -> creates an agent, returns api_key + claim_url (human verifies later)
  2. post()      -> creates a text/link post with the api_key as Bearer token

The autonomy loop can call post() on a schedule (rate-limited, non-spammy).
Account creation (register) needs NO interactive login; only the optional
"claim"/human-verification step (Twitter/X) is yours — and posting may work
before claiming (verification affects trust, not basic posting).

No secrets stored in repo: api_key is saved to .moltbook_key (gitignored) locally.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE = "https://www.moltbook.com/api/v1"
KEY_FILE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".moltbook_key"))

# Validated submolt names (seeded from GET /submolts; stable core set so drafts
# validate offline). `post()` rejects anything not in here with a clear error
# instead of a silent 404 "Submolt not found" (which let broken drafts
# pile up untracked + look like spam).
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
    """Return True if name is a known Moltbook submolt (empty = server default)."""
    if not name:
        return True
    return name in VALID_SUBMOLTS


def _req(method, path, data=None, api_key=None):
    url = BASE + path
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode()[:300] if e.fp else str(e))


def register(name="prem-autonomous-co"):
    """Create an agent. Returns (status, api_key, claim_url). No interactive login."""
    st, resp = _req("POST", "/agents/register", {"name": name})
    if st in (200, 201) and resp.get("agent", {}).get("api_key"):
        a = resp["agent"]
        key = a["api_key"]
        with open(KEY_FILE, "w") as f:
            f.write(key)
        return st, key, a.get("claim_url", ""), a.get("verification_code", "")
    return st, None, resp, None


def load_key():
    if os.path.isfile(KEY_FILE):
        return open(KEY_FILE).read().strip()
    return None


def post(title, content, submolt=None, link=None):
    """Create a post. Requires an api_key (register first).
    NOTE: Moltbook's /posts text endpoint rejects a top-level 'link' property
    (400 'property link should not exist'). Put URLs inside content instead.
    Rejects an invalid submolt up-front (clear error) instead of a silent 404."""
    if submolt and not validate_submolt(submolt):
        return 400, f"invalid submolt '{submolt}' — must be one of the valid Moltbook submolts"
    key = load_key()
    if not key:
        return 401, "no api_key — run register() first"
    body = content
    if link:
        body = f"{content}\n\n{link}"  # embed link in body; API has no top-level link field
    payload = {"title": title, "content": body}
    if submolt:
        payload["submolt"] = submolt
    return _req("POST", "/posts", payload, api_key=key)


def get_post(post_id):
    """Fetch a single post (metrics + content). Read-only."""
    return _req("GET", f"/posts/{post_id}")


def edit_post(post_id, title, content):
    """Edit an existing post in place via PATCH (title + content only;
    Moltbook's edit endpoint rejects a top-level 'submolt').

    GUARD: refuses obviously-destructive writes (empty/very-short content,
    or title/content that don't look like real post text). Verification
    scripts must NEVER call this with probe values like ('x','x') — it
    performs a real, irreversible overwrite of the live post."""
    if not title or not content:
        return 400, "refuse edit: empty title/content (would blank the post)"
    if len(content) < 80 or len(title) < 5:
        return 400, "refuse edit: content too short — likely a probe/destructive write"
    key = load_key()
    if not key:
        return 401, "no api_key — run register() first"
    payload = {"title": title, "content": content}
    return _req("PATCH", f"/posts/{post_id}", payload, api_key=key)


def get_comments(post_id):
    """Fetch comments for a post (real human feedback). Read-only."""
    return _req("GET", f"/posts/{post_id}/comments?limit=50")


def main():
    p = argparse.ArgumentParser(description="Moltbook agent poster")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("register").add_argument("--name", default="prem-autonomous-co")
    pp = sub.add_parser("post")
    pp.add_argument("--title", required=True)
    pp.add_argument("--content", required=True)
    pp.add_argument("--submolt", default=None)
    pp.add_argument("--link", default=None)
    sub.add_parser("feed")
    args = p.parse_args()

    if args.cmd == "register":
        st, key, claim, code = register(args.name)
        print(f"register status: {st}")
        if key:
            print(f"api_key saved to {KEY_FILE}")
            print(f"claim_url (your human-verify step, optional): {claim}")
            print(f"verification_code: {code}")
        else:
            print("register failed:", claim)
        return 0 if key else 1
    if args.cmd == "post":
        st, resp = post(args.title, args.content, args.submolt, args.link)
        print(f"post status: {st}")
        print(json.dumps(resp, indent=2)[:500] if isinstance(resp, dict) else resp)
        return 0 if st in (200, 201) else 1
    if args.cmd == "feed":
        st, resp = get_feed()
        print(f"feed status: {st}")
        print(json.dumps(resp, indent=2)[:600] if isinstance(resp, dict) else resp)
        return 0


if __name__ == "__main__":
    sys.exit(main())
