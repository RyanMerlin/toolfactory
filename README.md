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
4. Install the Alteryx workspace generator:
   ```powershell
   uv pip install ayx-plugin-cli
   ```
5. Inspect readiness:
   ```powershell
   toolsmith doctor
   toolsmith governance
   ```

## What Lives Here

- `toolsmith/`: deterministic CLI for scaffold, validate, validate-workflow, build, export, and governance checks.
- `toolsmith/pythonpack.py`: scaffolds the Python packaging workspace for external code imported into an Alteryx tool.
- `schemas/tool-intent.schema.json`: intent model for natural-language tool creation and maintenance workflows.
- `intents/`: generated intent files are written into the configured output repo, not the harness.
- `.agents/skills/`: repo-scoped Codex skills for repeated workflows.
- `.codex-plugin/`: distributable Codex plugin metadata.
- `docs/agent/quick-read.md`: the fastest read path for agents.
- `docs/reference/`: curated local Alteryx SDK references for offline agent use.
- `ARCHITECTURE.md`: plain-English overview of the Codex, CLI, and tool factory model.
- `AGENTS.md`: durable operating rules for Codex and humans.
- Generated tool specs and workspaces live in the configured output repo, not here.

## Output Repo

The generated tool output repo is configured in `.env` or `toolfactory.config.json`.

- Default local value: `~/.ayx-tools`
- Override env var: `TOOLFACTORY_OUTPUT_REPO_PATH`
- Engine override env var: `TOOLFACTORY_ALTERYX_ENGINE_CMD`
- `ayx_plugin_cli` is resolved from the active venv, `PATH`, or the local Alteryx bin folder such as:
  - `C:\Users\ryan.merlin\AppData\Local\Alteryx\bin`
  - if installed there, `toolsmith scaffold` and `toolsmith build` can use that local user install directly

The output repo is customer-owned and acts as the SSOT for shipped tools.

## Common Commands

```powershell
toolsmith doctor
toolsmith governance
toolsmith intent "Format JSON from stream input and demonstrate variable substitution"
toolsmith init-tool json_fixer --name "JSON Fixer"
toolsmith scaffold <output-repo>/tools/<slug>/tool.yaml
toolsmith validate <output-repo>/tools/<slug>/tool.yaml
toolsmith validate-workflow <output-repo>/tools/<slug>/tool.yaml
toolsmith validate-summary <output-repo>/tools/<slug>/tool.yaml
toolsmith build <output-repo>/tools/<slug>/tool.yaml
toolsmith export <slug>
toolsmith maintain-tool C:\path\to\existing\tool
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
- For example tools, use the supported CLI path in a temp workspace first, then promote the finished tool into the output repo.
- Never write generated tool artifacts into the harness repo.
- Use a repo-local Python 3.10.x venv at `.venv` for Tool Factory development.
- The factory minimum is currently `3.10.13`; `3.10.18` is a good recommended build.
- If `uv` is not installed, install it before running the factory workflow.
- Install `ayx-plugin-cli` into the same venv before scaffold/build validation.
- For external Python in generated tools, use the generated `python/` workspace with `requirements.in`, `manifest.json`, and a build script rather than ad hoc imports.
- For natural-language tool creation, start with a tool-intent file and then generate the tool spec from that intent.
- For maintenance, use `toolsmith maintain-tool` on the existing tool folder before making changes.
