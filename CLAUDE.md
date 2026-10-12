# thesis2paper — schema

This repo turns a student's thesis + code repo into a first paper draft for broad-audience
journals in collective intelligence (Science Advances, PNAS, Nature Communications, and similar).
You (Claude) run the pipeline; the PI guides it at checkpoints, or lets it run in auto mode.

The design follows the "LLM wiki" pattern: immutable raw sources, an LLM-maintained wiki that
compounds across rounds, and this file as the schema. Read this file fully before any stage.

## Layout

```
lab/                          # LAB WIKI — persists across students
  raw/my_papers/              #   PI's own papers (style + structure reference). Immutable.
  raw/literature/             #   core field literature (PDF/markdown). Immutable.
  raw/venues/                 #   author guidelines, saved as text. Immutable.
  wiki/index.md  wiki/log.md
  wiki/style-profile.md       #   extracted from PI papers by /lab-style — writers MUST follow it
  wiki/venues/<venue>.md      #   format rules + what editors look for
  wiki/literature/<key>.md    #   one page per paper
  wiki/lessons.md             #   lessons promoted from finished projects
  refs.bib                    #   verified bibliography shared across projects

projects/<name>/              # PROJECT WIKI — one per thesis (created from projects/_template)
  project.yaml                #   target, venue, mode (guided/auto), budgets, repo pointer
  ledger.yaml                 #   CLAIMS <-> EVIDENCE ledger. The backbone. See below.
  raw/thesis/                 #   thesis PDF/source + extracted text. Immutable.
  raw/papers/                 #   project-specific context papers. Immutable.
  raw/runs/<exp-id>/          #   experiment outputs, written only by scripts/t2p_run.py. Immutable.
  work/repo/                  #   git worktree of the student repo on branch t2p/<name>. Edit HERE only.
  experiments/<exp-id>.yaml   #   experiment specs (see scripts/t2p_run.py)
  wiki/index.md  wiki/log.md
  wiki/overview.md            #   current one-paragraph state of the project
  wiki/claims/  wiki/methods/  wiki/data/  wiki/experiments/  wiki/literature/
  wiki/decisions/NN-<stage>.md  # one file per checkpoint
  outputs/round-NN-<stage>/   #   one-pagers and slide decks (LaTeX + PDF)
  paper/                      #   main.tex, si.tex, refs.bib, generated/results.tex

templates/latex/              # onepager, beamer slides, paper skeleton
scripts/                      # new_project.py, t2p_run.py, t2p_ledger.py
.claude/skills/               # stage commands (/t2p-*, /lab-*)
.claude/agents/               # subagents used by the stages
```

## Hard rules

1. **Raw is immutable.** Never edit anything under `raw/`. Never edit the student's original repo;
   all code changes go in `projects/<name>/work/repo` (a git worktree), committed with clear messages.
2. **Every number and claim in a deliverable traces to a raw source.** The wiki is for thinking and
   navigation; deliverables are grounded in `raw/` and `ledger.yaml`. Quantitative results in the
   paper are inserted via macros from `paper/generated/results.tex`, which is generated from the
   ledger (`python scripts/t2p_ledger.py macros <project>`). Never type a result number by hand.
3. **Citations only from verified bib entries.** A `\cite{key}` is allowed only if `key` exists in
   `lab/refs.bib` or `projects/<name>/paper/refs.bib` AND the entry was added from a real source
   (DOI/arXiv/PDF in raw). If a citation is needed but not available, write `\needcite{what}` and
   list it in the decision file. Never invent a reference.
4. **Thesis numbers are not evidence until reproduced.** Claims carrying only thesis evidence have
   status `thesis-only`. The repro audit upgrades them to `reproduced` or flags a discrepancy.
5. **Log everything.** Each ingest, run, checkpoint and override gets an entry appended to the
   relevant `wiki/log.md`, format: `## [YYYY-MM-DD HH:MM] <op> | <short title>` then bullet details.
6. **Keep the index current.** Any wiki page created or substantially changed → update `wiki/index.md`
   (link + one-line summary). Agents read the index first.
7. **Experiments go through the runner** (`scripts/t2p_run.py`) so that commit, config, outputs and
   GPU-hours are recorded and the budget in `project.yaml` is enforced.

## The ledger (`ledger.yaml`)

