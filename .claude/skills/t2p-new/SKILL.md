---
name: t2p-new
description: Create a new thesis2paper project from a thesis (inbox/<name>/) and a student repo URL.
argument-hint: <name> [repo URL] [venue]
disable-model-invocation: true
---
Create a thesis2paper project. Arguments: $ARGUMENTS

1. Expected setup: the thesis (PDF and/or LaTeX source) is in `inbox/<name>/`, optional context
   papers in `inbox/<name>/papers/`, and the repo URL is given as argument or in `inbox/<name>/repo.txt`.
   If the inbox folder is missing or empty, tell the PI exactly where to put the files and stop.
2. Run `python scripts/new_project.py <name> [--repo <URL>] [--venue v]` from the repo root.
   If cloning fails because the repo is private, tell the PI to run `! gh auth login` (or give the
   student's repo access to their GitHub account) and retry. Report any warnings (Git LFS, etc.).
3. Show the `compute` and `mode` sections of `projects/<name>/project.yaml` compactly and ask if
   they should change for this project; apply changes.
4. Suggest `/t2p-intake <name>`.
