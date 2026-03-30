from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def default_catalog() -> dict[str, Any]:
    return {"schemaVersion": 1, "tools": {}}


def load_catalog(path: Path) -> dict[str, Any]:
    if not path.exists():
        return default_catalog()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid catalog: {path}")
    data.setdefault("schemaVersion", 1)
    data.setdefault("tools", {})
    return data


def save_catalog(path: Path, catalog: dict[str, Any]) -> Path:
    path.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def sync_catalog_from_output_repo(output_root: Path, repo_root: Path) -> dict[str, Any]:
    catalog = default_catalog()
    for child in output_root.iterdir():
        if not child.is_dir():
            continue
        if not (child / "ayx_workspace.json").exists():
            continue
        catalog["tools"][child.name] = {
            "sourceRepo": str(repo_root),
            "path": str(child),
            "packageName": child.name,
        }
    return catalog
