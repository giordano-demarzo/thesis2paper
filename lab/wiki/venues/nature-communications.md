# Nature Communications

## Source
- Article format: https://www.nature.com/ncomms/submit/article
- How to submit: https://www.nature.com/ncomms/submit/how-to-submit
- Editorial process: https://www.nature.com/ncomms/submit/editorial-process
- About: https://www.nature.com/ncomms/about
- Data and code statements (Nature Portfolio reporting standards): https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- Date checked: 2026-10-12. Raw extract: `../../raw/venues/nature-communications-2026-10-12.md`

## Article type to use
**Article**, the journal's only research format. It covers short and long papers.

## Limits
These are "best practice" guides. The initial format is flexible.

| Item | Limit |
|---|---|
| Title | ≤ 15 words |
| Abstract | ≤ 200 words, no references, a general introduction plus a non-technical summary of the results |
| Main text | ideally ≤ 5,000 words, excluding Abstract, Methods, References, and legends |
| Display items | up to 10 figures/tables. A paper under 2,000 words gets at most 4. No schemes |
| References | as a guide, ≤ 70 |
| Methods | typically < 3,000 words, at the end of the main text, with topical subheadings |
| Figure legends | ≤ 350 words each |
| Initial file | single file up to 30 MB |
| SI | single Word or PDF file. Each file ≤ 30 MB, all files ≤ 150 MB. Not copy-edited. Supplementary Notes only in consultation with editors. Separate SI references are discouraged; if used, number them from 1 |

## Required sections/statements
- Order: title page, then Introduction, Results, Discussion, Methods, then References, Acknowledgements (optional), **Author Contributions**, **Competing Interests**, Figure Legends, Tables.
- **Data availability statement**, required for all original research.
- **Code availability** statement, required when custom code is central to the conclusions. It goes after data availability and before the references. That code must also be available to editors and reviewers **at submission**.
- A separate funding statement. ORCID is required for corresponding authors.
- LLM use must be documented in the Methods.
- Cover letter: say why the work matters to the journal's diverse readership, and list suggested and excluded referees.

## Structure conventions
- Sections in order: Introduction, Results, Discussion (if appropriate), Methods (if appropriate).
- **Results and Methods use topical subheadings. The Discussion is succinct with no subheadings.**
- No footnotes. Equations are numbered (1) and referred to as "equation (1)".
- Word files: double-spaced, single column. No Word template.

## Reference style
- Nature style, numbered in order: text, tables, figures, boxes. If there are six or more authors, cite the first author followed by et al.
- Example: `Eigler, D. M. & Schweizer, E. K. Title. Nature 344, 524-526 (1990).`
- Preprint form: `... Preprint at <URL> (year).` Datasets with DOIs may be cited.

## LaTeX template availability
- **No journal template.** Use a standard class (article.cls, revtex.cls, amsart.cls) in Computer Modern, with no custom macros or non-standard packages.
- Use numerical citations only. **BibTeX .bib files are not accepted**: paste the .bbl into the .tex and delete the `\bibliography` and `\bibliographystyle` commands.
- The file must compile without errors or warnings.

## What editors say they look for
- The editor assesses "the novelty and potential impact of the work, the appropriateness for the journal's editorial scope, the conceptual or methodological advances described in the paper, and its potential interest" to readers.
- Papers should represent "important advances of significance to specialists within each field". This bar is specialist significance, not broad general interest.
- Preprints do not compromise novelty. Transparent peer review applies: reports are published.

## Notes for collective-intelligence papers
- The About page frames the scope as "all areas of the natural sciences". Whether a mainly social-science CI paper fits needs checking manually; check the journal's subject sections. Physics, complex-systems, or computational framings fit the stated scope more clearly.
- The 5,000-word main text plus about 3,000 words of Methods at the end suits model-plus-experiment papers. Put model and analysis details in the Methods, and use Supplementary Notes (with editor agreement) for long derivations.
- The audience is broad and partly non-native English. Keep jargon low and spell out terms like "collective intelligence" or "wisdom of crowds" operationally.
- Code for simulations or analyses must be shareable at submission (Code Ocean is offered). Also follow the journal's computational tools reporting guidelines; they were not fetched, so check manually.
