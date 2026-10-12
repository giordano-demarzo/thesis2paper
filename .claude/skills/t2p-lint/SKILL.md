---
name: t2p-lint
description: Health check of a project (or the lab wiki) — ledger validity, contradictions, stale pages, orphan claims, citation and number hygiene.
argument-hint: <project | lab>
disable-model-invocation: true
---
Lint `$ARGUMENTS`. Read `CLAUDE.md`.

For a project:
1. `python scripts/t2p_ledger.py check <p>` and `python scripts/t2p_run.py status <p>`.
2. Contradictions: numbers that differ between the thesis, wiki pages, ledger, deliverables and paper;
   claim pages whose status disagrees with the ledger; overview out of date with the latest decision.
3. Hygiene: wiki pages not in the index, index entries pointing nowhere, experiments with no wiki
   page, runs not referenced by any claim, hardcoded numbers in `paper/sections/*.tex` (any digit
   sequence in Results that is not a macro, citation, figure/section ref, or equation), `\needcite`
   and `\todo` counts, uncommitted changes in `work/repo`.
4. Write `wiki/lint-<date>.md` with errors / warnings / suggestions, fix the trivially mechanical ones
   (index entries, stale overview) and list the rest. Log it.

For `lab`: orphan pages, papers in raw without wiki pages, bib entries without `verified` note,
style profile older than the newest paper in `raw/my_papers/`.
