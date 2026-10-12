---
name: t2p-run
description: Stage 4 — launch approved experiments on the GPU server, monitor them, and handle failures.
argument-hint: <project> [exp-ids...]
disable-model-invocation: true
---
Stage 4 (run). Arguments: $ARGUMENTS (project, optional explicit experiment ids; default = the
approved ids from the latest plan decision).

1. Make sure `work/repo` has no uncommitted changes (commit with `t2p:` messages if needed).
2. Launch approved experiments with `python scripts/t2p_run.py launch <project> <id>`, respecting
   `max_parallel_jobs`; queue the rest. If launch says WAIT, wait for a running job to finish.
3. Monitor with `python scripts/t2p_run.py wait <project> <ids...>` run in the background, and check
   early logs (`raw/runs/<id>/stdout.log`/`stderr.log`) a few minutes in to catch crashes quickly.
4. On failure: diagnose from stderr. A code bug → fix in `work/repo`, commit, relaunch (it gets a
   new run id `-r2`; the failed run stays as a record). If the fix changes the experiment
   meaningfully, or the same experiment fails twice, stop and ask the PI (even in auto mode).
5. Never exceed the round budget without the PI's approval (`--force-budget` only after explicit OK).
6. When all are finished, write `wiki/experiments/<id>.md` stubs (what ran, run ids, state), log,
   and continue with `/t2p-report <project>`.
