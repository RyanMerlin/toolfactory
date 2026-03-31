---
name: scaffold-and-validate-alteryx-tool
description: Scaffold and validate an Alteryx Platform SDK tool in one workflow.
---

# scaffold-and-validate-alteryx-tool

Create, validate, package, and export a tool using the factory's canonical path and the configured output repo.

## Use When

- Starting a new tool.
- Upgrading or regenerating an existing tool.
- You want the full happy path, end to end.

## Flow

1. Run `toolsmith doctor`.
2. Run `toolsmith intent` or `toolsmith init-tool`, depending on whether the request starts from natural language or a tool template.
3. Run `toolsmith scaffold` against the output-repo tool spec.
4. Run `toolsmith validate`.
5. Run `toolsmith validate-workflow`.
6. Run `toolsmith build`.
7. Run `toolsmith export`.
8. Refresh the output catalog.

## Guardrails

- Stop on validation failure.
- Stop on workflow execution failure.
- Do not export without packaging.
- Do not package without a validated tool spec and reconciled workspace.
