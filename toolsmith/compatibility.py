from __future__ import annotations

from pathlib import Path


def compatibility_path(repo_root: Path) -> Path:
    return repo_root / "toolfactory.compatibility.json"


def default_compatibility() -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "alteryx": {
            "platformSdk": "current",
            "tooling": {
                "python": "3.10",
                "node": "16.20.1",
            },
        },
    }
