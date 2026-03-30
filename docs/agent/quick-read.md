# Tool Factory Agent Quick Read

Use this as the first read path for agents. It avoids repo-wide search and points to the authoritative files.

## What Tool Factory Is

Tool Factory is the harness repo for generating, validating, packaging, and maintaining modern Alteryx Platform SDK tools with Codex.

## Authoritative Files

- [README.md](/C:/code/toolfactory/README.md): consumer entry point and main workflow summary
- [AGENTS.md](/C:/code/toolfactory/AGENTS.md): repo contract and operating rules
- [toolfactory.config.json](/C:/code/toolfactory/toolfactory.config.json): repo config for output path
- [.env.example](/C:/code/toolfactory/.env.example): example local environment settings
- [toolfactory.catalog.json](/C:/code/toolfactory/toolfactory.catalog.json): tool registry snapshot
- [toolfactory.compatibility.json](/C:/code/toolfactory/toolfactory.compatibility.json): supported runtime/tooling matrix
- [toolfactory.governance.json](/C:/code/toolfactory/toolfactory.governance.json): governance policy summary
- [toolfactory.template-manifest.json](/C:/code/toolfactory/toolfactory.template-manifest.json): template catalog

## Canonical Commands

```bash
toolsmith doctor
toolsmith governance
toolsmith init-tool <slug> --name "<Human Name>"
toolsmith scaffold tools/<slug>/tool.yaml
toolsmith validate tools/<slug>/tool.yaml
toolsmith validate-workflow tools/<slug>/tool.yaml
toolsmith build tools/<slug>/tool.yaml
toolsmith export <slug>
toolsmith output-catalog
```

## Bootstrap Order

1. Create `.venv` if missing: `uv venv --python 3.10.18 .venv`
2. Activate `.venv`
3. Install the harness: `uv pip install -e .`
4. Run `toolsmith doctor`
5. Run `toolsmith governance`

## Readiness Rules

- Output repo path comes from `.env`, `toolfactory.config.json`, or `TOOLFACTORY_OUTPUT_REPO_PATH`.
- The output repo is customer-owned and acts as the SSOT for shipped tools.
- The harness repo is the managed factory.
- Validation must run before packaging or export.
- `AlteryxEngineCmd.exe` is the workflow runner for validation smoke tests.

## Versioning Rule

- Use git to track the evolution of one workflow implementation.
- Put materially different workflow designs or specs in separate folders.

## When Working on Tools

- Prefer the existing tool folder over creating new variants.
- Update the validation contract when the workflow changes.
- Update docs when behavior changes.
- Keep the output repo clean; do not treat it as the factory source.
