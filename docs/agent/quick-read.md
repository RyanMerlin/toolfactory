# Tool Factory Quick Read

Start here if you are building an Alteryx SDK tool with Codex.

## What This Repo Is

Tool Factory is the harness repo that helps Codex:
- scaffold a new SDK tool
- validate the generated workspace
- build the `.yxi`
- keep the workflow rules consistent

## First Things To Read

- [README.md](/C:/code/toolfactory/README.md): friendly start guide
- [AGENTS.md](/C:/code/toolfactory/AGENTS.md): repo rules
- [toolsmith/policy.py](/C:/code/toolfactory/toolsmith/policy.py): canonical harness policy
- `toolsmith policy-show`: prints the current policy in text and JSON
- [schemas/tool-intent.schema.json](/C:/code/toolfactory/schemas/tool-intent.schema.json): tool intent contract
- [docs/reference/README.md](/C:/code/toolfactory/docs/reference/README.md): local Alteryx references

## Good First Commands

```powershell
toolsmith policy-show
toolsmith doctor
toolsmith governance
toolsmith intent "Create a data obfuscation tool that masks selected columns"
toolsmith init-tool json_fixer --name "JSON Fixer"
toolsmith scaffold <output-repo>/tools/<slug>/tool.yaml
toolsmith validate <output-repo>/tools/<slug>/tool.yaml
toolsmith build <output-repo>/tools/<slug>/tool.yaml
```

## Simple User Prompts

If the user wants a tool and does not know what to type, suggest prompts like:
- "Create a simple data obfuscation tool that masks selected columns."
- "Build a tool that cleans text columns and keeps the row structure the same."
- "Make a tool that formats JSON and validates the result."

## Friendly Starting Point

If someone is new to Codex, point them to the README and suggest they start with a plain-English request. Example:

- "I want to use Alteryx and Codex to create a tool that masks selected columns and validates the output."
- "Help me scaffold a simple SDK tool that formats data and keeps the same structure."

## Canonical Rules

- The CLI is required for new SDK tool scaffolding.
- Do not copy another generated tool as a shortcut.
- Keep the harness repo and output repo separate.
- Validate before packaging or export.
- Use `AlteryxEngineCmd.exe` for workflow validation.
