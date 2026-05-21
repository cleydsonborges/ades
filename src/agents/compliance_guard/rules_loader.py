"""Load and validate YAML rule packs for Compliance Guard."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

RULES_ROOT = Path(__file__).resolve().parent / "rules"


def default_rule_pack_paths() -> list[str]:
    """Built-in HIPAA, SOX, and FISMA sample packs."""
    return [
        str(RULES_ROOT / "hipaa"),
        str(RULES_ROOT / "sox"),
        str(RULES_ROOT / "fisma"),
    ]


def load_rules(rule_pack_paths: list[str] | None = None) -> list[dict[str, Any]]:
    paths = rule_pack_paths or default_rule_pack_paths()
    rules: list[dict[str, Any]] = []
    for pack_path in paths:
        root = Path(pack_path)
        if not root.is_dir():
            continue
        for yaml_file in sorted(root.glob("*.yaml")):
            with yaml_file.open(encoding="utf-8") as f:
                doc = yaml.safe_load(f)
            if doc:
                doc["_source"] = str(yaml_file)
                rules.append(doc)
    return rules


def validate_rule_schema(rule: dict[str, Any]) -> list[str]:
    """Return validation errors for a single rule document."""
    errors: list[str] = []
    for field in ("id", "pack", "severity", "check"):
        if field not in rule:
            errors.append(f"missing required field: {field}")
    check = rule.get("check")
    if isinstance(check, dict) and "type" not in check:
        errors.append("check.type is required")
    return errors
