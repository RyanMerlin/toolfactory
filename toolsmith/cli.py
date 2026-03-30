from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from toolsmith.bootstrap import doctor
from toolsmith.catalog import load_catalog, save_catalog, sync_catalog_from_output_repo
from toolsmith.compat import resolve
from toolsmith.config import ensure_output_repo_path, load_config, write_config
from toolsmith.governance import governance_summary
from toolsmith.spec import find_tool_specs, load_schema, load_spec, validate_spec
from toolsmith.validation import (
    ensure_validation_contract,
    generate_validation_contract,
    validation_summary,
    run_validation_workflow,
)
from toolsmith.workspace import build_yxi, reconcile_workspace, scaffold_workspace, write_lock


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _schema_path() -> Path:
    return _repo_root() / "schemas" / "tool-spec.schema.json"


def _catalog_path() -> Path:
    return _repo_root() / "toolfactory.catalog.json"


def _compat_path() -> Path:
    return _repo_root() / "toolfactory.compatibility.json"


def _governance_path() -> Path:
    return _repo_root() / "toolfactory.governance.json"


def cmd_validate(args: argparse.Namespace) -> None:
    schema = load_schema(_schema_path())
    spec = load_spec(Path(args.spec))
    validate_spec(spec, schema)
    resolve(spec.alteryx_version)
    ensure_validation_contract(spec.path.parent)
    generate_validation_contract(spec.path.parent)
    result = run_validation_workflow(spec.path.parent)
    if result["status"] != "passed":
        raise RuntimeError(
            f"Validation workflow failed for {spec.slug}: {result['returnCode']}\n"
            f"{result['stderr'] or result['stdout'] or ''}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


def cmd_validate_all(_: argparse.Namespace) -> None:
    schema = load_schema(_schema_path())
    tools = find_tool_specs(_repo_root() / "tools")
    if not tools:
        print("No tools found under ./tools/*/tool.yaml")
        return
    for p in tools:
        spec = load_spec(p)
        validate_spec(spec, schema)
        resolve(spec.alteryx_version)
        ensure_validation_contract(spec.path.parent)
        generate_validation_contract(spec.path.parent)
        print(f"OK: {spec.slug} ({spec.alteryx_version})")


def cmd_lock(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    write_lock(spec, check=args.check)
    if args.check:
        print(f"OK (lock up to date): {spec.slug}")
    else:
        print(f"Wrote lock: tools/{spec.slug}/toolsmith.lock.json")


def cmd_lock_all(args: argparse.Namespace) -> None:
    tools = find_tool_specs(_repo_root() / "tools")
    for p in tools:
        spec = load_spec(p)
        write_lock(spec, check=args.check)
        if args.check:
            print(f"OK (lock up to date): {spec.slug}")
        else:
            print(f"Wrote lock: {spec.slug}")


def cmd_scaffold(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    scaffold_workspace(spec)
    generate_validation_contract(spec.path.parent)
    print(f"Scaffolded workspace: tools/{spec.slug}/workspace")


def cmd_reconcile(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    reconcile_workspace(spec, check=args.check)
    generate_validation_contract(spec.path.parent)
    if args.check:
        print(f"OK (workspace up to date): {spec.slug}")
    else:
        print(f"Reconciled workspace: tools/{spec.slug}/workspace")


def cmd_reconcile_all(args: argparse.Namespace) -> None:
    tools = find_tool_specs(_repo_root() / "tools")
    for p in tools:
        spec = load_spec(p)
        reconcile_workspace(spec, check=args.check)
        generate_validation_contract(spec.path.parent)
        if args.check:
            print(f"OK (workspace up to date): {spec.slug}")
        else:
            print(f"Reconciled workspace: {spec.slug}")


def cmd_build(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    out = build_yxi(spec)
    print(f"Built: {out}")


def cmd_build_all(_: argparse.Namespace) -> None:
    tools = find_tool_specs(_repo_root() / "tools")
    for p in tools:
        spec = load_spec(p)
        out = build_yxi(spec)
        print(f"Built: {out}")


def cmd_config_show(_: argparse.Namespace) -> None:
    cfg = load_config(_repo_root())
    print(json.dumps({"outputRepoPath": str(cfg.output_repo_path)}, indent=2))


def cmd_config_set(args: argparse.Namespace) -> None:
    path = write_config(_repo_root(), args.output_repo_path)
    print(f"Wrote config: {path}")


def cmd_output_check(_: argparse.Namespace) -> None:
    cfg = load_config(_repo_root())
    resolved = ensure_output_repo_path(cfg.output_repo_path)
    print(f"OK: {resolved}")


def _output_catalog_path(output_root: Path) -> Path:
    return output_root / "toolfactory.catalog.json"


def cmd_output_catalog(_: argparse.Namespace) -> None:
    cfg = load_config(_repo_root())
    output_root = ensure_output_repo_path(cfg.output_repo_path)
    catalog = sync_catalog_from_output_repo(output_root, _repo_root())
    save_catalog(_catalog_path(), catalog)
    print(json.dumps(catalog, indent=2, sort_keys=True))


def cmd_export(args: argparse.Namespace) -> None:
    cfg = load_config(_repo_root())
    output_root = ensure_output_repo_path(cfg.output_repo_path)
    source_tool_dir = _repo_root() / "tools" / args.slug
    if not source_tool_dir.exists():
        raise FileNotFoundError(f"Source tool not found: {source_tool_dir}")
    target_tool_dir = output_root / "tools" / args.slug
    target_tool_dir.parent.mkdir(parents=True, exist_ok=True)
    if target_tool_dir.exists():
        shutil.rmtree(target_tool_dir)
    shutil.copytree(
        source_tool_dir,
        target_tool_dir,
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", ".ayx_cli.cache", "build"),
    )
    catalog = sync_catalog_from_output_repo(output_root, _repo_root())
    save_catalog(_catalog_path(), catalog)
    print(f"Exported: {target_tool_dir}")


def cmd_init_tool(args: argparse.Namespace) -> None:
    root = _repo_root()
    tool_dir = root / "tools" / args.slug
    if tool_dir.exists():
        raise FileExistsError(f"Tool already exists: {tool_dir}")
    template_dir = root / "templates" / "tool-skeleton"
    if not template_dir.exists():
        raise FileNotFoundError(f"Missing template directory: {template_dir}")
    shutil.copytree(template_dir, tool_dir)
    spec_path = tool_dir / "tool.yaml"
    spec_text = spec_path.read_text(encoding="utf-8")
    spec_text = spec_text.replace("Example Tool", args.name)
    spec_text = spec_text.replace("example_tool", args.slug)
    spec_text = spec_text.replace('"2025.2"', f'"{args.alteryx_version}"')
    if args.description:
        spec_text = spec_text.replace('"Describe the tool here."', f'"{args.description}"')
    spec_path.write_text(spec_text, encoding="utf-8")
    readme_path = tool_dir / "README.md"
    readme_path.write_text(
        readme_path.read_text(encoding="utf-8").replace("Example Tool", args.name),
        encoding="utf-8",
    )
    generate_validation_contract(tool_dir)
    print(f"Initialized tool: {tool_dir}")


def cmd_validate_workflow(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    result = run_validation_workflow(spec.path.parent)
    print(json.dumps(result, indent=2, sort_keys=True))


def cmd_validate_summary(args: argparse.Namespace) -> None:
    spec = load_spec(Path(args.spec))
    print(json.dumps(validation_summary(spec.path.parent), indent=2, sort_keys=True))


def cmd_doctor(_: argparse.Namespace) -> None:
    status = doctor(_repo_root())
    print(json.dumps(status, indent=2, sort_keys=True))
    if not status["outputRepoExists"] or not status["outputRepoIsGitRepo"] or status["factoryVenvVersion"] != "3.10.18":
        print(
            "\nSetup hint: run `uv venv --python 3.10.18 .venv`, then `uv pip install -e .`, then re-run `toolsmith doctor`.",
            file=sys.stderr,
        )


def cmd_governance(_: argparse.Namespace) -> None:
    cfg = load_config(_repo_root())
    output_root = ensure_output_repo_path(cfg.output_repo_path)
    catalog = sync_catalog_from_output_repo(output_root, _repo_root())
    compat = json.loads(_compat_path().read_text(encoding="utf-8"))
    summary = governance_summary(_repo_root(), catalog, compat)
    print(json.dumps(summary, indent=2, sort_keys=True))


def main() -> None:
    ap = argparse.ArgumentParser(prog="toolsmith")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("validate", help="Validate a single tool spec and validation contract")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("validate-all", help="Validate all tool specs under ./tools")
    p.set_defaults(func=cmd_validate_all)

    p = sub.add_parser("validate-workflow", help="Run a tool's validation workflow")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.set_defaults(func=cmd_validate_workflow)

    p = sub.add_parser("validate-summary", help="Show the validation contract and derived checks")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.set_defaults(func=cmd_validate_summary)

    p = sub.add_parser("lock", help="Write or check toolsmith.lock.json for a tool")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.add_argument("--check", action="store_true", help="Fail if lock is missing/outdated")
    p.set_defaults(func=cmd_lock)

    p = sub.add_parser("lock-all", help="Write or check lock files for all tools")
    p.add_argument("--check", action="store_true", help="Fail if any lock is missing/outdated")
    p.set_defaults(func=cmd_lock_all)

    p = sub.add_parser("scaffold", help="Create (or re-create) the ayx workspace via ayx_plugin_cli")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.set_defaults(func=cmd_scaffold)

    p = sub.add_parser(
        "reconcile",
        help="Re-generate workspace from spec; optionally fail if committed workspace drifts",
    )
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.add_argument("--check", action="store_true", help="Fail if workspace is missing or out of date")
    p.set_defaults(func=cmd_reconcile)

    p = sub.add_parser("reconcile-all", help="Reconcile all workspaces under ./tools")
    p.add_argument("--check", action="store_true", help="Fail if any workspace is missing or out of date")
    p.set_defaults(func=cmd_reconcile_all)

    p = sub.add_parser("build", help="Build a YXI for a tool")
    p.add_argument("spec", help="Path to tools/<slug>/tool.yaml")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("build-all", help="Build YXIs for all tools")
    p.set_defaults(func=cmd_build_all)

    p = sub.add_parser("config-show", help="Show the resolved Tool Factory config")
    p.set_defaults(func=cmd_config_show)

    p = sub.add_parser("config-set", help="Write the Tool Factory config file")
    p.add_argument("output_repo_path", help="Path to the generated output repo, e.g. C:\\code\\sdk-tools")
    p.set_defaults(func=cmd_config_set)

    p = sub.add_parser("output-check", help="Validate the configured output repo path")
    p.set_defaults(func=cmd_output_check)

    p = sub.add_parser("export", help="Copy a generated tool into the configured output repo")
    p.add_argument("slug", help="Tool slug under ./tools and in the output repo")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("output-catalog", help="Print the output repo tool catalog")
    p.set_defaults(func=cmd_output_catalog)

    p = sub.add_parser("init-tool", help="Create a new tool skeleton from the factory template")
    p.add_argument("slug", help="Tool slug, e.g. json_fixer")
    p.add_argument("--name", required=True, help="Human-readable tool name")
    p.add_argument("--alteryx-version", default="2025.2", help="Target Alteryx version")
    p.add_argument("--description", default="", help="Short tool description")
    p.set_defaults(func=cmd_init_tool)

    p = sub.add_parser("doctor", help="Check the repo bootstrap and active configuration")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("governance", help="Show governance and SSOT summary")
    p.set_defaults(func=cmd_governance)

    args = ap.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)
