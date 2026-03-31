---
name: validate-alteryx-tool
description: Validate an Alteryx Platform SDK tool against the factory contract.
---

# validate-alteryx-tool

Validate a generated Alteryx tool spec, workspace, and support files against the tool-intent contract.

## Use When

- Before packaging.
- Before merging changes to templates or shared validation logic.
- Before approving a regenerated tool.

## Inputs

- Tool spec path
- Optional `--check` mode

## Workflow

- Follow the canonical harness policy from `toolsmith policy-show`.
- Validate the YAML spec against the schema.
- Verify compatibility metadata and output-repo configuration.
- Check workspace drift.
- Check the validation contract.
- Check output repo configuration if the workflow needs generated output.
- Run the validation workflow command if requested.
- Prefer a minimal engine-runnable XML validation workflow template by default.
- If the tool has been installed into Designer, run a post-install smoke test against the installed tool directory.

## Guardrails

- Fail fast on schema drift.
- Fail fast on workspace drift.
- Keep validation read-only unless the caller explicitly requests reconciliation.
