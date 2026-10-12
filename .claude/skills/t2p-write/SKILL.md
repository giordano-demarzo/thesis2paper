---
name: t2p-write
description: Stage 6 — outline, draft, review and revise the paper in LaTeX, with PI guidance at each round.
argument-hint: <project> [outline|draft|review|revise] [section or instructions]
disable-model-invocation: true
---
Stage 6 (write). Arguments: $ARGUMENTS. With no sub-step, continue from where `paper/` is
(no outline → outline; outline approved, no draft → draft; draft exists → review).

Setup (first time): copy `templates/latex/paper/*` into `projects/<p>/paper/` without overwriting
`refs.bib` entries already present; run `python scripts/t2p_ledger.py macros <p>`.

**outline** — Write `paper/outline.md`: title options (3), the one-sentence headline, abstract in
5 sentences (function of each per the style profile), then per section a paragraph-by-paragraph plan
(one sentence per paragraph stating its point + the ledger claim ids / citations it uses), the figure
plan (Fig. 1 conceptual; each main figure → claim ids, panels, source data), and the main-vs-SI split.
Optionally launch `reviewer-editor` on the outline alone. Checkpoint (guided: STOP for approval).

**draft** — Launch `writer` subagents per section. Results and Methods can be written in parallel;
then Introduction and Discussion; abstract (+ significance for PNAS) last. Generate main figures as
`paper/figures/fig_*.py` reading from `raw/runs/`. Compile `main.tex` and `si.tex`. Run the ledger check.

**review** — Launch `reviewer-editor` and `reviewer-specialist` in parallel on the compiled draft.
Save their reports to `paper/reviews/round-K-*.md`. Write `wiki/decisions/NN-write-K.md`: the merged
list of issues, each tagged writing-fix / analysis-on-existing-runs / new-experiment, with a
proposed action. Default = fix all writing issues + cheap analyses; new experiments go back to
/t2p-plan only with PI approval. Checkpoint (guided: STOP).

**revise** — Apply the approved fixes via `writer` subagents (or directly for small edits), recompile,
re-run the ledger check, log. Then ask whether to run another review round. The PI may also give
free-form writing instructions here ("make the intro more about X") — apply them and log them as
overrides; if an instruction reflects a general preference, offer to add it to
`lab/wiki/style-profile.md`.

Finish (when the PI says the draft is good): `state.stage: done`, write the closing log entry,
and propose lessons to promote into `lab/wiki/lessons.md`.
