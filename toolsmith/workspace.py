from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4

from packaging.version import Version

from toolsmith.compat import Compat, resolve
from toolsmith.spec import ToolSpec, dist_dir, tool_dir_from_spec_path, workspace_dir

IGNORED_WORKSPACE_PARTS = {
    "build",
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    "node_modules",
    ".ayx_cli.cache",
}


def _run(cmd: list[str], cwd: Path) -> None:
    p = subprocess.run(cmd, cwd=str(cwd), shell=False)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed ({p.returncode}): {' '.join(cmd)} (cwd={cwd})")


def _run_with_fallback(candidates: list[list[str]], cwd: Path) -> None:
    errors: list[str] = []
    for cmd in candidates:
        p = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, shell=False)
        if p.returncode == 0:
            return
        errors.append(
            f"Command failed ({p.returncode}): {' '.join(cmd)} (cwd={cwd})\n{p.stdout}\n{p.stderr}"
        )
    raise RuntimeError("\n---\n".join(errors))


def _capture(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {' '.join(cmd)}\n{p.stdout}\n{p.stderr}"
        )
    return p.stdout.strip()


def enforce_dev_runtime(compat: Compat) -> None:
    # Python enforcement: >= min_dev_python, major/minor must be 3.10 for this target.
    import sys

    py = Version(".".join(map(str, sys.version_info[:3])))
    if py < Version(compat.min_dev_python):
        raise RuntimeError(
            f"Python {py} is too old for {compat.alteryx_version}. "
            f"Need >= {compat.min_dev_python}."
        )
    if (sys.version_info.major, sys.version_info.minor) != (3, 10):
        raise RuntimeError(
            f"Python {py} does not match expected major/minor for {compat.alteryx_version}: 3.10.x"
        )

    # Node enforcement (best-effort; only if node exists)
    try:
        node_v = _capture(["node", "--version"]).lstrip("v")
        if not node_v.startswith(compat.node_version.split(".", 2)[0] + "."):
            raise RuntimeError(
                f"Node {node_v} does not match expected major for {compat.alteryx_version}: "
                f"{compat.node_version}"
            )
    except FileNotFoundError:
        # If you have no UI builds, you might be OK, but we keep this strict for reproducibility.
        raise RuntimeError("node is not installed or not on PATH; required for reproducible builds.")


def lock_path(tool_dir: Path) -> Path:
    return tool_dir / "toolsmith.lock.json"


