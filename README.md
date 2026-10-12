# thesis2paper

Turn a student thesis + code repo into a first paper draft for broad journals in collective
intelligence (Science Advances, PNAS, Nature Communications), with PI checkpoints along the way.
Runs inside Claude Code on the GPU server. Schema and rules: [CLAUDE.md](CLAUDE.md).

## Terminal interface: `t2p`
`t2p` (installed at `~/.local/bin/t2p`) wraps Claude Code with a thesis2paper system prompt, a
status bar (project · stage/round · GPU-h used/budget · running/failed jobs · ⏳ pending decision),
and project focus, so the slash commands default to the current project.
```
t2p                      # lab-level session (style profile, literature, venues)
t2p <project>            # session focused on a project; opens with its status
t2p <project> "/t2p-assess"     # start with a command or message
t2p ls | status <p> | runs <p>  # quick views, no LLM
t2p auto <p> [--until report]   # unattended run in the background (survives logout)
t2p tail <p> -f          # follow it
t2p stop <p>             # stop it (experiment jobs keep running)
t2p resume <p>           # reopen the latest session (interactive or background) and take over
```
A typical day: start `t2p auto <p> --until report` in the evening, `t2p tail <p>` in the morning,
then `t2p resume <p>` to discuss the round with the full context of what the run did.

## One-time setup
1. Put 3–6 of your papers in `lab/raw/my_papers/` (LaTeX source if you have it) and run `/lab-style`.
2. Optionally add core field papers: `/lab-ingest <pdf|arXiv|DOI> literature`.
3. Venue pages are in `lab/wiki/venues/`; refresh with `/lab-ingest <guidelines URL> venue`.

## Per thesis
```
/t2p-new <name> <thesis.pdf> <repo-path> [venue]   # project + git worktree of the student repo
/t2p-intake <name>     # ingest → chat: headline, venue, scope
/t2p-assess <name>     # repro audit + positioning + gaps → 1-page + 10 slides → chat
/t2p-plan <name>       # costed experiments → chat
/t2p-run <name>        # launch on GPUs, monitor, fix crashes
/t2p-report <name>     # results → 1-page + 5 slides → chat: iterate (plan) or write
/t2p-write <name>      # outline → draft → editor + referee reviews → revise (repeat)
/t2p-status [name]     # where are we
/t2p-lint <name|lab>   # consistency / hygiene check
/t2p-auto <name> [until-stage]   # run the rest with default decisions
```
Each checkpoint writes `projects/<name>/wiki/decisions/NN-<stage>.md` (proposal, options, default,
decision). Set `mode` in `project.yaml` to `guided` or `auto`, globally or per stage. Auto mode
still stops on: a headline discrepancy, budget overrun, a change of headline, or repeated failures.

## Guarantees the scripts enforce
- `scripts/t2p_run.py`: every experiment records its commit, spec, logs and GPU-hours; the
  per-round budget and parallel-job limit are enforced; run outputs are never overwritten.
- `scripts/t2p_ledger.py check`: each evidence path exists, each JSON-sourced number matches the
  ledger, and each `\cite` key is in a verified bib.
- `scripts/t2p_ledger.py macros`: paper numbers come from the ledger as LaTeX macros, and are only
  generated when the ledger is valid.
