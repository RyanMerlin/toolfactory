# Tool Factory

Tool Factory is the harness repo for generating, validating, packaging, and maintaining modern Alteryx Platform SDK tools with Codex.

## Quick Start

1. Create a local Python venv if needed:
   ```powershell
   uv venv --python 3.10.18 .venv
   ```
2. Activate it:
   ```powershell
   .\.venv\Scripts\activate
   ```
3. Install the harness:
   ```powershell
   uv pip install -e .
   ```
4. Inspect readiness:
   ```powershell
   toolsmith doctor
   toolsmith governance
   ```

## What Lives Here

- `toolsmith/`: deterministic CLI for scaffold, validate, validate-workflow, build, export, and governance checks.
- `.agents/skills/`: repo-scoped Codex skills for repeated workflows.
- `.codex-plugin/`: distributable Codex plugin metadata.
- `docs/agent/quick-read.md`: the fastest read path for agents.
- `AGENTS.md`: durable operating rules for Codex and humans.
- `tools/`: generated tool specs and workspaces.

## Output Repo

The generated tool output repo is configured in `.env` or `toolfactory.config.json`.

- Default local value: `~/.ayx-tools`
- Override env var: `TOOLFACTORY_OUTPUT_REPO_PATH`
- Engine override env var: `TOOLFACTORY_ALTERYX_ENGINE_CMD`

The output repo is customer-owned and acts as the SSOT for shipped tools.

## Common Commands

```powershell
toolsmith doctor
toolsmith governance
toolsmith init-tool json_fixer --name "JSON Fixer"
toolsmith scaffold tools/api_request_builder/tool.yaml
toolsmith validate tools/api_request_builder/tool.yaml
toolsmith validate-workflow tools/api_request_builder/tool.yaml
toolsmith validate-summary tools/api_request_builder/tool.yaml
toolsmith build tools/api_request_builder/tool.yaml
toolsmith export api_request_builder
toolsmith output-catalog
```

## Agent Read Path

Agents should read, in order:

1. [docs/agent/quick-read.md](/C:/code/toolfactory/docs/agent/quick-read.md)
2. [AGENTS.md](/C:/code/toolfactory/AGENTS.md)
3. [toolfactory.governance.json](/C:/code/toolfactory/toolfactory.governance.json)

## Notes

- Use the modern Alteryx Platform SDK path.
- Keep the harness repo and output repo separate.
- Do not hardcode machine-specific output paths in templates or scripts.
- Use a repo-local Python 3.10.x venv at `.venv` for Tool Factory development.
- The factory minimum is currently `3.10.13`; `3.10.18` is a good recommended build.
- If `uv` is not installed, install it before running the factory workflow.
