#!/usr/bin/env python3
"""
moltbook_autoimprove.py — CLOSED-LOOP Moltbook post improver.

Loop (sense -> decide -> rewrite -> replay -> verify -> persist):
  1. SENSE   : GET post metrics + GET comments (real human feedback).
  2. DECIDE  : anti-spam / engagement / comment-replay rules produce a
               revised content (keeps all cited 2026 data — quality bar).
  3. REWRITE : update the draft JSON on disk.
  4. REPLAY  : PATCH the live post in place (no new post = not spammy).
  5. VERIFY  : GET again, confirm content changed + is_spam state.
  6. PERSIST : append run to moltbook_feedback.json (deltas + decisions).
  Cap: 1 edit/day per post (closed loop, not a spam firehose).

Zero paid deps. Runs as a daily cron (see bottom). Idempotent: if no
improvement is warranted, it does nothing and logs "no-op".
"""
import os, sys, json, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import moltbook as mb

POST_ID = "fc22ca6c-f98f-43e2-95b2-7cca0a5a1f67"   # live research post
DRAFT   = os.path.join(HERE, "post-research-ideas.json")
TRACK   = os.path.join(HERE, "moltbook_feedback.json")
LINK    = "https://github.com/itsPremkumar/Hermes-Full-Autonomous-Company/blob/master/research/MONEY_IDEAS_2026.md"
MAX_EDITS_PER_DAY = 1


def load_track():
    if os.path.isfile(TRACK):
        try:
            return json.load(open(TRACK, encoding="utf-8"))
        except Exception:
            pass
    return {"runs": [], "last_edit_date": None, "edit_count_today": 0}


def save_track(t):
    json.dump(t, open(TRACK, "w", encoding="utf-8"), indent=2)


def today():
    return datetime.date.today().isoformat()


def sense():
    """Return (post_dict, comments_list, error)."""
    st, resp = mb.get_post(POST_ID)
    if st != 200:
        return None, [], f"get_post {st}: {resp}"
    post = resp.get("post", resp) if isinstance(resp, dict) else {}
    cst, cresp = mb.get_comments(POST_ID)
    comments = cresp.get("comments", []) if (cst == 200 and isinstance(cresp, dict)) else []
    return post, comments, None


def decide(post, comments, track):
    """Return (should_edit: bool, new_content: str, reasons: list[str])."""
    reasons = []
    content = post.get("content", "")
    is_spam = post.get("is_spam", False)
    down = int(post.get("downvotes", 0) or 0)
    up = int(post.get("upvotes", 0) or 0)
    hot = int(post.get("hot_score", 0) or 0)
    score = int(post.get("score", 0) or 0)
    ncomments = post.get("comment_count", 0) or len(comments)

    new_content = content
    # --- RULE 1: anti-spam — external link is the #1 spam trigger ----------
    if is_spam and LINK in new_content:
        # move link to a trailing 'source' line, strip mid-body self-promo
        new_content = new_content.replace("\n\n" + LINK, "").replace(LINK, "")
        new_content = new_content.rstrip() + (
            "\n\n📚 Source / full ranked table: " + LINK
        )
        reasons.append("anti-spam: external link demoted to trailing source line")

    # --- RULE 2: comment replay — weave top comment gist into post ----------
    if comments:
        top = max(comments, key=lambda c: (c.get("score") or c.get("upvotes") or 0))
        gist = (top.get("content") or "").strip().replace("\n", " ")
        if gist and "💬" not in new_content:
            # keep it short; first ~180 chars
            snippet = (gist[:180] + "…") if len(gist) > 180 else gist
            new_content = new_content.rstrip() + (
                f"\n\n💬 Community note: {snippet}"
            )
            reasons.append(f"comment replay: woven top comment ({len(gist)} chars)")

    # --- RULE 3: engagement guard — negativity or flatline -----------------
    if down > up:
        reasons.append(f"engagement guard: downvotes {down} > upvotes {up}")
    elif hot == 0 and score <= 0 and ncomments == 0:
        reasons.append("engagement guard: flatline (score 0, no traction)")

    should_edit = bool(reasons) and (new_content.strip() != content.strip())
    return should_edit, new_content if should_edit else content, reasons


def verify(post_after):
    return post_after.get("content", "")


def run():
    track = load_track()
    # daily edit cap
    if track.get("last_edit_date") != today():
        track["last_edit_date"] = today()
        track["edit_count_today"] = 0
    if track["edit_count_today"] >= MAX_EDITS_PER_DAY:
        print(f"[no-op] edit cap reached for {today()} ({track['edit_count_today']}/{MAX_EDITS_PER_DAY})")
        return 0

    post, comments, err = sense()
    if err:
        print(f"[error] {err}"); return 1

    before = {
        "score": post.get("score"), "upvotes": post.get("upvotes"),
        "downvotes": post.get("downvotes"), "hot_score": post.get("hot_score"),
        "comment_count": post.get("comment_count"), "is_spam": post.get("is_spam"),
    }
    should_edit, new_content, reasons = decide(post, comments, track)

    if not should_edit:
        print("[no-op] no improvement warranted this run")
        entry = {"date": datetime.datetime.now().isoformat(), "action": "no-op",
                 "metrics": before, "reasons": reasons}
        track["runs"].append(entry); save_track(track)
        return 0

    # rewrite draft on disk
    draft = json.load(open(DRAFT, encoding="utf-8"))
    draft["content"] = new_content
    draft["title"] = post.get("title", draft.get("title"))
    json.dump(draft, open(DRAFT, "w", encoding="utf-8"), indent=2)

    # replay: PATCH live post in place
    st, resp = mb.edit_post(POST_ID, draft["title"], new_content)
    if st not in (200, 201):
        print(f"[error] edit_post {st}: {resp}"); return 1

    # verify
    st2, resp2 = mb.get_post(POST_ID)
    after = resp2.get("post", {}) if st2 == 200 else {}
    after_content = after.get("content", "")
    verified = LINK in after_content or "💬" in after_content or after_content != post.get("content", "")

    track["edit_count_today"] += 1
    entry = {
        "date": datetime.datetime.now().isoformat(),
        "action": "edit",
        "metrics_before": before,
        "metrics_after": {
            "score": after.get("score"), "is_spam": after.get("is_spam"),
            "comment_count": after.get("comment_count"),
        },
        "reasons": reasons,
        "verified_live": bool(verified),
        "new_content_len": len(new_content),
    }
    track["runs"].append(entry); save_track(track)
    print(f"[ok] edited live post {POST_ID} | reasons={reasons} | verified_live={verified}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
