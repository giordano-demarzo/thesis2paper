# Science Advances

## Source
- Information for authors: https://www.science.org/content/page/science-advances-information-authors
- LaTeX instructions (Science family): https://www.science.org/content/page/preparing-manuscripts-using-latex
- Editorial policies (Science journals): https://www.science.org/content/page/science-journals-editorial-policies
- Date checked: 2026-10-12. Raw extract: `../../raw/venues/science-advances-2026-10-12.md`

## Article type to use
**Research Article** ("should present a major advance"; flexible short or long format). Research Resources is an alternative only for a tool, dataset, or method without a new research insight.

## Limits
| Item | Limit |
|---|---|
| Title | ≤ 135 characters; short title ≤ 50 characters |
| Abstract | ≤ 150 words, one paragraph, no citations, written for a general readership |
| Main text | up to 15,000 words (no page limit stated) |
| Display items | up to 10 figures and/or tables combined |
| References | 80 (main text and SM share one list) |
| Methods | "Materials and Methods" goes after Discussion, before References; no separate word limit found |
| Table legends | ≤ 250 words |
| Figure legend length | not found, check manually |
| SI | single PDF ≤ 25 MB; auxiliary or movie files ≤ 10 files, ≤ 25 MB combined; supplementary text may not develop arguments beyond the main text |

## Required sections/statements
- Main text order: Title, Short title, Authors and Affiliations, Abstract, Introduction, Results, Discussion, Materials and Methods, References, Acknowledgments.
- **Acknowledgments** must hold funding, author contributions (by initials; CRediT encouraged), a competing interests statement, and a data and materials availability statement (MTAs included). Data and code citations go in the "Data, code, and materials availability" section.
- Discussion must include a paragraph on the study's limitations.
- Cover letter must explain what is new and how it advances the field, and say where the data are or will be available.
- You must suggest five reviewers and may exclude up to three. ORCID is required for the first and corresponding authors.
- If AI tools were used in the research or writing, say so in the cover letter and in the methods or acknowledgments.
- Code central to the findings must be archived in a permanent repository (Zenodo, Code Ocean) and cited. A GitHub link alone is not enough. Tabulated data underlying the figures must be in a machine-readable format.

## Structure conventions
- Results are split into subsections, with descriptive-phrase subheads. Materials and Methods subheads are also descriptive phrases.
- Figures and tables are embedded at first mention. Display equations are numbered and not punctuated.
- No footnotes or endnotes.
- The initial submission has no required format. The template is required at revision, along with the topical checklist ("Social and Interdisciplinary Sciences" exists).

## Reference style
- Numbered in-text references in parentheses: (1), (2, 3), (4–6). Order: text, then captions, then SM-only refs.
- Full author lists, with no et al. in the reference list. Example: `N. Tang, Title. Atmos. Environ. 14, 819-834 (1980).`
- Personal communications and working papers are not allowed. Preprints are allowed as URLs.

## LaTeX template availability
- Science-family LaTeX template: `science_template_v1.1.zip` (v1.1, April 2026), https://www.science.org/cms/asset/b7828fbf-d59a-4277-b199-753782283f9e/science_template_v1.1.zip
- Rules: no extra `\usepackage`, a single .tex file, `\cite{}` with BibTeX, and keep the .bbl. .docx is preferred overall.
- Word template: https://www.science.org/cms/asset/31ef4809-4465-48df-ab24-4cfc11f381df/advances_ms_template_07_2026.docx

## What editors say they look for
- Research articles "should present a major advance". The journal calls itself a "highly selective, open access journal".
- The Introduction should give context so that "researchers outside the authors' area" can understand the implications.
- The Editorial Board (active researchers, not professional editors) decides which papers go to review.
- No public acceptance rate or extra scope criteria found; check manually.

## Notes for collective-intelligence papers
- The generous length (15k words, 10 display items) suits multi-study or model-plus-data CI papers. The 150-word abstract is the tightest constraint.
- Choose field codes and the "Social and Interdisciplinary Sciences" revision checklist. The checklist's contents were not fetched; check manually.
- For survey or online-experiment data, the policies require disclosure of sampling design, question wording, and weighting in the SM. They also restrict the phrase "representative sample".
- Computational models must be validated experimentally or on an independent dataset, and their assumptions stated. This applies to agent-based or simulation CI models.
- Limitations need their own paragraph in the Discussion.
