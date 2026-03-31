from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from toolsmith.spec import ToolSpec, tool_dir_from_spec_path


def python_pack_root(tool_dir: Path) -> Path:
    return tool_dir / "python"


def python_pack_manifest_path(tool_dir: Path) -> Path:
    return python_pack_root(tool_dir) / "manifest.json"


def _python_pack_profile(spec: ToolSpec) -> Dict[str, Any]:
    python_spec = spec.python
    return {
        "toolSlug": spec.slug,
        "toolName": spec.name,
        "packageMode": python_spec.get("package_mode", "none"),
        "dependencies": list(python_spec.get("dependencies", []) or []),
        "localPackages": list(python_spec.get("local_packages", []) or []),
        "entryModule": python_spec.get("entry_module", ""),
        "bootstrapScript": python_spec.get("bootstrap_script", "build.ps1"),
        "requiresNetwork": bool(python_spec.get("requires_network", False)),
    }


def ensure_python_packaging_layout(spec: ToolSpec) -> Path:
    tool_dir = tool_dir_from_spec_path(spec.path)
    root = python_pack_root(tool_dir)
    src = root / "src"
    vendor = root / "vendor"
    docs = root / "README.md"
    requirements_in = root / "requirements.in"
    requirements_txt = root / "requirements.txt"
    build_script = root / "build.ps1"

    for path in [root, src, vendor]:
        path.mkdir(parents=True, exist_ok=True)

    profile = _python_pack_profile(spec)
    python_pack_manifest_path(tool_dir).write_text(
        json.dumps(profile, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    if not requirements_in.exists():
        requirements_in.write_text(
            "\n".join(profile["dependencies"]) + ("\n" if profile["dependencies"] else ""),
            encoding="utf-8",
        )
    if not requirements_txt.exists():
        requirements_txt.write_text(
            "# Lockfile generated from requirements.in\n", encoding="utf-8"
        )
    if not docs.exists():
        docs.write_text(
            "# Python packaging workspace\n\n"
            "This folder holds external Python packaging inputs for the Alteryx tool.\n\n"
            "Recommended modes:\n"
            "- `requirements`: declare dependencies in `requirements.in` and lock them before packaging.\n"
            "- `vendored-wheelhouse`: download wheels into `vendor/` during build and package them with the tool.\n"
            "- `editable-local`: point the tool at local source packages for development only.\n",
            encoding="utf-8",
        )
    if not build_script.exists():
        build_script.write_text(
            "param()\n"
            "Write-Host 'Implement python packaging build steps here.'\n",
            encoding="utf-8",
        )

    return root
