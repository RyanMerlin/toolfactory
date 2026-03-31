from __future__ import annotations

from types import SimpleNamespace

import pytest

from toolsmith import workspace


def test_verify_ayx_plugin_cli_accepts_runnable_command(monkeypatch):
    calls: list[list[str]] = []

    def fake_run(cmd, cwd=None, capture_output=None, text=None, shell=None, env=None):
        calls.append(cmd)
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(workspace.subprocess, "run", fake_run)

    workspace._verify_ayx_plugin_cli("ayx_plugin_cli.exe")

    assert calls == [["ayx_plugin_cli.exe", "--help"]]


def test_verify_ayx_plugin_cli_rejects_broken_command(monkeypatch):
    def fake_run(cmd, cwd=None, capture_output=None, text=None, shell=None, env=None):
        return SimpleNamespace(returncode=1, stdout="", stderr="boom")

    monkeypatch.setattr(workspace.subprocess, "run", fake_run)

    with pytest.raises(RuntimeError, match="manual workspace fabrication is forbidden"):
        workspace._verify_ayx_plugin_cli("ayx_plugin_cli.exe")


def test_build_yxi_sets_node_open_ssl_legacy_provider(monkeypatch, tmp_path):
    captured_env = {}

    def fake_run(cmd, cwd=None, capture_output=None, text=None, shell=None, env=None):
        captured_env["env"] = env
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(workspace, "resolve_ayx_plugin_cli", lambda: "ayx_plugin_cli.exe")
    monkeypatch.setattr(workspace, "_run", fake_run)
    monkeypatch.setattr(workspace, "workspace_dir", lambda tool_dir: tmp_path)
    (tmp_path / "ayx_workspace.json").write_text("{}", encoding="utf-8")
    (tmp_path / "build" / "yxi").mkdir(parents=True, exist_ok=True)
    (tmp_path / "build" / "yxi" / "data_obfuscator.yxi").write_bytes(b"yxi")
    monkeypatch.setattr(workspace, "dist_dir", lambda tool_dir: tmp_path / "dist")

    spec = SimpleNamespace(
        path=tmp_path / "tool.yaml",
        slug="data_obfuscator",
        package_name="data_obfuscator",
        version="0.1.0",
    )
    monkeypatch.setattr(workspace, "tool_dir_from_spec_path", lambda path: tmp_path)

    out = workspace.build_yxi(spec)

    assert out.name == "data_obfuscator-0.1.0.yxi"
    assert captured_env["env"]["NODE_OPTIONS"] == "--openssl-legacy-provider"
