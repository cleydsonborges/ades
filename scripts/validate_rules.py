#!/usr/bin/env python3
"""Validate all YAML rule packs under compliance_guard/rules/."""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root without install
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.agents.compliance_guard.rules_loader import (  # noqa: E402
    default_rule_pack_paths,
    load_rules,
    validate_rule_schema,
)


def main() -> int:
    errors: list[str] = []
    rules = load_rules(default_rule_pack_paths())
    if not rules:
        print("ERROR: no rules loaded", file=sys.stderr)
        return 1
    for rule in rules:
        errs = validate_rule_schema(rule)
        for e in errs:
            errors.append(f"{rule.get('id', '?')}: {e}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"OK: validated {len(rules)} rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
