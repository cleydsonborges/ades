# Custom rule packs

Organization-specific Policy-as-Code definitions (YAML). Load via:

```python
ComplianceGuardAgent(rule_pack_paths=["/path/to/custom", ...])
```

See `hipaa/`, `sox/`, and `fisma/` for schema examples.
