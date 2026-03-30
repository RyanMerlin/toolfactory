# Tool Factory Checkpoint

Date: 2026-03-30

## Current State

- `C:\code\toolfactory` is now a git repository.
- `C:\code\sdk-tools` is the output repo and already contains the `jsonify` tool.
- Tool Factory has a repo-local Codex plugin manifest, repo-scoped skills, an `AGENTS.md`, and a template-driven `toolsmith` CLI.
- The harness now supports:
  - `toolsmith init-tool`
  - `toolsmith validate`
  - `toolsmith reconcile`
  - `toolsmith build`
  - `toolsmith export`
  - `toolsmith output-catalog`
- Output repo configuration is supported via:
  - `.env`
  - `toolfactory.config.json`
  - `TOOLFACTORY_OUTPUT_REPO_PATH`

## Validation Direction

The validation workflow must be part of the factory:

- generate a simple local validation workflow for each tool,
- write outputs locally,
- run it via `AlteryxEngineCmd.exe`,
- treat `0` as success, `1` as warning, and `2` as failure,
- use that validation step as part of the scaffold/build/export gate.

## What Is Still Open

- Final shape of the generated validation workflow template.
- Exact local output folder convention for validation artifacts.

## Production Readiness Goals

- Make it easy for a new executive to start Codex and quickly reach a working, validated workflow.
- Keep the system deterministic and template-driven.
- Make the harness easy to share, clone, and extend.
- Keep the output repo separate from the harness repo.

## Decisions Confirmed

- Validation should be end to end and use a real workflow that exercises the tool.
- Validation outputs should live inside each tool workspace.
- Git should track version history for a single workflow implementation.
- Different workflow designs or specs should live in different folders.
- The first user entrypoint should be Codex-native.
- The first production slice should include scaffold, validate, and package.
- The first release should enforce all major checks: CI, docs, catalog, drift detection, and validation smoke tests.
- The harness repo is the only repo we actively manage here; the output repo remains customer-owned and acts as the SSOT for distributed tools, audit, governance, and vulnerability checks.

## Agent Notes

This checkpoint is historical context only.

For active use, prefer:

- [README.md](/C:/code/toolfactory/README.md)
- [docs/agent/quick-read.md](/C:/code/toolfactory/docs/agent/quick-read.md)
- [AGENTS.md](/C:/code/toolfactory/AGENTS.md)
