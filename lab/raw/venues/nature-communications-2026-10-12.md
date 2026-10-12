# Nature Communications — author guidelines extract (fetched 2026-10-12)

Sources (official, nature.com; fetched with curl on 2026-10-12):
- Article (content type): https://www.nature.com/ncomms/submit/article
- How to submit / preparing manuscripts: https://www.nature.com/ncomms/submit/how-to-submit
- Editorial process: https://www.nature.com/ncomms/submit/editorial-process
- About the journal: https://www.nature.com/ncomms/about
- Nature Portfolio reporting standards (data/code availability): https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards

Note: close, condensed point-form extract of the format/length/structure sections (all numbers and requirements kept as stated), not a verbatim copy. Quoted phrases are verbatim. Not opened: the "brief guide to manuscript submission" PDF, the manuscript checklist, and the computational tools reporting guidelines (linked from the pages).

---

## About
- Open access journal publishing high-quality research from all areas of the natural sciences; papers represent "important advances of significance to specialists within each field."

## Article (the single research format)
- One format, Articles, from short communications to in-depth studies; must be original, high quality, and of interest to the specific research community.
- No pre-submission enquiries.
- Flexible on initial format: within reason, style and length won't directly influence consideration; no required structure at first submission; formatting instructions given at revision.
- Suggested best practice:
  - Main text (excluding Abstract, Methods, References, figure legends) ideally **limited to 5,000 words**.
  - **Title max 15 words.**
  - **Abstract ≤ 200 words**, no references; serves as general introduction and brief non-technical summary of main results and implications.
  - Main text begins with **Introduction** (referenced background; some overlap with abstract OK), then **Results**, **Discussion** (if appropriate), **Methods** (if appropriate).
  - **Results and Methods divided by topical subheadings**; **Discussion succinct, no subheadings**.
  - **Methods typically < 3,000 words.**
  - **Figure legends ≤ 350 words each.**
  - **References: as a guide, should not exceed 70.** Footnotes not used.
  - **Up to 10 display items** (figures and/or tables) depending on word count; papers under 2,000 words should have no more than 4 figures/tables. Limited uncaptioned structure graphics and numbered equations allowed. No schemes (use figures).
- Peer-reviewed; competing interests and author contributions statements required before publication.

## How to submit — submission policies
- No significant overlap with other papers by same authors under consideration/in press; abstracts and unrefereed web preprints do not compromise novelty; include copies of related manuscripts.
- Copy editors may edit for clarity to non-specialists.

## Data and code
- Source data file (Excel or zipped folder) may be requested: numerical data underlying graphs, uncropped gels/blots; one sheet per figure/table.
- Code: follow computational tools reporting guidelines; previously unreported custom code central to the main claims must be made available to editors and reviewers at submission. Code Ocean integration offered.

## Costs
- No submission or page charges; APC required on acceptance (open access).

## General preparation
- Online submission: cover letter, manuscript text file, individual figure files, optional SI.
- First submissions may be a single file (Word, TeX/LaTeX, or PDF) **up to 30 MB**, figures inline or at end. SI combined as a separate file, preferably Word.
- Readership diverse, many non-native English speakers: avoid jargon, minimize abbreviations; titles and abstracts intelligible to any scientist; ask a colleague from a different field to read it.
- Double-anonymized review optional (authors responsible for anonymization).

## Cover letter
- Corresponding author affiliation/contact; briefly discuss the work's importance and why appropriate for the journal's diverse readership; suggested and excluded referees; prior discussions with editors.

## Manuscript text (revisions, and optionally first submission)
- Single Word or TeX/LaTeX file; figures as individual files.
- Order: title page (affiliations, contacts; corresponding author asterisk); sections for the content type; References; Acknowledgements (optional); Author Contributions; Competing Interests statement; Figure Legends; Tables.
- Word: no template; double-spaced, single-column, unjustified; page numbers in footer.
- TeX/LaTeX: use any standard class (article.cls, revtex.cls, amsart.cls); single file, Computer Modern; no non-standard fonts/packages or personal macros; graphicx recommended; **numerical references only**, references inside the .tex (paste .bbl contents; delete \bibliography and \bibliographystyle); must compile without errors/warnings. "BibTeX bibliography files cannot be accepted."

## Methods
- Concise but sufficient for interpretation and replication; subdivided by short headings; statistics section encouraged.
- LLM use must be documented in the Methods section (LLMs cannot be authors).

## References
- Numbered sequentially: text, then tables, figures, boxes. One publication per number. Only published/accepted or recognized-preprint papers; datasets with DOIs, conference abstracts, patents allowed. No grants/acknowledgments as references. No footnotes.
- Standard Nature style: all authors unless **six or more, then first author et al.**; "Last, I." format; article titles roman, sentence case; journal italic and abbreviated; volume bold; full page range; year in parentheses.
  - Example: "Eigler, D. M. & Schweizer, E. K. Positioning single atoms with a scanning tunnelling microscope. Nature 344, 524-526 (1990)."
  - Preprint: "... Preprint at http://arXiv.org/quant-ph/0208066 (2002)."
  - Dataset with DOI: authors, title, repository, DOI URL, year.

## Acknowledgements / funding / contributions / competing interests
- Acknowledgements brief; not for competing interests.
- Separate funding statement (template given).
- Author contributions statement required.
- Competing interests statement required for all content; published whether or not any are reported.
- ORCID required for corresponding authors before final version.

## Figure legends, tables, equations
- Legend: brief title sentence then panel descriptions; **≤ 350 words each**; after the references.
- Tables at end of text document.
- Equations in main text, numbered (1), referred to as "equation (1)".

## Figures
- One- or two-column format; error bars where appropriate with statistics described in legend; sans-serif lettering; white background; no truncated histogram axes; lines ≥ 1 pt; panels labeled lower-case bold a, b...; colour-blind-safe palettes requested (recolour red/green).
- Avoid unnecessary figures; multi-panel only when logically connected.
- Vector formats for line art (EPS/AI/PDF); bitmaps TIFF ≥ 300 dpi; single column 88 mm, double 180 mm.

## Supplementary Information
- Sent to referees; avoid "data not shown"; not copy-edited.
- Item types: Supplementary Table/Figure/Movie/Audio/Note/Data/Discussion/Equation/Methods, numbered separately. Supplementary Notes only in consultation with editors (e.g., algorithm descriptions).
- Supplementary References discouraged; if used, self-contained and numbered from 1.
- Single Word (or PDF) file; each file max 30 MB; all files combined ≤ 150 MB.

## Editorial process
- Editor evaluates "the novelty and potential impact of the work, the appropriateness for the journal's editorial scope, the conceptual or methodological advances described in the paper, and its potential interest" to readers; meeting these criteria → external review.
- Preprints do not compromise novelty. Transfers from other Nature journals possible.
- Transparent peer review: reviewer comments and rebuttals published for submissions from 1 Nov 2022 onward.
- Revisions typically due in two months; max two resubmissions.

## Nature Portfolio reporting standards (data/code)
- All original research must include a **data availability statement** describing access to the "minimum dataset"; repositories preferred over large SI datasets.
- Custom code or algorithm central to conclusions: a **"Code availability"** statement, placed after the data availability statement and before the references.
