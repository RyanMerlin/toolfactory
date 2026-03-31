from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from toolsmith.spec import load_spec
from toolsmith.validation import validation_summary


def maintenance_report(tool_dir: Path) -> dict[str, Any]:
    spec = load_spec(tool_dir / "tool.yaml")
    report: dict[str, Any] = {
        "tool": {
            "name": spec.name,
            "slug": spec.slug,
            "version": spec.version,
            "alteryxVersion": spec.alteryx_version,
            "toolType": spec.tool_type,
            "packageName": spec.package_name,
        },
        "paths": {
            "toolDir": str(tool_dir),
            "workspace": str(tool_dir / "workspace"),
            "validation": str(tool_dir / "validation"),
            "python": str(tool_dir / "python"),
        },
        "checks": [],
    }
    ws = tool_dir / "workspace"
    if ws.exists():
        report["checks"].append({"name": "workspace-present", "status": "pass"})
    else:
        report["checks"].append({"name": "workspace-present", "status": "warn"})
    py = tool_dir / "python"
    if py.exists():
        report["checks"].append({"name": "python-packaging-present", "status": "pass"})
    else:
        report["checks"].append({"name": "python-packaging-present", "status": "warn"})
    val = tool_dir / "validation" / "validation.json"
    if val.exists():
        report["checks"].append({"name": "validation-contract-present", "status": "pass"})
        report["validation"] = validation_summary(tool_dir)
    else:
        report["checks"].append({"name": "validation-contract-present", "status": "warn"})
    return report
