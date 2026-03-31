from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from toolsmith import validation


def test_verify_ayx_plugin_cli_runnable(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd, capture_output=None, text=None, shell=None):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(validation.subprocess, "run", fake_run)

    validation.verify_ayx_plugin_cli_runnable("ayx_plugin_cli.exe")

    assert calls == [["ayx_plugin_cli.exe", "--help"]]


def test_verify_ayx_plugin_cli_runnable_fails(monkeypatch):
    def fake_run(cmd, capture_output=None, text=None, shell=None):
        return SimpleNamespace(returncode=1, stdout="", stderr="boom")

    monkeypatch.setattr(validation.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="working CLI"):
        validation.verify_ayx_plugin_cli_runnable("ayx_plugin_cli.exe")


def test_generate_validation_contract_writes_minimal_workflow(tmp_path):
    tool_dir = tmp_path / "tool"
    tool_dir.mkdir()
    (tool_dir / "tool.yaml").write_text(
        "\n".join(
            [
                "apiVersion: toolsmith.alteryx/v1",
                "kind: AyxTool",
                "metadata:",
                "  name: Sample",
                "  slug: sample",
                "spec:",
                "  alteryx_version: '2025.2'",
                "  tool_type: 'single-input-single-output'",
                "  version: '0.1.0'",
                "  category: 'Developer'",
                "  package_name: 'sample'",
            ]
        ),
        encoding="utf-8",
    )

    contract_path = validation.generate_validation_contract(tool_dir)
    workflow = tool_dir / "validation" / "workflow" / "sample.validation.yxmd"

    assert contract_path.exists()
    assert workflow.exists()
    assert "<Nodes>" in workflow.read_text(encoding="utf-8")
    assert "<Connections>" in workflow.read_text(encoding="utf-8")


def test_run_designer_install_smoke_test(monkeypatch, tmp_path):
    installed = tmp_path / "DataObfuscator_0_1_0"
    installed.mkdir()
    (installed / "main.pyz").write_text("placeholder", encoding="utf-8")

    def fake_run(cmd, capture_output=None, text=None, shell=None):
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(validation.subprocess, "run", fake_run)

    result = validation.run_designer_install_smoke_test(installed)

    assert result["status"] == "passed"
    assert result["command"][1].endswith("main.pyz")


def test_smoke_test_installed_tool_cli(monkeypatch, capsys, tmp_path):
    installed = tmp_path / "DataObfuscator_0_1_0"
    installed.mkdir()
    (installed / "main.pyz").write_text("placeholder", encoding="utf-8")

    monkeypatch.setattr(validation, "run_designer_install_smoke_test", lambda path: {
        "command": ["python", str(path / "main.pyz"), "--help"],
        "returnCode": 0,
        "stdout": "ok",
        "stderr": "",
        "status": "passed",
    })

    from toolsmith.cli import cmd_smoke_test_installed_tool

    cmd_smoke_test_installed_tool(SimpleNamespace(installed_tool_dir=str(installed)))
    out = capsys.readouterr().out
    assert '"status": "passed"' in out


def test_run_post_install_validation_skips_when_missing(monkeypatch, tmp_path):
    tool_dir = tmp_path / "tool"
    tool_dir.mkdir()
    (tool_dir / "tool.yaml").write_text(
        "\n".join(
            [
                "apiVersion: toolsmith.alteryx/v1",
                "kind: AyxTool",
                "metadata:",
                "  name: Sample Tool",
                "  slug: sample_tool",
                "spec:",
                "  alteryx_version: '2025.2'",
                "  tool_type: 'single-input-single-output'",
                "  version: '0.1.0'",
                "  category: 'Developer'",
                "  package_name: 'sample_tool'",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(validation.Path, "home", lambda: tmp_path)

    result = validation.run_post_install_validation(tool_dir)

    assert result["status"] == "skipped"
    assert "Installed tool directory not found" in result["reason"]
