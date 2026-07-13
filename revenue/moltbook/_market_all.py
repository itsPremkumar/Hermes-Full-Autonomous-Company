import json, subprocess, sys, os, time

# Background Moltbook marketer for the 31-product stack.
# Posts ONE draft, then waits. On 429 (Moltbook's tight new-agent window)
# it backs off exponentially (5 -> 10 -> 20 -> 30 min) instead of
# spinning every 90s. On success it resets backoff and waits 90s.
# Logs progress to .posted.json. Stdlib + moltbook.py.

base = r"C:\one\paperclip-company\revenue\moltbook"
LOG = os.path.join(base, ".posted.json")
drafts = sorted(f for f in os.listdir(base)
                if f.startswith("post-") and f.endswith(".json"))
done = set()
if os.path.isfile(LOG):
    try:
        done = set(json.load(open(LOG, encoding="utf-8")))
    except Exception:
        done = set()

backoff = 90  # seconds; grows on 429
print(f"start: {len(drafts)} drafts, {len(done)} posted")
for d in drafts:
    if d in done:
        continue
    p = os.path.join(base, d)
    j = json.load(open(p, encoding="utf-8"))
    out = subprocess.run(
        [sys.executable, os.path.join(base, "moltbook.py"), "post",
         "--title", j["title"], "--content", j["content"], "--submolt", j["submolt"]],
        capture_output=True, text=True, timeout=30).stdout
    if "201" in out and ("success" in out.lower() or '"success": true' in out):
        done.add(d)
        json.dump(sorted(done), open(LOG, "w"), indent=2)
        print(f"POSTED {d} ({len(done)}/{len(drafts)}) - gap 90s")
        backoff = 90
        time.sleep(90)
    else:
        # 429 or drop: exponential backoff, capped at 30 min
        print(f"DEFER {d}: {out.strip()[:50]} - backoff {backoff}s")
        time.sleep(backoff)
        backoff = min(backoff * 2, 1800)
print(f"DONE: {len(done)}/{len(drafts)} posted (rest blocked by Moltbook rate window)")
