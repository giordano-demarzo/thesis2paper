# PNAS

## Source
- Submitting your manuscript: https://www.pnas.org/author-center/submitting-your-manuscript
- Editorial and journal policies: https://www.pnas.org/author-center/editorial-and-journal-policies
- Date checked: 2026-10-12. Raw extract: `../../raw/venues/pnas-2026-10-12.md`

## Article type to use
**Research Report** submitted as a Direct Submission, unless an NAS member contributes it. A Brief Report (3 pages, about 1,600 words, 15 refs, SI without extra figures or tables) is only for a single concise advance.

## Limits
| Item | Limit |
|---|---|
| Title | < 135 characters; avoid numbers, acronyms, abbreviations, punctuation, puns |
| Abstract | ≤ 250 words |
| Significance statement | ≤ 120 words (Direct and Contributed submissions) |
| Length | preferred 6 pages, max 12 pages; a 6-page paper ≈ 4,000 words, 50 references, 4 medium figures/tables |
| Display items | no hard cap stated; about 4 medium items per 6 pages |
| References | about 50 per 6 pages (guide); SI has its **own separate** reference list |
| Methods | Materials and Methods section **required in main text** (after Discussion); details can go to SI only if the main text lets readers follow the logic and references the SI methods; method papers must describe methods fully in the main text |
| SI | single SI Appendix PDF (not edited); movies ≤ 10 MB; main text must stand on its own |
| Keywords | ≥ 3 |

## Required sections/statements
- Title page: title, authors, affiliations, corresponding author, preprint disclosure, **classification** (major and minor), and keywords.
- **Significance statement**, written for an undergraduate-educated scientist outside the field.
- **Data sharing plans** for all data, documentation, and code. The published article includes a sharing statement. Datasets must be cited in the references, and code made available (e.g., GitHub or Zenodo).
- **Author contributions** are entered in the submission system and published as a footnote, e.g. "designed research; performed research; analyzed data; wrote the paper".
- **Competing interests** are entered in the system and cover 48 months. Funding is also declared.
- Suggest at least 3 each of Editorial Board members, NAS members, and reviewers.
- AI/LLM use must be disclosed in Materials and Methods with the tool name and model version.
- Survey and experiment papers have extra requirements: probability vs nonprobability sample, fielding company and dates, all verbatim questions in SI, and nonprobability samples must not be called "representative".

## Structure conventions
- Order: Title page, Abstract, Significance, Introduction, Results, Discussion, Materials and Methods, Acknowledgments, References, Figure legends.
- No subheading rules were stated for Results or Discussion. The template's conventions were not fetched; check manually.
- "Do not include statements of novelty or priority."
- Initial submission is format-neutral. The template is required for publication-ready files.

## Reference style
- PNAS style, numbered in order of appearance. Full article titles and MEDLINE abbreviations. More than five authors becomes "first author et al.".
- Example: `J.-M. Neuhaus, L. Sticher, F. Meins, Jr., T. Boller, Title. Proc. Natl. Acad. Sci. U.S.A. 88, 10362–10366 (1991).`
- Preprints are cited as "arXiv [Preprint] (year). URL (accessed date)". Archived code is cited with its Zenodo DOI.
- No "data not shown" and no unpublished abstracts. Main-text and SI references are not cross-cited.

## LaTeX template availability
- **pnas-new.cls**: https://www.pnas.org/pb-assets/authors/pnas-new-1764608846380.cls
- Style file pnasresearcharticle.sty, widetext.sty, and **pnas-new.bst**. Links are in the raw extract.
- Overleaf research-article template: https://www.overleaf.com/latex/templates/template-for-preparing-your-research-report-submission-to-pnas-using-overleaf/fzcbzjvpvnxn
- Overleaf SI template: https://www.overleaf.com/latex/templates/pnas-template-for-supplementary-information/wqfsfqwyjtsd
- Rules: compile with PDFLaTeX only, no `\input`, keep the template packages, and put tables inside the .tex.

## What editors say they look for
- Research Reports should report "original research of exceptional importance".
- Review has three tiers: Editorial Board (NAS members), then a member or guest editor, then at least 2 reviewers. "More than 50% of submissions are declined at initial evaluation", and "The acceptance rate is currently 14%."
- Guest editors handle "emerging and interdisciplinary fields". Appeals "based solely on assessments of novelty or general interest are unlikely to be granted".

## Notes for collective-intelligence papers
- Classification: Social Sciences (e.g., Social Sciences, Psychological and Cognitive Sciences, Economic Sciences) or Physical Sciences (Applied Mathematics, Computer Sciences, Physics, Statistics). **Dual classification across major categories is allowed** and is a natural fit for CI.
- The 6-page target (about 4,000 words) forces heavy use of the SI. Keep enough Methods in the main text, because PNAS rejects Methods that exist only in the SI.
- The significance statement is a separate 120-word pitch to non-specialists. Draft it early.
- Online experiments and surveys trigger the survey transparency requirements: verbatim questions in SI, sampling type, AI use in the survey workflow, and synthetic respondents.
- Suggest a guest editor or reviewers with interdisciplinary justification. PNAS explicitly welcomes justification for interdisciplinary papers.