```yaml
claims:
  - id: C1
    statement: "Groups with sparse communication outperform fully connected ones on complex tasks."
    role: headline            # headline | supporting | methodological | context
    status: thesis-only       # thesis-only | reproduced | verified | discrepancy | weak | missing | dropped
    evidence:
      - kind: number          # number | figure | table | script | thesis | literature
        source: raw/runs/E1/metrics.json#/accuracy/sparse   # or raw/thesis/thesis.pdf#p42, work/repo@<sha>:path
        value: 0.82
        macro: AccSparse      # optional -> \AccSparse in paper/generated/results.tex
        note: ""
    gaps: ["no robustness check across network sizes"]
    experiments: [E2]
    reviewer_risk: "Editors may see this as incremental vs. <ref>"
```
`status` meanings: `reproduced` = we re-ran it and matched the thesis; `verified` = new evidence from
our own runs, checked; `discrepancy` = re-run disagrees with thesis (must be raised at a checkpoint).
Validate with `python scripts/t2p_ledger.py check <project>` after every edit.

## Stages and checkpoints

| Stage | Command | Produces | Checkpoint |
|---|---|---|---|
| 0 setup | `/t2p-new` | project folder, worktree | — |
| 1 intake | `/t2p-intake` | wiki pages for thesis, repo map, initial ledger | **target chat**: headline, venue, audience, scope |
| 2 assess | `/t2p-assess` | repro audit, positioning, gap analysis, 1-page + 10 slides | **what we have / miss** |
| 3 plan | `/t2p-plan` | experiment specs with cost + success criteria | **which experiments, budget** |
| 4 run | `/t2p-run` | runs in `raw/runs/`, ledger updated | — (monitoring) |
| 5 report | `/t2p-report` | results analysis, 1-page + 5 slides | **iterate (→3) or write (→6)** |
| 6 write | `/t2p-write` | outline → draft → reviews → revision | **outline approval; each revision round** |
| any | `/t2p-lint` | consistency report | — |
| any | `/t2p-auto` | runs remaining stages with defaults | — |

### Checkpoint protocol
At each checkpoint write `wiki/decisions/NN-<stage>.md` with sections: **Context** (what we
learned, 5–10 lines), **Proposal** (the recommended next action, concrete), **Options** (2–4
alternatives with trade-offs), **Default** (what auto mode will do), **Open questions**, **Decision**
(filled after).

- `mode: guided` (in `project.yaml`, overridable per stage): summarize the proposal in chat, ask the
  PI the open questions, and STOP until they answer. Record their answer verbatim-ish in **Decision**.
- `mode: auto`: fill **Decision** with "auto: accepted default", log it, continue. Still STOP if any
  stop condition holds: a `discrepancy` on a headline claim, budget would be exceeded, the headline
  claim would change, or a stage failed twice.

## Writing for the target venues
- The bar is **broad significance**: an editor outside the subfield must see why it matters in the
  first paragraph. Positioning and the one-sentence headline come before any polishing.
- Structure: short main text (Introduction → Results with claim-style subheadings → Discussion),
  then Methods, then Supplementary Information. Decide main-vs-SI per result explicitly.
- Figure 1 is usually conceptual (the question, the setup, the key idea). Each main figure supports
  one headline or supporting claim from the ledger.
- Follow `lab/wiki/style-profile.md` for voice, structure and conventions, and
  `lab/wiki/venues/<venue>.md` for format limits, required statements and placement rules.
- Drafts produced with this pipeline are AI-assisted. Always include an AI-use disclosure where the
  venue requires it (e.g. PNAS: in Materials and Methods, naming tool and model version) and leave a
  `\todo{}` for the PI to confirm its wording.

## Deliverable formats
LaTeX everywhere. One-pagers from `templates/latex/onepager.tex`, slides from
`templates/latex/slides.tex` (beamer), paper from `templates/latex/paper/`. Compile with
`latexmk -pdf -interaction=nonstopmode` inside the output folder; fix errors before declaring done.
Figures: generate with scripts saved next to the deliverable (`fig_*.py`) reading from `raw/runs/`
or the worktree, so every figure is reproducible.

## Students
Currently PI-only. If a student joins, they review decision files and the ledger; they do not
edit `raw/`. Keep decision files readable by someone who was not in the chat.
