---
name: t2p-assess
description: Stage 2 — reproduce key results, position against literature, find gaps, and brief the PI with a 1-page + 10-slide deck.
argument-hint: <project>
disable-model-invocation: true
---
Stage 2 (assess) for project `$ARGUMENTS`. Read `CLAUDE.md`, `project.yaml` (target is set), `ledger.yaml`.

1. Launch **in parallel**:
   - `repro-auditor` on the headline + supporting claims (round 0 budget; tell it the claim ids).
   - `literature` for positioning against the agreed headline and venue.
2. When both return, launch `gap-analyst` in gap mode (no specs yet) with both reports.
3. Update `wiki/overview.md`. Validate the ledger. If any headline claim is `discrepancy`, flag it
   first in everything that follows.
4. Launch `presenter` for round `round-00-assess`: one-pager + **10 slides**.
5. Write `wiki/decisions/NN-assess.md`. Proposal = which gaps to address with experiments vs.
   reframing vs. dropping, and whether the headline needs adjusting. Default = address all
   "blocks acceptance" gaps that fit in the round budget.
6. **Checkpoint**: guided → show the PDF paths, a 5-line summary, the decisions needed; STOP.
   auto → accept default unless a stop condition holds (CLAUDE.md).
7. Record decision, update `state` (stage: assess, round: 0), log. Next: `/t2p-plan $ARGUMENTS`.
