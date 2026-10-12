---
name: lab-style
description: Build or refresh the PI's writing style profile from their papers in lab/raw/my_papers.
disable-model-invocation: true
---
1. List `lab/raw/my_papers/`. If empty, ask the PI to drop 3–6 representative papers there (PDF or
   LaTeX source — source is better), ideally in the target journals. Extract text from PDFs with
   `pdftotext -layout` into `.txt` next to them (raw files themselves stay unchanged).
2. Launch the `style-extractor` subagent.
3. Show the PI the top ~10 rules and the draft checklist; ask if anything is wrong or missing, apply
   their corrections to `lab/wiki/style-profile.md` (mark them `[PI]` — they override extracted rules).
4. Also create/refresh `lab/wiki/literature/<key>.md` pages for each of the PI's papers and add
   verified bib entries to `lab/refs.bib`. Log.
