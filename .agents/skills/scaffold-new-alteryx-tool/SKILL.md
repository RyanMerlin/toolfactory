---
name: scaffold-new-alteryx-tool
description: Create a new modern Alteryx Platform SDK tool using the factory's CLI-first workflow and promote the finished workspace into the output repo.
---

# scaffold-new-alteryx-tool

Create a new modern Alteryx Platform SDK tool using the factory's CLI-first workflow and promote the finished workspace into the output repo.

## Use When

- A new tool is being started.
- A new generated tool workspace needs to be created from the factory templates.

## Inputs

- Tool name
- Tool slug
- Target Alteryx version
- Tool type
- Output repo path from `toolfactory.config.json` or `TOOLFACTORY_OUTPUT_REPO_PATH`

## Workflow

- Validate the tool spec.
- Resolve the configured output repo path.
- Follow the canonical harness policy from `toolsmith policy-show`.
- Create or initialize the tool workspace only by running `ayx_plugin_cli`.
- If the CLI is missing, broken, or cannot create the workspace, stop immediately and fix the CLI path. Do not fabricate workspace files by hand.
- Scaffold the workspace from the CLI-generated SDK workspace only.
- Write the tool README and metadata.

## Guardrails

- Never hardcode repo paths.
- Never write outside the configured output repo.
- Do not overwrite an existing tool without an explicit update request.
- Do not use another generated tool as a structural substitute.
- Do not search for another tool to copy when the CLI path fails.

## Implementation Notes

- Prefer `toolsmith init-tool`, `toolsmith scaffold`, and shared template files over ad hoc generation.
- Keep output deterministic.
