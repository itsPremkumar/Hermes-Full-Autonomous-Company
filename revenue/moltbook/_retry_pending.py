import json, subprocess, sys, os, time
base = r"C:\one\paperclip-company\revenue\moltbook"
for f in ["post-dev-prompts", "post-company-ops"]:
    d = json.load(open(os.path.join(base, f + ".json"), encoding="utf-8"))
    for attempt in range(8):
        r = subprocess.run([sys.executable, os.path.join(base, "moltbook.py"), "post",
                            "--title", d["title"], "--content", d["content"], "--submolt", d["submolt"]],
                           capture_output=True, text=True)
        out = (r.stdout or r.stderr).strip()
        if "201" in out:
            print(f, "-> POSTED 201"); break
        print(f, "-> retry", attempt+1, "status", out.split("status:")[-1].strip()[:30])
        time.sleep(45)
