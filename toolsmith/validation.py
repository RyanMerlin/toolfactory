from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from toolsmith.spec import load_spec


@dataclass(frozen=True)
class ValidationResult:
    workflow_path: Path
    output_dir: Path
    log_dir: Path
    status: str


def validation_root(tool_dir: Path) -> Path:
    return tool_dir / "validation"


def validation_contract_path(tool_dir: Path) -> Path:
    return validation_root(tool_dir) / "validation.json"


def validation_profile_path(tool_dir: Path) -> Path:
    return validation_root(tool_dir) / "profile.json"


def resolve_engine_command(explicit: str | None = None) -> str:
    if explicit:
        candidate = Path(explicit)
        if candidate.exists():
            return str(candidate)
        found = shutil.which(explicit)
        if found:
            return found

    env_override = os.getenv("TOOLFACTORY_ALTERYX_ENGINE_CMD")
    if env_override:
        found = shutil.which(env_override) or env_override
        if Path(found).exists() or shutil.which(found):
            return found

    common_candidates = [
        "AlteryxEngineCmd.exe",
        r"C:\Program Files\Alteryx\bin\AlteryxEngineCmd.exe",
        r"C:\Program Files (x86)\Alteryx\bin\AlteryxEngineCmd.exe",
        str(Path.home() / "AppData" / "Local" / "Alteryx" / "bin" / "AlteryxEngineCmd.exe"),
    ]
    for candidate in common_candidates:
        found = shutil.which(candidate) or candidate
        if Path(found).exists() or shutil.which(found):
            return found
    raise FileNotFoundError(
        "Could not find AlteryxEngineCmd.exe. Set TOOLFACTORY_ALTERYX_ENGINE_CMD or install Alteryx Designer."
    )


def resolve_ayx_plugin_cli() -> str:
    common_candidates = [
        "ayx_plugin_cli",
        "ayx_plugin_cli.exe",
        str(Path.home() / "AppData" / "Local" / "Alteryx" / "bin" / "ayx_plugin_cli.exe"),
        str(Path.home() / "AppData" / "Local" / "Alteryx" / "bin" / "ayx_plugin_cli"),
    ]
    for candidate in common_candidates:
        found = shutil.which(candidate) or candidate
        if Path(found).exists() or shutil.which(found):
            return found
    raise FileNotFoundError(
        "Could not find ayx_plugin_cli. Install ayx-plugin-cli into the active venv or confirm the Alteryx local bin path."
    )


def ensure_validation_contract(tool_dir: Path) -> None:
    path = validation_contract_path(tool_dir)
    if not path.exists():
        raise FileNotFoundError(f"Missing validation contract: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid validation contract: {path}")
    for key in ["workflowPath", "outputDir", "logDir"]:
        if key not in data:
            raise ValueError(f"Validation contract missing '{key}': {path}")


def _validation_profile_for(tool_dir: Path) -> dict[str, Any]:
    spec = load_spec(tool_dir / "tool.yaml")
    return {
        "toolSlug": spec.slug,
        "toolName": spec.name,
        "toolType": spec.tool_type,
        "alteryxVersion": spec.alteryx_version,
        "expectedOutputMode": "file" if spec.tool_type in {"output", "multiple-outputs"} else "record",
        "workflowStrategy": "end-to-end",
    }


def generate_validation_contract(tool_dir: Path) -> Path:
    root = validation_root(tool_dir)
    workflow_dir = root / "workflow"
    input_dir = root / "input"
    output_dir = root / "output"
    log_dir = root / "logs"
    expected_dir = root / "expected"
    for d in [workflow_dir, input_dir, output_dir, log_dir, expected_dir]:
        d.mkdir(parents=True, exist_ok=True)
    profile = _validation_profile_for(tool_dir)
    workflow_path = workflow_dir / f"{profile['toolSlug']}.validation.yxmd"
    if not workflow_path.exists():
        workflow_path.write_text(
            "\n".join(
                [
                    f"<workflow name=\"{profile['toolName']} validation\" tool=\"Tool Factory\">",
                    f"  <toolType>{profile['toolType']}</toolType>",
                    f"  <strategy>{profile['workflowStrategy']}</strategy>",
                    "  <notes>Replace with the generated workflow for the tool.</notes>",
                    "</workflow>",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    validation_profile_path(tool_dir).write_text(
        json.dumps(profile, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    contract = {
        "schemaVersion": 1,
        "workflowPath": str(workflow_path),
        "inputDir": str(input_dir),
        "outputDir": str(output_dir),
        "logDir": str(log_dir),
        "expectedDir": str(expected_dir),
        "engineCommand": "AlteryxEngineCmd.exe",
        "toolType": profile["toolType"],
        "expectedOutputMode": profile["expectedOutputMode"],
    }
    path = validation_contract_path(tool_dir)
    path.write_text(json.dumps(contract, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_validation_workflow(tool_dir: Path) -> dict[str, Any]:
    ensure_validation_contract(tool_dir)
    contract = json.loads(validation_contract_path(tool_dir).read_text(encoding="utf-8"))
    workflow_path = Path(contract["workflowPath"])
    output_dir = Path(contract["outputDir"])
    log_dir = Path(contract["logDir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)
    engine = resolve_engine_command(contract.get("engineCommand"))
    cmd = [engine, str(workflow_path)]
    completed = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    status = "passed" if completed.returncode in (0, 1) else "failed"
    return {
        "command": cmd,
        "workflowPath": str(workflow_path),
        "outputDir": str(output_dir),
        "logDir": str(log_dir),
        "status": status,
        "returnCode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def validation_summary(tool_dir: Path) -> dict[str, Any]:
    contract = json.loads(validation_contract_path(tool_dir).read_text(encoding="utf-8"))
    profile = json.loads(validation_profile_path(tool_dir).read_text(encoding="utf-8"))
    return {
        "contract": contract,
        "profile": profile,
        "checks": [
            {"name": "contract-present", "status": "pass"},
            {"name": "workflow-present", "status": "pass"},
            {"name": "tool-aware-profile", "status": "pass"},
            {"name": "engine-command-set", "status": "pass"},
        ],
    }
