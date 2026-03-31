from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

from toolsmith.config import ensure_not_harness_repo_target, ensure_output_repo_path, load_config


def intent_path(tool_dir: Path) -> Path:
    return tool_dir / "tool-intent.json"


def intent_root(repo_root: Path) -> Path:
    cfg = load_config(repo_root)
    output_root = ensure_output_repo_path(cfg.output_repo_path)
    intent_dir = output_root / "intents"
    return ensure_not_harness_repo_target(intent_dir, repo_root)


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return slug or "new_tool"


def generate_intent_payload(
    summary: str,
    *,
    name: str | None = None,
    slug: str | None = None,
    mode: str = "from-scratch",
    inputs: Iterable[str] | None = None,
    outputs: Iterable[str] | None = None,
    workflow_expectation: str | None = None,
    local_output_mode: str | None = None,
    source_code_kind: str = "none",
    source_code_path: str = "",
    maintenance_target: str = "",
    maintenance_goal: str = "",
) -> dict[str, Any]:
    resolved_name = name or summary.strip().splitlines()[0].strip()[:80] or "New Tool"
    resolved_slug = slug or _slugify(resolved_name)
    return {
        "apiVersion": "toolsmith.alteryx.intent/v1",
        "kind": "AyxToolIntent",
        "metadata": {
            "name": resolved_name,
            "slug": resolved_slug,
        },
        "intent": {
            "mode": mode,
            "summary": summary.strip(),
            "inputs": list(inputs or []),
            "outputs": list(outputs or []),
            "validation": {
                "workflowExpectation": workflow_expectation
                or "Build, run, and validate the generated workflow end to end.",
                "localOutputMode": local_output_mode or "workspace-local-files",
                "acceptanceNotes": [],
            },
            "sourceCode": {
                "kind": source_code_kind,
                "path": source_code_path,
                "notes": "",
            },
            "maintenance": {
                "targetToolSlug": maintenance_target,
                "updateGoal": maintenance_goal,
            },
        },
    }


def write_intent_file(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path
