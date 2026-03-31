# Tool Factory Architecture

This document gives a plain-English overview of how Tool Factory is put together and how Codex fits into the workflow.

The goal is simple:

- help people understand what each piece does
- show how the pieces work together
- make it easier for the team to explore, extend, and maintain the system

## Big Picture

Tool Factory is a harness repo.

It does not hold the shipped tool output itself. Instead, it provides the rules, templates, skills, and commands that Codex uses to create and maintain tools in the output repo.

Think of it like this:

- **Tool Factory** is the workshop
- **the output repo** is the finished parts shelf
- **Codex** is the assistant that helps move work through the workshop
- **Alteryx** is the destination where the finished tool runs

## The Main Pieces

### Codex Plugin

The plugin is the package that makes Tool Factory reusable by Codex.

Non-technical view:
- It is the “installable bundle” that tells Codex what workflows this repo supports.
- It helps Codex find the right skills and use them consistently.

Why it matters:
- It gives the factory a standard way to be loaded and reused.
- It makes the workflows portable across Codex sessions.

In Tool Factory:
- the plugin points at the repo’s skills
- it helps define the entry points Codex should know about first

### Skills

Skills are focused workflow instructions for Codex.

Non-technical view:
- A skill is a playbook for one repeatable job.
- Instead of asking Codex to guess what to do, you give it a named process.

Examples in Tool Factory:
- create a new tool
- validate a tool
- package a YXI
- maintain an existing tool
- troubleshoot a packaging failure

Why it matters:
- skills reduce guesswork
- they keep work consistent between different people and different Codex sessions
- they are the easiest way to teach Codex a repeatable factory process

### CLI

The CLI is the command-line front end for the factory.

Non-technical view:
- It is the set of commands Codex and humans can run to do actual work.
- It handles the deterministic parts of the process.

Why it matters:
- Codex is good at deciding what should happen.
- The CLI is good at doing it the same way every time.

What the CLI does in Tool Factory:
- reads repo config
- checks readiness
- creates tool intents
- scaffolds tools
- validates workflows
- builds packages
- exports finished tools into the output repo

### AGENTS.md

AGENTS.md is the operating rulebook.

Non-technical view:
- It tells Codex how this repo expects to be used.
- It is the “do this, not that” file for future sessions.

Why it matters:
- it prevents accidental drift
- it keeps the harness and output repo boundaries clear
- it gives Codex a fast summary without needing to search the whole repo

### Configuration

Tool Factory uses config files and environment variables to decide where things go.

Non-technical view:
- configuration tells the factory where the output repo lives and how local tooling should behave
- it keeps machine-specific values out of the shared repo

Why it matters:
- different people can use different output paths
- the repo stays shareable
- generated artifacts stay out of the harness

### Templates

Templates are starting points for new tools.

Non-technical view:
- a template is the “starter kit” for a tool
- it gives a new tool its first structure

Why it matters:
- it makes new tools consistent
- it speeds up creation
- it gives Codex a known shape to fill in

### Validation Workflows

Validation workflows are the proof that a tool actually works.

Non-technical view:
- they are test runs that exercise the tool end to end
- they help catch failures before packaging or shipping

Why it matters:
- they are the main quality gate
- they help surface runtime issues instead of letting them reach users

For Tool Factory:
- validation should run through `AlteryxEngineCmd.exe`
- validation should be tool-specific
- validation should write outputs locally so results are inspectable

### Output Repo

The output repo is where generated tools live.

Non-technical view:
- this is the place where finished tools are stored
- it is customer-owned

Why it matters:
- it is the source of truth for shipped tools
- it keeps Tool Factory itself clean
- it allows governance, audit, and lifecycle management in one place

## How the Pieces Work Together

The usual flow looks like this:

1. A person describes a new tool or an existing tool to update.
2. Codex turns that into an intent or maintenance request.
3. The CLI reads the config and decides where the output repo is.
4. A skill tells Codex which workflow to follow.
5. The CLI scaffolds or updates the tool in the output repo.
6. The validation workflow runs through Alteryx.
7. If validation passes, the tool is packaged.
8. The finished tool is exported or updated in the output repo.

## How the CLI Helps Codex

The CLI is not just for humans.

It is also the fastest way for Codex to do real work without improvising file paths or guessing structure.

Why this is important:
- Codex can reason about intent
- the CLI can execute deterministic steps
- together they create fewer surprises

Examples of good CLI behavior:
- read the output repo from config instead of hardcoding it
- create a workspace in a temp location before promoting it
- validate before packaging
- refuse to write generated artifacts into the harness repo

## Why This Structure Was Chosen

Tool Factory was designed this way because the team needs:

- repeatability
- clear boundaries
- safe updates
- fast onboarding
- room to grow into more advanced agent workflows

This structure is especially useful because it supports three different ways of working:

- **natural language creation**: describe the tool in plain English
- **existing code packaging**: wrap a tested Python codebase as an Alteryx tool
- **maintenance**: inspect and update an existing tool safely

## What a New Team Member Should Remember

If you only remember a few things, remember these:

- Tool Factory is the harness, not the output.
- Skills are the repeatable playbooks.
- The CLI is the deterministic executor.
- Validation is the quality gate.
- The output repo is the place where finished tools live.
- Codex works best here when it follows the factory rules instead of inventing new ones.

## Where to Start Exploring

Recommended reading order:

1. `README.md`
2. `AGENTS.md`
3. `docs/agent/quick-read.md`
4. `docs/reference/README.md`
5. the relevant skill under `.agents/skills/`

## Future Ideas

Once the team is comfortable with the current model, the next areas to explore are:

- more tool templates
- richer validation flows
- stronger catalog and governance rules
- better packaging for external Python code
- more specialized Codex skills for maintenance and upgrade work

The basic idea should stay the same:

- keep the harness clean
- keep the output repo authoritative
- let Codex follow repeatable playbooks
- use the CLI to keep work deterministic
