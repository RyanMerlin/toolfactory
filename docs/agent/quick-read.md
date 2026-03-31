# Tool Factory Agent Quick Read

Use this as the first read path for agents. It avoids repo-wide search and points to the authoritative files.

## What Tool Factory Is

Tool Factory is the harness repo for generating, validating, packaging, and maintaining modern Alteryx Platform SDK tools with Codex.

## Entry Modes

- Natural-language creation: describe the desired tool behavior and let the factory turn it into a spec and scaffold.
- External Python packaging: provide tested Python code and let the factory wrap it as an Alteryx tool.
- Maintenance: point the factory at an existing SDK tool and update or harden it safely.

## Authoritative Files

- [README.md](/C:/code/toolfactory/README.md): consumer entry point and main workflow summary
- [AGENTS.md](/C:/code/toolfactory/AGENTS.md): repo contract and operating rules
- [schemas/tool-intent.schema.json](/C:/code/toolfactory/schemas/tool-intent.schema.json): intent contract for new tools and maintenance flows
- Generated intent files are written into the configured output repo, not the harness repo.
- [toolfactory.config.json](/C:/code/toolfactory/toolfactory.config.json): repo config for output path
- [.env.example](/C:/code/toolfactory/.env.example): example local environment settings
- [toolfactory.catalog.json](/C:/code/toolfactory/toolfactory.catalog.json): tool registry snapshot
- [toolfactory.compatibility.json](/C:/code/toolfactory/toolfactory.compatibility.json): supported runtime/tooling matrix
- [toolfactory.governance.json](/C:/code/toolfactory/toolfactory.governance.json): governance policy summary
- [toolfactory.template-manifest.json](/C:/code/toolfactory/toolfactory.template-manifest.json): template catalog
- [docs/reference/README.md](/C:/code/toolfactory/docs/reference/README.md): local curated Alteryx SDK references
- [ARCHITECTURE.md](/C:/code/toolfactory/ARCHITECTURE.md): plain-English architecture overview

## Canonical Commands

```bash
toolsmith doctor
toolsmith governance
toolsmith intent "<natural language summary>"
toolsmith init-tool <slug> --name "<Human Name>"
toolsmith scaffold <output-repo>/tools/<slug>/tool.yaml
toolsmith validate <output-repo>/tools/<slug>/tool.yaml
toolsmith validate-workflow <output-repo>/tools/<slug>/tool.yaml
toolsmith maintain-tool <tool-folder>
toolsmith build <output-repo>/tools/<slug>/tool.yaml
toolsmith export <slug>
toolsmith output-catalog
```

## Bootstrap Order

1. Create `.venv` if missing: `uv venv --python 3.10.18 .venv`
2. Activate `.venv`
3. Install the harness: `uv pip install -e .`
4. Run `toolsmith doctor`
5. Run `toolsmith governance`
6. Use `docs/reference/` before web browsing when a local Alteryx SDK reference exists

## Readiness Rules

- Output repo path comes from `.env`, `toolfactory.config.json`, or `TOOLFACTORY_OUTPUT_REPO_PATH`.
- `ayx_plugin_cli` may resolve from the active venv, `PATH`, or a local Alteryx bin folder such as `C:\Users\ryan.merlin\AppData\Local\Alteryx\bin`.
- The output repo is customer-owned and acts as the SSOT for shipped tools.
- The harness repo is the managed factory.
- Validation must run before packaging or export.
- `AlteryxEngineCmd.exe` is the workflow runner for validation smoke tests.
- For external Python dependencies in a generated tool, look for the tool-local `python/` workspace and its `manifest.json`; do not invent import paths on the fly.
- For supported example tools, prefer the CLI-first pattern: initialize a temp workspace, generate and package there, then promote the finished workspace into the output repo.
- If a generated artifact is about to land in the harness repo, stop and reroute it to the configured output repo.

## Versioning Rule

- Use git to track the evolution of one workflow implementation.
- Put materially different workflow designs or specs in separate folders.

## When Working on Tools

- Prefer the existing tool folder over creating new variants.
- Update the validation contract when the workflow changes.
- Update docs when behavior changes.
- Keep the output repo clean; do not treat it as the factory source.
