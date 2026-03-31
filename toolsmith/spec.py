from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class ToolSpec:
    path: Path
    raw: Dict[str, Any]

    @property
    def name(self) -> str:
        return self.raw["metadata"]["name"]

    @property
    def slug(self) -> str:
        return self.raw["metadata"]["slug"]

    @property
    def alteryx_version(self) -> str:
        return self.raw["spec"]["alteryx_version"]

    @property
    def tool_type(self) -> str:
        return self.raw["spec"]["tool_type"]

    @property
    def version(self) -> str:
        return self.raw["spec"]["version"]

    @property
    def category(self) -> str:
        return self.raw["spec"]["category"]

    @property
    def description(self) -> str:
        return self.raw["spec"].get("description", "")

    @property
    def author(self) -> str:
        return self.raw["spec"].get("author", "")

    @property
    def company(self) -> str:
        return self.raw["spec"].get("company", "")

    @property
    def package_name(self) -> str:
        return self.raw["spec"].get("package_name") or self.slug

    @property
    def omit_ui(self) -> bool:
        return bool(self.raw["spec"].get("omit_ui", False))

    @property
    def python(self) -> Dict[str, Any]:
        value = self.raw["spec"].get("python", {})
        return value if isinstance(value, dict) else {}


def load_schema(schema_path: Path) -> Dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def load_spec(spec_path: Path) -> ToolSpec:
    raw = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Spec is not a YAML mapping: {spec_path}")
    return ToolSpec(path=spec_path, raw=raw)


def validate_spec(spec: ToolSpec, schema: Dict[str, Any]) -> None:
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(spec.raw), key=lambda e: e.path)
    if errors:
        msg_lines = [f"Spec validation failed: {spec.path}"]
        for e in errors:
            loc = ".".join([str(x) for x in e.path]) or "<root>"
            msg_lines.append(f" - {loc}: {e.message}")
        raise ValueError("\n".join(msg_lines))


def find_tool_specs(tools_root: Path) -> list[Path]:
    if not tools_root.exists():
        return []
    return sorted(tools_root.glob("*/tool.yaml"))


def tool_dir_from_spec_path(spec_path: Path) -> Path:
    return spec_path.parent


def workspace_dir(tool_dir: Path) -> Path:
    return tool_dir / "workspace"


def dist_dir(tool_dir: Path) -> Path:
    return tool_dir / "dist"