def compute_lock(spec: ToolSpec, compat: Compat) -> Dict[str, Any]:
    return {
        "schema_version": 1,
        "tool": {
            "name": spec.name,
            "slug": spec.slug,
            "version": spec.version,
            "package_name": spec.package_name,
            "category": spec.category,
            "tool_type": spec.tool_type,
            "alteryx_version": spec.alteryx_version,
        },
        "compat": {
            "embedded_python": compat.embedded_python,
            "min_dev_python": compat.min_dev_python,
            "recommended_dev_python": compat.recommended_dev_python,
            "node_version": compat.node_version,
            "ayx_python_sdk": compat.ayx_python_sdk,
            "ayx_plugin_cli": compat.ayx_plugin_cli,
        },
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def write_lock(spec: ToolSpec, check: bool = False) -> None:
    tool_dir = tool_dir_from_spec_path(spec.path)
    compat = resolve(spec.alteryx_version)

    expected = compute_lock(spec, compat)
    lp = lock_path(tool_dir)

    if check:
        if not lp.exists():
            raise RuntimeError(f"Missing lock file: {lp}")
        current = json.loads(lp.read_text(encoding="utf-8"))
        # Ignore timestamp drift when checking
        current["generated_at_utc"] = expected["generated_at_utc"]
        if current != expected:
            raise RuntimeError(
                f"Lock is out of date: {lp}\nRun: toolsmith lock {spec.path}"
            )
        return

    lp.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _is_ignored_workspace_path(path: Path) -> bool:
    return any(part in IGNORED_WORKSPACE_PARTS for part in path.parts)


def _workspace_file_map(root: Path) -> Dict[str, bytes]:
    result: Dict[str, bytes] = {}
    if not root.exists():
        return result
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        if _is_ignored_workspace_path(rel):
            continue
        result[str(rel).replace("\\", "/")] = p.read_bytes()
    return result


def _workspace_diffs(expected: Path, actual: Path) -> list[str]:
    expected_map = _workspace_file_map(expected)
    actual_map = _workspace_file_map(actual)
    diffs: list[str] = []

    expected_paths = set(expected_map)
    actual_paths = set(actual_map)

    for path in sorted(expected_paths - actual_paths):
        diffs.append(f"missing: {path}")
    for path in sorted(actual_paths - expected_paths):
        diffs.append(f"unexpected: {path}")
    for path in sorted(expected_paths & actual_paths):
        if expected_map[path] != actual_map[path]:
            diffs.append(f"changed: {path}")
    return diffs


def _on_rm_error(func: Any, path: str, exc_info: Any) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def _remove_tree(path: Path) -> None:
    if not path.exists():
        return
    shutil.rmtree(path, onerror=_on_rm_error)


def _swap_workspace(tool_dir: Path, generated_ws: Path, current_ws: Path) -> None:
    staged_ws = tool_dir / f".workspace.staged.{uuid4().hex}"
    backup_ws = tool_dir / f".workspace.backup.{uuid4().hex}"
    shutil.copytree(generated_ws, staged_ws)

    if current_ws.exists():
        os.replace(current_ws, backup_ws)
    os.replace(staged_ws, current_ws)

    # Best-effort cleanup of previous workspace snapshot.
    if backup_ws.exists():
        try:
            _remove_tree(backup_ws)
        except Exception:
            pass


def scaffold_workspace(spec: ToolSpec, workspace_root: Path | None = None) -> None:
    tool_dir = tool_dir_from_spec_path(spec.path)
    ws_dir = workspace_root or workspace_dir(tool_dir)
    compat = resolve(spec.alteryx_version)

    enforce_dev_runtime(compat)

    ws_dir.mkdir(parents=True, exist_ok=True)

    # Non-interactive init using documented parameters (package-name + backend-language are required).
    # If you omit args, CLI waits for stdin.
    cmd_init = [
        "ayx_plugin_cli",
        "sdk-workspace-init",
        "--package-name",
        spec.package_name,
        "--backend-language",
        "python",
        "--tool-category",
        spec.category,
    ]
    if spec.description:
        cmd_init.extend(["--description", spec.description])
    if spec.author:
        cmd_init.extend(["--author", spec.author])
    if spec.company:
        cmd_init.extend(["--company", spec.company])
    _run(cmd_init, cwd=ws_dir)

    writes_output = spec.tool_type in {"output", "multiple-outputs"}
    writes_output_flag = "--writes-output-data" if writes_output else "--no-writes-output-data"
    omit_ui_flag = "--omit-ui" if spec.omit_ui else "--no-omit-ui"

    base_create_tool = [
        "ayx_plugin_cli",
        "create-ayx-plugin",
        "--tool-name",
        spec.name,
        "--tool-type",
        spec.tool_type,
        writes_output_flag,
        "--description",
        spec.description or "",
        "--dcm-namespace",
        spec.package_name,
        omit_ui_flag,
    ]
    # ayx_plugin_cli uses --tool-version in newer versions; some older docs use --version.
    _run_with_fallback(
        [
            [*base_create_tool, "--tool-version", spec.version],
            [*base_create_tool, "--version", spec.version],
        ],
        cwd=ws_dir,
    )

    # Ensure config/manifests regenerated
    _run(["ayx_plugin_cli", "generate-config-files"], cwd=ws_dir)

    # Patch workspace json for python_version if present
    ws_json = ws_dir / "ayx_workspace.json"
    if ws_json.exists():
        data = json.loads(ws_json.read_text(encoding="utf-8"))
        bls = data.get("backend_language_settings")
        if isinstance(bls, dict):
            bls["python_version"] = "3.10"
        ws_json.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def reconcile_workspace(spec: ToolSpec, check: bool = False) -> None:
    tool_dir = tool_dir_from_spec_path(spec.path)
    current_ws = workspace_dir(tool_dir)

    if check and not current_ws.exists():
        raise RuntimeError(
            f"Missing workspace for {spec.slug}: {current_ws}\nRun: toolsmith reconcile {spec.path}"
        )

    with tempfile.TemporaryDirectory(prefix=f"toolsmith-{spec.slug}-") as tmp:
        generated_ws = Path(tmp) / "workspace"
        scaffold_workspace(spec, workspace_root=generated_ws)
        diffs = _workspace_diffs(generated_ws, current_ws)

        if check:
            if diffs:
                preview = "\n".join(f" - {d}" for d in diffs[:25])
                extra = "" if len(diffs) <= 25 else f"\n ... and {len(diffs) - 25} more"
                raise RuntimeError(
                    f"Workspace drift detected for {spec.slug}: {current_ws}\n"
                    f"{preview}{extra}\n"
                    f"Run: toolsmith reconcile {spec.path}"
                )
            return

        _swap_workspace(tool_dir, generated_ws, current_ws)


def build_yxi(spec: ToolSpec) -> Path:
    tool_dir = tool_dir_from_spec_path(spec.path)
    ws_dir = workspace_dir(tool_dir)

    if not (ws_dir / "ayx_workspace.json").exists():
        raise RuntimeError(
            f"No workspace found for {spec.slug}. Run: toolsmith scaffold {spec.path}"
        )

    _run(["ayx_plugin_cli", "create-yxi"], cwd=ws_dir)

    yxi_dir = ws_dir / "build" / "yxi"
    if not yxi_dir.exists():
        raise RuntimeError(f"Expected build output not found: {yxi_dir}")

    candidates = sorted(yxi_dir.glob("*.yxi"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise RuntimeError(f"No .yxi produced under: {yxi_dir}")

    out_dir = dist_dir(tool_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{spec.package_name}-{spec.version}.yxi"
    shutil.copy2(candidates[0], out_path)
    return out_path
