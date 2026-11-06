#!/usr/bin/env python3
"""Score nodes and paths from a ledger under one or more weight profiles.

    python scripts/score.py runs/<run-id>/ledger.yaml
    python scripts/score.py runs/<run-id>/ledger.yaml --profiles balanced,venture,bootstrapped --json scores.json

- Criteria are scored 1-5 (5 favourable) with central/low/high (config/rubric.yaml).
- Missing criteria are treated as maximally uncertain (config/weights.yaml -> missing_score).
- Nodes with any failed gate are excluded and listed as killed.
- Coverage = share of weighted criteria whose basis is 'evidence'.
- Path score = weighted wedge (first node), terminal (broadest node in the sequence) and
  expansion plausibility, capped at weakest component + cap_margin.
- Flags rank flips across profiles: those are values choices for the founder.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import level_rank, load, load_config  # noqa: E402


def criterion_weights(rubric: dict, profile: dict) -> dict[str, float]:
    """Absolute weight per criterion: family weight (normalised) split across its criteria by multiplier."""
    fam_w = profile["families"]
    total = sum(fam_w.values())
    mult = profile.get("criterion_multipliers") or {}
    by_family: dict[str, list[str]] = {}
    for cid, c in rubric["criteria"].items():
        by_family.setdefault(c["family"], []).append(cid)
    weights: dict[str, float] = {}
    for fam, cids in by_family.items():
        fw = fam_w.get(fam, 0.0) / total if total else 0.0
        m_total = sum(mult.get(c, 1.0) for c in cids)
        for c in cids:
            weights[c] = fw * mult.get(c, 1.0) / m_total if m_total else 0.0
    return weights


def score_node(node: dict, weights: dict[str, float], missing: dict) -> dict:
    scores = node.get("scores") or {}
    out = {"central": 0.0, "low": 0.0, "high": 0.0, "coverage": 0.0, "missing": [], "assumed": []}
    for cid, w in weights.items():
        s = scores.get(cid)
        if s is None:
            s = {**missing, "basis": "missing"}
            out["missing"].append(cid)
        elif s.get("basis") != "evidence":
            out["assumed"].append(cid)
        else:
            out["coverage"] += w
        for k in ("central", "low", "high"):
            out[k] += w * float(s[k])
    return out


def gate_state(node: dict) -> tuple[bool, list[str]]:
    gates = node.get("gates") or {}
    failed = [g for g, v in gates.items() if v.get("result") == "fail"]
    unknown = [g for g, v in gates.items() if v.get("result") == "unknown"]
    return bool(failed) or node.get("status") == "killed", unknown


def score_path(path: dict, node_scores: dict, nodes_by_id: dict, path_cfg: dict, missing: dict) -> dict | None:
    seq = path.get("sequence") or []
    if not seq or any(n not in node_scores for n in seq):
        return None  # contains a killed or unknown node
    wedge = node_scores[seq[0]]
    terminal_id = min(seq, key=lambda n: (level_rank(nodes_by_id[n].get("level")), -seq.index(n)))
    terminal = node_scores[terminal_id]
    exp = path.get("expansion_plausibility") or (missing if len(seq) > 1 else {"central": 5, "low": 5, "high": 5})
    w = path_cfg["weights"]
    wt = w["wedge"] + w["terminal"] + w["expansion"]
    cap_margin = path_cfg.get("cap_margin", 1.0)
    out = {"terminal": terminal_id}
    for k in ("central", "low", "high"):
        comps = [wedge[k], terminal[k], float(exp[k])]
        raw = (w["wedge"] * comps[0] + w["terminal"] * comps[1] + w["expansion"] * comps[2]) / wt
        out[k] = min(raw, min(comps) + cap_margin)
    out["coverage"] = (wedge["coverage"] + terminal["coverage"]) / 2
    return out


def rank(items: dict[str, dict]) -> list[str]:
    return sorted(items, key=lambda i: (-items[i]["central"], -items[i]["low"]))


def main() -> int:
    ap = argparse.ArgumentParser(description="Score a marketplace-opportunity ledger.")
    ap.add_argument("ledger")
    ap.add_argument("--profiles", help="comma-separated profile names (default: all)")
    ap.add_argument("--config-dir")
    ap.add_argument("--json", help="write full results to this JSON file")
    args = ap.parse_args()

    ledger = load(args.ledger)
    rubric, weights_cfg, _gates = load_config(args.config_dir)
    profiles = weights_cfg["profiles"]
    names = args.profiles.split(",") if args.profiles else list(profiles)
    missing = weights_cfg.get("missing_score", {"central": 3, "low": 1, "high": 5})
    path_cfg = weights_cfg["path"]

    nodes = ledger.get("nodes") or []
    nodes_by_id = {n["id"]: n for n in nodes}
    killed = {n["id"]: n.get("kill_reason") or "failed gate" for n in nodes if gate_state(n)[0]}
    scorable = [n for n in nodes if n["id"] not in killed and (n.get("scores") or {})]

    results: dict = {"profiles": {}, "killed": killed}
    for name in names:
        prof = profiles[name]
        cw = criterion_weights(rubric, prof)
        ns = {n["id"]: score_node(n, cw, missing) for n in scorable}
        ps = {}
        for p in ledger.get("paths") or []:
            r = score_path(p, ns, nodes_by_id, path_cfg, missing)
            if r is not None:
                ps[p["id"]] = r
        results["profiles"][name] = {"nodes": ns, "paths": ps, "node_rank": rank(ns), "path_rank": rank(ps)}

    # Output
    first = names[0]
    print(f"# Scores ({', '.join(names)})\n")
    print("Scale 1-5, 5 favourable. Range = low-high. Coverage = share of weight backed by evidence.\n")
    for name in names:
        r = results["profiles"][name]
        print(f"## Profile: {name}\n")
        if r["path_rank"]:
            print("| Rank | Path | Central | Range | Coverage | Terminal node |\n|---|---|---|---|---|---|")
            for i, pid in enumerate(r["path_rank"], 1):
                s = r["paths"][pid]
                print(f"| {i} | {pid} | {s['central']:.2f} | {s['low']:.2f}-{s['high']:.2f} | {s['coverage']:.0%} | {s['terminal']} |")
            print()
        print("| Rank | Node | Level | Central | Range | Coverage | Missing | Unknown gates |\n|---|---|---|---|---|---|---|---|")
        for i, nid in enumerate(r["node_rank"], 1):
            s = r["nodes"][nid]
            unknown = gate_state(nodes_by_id[nid])[1]
            print(f"| {i} | {nid} {nodes_by_id[nid].get('name', '')[:40]} | {nodes_by_id[nid].get('level')} | "
                  f"{s['central']:.2f} | {s['low']:.2f}-{s['high']:.2f} | {s['coverage']:.0%} | {len(s['missing'])} | "
                  f"{','.join(unknown) or '-'} |")
        print()

    # Rank flips
    if len(names) > 1:
        flips = []
        for kind in ("path_rank", "node_rank"):
            base = results["profiles"][first][kind]
            for name in names[1:]:
                other = results["profiles"][name][kind]
                if base[:1] != other[:1] and base and other:
                    flips.append(f"{kind.split('_')[0]} leader differs: {first}={base[0]} vs {name}={other[0]}")
                for item in base:
                    if item in other and abs(base.index(item) - other.index(item)) >= 2:
                        flips.append(f"{item} moves {base.index(item) + 1}->{other.index(item) + 1} ({first}->{name})")
        print("## Rank flips across profiles\n")
        print("\n".join(f"- {f}" for f in sorted(set(flips))) if flips else "- None. Ranking is robust to the profiles tested.")
        print("\nRank flips are values choices (ambition, capital, time) for the founder, not analytical findings.\n")

    # Overlap warning for the top two paths in the first profile
    r = results["profiles"][first]
    if len(r["path_rank"]) >= 2:
        a, b = (r["paths"][r["path_rank"][0]], r["paths"][r["path_rank"][1]])
        if a["low"] <= b["high"]:
            print(f"Note: the top two paths' ranges overlap under '{first}'. Report them as tied and name the evidence that would separate them.\n")

    if killed:
        print("## Killed (excluded)\n")
        for nid, reason in killed.items():
            print(f"- {nid} {nodes_by_id[nid].get('name', '')}: {reason}")

    if args.json:
        Path(args.json).write_text(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
