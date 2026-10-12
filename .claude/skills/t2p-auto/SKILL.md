---
name: t2p-auto
description: Run the remaining pipeline stages automatically with default decisions, stopping only at stop conditions.
argument-hint: <project> [until-stage]
disable-model-invocation: true
---
Automatic mode for $ARGUMENTS (project, optional stage to stop after: intake|assess|plan|run|report|write).

1. Read `CLAUDE.md` and `project.yaml`. Treat every stage as `mode: auto` for this invocation
   (do not modify the file; note "auto via /t2p-auto" in each decision).
2. From `state.stage`, execute the next stages in order following each stage skill's instructions
   (intake → assess → plan → run → report → [plan → run → report]* → write: outline, draft, review,
   revise once), accepting defaults at checkpoints.
3. Stop conditions (always, even in auto): headline claim in `discrepancy`; budget would be exceeded;
   the default would change the agreed headline; an experiment failed twice; `max_experiment_rounds`
   reached with blocking gaps; anything destructive or outside the project folder. On stop: write the
   decision file with the question and summarise in chat.
4. At the end, give a short report: stages run, decisions auto-taken (links), GPU-h used, deliverables.
