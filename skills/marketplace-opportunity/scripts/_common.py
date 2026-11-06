"""Shared helpers for the framework scripts. Requires PyYAML for .yaml files."""
from __future__ import annotations

import datetime
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = SKILL_DIR / "config"


def _stringify_dates(obj):
    """YAML parses unquoted dates into date objects; the schemas expect ISO strings."""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _stringify_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_stringify_dates(v) for v in obj]
    return obj


def load(path: str | Path) -> dict:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise SystemExit("PyYAML is required for YAML files: pip install pyyaml") from exc
    return _stringify_dates(yaml.safe_load(text) or {})


def load_config(config_dir: str | Path | None = None) -> tuple[dict, dict, dict]:
    d = Path(config_dir) if config_dir else CONFIG_DIR
    return load(d / "rubric.yaml"), load(d / "weights.yaml"), load(d / "gates.yaml")


def level_rank(level: str) -> int:
    """L0 -> 0 ... L4 -> 4. Lower is broader."""
    try:
        return int(str(level).lstrip("L"))
    except ValueError:
        return 99
