---
name: maintain-existing-alteryx-tool
description: Maintain an existing generated Alteryx Platform SDK tool safely.
---

# maintain-existing-alteryx-tool

Inspect, update, and re-validate an existing Alteryx SDK tool without changing its intended behavior unless explicitly requested.

## Use When

- A tool already exists and needs a safe update.
- You want to compare the tool against current templates, compatibility, or validation expectations.
- You need to fix drift without starting from scratch.

## Inputs

- Existing tool folder or tool spec
- Desired maintenance goal
- Target Alteryx version, if changing

## Workflow

1. Load the current tool spec and validation contract.
2. Compare the tool workspace against the current factory templates.
3. Identify drift, compatibility issues, and packaging risk.
4. Propose the smallest safe change set.
5. Re-run validation.
6. Rebuild and export if the change is approved.

## Guardrails

- Preserve behavior unless the update request explicitly changes behavior.
- Do not widen scope during maintenance.
- Stop if validation fails.
- Stop if the tool intent and current implementation conflict and cannot be reconciled safely.
