# Ayx Python SDK: Third-Party Dependencies

Source:
- https://alteryx.github.io/ayx-python-sdk/

Purpose:
- Reference the packaging and dependency model when Tool Factory needs to vendor or package external Python code into an Alteryx tool.

Tool Factory relevance:
- Use this when deciding whether a tool should:
  - vendor wheels locally
  - pin requirements
  - package a wheelhouse
  - rely on a local Python project checkout during development only

Notes:
- This reference pack should stay aligned with the packaging model used by `toolsmith/pythonpack.py`.
- Keep the actual workflow artifacts inside the output repo, not the harness repo.
