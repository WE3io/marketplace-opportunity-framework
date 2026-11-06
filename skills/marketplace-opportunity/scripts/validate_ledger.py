#!/usr/bin/env python3
"""Validate a run's ledger (and evidence log) against the framework's rules.

    python scripts/validate_ledger.py runs/<run-id>/ledger.yaml [--evidence runs/<run-id>/evidence.yaml]

Checks structure, ids, enums, score ranges, gate and criterion ids, evidence references,
path integrity and assumption fields. Exits 1 if there are errors. Warnings do not fail.
If jsonschema is installed, also validates against schemas/*.schema.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import SKILL_DIR, load, load_config  # noqa: E402

LEVELS = {"L0", "L1", "L2", "L3", "L4"}
STATUSES = {"candidate", "shortlisted", "killed", "recommended"}
GATE_RESULTS = {"pass", "fail", "unknown"}
BASES = {"evidence", "assumed"}
CONFIDENCE = {"high", "moderate", "low"}
SOURCE_TYPES = {"official", "filing", "regulator", "court", "independent", "analyst", "press",
                "vendor", "investor", "forum", "founder", "synthetic"}


def schema_check(doc: dict, schema_name: str, errors: list[str]) -> None:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return
    schema = json.loads((SKILL_DIR / "schemas" / schema_name).read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        errors.append(f"schema {schema_name}: {loc}: {err.message}")


EV_BY_ID: dict[str, dict] = {}


def check_score(where: str, s: dict, criteria: set[str] | None, ev_ids: set[str] | None,
                errors: list[str], warnings: list[str]) -> None:
    for k in ("central", "low", "high", "basis"):
        if k not in s:
            errors.append(f"{where}: missing '{k}'")
            return
    c, lo, hi = s["central"], s["low"], s["high"]
    if not all(isinstance(v, (int, float)) for v in (c, lo, hi)):
        errors.append(f"{where}: central/low/high must be numbers")
        return
    if not (1 <= lo <= c <= hi <= 5):
        errors.append(f"{where}: need 1 <= low <= central <= high <= 5 (got {lo}, {c}, {hi})")
    if s["basis"] not in BASES:
        errors.append(f"{where}: basis must be one of {sorted(BASES)}")
    evs = s.get("evidence") or []
    if s["basis"] == "evidence" and not evs:
        errors.append(f"{where}: basis 'evidence' but no evidence ids")
    if s["basis"] == "assumed" and (hi - lo) < 2:
        warnings.append(f"{where}: assumed score with narrow range ({lo}-{hi}); widen it")
    if ev_ids is not None:
        for e in evs:
            if e not in ev_ids:
                errors.append(f"{where}: evidence id '{e}' not in evidence log")
        if s["basis"] == "evidence" and evs and all(EV_BY_ID.get(e, {}).get("confidence") == "low" for e in evs):
            warnings.append(f"{where}: basis 'evidence' rests only on low-confidence sources; treat as assumed")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a marketplace-opportunity ledger.")
    ap.add_argument("ledger")
    ap.add_argument("--evidence", help="evidence log (default: evidence.yaml next to the ledger)")
    ap.add_argument("--config-dir")
    args = ap.parse_args()

    ledger_path = Path(args.ledger)
    ledger = load(ledger_path)
    rubric, _weights, gates_cfg = load_config(args.config_dir)
    criteria = set(rubric["criteria"].keys())
    gate_ids = set(gates_cfg["gates"].keys())

    errors: list[str] = []
    warnings: list[str] = []

    # Evidence log
    ev_path = Path(args.evidence) if args.evidence else ledger_path.with_name("evidence.yaml")
    ev_ids: set[str] | None = None
    ev_by_id: dict[str, dict] = {}
    if ev_path.exists():
        ev_doc = load(ev_path)
        schema_check(ev_doc, "evidence.schema.json", errors)
        ev_ids = set()
        for i, e in enumerate(ev_doc.get("evidence") or []):
            eid = e.get("id")
            if not eid:
                errors.append(f"evidence[{i}]: missing id")
                continue
            if eid in ev_ids:
                errors.append(f"evidence {eid}: duplicate id")
            ev_ids.add(eid)
            ev_by_id[eid] = e
            if e.get("confidence") not in CONFIDENCE:
                errors.append(f"evidence {eid}: confidence must be one of {sorted(CONFIDENCE)}")
            stype = (e.get("source") or {}).get("type")
            if stype not in SOURCE_TYPES:
                errors.append(f"evidence {eid}: source.type must be one of {sorted(SOURCE_TYPES)}")
            if stype == "synthetic":
                warnings.append(f"evidence {eid}: synthetic source; must not appear in a real memo")
    else:
        warnings.append(f"no evidence log found at {ev_path}; evidence ids not checked")
    EV_BY_ID.update(ev_by_id)

    schema_check(ledger, "ledger.schema.json", errors)

    # Nodes
    nodes = ledger.get("nodes") or []
    node_ids: set[str] = set()
    for n in nodes:
        nid = n.get("id", "?")
        if nid in node_ids:
            errors.append(f"node {nid}: duplicate id")
        node_ids.add(nid)
    for n in nodes:
        nid = n.get("id", "?")
        if n.get("level") not in LEVELS:
            errors.append(f"node {nid}: level must be one of {sorted(LEVELS)}")
        if n.get("status") not in STATUSES:
            errors.append(f"node {nid}: status must be one of {sorted(STATUSES)}")
        parent = n.get("parent")
        if parent and parent not in node_ids:
            errors.append(f"node {nid}: parent '{parent}' not found")
        if n.get("status") == "killed" and not n.get("kill_reason"):
            errors.append(f"node {nid}: killed without kill_reason")
        cards = n.get("transaction_cards") or []
        if not cards:
            warnings.append(f"node {nid}: no transaction card (required before scoring)")
        for j, card in enumerate(cards):
            for k in ("buyer", "seller", "object", "trigger"):
                if not card.get(k):
                    warnings.append(f"node {nid} card {j}: '{k}' empty")
            if ev_ids is not None:
                for e in card.get("evidence") or []:
                    if e not in ev_ids:
                        errors.append(f"node {nid} card {j}: evidence id '{e}' not in evidence log")
            if not card.get("evidence"):
                warnings.append(f"node {nid} card {j}: no evidence that the transaction happens today")
        gates = n.get("gates") or {}
        for gid, g in gates.items():
            if gid not in gate_ids:
                errors.append(f"node {nid}: unknown gate '{gid}'")
                continue
            if g.get("result") not in GATE_RESULTS:
                errors.append(f"node {nid} {gid}: result must be one of {sorted(GATE_RESULTS)}")
            if not g.get("rationale"):
                warnings.append(f"node {nid} {gid}: no rationale")
            if g.get("result") == "fail" and n.get("status") != "killed":
                warnings.append(f"node {nid}: {gid} failed but status is '{n.get('status')}' (redesign as a new node?)")
            if ev_ids is not None:
                for e in g.get("evidence") or []:
                    if e not in ev_ids:
                        errors.append(f"node {nid} {gid}: evidence id '{e}' not in evidence log")
                # single-source alone must not support a gate result
                evs = g.get("evidence") or []
                if g.get("result") in {"pass", "fail"} and evs and all(ev_by_id.get(e, {}).get("single_source") for e in evs):
                    warnings.append(f"node {nid} {gid}: decided on single-source evidence only")
        if n.get("status") in {"shortlisted", "recommended"}:
            unknown = [gid for gid, g in gates.items() if g.get("result") == "unknown"]
            missing = sorted(gate_ids - set(gates))
            if unknown:
                warnings.append(f"node {nid}: shortlisted with unknown gates {unknown}; add priority assumptions")
            if missing:
                warnings.append(f"node {nid}: shortlisted with gates not run {missing}")
        for cid, s in (n.get("scores") or {}).items():
            if cid not in criteria:
                errors.append(f"node {nid}: unknown criterion '{cid}' (see config/rubric.yaml)")
                continue
            check_score(f"node {nid} {cid}", s, criteria, ev_ids, errors, warnings)

    # Paths
    path_ids: set[str] = set()
    for p in ledger.get("paths") or []:
        pid = p.get("id", "?")
        if pid in path_ids:
            errors.append(f"path {pid}: duplicate id")
        path_ids.add(pid)
        seq = p.get("sequence") or []
        if not seq:
            errors.append(f"path {pid}: empty sequence")
        for nid in seq:
            if nid not in node_ids:
                errors.append(f"path {pid}: node '{nid}' not found")
        if "expansion_plausibility" in p:
            check_score(f"path {pid} expansion_plausibility", p["expansion_plausibility"], None, ev_ids, errors, warnings)
        elif len(seq) > 1:
            warnings.append(f"path {pid}: no expansion_plausibility score")

    # Assumptions
    for a in ledger.get("assumptions") or []:
        aid = a.get("id", "?")
        for k in ("impact", "uncertainty"):
            v = a.get(k)
            if not isinstance(v, int) or not 1 <= v <= 5:
                errors.append(f"assumption {aid}: {k} must be an integer 1-5")
        target = a.get("applies_to")
        if target and target not in node_ids | path_ids:
            warnings.append(f"assumption {aid}: applies_to '{target}' not found")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s). "
          f"{len(nodes)} nodes, {len(path_ids)} paths, {len(ledger.get('assumptions') or [])} assumptions.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
