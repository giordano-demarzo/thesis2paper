---
name: t2p-plan
description: Stage 3 — design costed experiments to close the agreed gaps and get them approved.
argument-hint: <project>
disable-model-invocation: true
---
Stage 3 (plan) for project `$ARGUMENTS`. Read `CLAUDE.md`, `project.yaml`, `ledger.yaml`, the latest
decision file (which gaps were chosen), `wiki/positioning.md`.

1. Increment `state.round` (round R). Launch `gap-analyst` in plan mode with the chosen gaps and
   round R; it writes `experiments/E*.yaml` with `round: R`.
2. Review the specs yourself: commands exist in `work/repo`, outputs go to `$T2P_OUT`, success
   criteria are decided before running, estimates are plausible. Dry-run each:
   `python scripts/t2p_run.py launch $ARGUMENTS <id> --dry-run`.
3. Write `wiki/decisions/NN-plan.md`: a table (id, hypothesis, claims, GPU-h, success criterion,
   what we do if it fails), the cut line at the budget, total GPU-h. Default = everything above the cut.
4. **Checkpoint**: guided → show the table, ask which to run / budget changes; STOP. auto → default.
5. Record decision (list of approved ids) and log. Next: `/t2p-run $ARGUMENTS`.
