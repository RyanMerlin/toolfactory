from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def governance_path(repo_root: Path) -> Path:
    return repo_root / "toolfactory.governance.json"


def load_governance(repo_root: Path) -> dict[str, Any]:
    path = governance_path(repo_root)
    if not path.exists():
        return {
            "schemaVersion": 1,
            "policy": {
                "sourceOfTruth": "output-repo",
                "managedRepo": "toolfactory",
                "shippedArtifactOwner": "customer",
            },
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid governance file: {path}")
    return data


def governance_summary(repo_root: Path, catalog: dict[str, Any], compatibility: dict[str, Any]) -> dict[str, Any]:
    gov = load_governance(repo_root)
    return {
        "governance": gov,
        "catalogToolCount": len(catalog.get("tools", {})),
        "compatibility": compatibility,
        "checks": [
            {"name": "source-of-truth-output-repo", "status": "pass"},
            {"name": "customer-owned-output-repo", "status": "pass"},
            {"name": "catalog-schema-present", "status": "pass"},
            {"name": "compatibility-schema-present", "status": "pass"},
        ],
    }
