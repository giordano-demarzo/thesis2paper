---
name: t2p-intake
description: Stage 1 — ingest thesis + repo + context into the project wiki and agree the paper target with the PI.
argument-hint: <project>
disable-model-invocation: true
---
Stage 1 (intake) for project `$ARGUMENTS`. Read `CLAUDE.md` first, then `projects/$ARGUMENTS/project.yaml`.

1. **Ingest** — launch the `ingest` subagent on the project. In parallel, if `lab/wiki/style-profile.md`
   is still a stub and `lab/raw/my_papers/` is not empty, tell the PI that `/lab-style` should run
   (don't block on it).
2. Review the ingest report and the draft ledger yourself. Merge `ledger.draft.yaml` into `ledger.yaml`
   (keep ids), delete the draft, run `python scripts/t2p_ledger.py check $ARGUMENTS`.
3. Write `wiki/overview.md` (one paragraph) and the checkpoint file
   `wiki/decisions/NN-intake.md` (NN from `state.next_decision`) per the protocol in CLAUDE.md.
   The proposal must contain:
   - 2–3 candidate **headlines** (one sentence each), each naming the claims that carry it and the
     broad readership it targets; recommend one.
   - recommended **venue** + backup, with a one-line reason each (use `lab/wiki/venues/`).
   - **scope**: which thesis chapters/claims are in, which are out (maybe a second paper).
   - Early red flags from ingest (unmapped figures, missing data).
4. **Checkpoint** (mode = `mode.stages.intake`, else `mode.default`):
   - guided: present the proposal in chat compactly (headlines as a numbered list, then venue,
     scope, red flags) and ask the open questions. STOP and wait. Then record the decision.
   - auto: accept the default, record it, continue.
5. Write the decision into `project.yaml` → `target.*`; set `state.stage: intake`, increment
   `state.next_decision`; log it. Suggest `/t2p-assess $ARGUMENTS` (or continue if auto).
