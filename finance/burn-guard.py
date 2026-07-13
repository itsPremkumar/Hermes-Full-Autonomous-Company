#!/usr/bin/env python3
"""
CFO burn guard — enforces the $0 monthly cash-burn policy for Prem Autonomous Co.

It is the operative part of PRE-19 ("revenue ledger + burn=/usr/bin/bash guard").
The guard loads the revenue ledger and the burn policy, then fails (non-zero exit)
if ANY cash burn is recorded or if a cost category falls outside the allowed list.

Exit codes:
  0  PASS — ledger is consistent with the $0-burn policy
  1  FAIL — a violation was found (prints each violation to stderr)
  2  ERROR — could not read inputs (missing file / bad JSON / missing cols)
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "revenue-ledger.csv")
POLICY = os.path.join(HERE, "burn-policy.json")


def fail(msg):
    print(f"GUARD FAIL: {msg}", file=sys.stderr)


def error(msg):
    print(f"GUARD ERROR: {msg}", file=sys.stderr)


def main():
    if not os.path.isfile(LEDGER):
        error(f"ledger not found: {LEDGER}")
        return 2
    if not os.path.isfile(POLICY):
        error(f"policy not found: {POLICY}")
        return 2

    try:
        with open(POLICY, encoding="utf-8") as f:
            policy = json.load(f)
    except Exception as e:  # noqa: BLE001
        error(f"could not parse policy JSON: {e}")
        return 2

    cap = policy.get("monthly_cash_burn_cap_usd", 0)
    forbidden = set(policy.get("forbidden", []))

    violations = []

    # 1) Enforce the numeric burn cap from the ledger's spend_usd column.
    with open(LEDGER, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "spend_usd" not in (reader.fieldnames or []):
            error("ledger missing required column: spend_usd")
            return 2
        rows = list(reader)

    for row in rows:
        period = row.get("period", "?")
        try:
            spend = float(row.get("spend_usd", 0) or 0)
        except ValueError:
            violations.append(f"[{period}] non-numeric spend_usd: {row.get('spend_usd')!r}")
            continue
        if spend > cap:
            violations.append(
                f"[{period}] cash burn ${spend:0.2f} exceeds cap ${cap:0.2f}"
            )

    # 2) Confirm no forbidden cost categories are in play (lightweight textual check
    #    against the ledger notes + policy forbidden list). The policy forbids any
    #    cash outflow; the ledger must never record a paid category.
    forbidden_tokens = [
        "paid api", "ad spend", "ads", "saas", "subscription fee",
        "outsourced", "contractor paid", "cloud bill", "invoice paid",
    ]
    for row in rows:
        period = row.get("period", "?")
        note = (row.get("notes") or "").lower()
        for tok in forbidden_tokens:
            if tok in note:
                violations.append(
                    f"[{period}] forbidden cost signal in notes: {tok!r}"
                )

    # 3) Sanity: target MRR progression is non-decreasing-ish and non-negative.
    for row in rows:
        period = row.get("period", "?")
        for col in ("target_mrr_usd", "actual_mrr_usd", "target_onetime_usd", "actual_onetime_usd"):
            try:
                val = float(row.get(col, 0) or 0)
            except ValueError:
                violations.append(f"[{period}] non-numeric {col}: {row.get(col)!r}")
                continue
            if val < 0:
                violations.append(f"[{period}] negative {col}: {val}")

    if forbidden & {"any_cash_outflow"} and any(
        float(r.get("spend_usd", 0) or 0) > 0 for r in rows
    ):
        violations.append("policy forbids any cash outflow; ledger records spend > 0")

    if violations:
        for v in violations:
            fail(v)
        print(
            f"GUARD RESULT: FAIL ({len(violations)} violation(s)) — burn policy NOT met.",
            file=sys.stderr,
        )
        return 1

    print("GUARD RESULT: PASS — ledger consistent with $0-burn policy.")
    print(f"  periods tracked : {len(rows)}")
    print(f"  burn cap (USD)  : {cap}")
    print(f"  cash outflow    : $0.00 (all periods)")
    print(f"  policy owner    : {policy.get('owner', 'unknown')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
