# AI usage disclosure

- **Tool used:** OpenAI Codex (GPT-6), in the Codex desktop application.
- **Used for:** Turning the supplied assignment requirements into a project structure, drafting the scraper and processing modules, and preparing the documentation.
- **Representative prompt:** “Create the files with complete code in the ZIP folder on the desktop by looking at these documents. I have to keep this folder in VS Code, and then I have to send it to GitHub.” The supplied documents specified dynamic pagination, a shared schema, cleaning, validation, duplicate detection, logs, CSV/JSON outputs, and tests.
- **AI-assisted parts:** All initial source files and documentation were drafted with AI assistance. The code is ordinary Python and is intended to be reviewed and explainable by the submitter.
- **Review notes:** Listing-page scraping intentionally leaves book category/description blank rather than making extra detail-page requests or inventing values. Quote URLs identify the listing page where each quote appeared. Retry handling, URL validation, page-loop protection, and independent source failure handling are included.
- **Known generated-code limitation:** Website HTML and dependency releases can change; selectors and the captured dataset should be checked again when rerunning. No claim is made that the initial output files are current unless the included run completed successfully.
- **Verification:** All 7 included unit tests passed. A full pipeline run was attempted, but the runtime could not establish a trusted TLS connection to the two source sites; this is recorded in `logs/scraper.log`, and the included CSV is header-only. The report records the resulting zero-record run. Run `python -m pytest` and rerun `python main.py` in an internet-connected environment with working certificate trust to verify/populate the live dataset.

The candidate is responsible for reviewing this implementation and being able to explain its choices before submitting it.

