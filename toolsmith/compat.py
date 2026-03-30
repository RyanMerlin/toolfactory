from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Compat:
    alteryx_version: str
    embedded_python: str
    min_dev_python: str
    recommended_dev_python: str
    # Node is mainly relevant if you build UI assets; we still lock it for reproducibility.
    node_version: str
    ayx_python_sdk: str
    ayx_plugin_cli: str


# Single-target MVP: 2025.2
# Source: 25.1 release notes mention embedded Python upgraded to 3.10.18.
# 25.2 release notes mention conda removal + PEDs for v2 tools.
COMPAT_MATRIX: Dict[str, Compat] = {
    "2024.2": Compat(
        alteryx_version="2024.2",
        embedded_python="3.10.18",
        min_dev_python="3.10.13",
        recommended_dev_python="3.10.18",
        node_version="24.13.1",
        ayx_python_sdk="2.5.1",
        ayx_plugin_cli="1.3.1",
    ),
    "2025.2": Compat(
        alteryx_version="2025.2",
        embedded_python="3.10.18",
        min_dev_python="3.10.13",
        recommended_dev_python="3.10.18",
        # Alteryx docs historically said Node 14; some devs use Node 16 for fewer TS issues.
        # For 2025.2 MVP, we lock Node 16 LTS line.
        node_version="16.20.1",
        ayx_python_sdk="2.5.1",
        ayx_plugin_cli="1.3.1",
    )
}


def resolve(alteryx_version: str) -> Compat:
    if alteryx_version not in COMPAT_MATRIX:
        supported = ", ".join(sorted(COMPAT_MATRIX.keys()))
        raise ValueError(
            f"Unsupported alteryx_version '{alteryx_version}'. Supported: {supported}"
        )
    return COMPAT_MATRIX[alteryx_version]
