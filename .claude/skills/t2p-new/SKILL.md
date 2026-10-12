---
name: t2p-new
description: Create a new thesis2paper project from a thesis and a student repo.
argument-hint: <name> <thesis-path> <repo-path> [venue] [context papers...]
disable-model-invocation: true
---
Create a thesis2paper project. Arguments: $ARGUMENTS

1. If any of name / thesis path / repo path is missing, ask for it (one question).
2. Run `python scripts/new_project.py <name> --thesis <path> --repo <path> [--venue v] [--papers ...]`
   from the repo root. Report any warnings (uncommitted changes in the student repo, non-git repo).
3. Ask the PI to check `projects/<name>/project.yaml` → `compute` (GPU ids, budget per round,
   parallel jobs) and `mode`. Show the current values in a compact form; apply their changes.
4. Suggest `/t2p-intake <name>`.
