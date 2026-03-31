from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class HarnessPolicy:
    cli_required: bool
    cli_version: str
    validation_workflow_shape: str
    smoke_test_enabled: bool


def load_policy(_: Path | None = None) -> dict[str, Any]:
    return {
        "cliRequired": True,
        "cliVersion": "1.3.2",
        "validationWorkflowShape": "minimal-xml-skeleton",
        "smokeTestEnabled": True,
        "nonInteractiveScaffold": True,
        "nodeOpenSslLegacyProvider": True,
    }


def harness_policy(_: Path | None = None) -> HarnessPolicy:
    data = load_policy()
    return HarnessPolicy(
        cli_required=bool(data["cliRequired"]),
        cli_version=str(data["cliVersion"]),
        validation_workflow_shape=str(data["validationWorkflowShape"]),
        smoke_test_enabled=bool(data["smokeTestEnabled"]),
    )


def render_policy_summary(_: Path | None = None) -> dict[str, Any]:
    data = load_policy()
    return {
        "cli": {
            "required": data["cliRequired"],
            "version": data["cliVersion"],
            "startupProbe": ["--help", "version"],
        },
        "scaffold": {
            "nonInteractive": data["nonInteractiveScaffold"],
            "cliOnly": True,
        },
        "build": {
            "nodeOpenSslLegacyProvider": data["nodeOpenSslLegacyProvider"],
            "smokeTestEnabled": data["smokeTestEnabled"],
        },
        "validation": {
            "workflowShape": data["validationWorkflowShape"],
            "postInstallSmokeTest": data["smokeTestEnabled"],
        },
    }


def render_policy_text(_: Path | None = None) -> str:
    summary = render_policy_summary()
    return "\n".join(
        [
            "CLI required: yes",
            f"CLI version: {summary['cli']['version']}",
            "Scaffold: CLI-only, non-interactive",
            "Build: NODE_OPTIONS=--openssl-legacy-provider",
            "Validation: minimal XML workflow skeleton by default",
            "Post-install smoke test: enabled",
        ]
    )
