from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONFIG_FILENAME = "toolfactory.config.json"
ENV_FILENAME = ".env"
ENV_EXAMPLE_FILENAME = ".env.example"
OUTPUT_REPO_ENV = "TOOLFACTORY_OUTPUT_REPO_PATH"


@dataclass(frozen=True)
class FactoryConfig:
    output_repo_path: Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def config_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / CONFIG_FILENAME


def env_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / ENV_FILENAME


def env_example_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / ENV_EXAMPLE_FILENAME


def default_config() -> dict[str, Any]:
    return {
        "outputRepoPath": str(Path.home() / ".ayx-tools"),
    }


def _parse_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key:
            data[key] = value
    return data


def load_config(root: Path | None = None) -> FactoryConfig:
    root = root or repo_root()
    path = config_path(root)
    data: dict[str, Any] = default_config()
    env_file_data = _parse_env_file(env_path(root))
    if OUTPUT_REPO_ENV in env_file_data:
        data["outputRepoPath"] = env_file_data[OUTPUT_REPO_ENV]
    if path.exists():
        loaded = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError(f"Invalid config file: {path}")
        data.update(loaded)

    env_output = os.getenv(OUTPUT_REPO_ENV)
    if env_output:
        data["outputRepoPath"] = env_output

    output_repo_path = Path(str(data["outputRepoPath"])).expanduser()
    if not output_repo_path.is_absolute():
        output_repo_path = (root / output_repo_path).resolve()
    return FactoryConfig(output_repo_path=output_repo_path)


def write_config(root: Path | None = None, output_repo_path: str | None = None) -> Path:
    root = root or repo_root()
    path = config_path(root)
    data = default_config()
    if output_repo_path:
        data["outputRepoPath"] = output_repo_path
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def write_env_file(root: Path | None = None, output_repo_path: str | None = None) -> Path:
    root = root or repo_root()
    path = env_path(root)
    value = output_repo_path or default_config()["outputRepoPath"]
    path.write_text(
        "# Local Tool Factory settings\n"
        f"{OUTPUT_REPO_ENV}={value}\n",
        encoding="utf-8",
    )
    return path


def write_env_example(root: Path | None = None) -> Path:
    root = root or repo_root()
    path = env_example_path(root)
    path.write_text(
        "# Example Tool Factory environment file\n"
        f"{OUTPUT_REPO_ENV}=C:\\\\Users\\\\<you>\\\\.ayx-tools\n",
        encoding="utf-8",
    )
    return path


def recommended_venv_commands() -> dict[str, str]:
    return {
        "create": "uv venv --python 3.10.18 .venv",
        "activate": r".\.venv\Scripts\activate",
        "install": "uv pip install -e .",
    }


def ensure_output_repo_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Output repo path does not exist: {resolved}")
    if not (resolved / ".git").exists():
        raise ValueError(f"Output repo path is not a git repo root: {resolved}")
    return resolved
