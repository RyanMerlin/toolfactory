# Tool Factory

Tool Factory is the harness repo for generating and maintaining Alteryx Platform SDK tools with Codex.

## Agent First Read

- [docs/agent/quick-read.md](/C:/code/toolfactory/docs/agent/quick-read.md)

## Source of Truth

- The tool factory source lives in this repo.
- Generated tool output lives in the configured output repo path.
- `.env` is the preferred local override for the output repo path.
- `toolfactory.config.json` is the repo-level config for the output repo path.
- `TOOLFACTORY_OUTPUT_REPO_PATH` overrides the config file when set.
- The default output repo path is `~/.ayx-tools` unless overridden.

## Operating Rules

- Keep the harness repo and output repo separate.
- Use git commits to track evolution of a single workflow implementation over time.
- Use separate folders for materially different workflow designs or specs.
- Do not hardcode absolute output paths in tool generation logic.
- Treat `toolsmith` as the deterministic CLI surface for scaffold, validate, reconcile, and build.
- Keep `.env` out of git; use `.env.example` for the checked-in reference values.
- Use `toolsmith init-tool` to create a new tool from the factory template.
- Use `toolsmith export <slug>` to publish a generated tool into the configured output repo.
- Prefer edits to templates and scripts over one-off manual changes in generated tools.
- Do not break existing generated tools when updating templates or shared logic.

## Validation Rules

- Validate tool specs before scaffolding or building.
- Reconcile workspaces before packaging.
- Verify the output repo path is a git repository before writing generated output.
- Keep generated artifacts reproducible.

## Upgrade Rules

- When Alteryx SDK versions change, update compatibility data first, then templates, then docs.
- When Codex plugin or skill conventions change, update the plugin manifest, skill docs, and AGENTS.md together.
- When behavior changes, update human docs and agent-facing docs together.

## Codex Guidance

- Use repo-scoped skills for repeated workflows.
- Use the plugin layer for distribution and reuse.
- Use hooks only for optional guardrails.
- Use the Codex SDK only for programmatic orchestration and CI/CD.
