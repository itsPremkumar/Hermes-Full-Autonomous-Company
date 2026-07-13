# Production Readiness Checklist

No project ships to "production" (published, sold, or promoted) until ALL boxes are
checked. This is the gate referenced by CONSTITUTION §12 and the maturity levels
(docs/maturity.md).

- [ ] **Documentation complete** — README, install, usage example, troubleshooting
- [ ] **Tests passing** — at least a smoke test / build check is green
- [ ] **Security review completed** — no secrets committed; deps scanned; §0.3 claims true
- [ ] **Performance acceptable** — runs within hardware constraints (§6): RAM/CPU budget met
- [ ] **Rollback available** — last-known-good git tag + changelog rollback note
- [ ] **Monitoring enabled** — metrics flow to knowledge-base/benchmarks.md + autonomy-loop.log
- [ ] **Version tagged** — semantic version in product dir + CHANGELOG entry
- [ ] **Checkpoint saved** — state snapshot in checkpoints/ before publish
- [ ] **Human sign-off** — for anything money-moving or publicly claimed (§0.1, §0.2)

If any box is unchecked, the item stays at its current maturity level and is NOT published.
Human-gated items (Gumroad publish, payouts) additionally require the principal's action.
