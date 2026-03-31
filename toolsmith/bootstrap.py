from __future__ import annotations

import json
import os
import subprocess
import shutil
from pathlib import Path

from toolsmith.catalog import load_catalog
from toolsmith.compat import resolve
from toolsmith.config import ensure_not_harness_repo_target, load_config, recommended_venv_commands
from toolsmith.validation import resolve_ayx_plugin_cli, resolve_engine_command


def _venv_python_path(repo_root: Path) -> Path:
    return repo_root / ".venv" / "Scripts" / "python.exe"


def _python_version_from_exe(python_exe: Path) -> str | None:
    if not python_exe.exists():
        return None
    try:
        completed = subprocess.run(
            [str(python_exe), "--version"],
            capture_output=True,
            text=True,
            shell=False,
            check=False,
        )
    except Exception:
        return None
    output = (completed.stdout or completed.stderr or "").strip()
    if output.lower().startswith("python "):
        return output.split(" ", 1)[1].strip()
    return output or None


def doctor(repo_root: Path) -> dict[str, object]:
    cfg = load_config(repo_root)
    output_repo = cfg.output_repo_path
    python_path = shutil.which("python")
    node_path = shutil.which("node")
    try:
        ayx_plugin_cli_path = resolve_ayx_plugin_cli()
    except Exception:
        ayx_plugin_cli_path = None
    venv_python = _venv_python_path(repo_root)
    venv_python_version = _python_version_from_exe(venv_python)
    compat = resolve("2025.2")
    engine_path = None
    engine_error = None
    try:
        engine_path = resolve_engine_command(None)
    except Exception as exc:
        engine_error = str(exc)
    venv_ok = False
    venv_reason = None
    if venv_python_version:
        try:
            parts = [int(p) for p in venv_python_version.split(".")[:3]]
            vmaj, vmin, vpatch = (parts + [0, 0, 0])[:3]
            min_parts = [int(p) for p in compat.min_dev_python.split(".")[:3]]
            mmaj, mmin, mpatch = (min_parts + [0, 0, 0])[:3]
            venv_ok = (vmaj, vmin, vpatch) >= (mmaj, mmin, mpatch) and (vmaj, vmin) == (3, 10)
            if not venv_ok:
                venv_reason = f"Expected Python 3.10.x at or above {compat.min_dev_python}"
        except Exception:
            venv_reason = f"Unparseable Python version: {venv_python_version}"
    checks = [
        {"name": "repo-root", "status": "pass" if repo_root.exists() else "fail"},
        {"name": "output-repo-exists", "status": "pass" if output_repo.exists() else "fail"},
        {"name": "output-repo-git", "status": "pass" if (output_repo / ".git").exists() else "fail"},
        {"name": "python", "status": "pass" if python_path else "fail"},
        {"name": "factory-venv", "status": "pass" if venv_python.exists() else "fail"},
        {"name": "factory-venv-python", "status": "pass" if venv_ok else "fail"},
        {"name": "node", "status": "pass" if node_path else "fail"},
        {"name": "ayx-plugin-cli", "status": "pass" if ayx_plugin_cli_path else "fail"},
        {"name": "alteryx-engine", "status": "pass" if engine_path else "fail"},
        {"name": "config-file", "status": "pass" if (repo_root / "toolfactory.config.json").exists() else "fail"},
        {"name": "env-file", "status": "pass" if (repo_root / ".env").exists() else "warn"},
        {"name": "template-manifest", "status": "pass" if (repo_root / "toolfactory.template-manifest.json").exists() else "fail"},
        {"name": "compatibility-file", "status": "pass" if (repo_root / "toolfactory.compatibility.json").exists() else "fail"},
        {"name": "output-not-harness", "status": "pass"},
    ]
    harness_generated_outputs = False
    try:
        ensure_not_harness_repo_target(output_repo, repo_root)
    except Exception:
        harness_generated_outputs = True
        checks[-1] = {"name": "output-not-harness", "status": "fail"}
    status = {
        "repoRoot": str(repo_root),
        "outputRepoPath": str(output_repo),
        "outputRepoExists": output_repo.exists(),
        "outputRepoIsGitRepo": (output_repo / ".git").exists(),
        "python": python_path,
        "factoryVenv": str(venv_python),
        "factoryVenvVersion": venv_python_version,
        "factoryVenvCheck": venv_reason,
        "node": node_path,
        "ayxPluginCli": ayx_plugin_cli_path,
        "alteryxEngineCmd": engine_path,
        "alteryxEngineCmdError": engine_error,
        "toolfactoryConfig": str(repo_root / "toolfactory.config.json"),
        "envFile": str(repo_root / ".env"),
        "templateManifest": str(repo_root / "toolfactory.template-manifest.json"),
        "compatibility": str(repo_root / "toolfactory.compatibility.json"),
        "governance": str(repo_root / "toolfactory.governance.json"),
        "catalog": load_catalog(repo_root / "toolfactory.catalog.json"),
        "checks": checks,
        "recommendedSetup": {
            "createVenvCommand": recommended_venv_commands()["create"],
            "activateVenvCommand": recommended_venv_commands()["activate"],
            "installToolsmithCommand": recommended_venv_commands()["install"],
            "installAyxPluginCliCommand": recommended_venv_commands()["installAyxPluginCli"],
            "minimumPython": compat.min_dev_python,
        },
        "harnessGeneratedOutputs": harness_generated_outputs,
    }
    return status
