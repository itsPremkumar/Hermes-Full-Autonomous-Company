#!/usr/bin/env python3
"""
Backup all Hermes "learned" skills to the Hermes-Full-Autonomous-Company repo.
Copies hermes/skills/<category>/<name>/ -> <repo>/skills/<category>/<name>/
Generates SKILLS_INDEX.md with usage stats from .usage.json.
Excludes .curator_backups and internal-only dirs (references/templates w/o SKILL.md).
"""
import os
import json
import shutil

SRC = r"C:\Users\PREM KUMAR\AppData\Local\hermes\skills"
DST = r"C:\one\paperclip-company\skills"
USAGE = r"C:\Users\PREM KUMAR\AppData\Local\hermes\skills\.usage.json"

EXCLUDE = {".curator_backups", ".git"}

def main():
    os.makedirs(DST, exist_ok=True)

    # Load usage stats
    usage = {}
    if os.path.isfile(USAGE):
        with open(USAGE, encoding="utf-8") as f:
            usage = json.load(f)

    copied = []
    for cat in sorted(os.listdir(SRC)):
        catpath = os.path.join(SRC, cat)
        if cat in EXCLUDE or not os.path.isdir(catpath):
            continue
        # sub-items may be skill-folders OR reference/template dirs
        for item in sorted(os.listdir(catpath)):
            itempath = os.path.join(catpath, item)
            if not os.path.isdir(itempath):
                continue
            skill_md = os.path.join(itempath, "SKILL.md")
            if not os.path.isfile(skill_md):
                # reference/template subdir of a category — skip (not a skill)
                continue
            dst_skill = os.path.join(DST, cat, item)
            os.makedirs(os.path.dirname(dst_skill), exist_ok=True)
            # copy entire skill folder
            if os.path.exists(dst_skill):
                shutil.rmtree(dst_skill)
            shutil.copytree(itempath, dst_skill)
            # strip __pycache__
            for root, dirs, files in os.walk(dst_skill):
                for d in list(dirs):
                    if d == "__pycache__":
                        shutil.rmtree(os.path.join(root, d))
            u = usage.get(item, {})
            copied.append({
                "category": cat,
                "name": item,
                "use_count": u.get("use_count", 0),
                "state": u.get("state", "unknown"),
            })
            print(f"copied: {cat}/{item} (uses={u.get('use_count',0)})")

    # Write index
    copied.sort(key=lambda x: (-x["use_count"], x["name"]))
    lines = ["# Hermes Learned Skills Backup", ""]
    lines.append(f"Total skills backed up: **{len(copied)}**")
    lines.append("")
    lines.append("Generated automatically from the local Hermes skill library. "
                 "Each folder maps to `hermes/skills/<category>/<name>/`.")
    lines.append("")
    lines.append("## By usage (most-used first)")
    lines.append("")
    lines.append("| Skill | Category | Uses | State |")
    lines.append("|-------|----------|------|-------|")
    for c in copied:
        lines.append(f"| {c['name']} | {c['category']} | {c['use_count']} | {c['state']} |")
    lines.append("")
    with open(os.path.join(DST, "SKILLS_INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Write raw usage snapshot
    with open(os.path.join(DST, "usage_snapshot.json"), "w", encoding="utf-8") as f:
        json.dump(usage, f, indent=2)

    print(f"\nDONE: {len(copied)} skills backed up to {DST}")
    print(f"Index written: SKILLS_INDEX.md")

if __name__ == "__main__":
    main()
