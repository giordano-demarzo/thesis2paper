---
name: t2p-status
description: Show where a thesis2paper project stands — stage, ledger summary, runs, budget, pending decision.
argument-hint: [project]
disable-model-invocation: true
---
Status for `$ARGUMENTS` (if empty, list all projects under `projects/` except `_template` with their
`state.stage` and round).

For a project: show `state` from project.yaml, `python scripts/t2p_ledger.py table`, 
`python scripts/t2p_run.py status` and `budget`, the latest decision file's Proposal and Decision
(or "pending"), and the latest deliverable PDFs. Keep it to one screen. Suggest the next command.
