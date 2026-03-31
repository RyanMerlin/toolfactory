---
name: maintain-tool-catalog
description: Maintain the catalog of generated tools and related metadata.
---

# maintain-tool-catalog

Maintain the catalog of generated tools in the output repo as the shipped-tool source of truth.

## Use When

- A new generated tool is added.
- A tool is renamed, deprecated, or upgraded.

## Workflow

- Update the catalog metadata and any generated-tool registry files.
- Update version and compatibility records from the current compatibility matrix.
- Flag deprecations explicitly and keep the output repo catalog in sync with exports.
