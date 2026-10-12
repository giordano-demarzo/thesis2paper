---
name: lab-ingest
description: Add sources to the lab wiki — field literature, venue author guidelines, or lessons — so all projects benefit.
argument-hint: <path-or-url> [literature|venue]
---
Ingest `$ARGUMENTS` into the lab wiki (read `CLAUDE.md` first).

- **literature** (PDF/arXiv/DOI): save the PDF or a text copy into `lab/raw/literature/` (never edit
  it after), write `lab/wiki/literature/<bibkey>.md` (claims, methods, relevance to collective
  intelligence, which projects it matters for), add a verified entry to `lab/refs.bib`
  (`note = {verified: doi|arxiv|pdf}`), and update related pages (concept pages if they exist).
- **venue** (author-guidelines URL): fetch it, save the text in `lab/raw/venues/<venue>-<date>.md`,
  and update `lab/wiki/venues/<venue>.md`: limits (words, abstract, figures, refs, Methods/SI rules),
  required statements, and what the journal says it looks for. Mark each fact with the date checked.
- Discuss key takeaways with the PI briefly if they are present; update `lab/wiki/index.md`; append
  to `lab/wiki/log.md`.
