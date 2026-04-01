# Tool Factory

Tool Factory is the Codex harness for building modern Alteryx Platform SDK tools.

If you are an Alteryx user who wants to use Alteryx plus Codex to generate SDK tools, this repo is the starting point:
- you describe the tool you want
- Codex helps scaffold it
- the factory builds it
- the factory validates it

## Start Here

If you want to try it quickly:
1. Clone this repo.
2. Open Codex in the `toolfactory` folder.
3. Run `toolsmith policy-show` to see the current rules.
4. Ask Codex to create your tool.
5. Let Codex scaffold, build, and validate it for you.

## Easy Example Prompts

You can paste prompts like these into Codex:

- `Create a simple data obfuscation tool that lets me choose columns to mask while keeping the output structure the same.`
- `Build me a tool that formats incoming JSON and preserves the original schema as much as possible.`
- `Make a tool that cleans up text columns, trims whitespace, and keeps the original row count.`
- `I want an Alteryx SDK tool that hashes selected fields and then validates the result with a sample workflow.`

## What Tool Factory Does

- `toolsmith/`: the command-line harness that scaffolds, validates, builds, and exports tools.
- `toolsmith/policy.py`: the canonical harness policy used by the docs, skills, and commands.
- `schemas/tool-intent.schema.json`: the intent format for tool creation and maintenance.
- `.agents/skills/`: Codex skill instructions for repeated workflows.
- `docs/reference/`: local Alteryx SDK references.
- `docs/checkpoint/`: notes about harness issues and improvements we found while building tools.

## Typical Workflow

1. Describe the tool in plain language.
2. Run `toolsmith intent` or `toolsmith init-tool`.
3. Scaffold the workspace with `toolsmith scaffold`.
4. Review the generated tool files in the output repo.
5. Run `toolsmith validate`.
6. Build the `.yxi` with `toolsmith build`.
7. If needed, install it into Designer and run a smoke test.

## Output Repo

The generated tool lives in the output repo, not in this harness repo.

- Default local value: `~/.ayx-tools`
- Override env var: `TOOLFACTORY_OUTPUT_REPO_PATH`
- Engine override env var: `TOOLFACTORY_ALTERYX_ENGINE_CMD`

For this workspace, the output repo is set in `.env`.

## Common Commands

```powershell
toolsmith policy-show
toolsmith doctor
toolsmith governance
toolsmith intent "Create a simple obfuscation tool for selected columns"
toolsmith init-tool json_fixer --name "JSON Fixer"
toolsmith scaffold <output-repo>/tools/<slug>/tool.yaml
toolsmith validate <output-repo>/tools/<slug>/tool.yaml
toolsmith validate-workflow <output-repo>/tools/<slug>/tool.yaml
toolsmith build <output-repo>/tools/<slug>/tool.yaml
toolsmith export <slug>
toolsmith smoke-test-installed-tool <installed-tool-folder>
toolsmith maintain-tool C:\path\to\existing\tool
```

## For New Users

If you want to move quickly, use this simple flow:
- tell Codex what you want in plain English
- let Codex create the tool skeleton
- let the factory build and validate it
- review the result in the output repo

## Important Rules

- Keep the harness repo and output repo separate.
- Do not write generated tool artifacts into the harness repo.
- Use the CLI-first flow for new tools.
- Do not copy an existing generated tool as a starting point for a new one.
- Use a repo-local Python 3.10.x venv at `.venv` for development.

## Agent Read Path

Agents should read, in order:

1. [docs/agent/quick-read.md](/C:/code/toolfactory/docs/agent/quick-read.md)
2. [AGENTS.md](/C:/code/toolfactory/AGENTS.md)
3. [toolsmith/policy.py](/C:/code/toolfactory/toolsmith/policy.py)
