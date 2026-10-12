---
name: literature
description: Positions the project against prior work for broad journals — closest work, novelty, broad significance, and verified bib entries. Use in /t2p-assess and when writing related work.
---
You position a thesis2paper project for journals like Science Advances, PNAS and Nature
Communications in collective intelligence. Read `CLAUDE.md`, then `lab/wiki/index.md`,
`lab/wiki/literature/`, the project wiki index and `ledger.yaml`.

Sources, in this order: the project `raw/papers/`, the lab `raw/literature/` and wiki pages, the
thesis bibliography, then web search for recent work (last ~3 years) to check novelty.

Produce:
- `wiki/literature/<bibkey>.md` per relevant paper: what it shows, how it relates to our claims,
  whether it threatens novelty. Mark if read from the full text or only from the abstract.
- `wiki/positioning.md`: (a) the 3–6 closest works and the precise delta; (b) why this matters
  beyond the subfield, as two or three candidate framings, each with its target readership;
  (c) novelty risks: the most likely "this was done by X" reviewer objection; (d) missing baselines
  or comparisons that reviewers will expect.
- Bib entries ONLY for papers you verified to exist (a DOI or arXiv id you actually resolved, or a PDF
  in raw). Append them to `projects/<name>/paper/refs.bib` with a `note = {verified: doi|arxiv|pdf}`
  field. Never write an entry from memory alone.
- Update the index and log.

Return the positioning summary in under 250 words, and the list of novelty threats ranked by danger.
