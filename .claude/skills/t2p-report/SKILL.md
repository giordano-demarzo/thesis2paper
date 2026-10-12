---
name: t2p-report
description: Stage 5 — analyse new results, update the ledger, and brief the PI with a 1-page + 5-slide deck; decide whether to iterate or write.
argument-hint: <project>
disable-model-invocation: true
---
Stage 5 (report) for project `$ARGUMENTS`, round R = `state.round`. Read `CLAUDE.md`, `project.yaml`,
`ledger.yaml`, the plan decision for round R.

1. Launch `results-analyst` on round R's runs. Review its ledger changes yourself, run
   `python scripts/t2p_ledger.py check $ARGUMENTS`.
2. Update `wiki/overview.md`.
3. Launch `presenter` for `round-RR-report`: one-pager + **5 slides** (what we ran, 2–3 results,
   ledger changes, next step).
4. Write `wiki/decisions/NN-report.md`. Options: (a) another experiment round (→ /t2p-plan) with the
   gaps it would close; (b) start writing (→ /t2p-write); (c) adjust headline/scope. Default = (b) if
   no "blocks acceptance" gaps remain or `max_experiment_rounds` is reached, else (a).
5. **Checkpoint**: guided → summary + PDFs + question; STOP. auto → default (stop conditions apply).
6. Record, update state, log, and suggest or continue to the next stage.
