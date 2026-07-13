# Knowledge Graph

Documents are linked, not孤立. This index is the entry point — follow the links. The
graph is markdown links (no separate DB needed).

```
CONSTITUTION.md (root)
├── docs/ai-kernel.md ─────────────→ maps kernel subsystems to real impl
├── docs/dependency-graph.md ──────→ who-depends-on-whom
├── docs/failure-taxonomy.md ──────→ categories + confidence gate
├── docs/production-readiness.md ──→ ship gate
├── docs/model-registry.md ────────→ task→model routing
├── docs/roadmap.md ───────────────→ V1→V7 evolution
├── docs/maturity.md ──────────────→ per-project level
├── agents/registry.md ────────────→ agent standard interface
├── tools/repo-index.md ───────────→ repo catalog
├── tools/approved.md / rejected.md → tool validation
├── knowledge-base/lessons-learned.md → what worked/failed
├── knowledge-base/benchmarks.md ──→ metrics over time
├── knowledge-base/experiments.md ─→ experiment log (hypothesis→result)
└── knowledge-base/graph.md ───────→ (this file)

Cross-links:
  OpenHands/coding agents ──→ GitHub (repo-index) ──→ CI/CD (production-readiness)
  Gumroad products ──→ revenue/ ──→ blog (content funnel) ──→ affiliate (§0.3 compliant)
  autonomy-loop ──→ failure-taxonomy (confidence) ──→ benchmarks (trends)
```

## Rule
When you create a document, add it here and link it from its parent. Isolated docs rot;
linked docs get reused. Re-validate links quarterly.
