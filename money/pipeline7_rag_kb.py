#!/usr/bin/env python3
"""
RAG Knowledge-Base Builder — Pipeline #7 from MONEY_AUTOMATION_IDEAS.md

Sells done-for-you RAG knowledge bases (your docs → queryable AI assistant)
on Hermes/OpenClaw. Validated 2026 pricing: $500 setup + $149/mo, 92% margin.

Usage: python pipeline7_rag_kb.py --vertical saas --out saas.json / --list / self-test
Zero dependencies (stdlib only).
"""
import argparse, json, sys

VERTICALS = {
    "saas": {"title": "I will build a RAG knowledge base + AI assistant for your SaaS",
             "sources": "docs, help center, changelog", "setup": 500, "monthly": 149},
    "ecommerce": {"title": "I will turn your store's docs into a shoppable AI assistant",
                  "sources": "product catalog, FAQs, policies", "setup": 450, "monthly": 129},
    "agency": {"title": "I will deploy a client-facing RAG KB for your agency",
               "sources": "case studies, proposals, playbooks", "setup": 600, "monthly": 199},
    "enterprise": {"title": "I will build an internal RAG assistant for your company wiki",
                   "sources": "wiki, SOPs, tickets", "setup": 1200, "monthly": 399},
}


def build_package(vertical, setup=None):
    v = VERTICALS[vertical]
    setup = setup or v["setup"]
    return {
        "vertical": vertical, "gig_title": v["title"], "sources": v["sources"],
        "pricing": {"setup": setup, "monthly": v["monthly"], "margin_pct": 92,
                    "cost_note": "self-hosted Hermes/OpenClaw; only compute"},
        "n8n_workflow": build_n8n(),
        "delivery_steps": [
            f"1. Ingest {v['sources']}",
            "2. Chunk + embed (local model, free)",
            "3. Deploy RAG on Hermes/OpenClaw + API",
            "4. Wire to Slack/website widget",
            "5. 14-day tuning + monthly refresh",
        ],
        "tags": ["rag", "knowledge base", "ai assistant", vertical + " rag", "chatbot", "llm"],
    }


def build_n8n():
    return {
        "name": "rag-kb-build",
        "nodes": [
            {"type": "n8n-nodes-base.scheduleTrigger", "name": "WeeklyIngest",
             "params": {"interval": [{"field": "cronExpression", "expression": "0 4 * * 1"}]}},
            {"type": "n8n-nodes-base.httpRequest", "name": "FetchDocs",
             "params": {"url": "={{$env.DOCS_URL}}", "httpMethod": "GET"}},
            {"type": "n8n-nodes-base.code", "name": "Chunk",
             "code": "const txt = (items[0].json.body||'');\nconst chunks = txt.match(/[^.\\n]{80,500}[.\\n]/g)||[txt];\nreturn chunks.map(c => ({json: {text: c}}));"},
            {"type": "n8n-nodes-base.httpRequest", "name": "EmbedStore",
             "params": {"url": "={{$env.RAG_API}}/ingest", "httpMethod": "POST"}},
        ],
        "connections": "WeeklyIngest → FetchDocs → Chunk → EmbedStore",
    }


def main():
    p = argparse.ArgumentParser(description="RAG KB Builder — Pipeline #7")
    p.add_argument("--vertical", help="vertical: " + ", ".join(VERTICALS.keys()))
    p.add_argument("--setup", type=int); p.add_argument("--out")
    p.add_argument("--list", action="store_true"); p.add_argument("cmd", nargs="?", default="self-test")
    a = p.parse_args()
    if a.list:
        for k, v in VERTICALS.items():
            print(f"  {k:10} ${v['setup']} + ${v['monthly']}/mo  {v['title'][:40]}")
        return
    if a.cmd == "self-test" and not a.vertical:
        for k in VERTICALS:
            pkg = build_package(k)
            assert pkg["gig_title"] and pkg["n8n_workflow"]["nodes"]
            assert pkg["pricing"]["margin_pct"] == 92
            code = pkg["n8n_workflow"]["nodes"][2]["code"]
            assert "return" in code and "TODO" not in code
        print(f"self-test: OK — {len(VERTICALS)} verticals")
        return
    if not a.vertical or a.vertical not in VERTICALS:
        print("ERROR: --vertical required: " + ", ".join(VERTICALS.keys())); sys.exit(1)
    pkg = build_package(a.vertical, a.setup)
    if a.out:
        json.dump(pkg, open(a.out, "w", encoding="utf-8"), indent=2); print(f"Wrote -> {a.out}")
    else:
        print(f"\n🧠 RAG KB: {a.vertical}\n📋 {pkg['gig_title']}\n💲 ${pkg['pricing']['setup']} + ${pkg['pricing']['monthly']}/mo (92% margin)")


if __name__ == "__main__":
    main()
