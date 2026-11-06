#!/usr/bin/env python3
"""Bottom-up sizing and unit-economics model (template).

Copy to runs/<run-id>/models/<path-id>.py and edit PARAMS. Every parameter is a
triangular (low, mode, high) with an evidence id or "assumed". Standard library only.

    python sizing_model.py            # prints P10/P50/P90 and a sensitivity table
    python sizing_model.py --json out.json

The default PARAMS are placeholders to demonstrate the mechanics. They are NOT data.
"""
from __future__ import annotations

import argparse
import json
import random
import statistics

# --------------------------------------------------------------------------------------
# PARAMS: (low, mode, high, source). Source is an evidence id (ev-###) or "assumed".
# Annual figures, one currency.
# --------------------------------------------------------------------------------------
CURRENCY = "GBP"
PARAMS = {
    # Demand
    "addressable_buyers":        (2_000, 5_000, 9_000, "assumed"),   # in the atomic network or market being sized
    "adoption_share":            (0.02, 0.06, 0.15, "assumed"),      # share of addressable buyers who transact via the platform
    "transactions_per_buyer":    (1.0, 2.0, 4.0, "assumed"),         # per year
    "repeat_share":              (0.3, 0.5, 0.7, "assumed"),         # share of transactions that are repeats with the same counterparty
    "leakage_rate":              (0.1, 0.3, 0.6, "assumed"),         # share of repeat transactions lost off-platform
    "order_value":               (80, 150, 300, "assumed"),
    # Monetisation
    "take_rate":                 (0.08, 0.12, 0.18, "assumed"),
    "ancillary_rate":            (0.00, 0.01, 0.03, "assumed"),      # ancillary revenue as share of GMV
    # Variable costs
    "payment_cost_rate":         (0.015, 0.02, 0.03, "assumed"),     # share of GMV
    "support_cost_per_txn":      (2.0, 4.0, 8.0, "assumed"),         # support plus trust and safety
    "compliance_cost_per_txn":   (0.5, 1.5, 3.0, "assumed"),         # verification, reporting, product safety
    # Acquisition
    "buyer_cac":                 (20, 45, 90, "assumed"),
    "suppliers_needed":          (50, 120, 250, "assumed"),          # for the atomic network
    "supplier_cac":              (50, 150, 400, "assumed"),
}
N_SIMULATIONS = 20_000
SEED = 7


def model(p: dict) -> dict:
    """Deterministic model for one draw of parameters."""
    buyers = p["addressable_buyers"] * p["adoption_share"]
    gross_txns = buyers * p["transactions_per_buyer"]
    lost = gross_txns * p["repeat_share"] * p["leakage_rate"]
    txns = gross_txns - lost
    gmv = txns * p["order_value"]
    net_revenue = gmv * (p["take_rate"] + p["ancillary_rate"])
    variable_costs = gmv * p["payment_cost_rate"] + txns * (p["support_cost_per_txn"] + p["compliance_cost_per_txn"])
    contribution = net_revenue - variable_costs
    contribution_per_buyer = contribution / buyers if buyers else 0.0
    payback_months = (p["buyer_cac"] / contribution_per_buyer * 12) if contribution_per_buyer > 0 else float("inf")
    supply_launch_cost = p["suppliers_needed"] * p["supplier_cac"]
    return {
        "buyers": buyers,
        "transactions": txns,
        "gmv": gmv,
        "net_revenue": net_revenue,
        "contribution": contribution,
        "contribution_margin_on_gmv": contribution / gmv if gmv else 0.0,
        "buyer_payback_months": payback_months,
        "supply_launch_cost": supply_launch_cost,
    }


def draw(rng: random.Random) -> dict:
    return {k: rng.triangular(lo, hi, mode) for k, (lo, mode, hi, _src) in PARAMS.items()}


def modes() -> dict:
    return {k: mode for k, (lo, mode, hi, _src) in PARAMS.items()}


def percentiles(values: list[float]) -> dict:
    finite = sorted(v for v in values if v != float("inf"))
    if not finite:
        return {"p10": None, "p50": None, "p90": None}
    q = statistics.quantiles(finite, n=10, method="inclusive")
    return {"p10": q[0], "p50": statistics.median(finite), "p90": q[8]}


def simulate() -> dict:
    rng = random.Random(SEED)
    runs = [model(draw(rng)) for _ in range(N_SIMULATIONS)]
    keys = runs[0].keys()
    return {k: percentiles([r[k] for r in runs]) for k in keys}


def sensitivity(output: str = "contribution") -> tuple[list[tuple[str, float, float, float]], float]:
    """One-at-a-time swing: each parameter at low and high, others at mode."""
    base = model(modes())[output]
    rows = []
    for k, (lo, mode, hi, _src) in PARAMS.items():
        p_lo, p_hi = modes(), modes()
        p_lo[k], p_hi[k] = lo, hi
        out_lo, out_hi = model(p_lo)[output], model(p_hi)[output]
        rows.append((k, out_lo, out_hi, abs(out_hi - out_lo)))
    rows.sort(key=lambda r: r[3], reverse=True)
    return [(k, lo, hi, swing) for k, lo, hi, swing in rows], base


def fmt(x) -> str:
    if x is None:
        return "n/a"
    if x == float("inf"):
        return "never"
    if abs(x) >= 1000:
        return f"{x:,.0f}"
    return f"{x:,.3f}" if abs(x) < 1 else f"{x:,.1f}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", help="write results to this JSON file")
    args = ap.parse_args()

    assumed = [k for k, v in PARAMS.items() if v[3] == "assumed"]
    results = simulate()
    sens, base = sensitivity("contribution")

    print(f"# Sizing model ({CURRENCY}, annual). {N_SIMULATIONS:,} simulations, seed {SEED}\n")
    if assumed:
        print(f"WARNING: {len(assumed)} of {len(PARAMS)} parameters are 'assumed' (no evidence id): {', '.join(assumed)}\n")
    print("| Output | P10 | P50 | P90 |\n|---|---|---|---|")
    for k, v in results.items():
        print(f"| {k} | {fmt(v['p10'])} | {fmt(v['p50'])} | {fmt(v['p90'])} |")
    print(f"\n## Sensitivity of contribution (base at modes: {fmt(base)})\n")
    print("| Parameter | At low | At high | Swing |\n|---|---|---|---|")
    for k, lo, hi, swing in sens:
        print(f"| {k} | {fmt(lo)} | {fmt(hi)} | {fmt(swing)} |")
    print("\nTop three drivers become Stage 7 assumptions:", ", ".join(k for k, *_ in sens[:3]))

    if args.json:
        with open(args.json, "w") as f:
            json.dump({"currency": CURRENCY, "params": {k: list(v) for k, v in PARAMS.items()},
                       "results": results,
                       "sensitivity": [{"param": k, "low": lo, "high": hi, "swing": s} for k, lo, hi, s in sens]},
                      f, indent=2, default=str)


if __name__ == "__main__":
    main()
