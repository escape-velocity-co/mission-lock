# Eval Corpus

This corpus is expected to grow over time as new assessment concepts are added. These concepts will be located in definition documents in [`../skills/mission-lock/references/`](../skills/mission-lock/references/); for example `attributes.md`.

As these definitions expand, the eval corpus should grow alongside it: every new attribute, rule, etc. worth should have at least one document in this corpus that exercises it (and ideally one that clearly lacks it, for contrast).

## Why This Corpus?

This corpus uses publicly available governance documents (e.g. Certificate/Articles of Incorporation), mostly sourced as exhibits (typically "Exhibit 3.1") to SEC EDGAR filings. Using real documents surfaces major and minor drafting details that we want to test against.

## Structure

```
evals/
├── documents/
│   └── <company-slug>-cert-of-incorporation/
│       ├── <original-exhibit-file>.htm   # unmodified source document
│       └── metadata.json
└── evals.json                            # test prompts, referencing documents/
```

### `metadata.json` format

```json
{
  "company_name": "Example Inc.",
  "cik": "0001234567",
  "accession_number": "0001234567-24-000123",
  "form_type": "S-1",
  "filing_date": "2024-03-01",
  "source_url": "https://www.sec.gov/Archives/edgar/data/...",
  "entity_type": "public benefit corporation",
  "state_of_incorporation": "Delaware",
  "note": "Explicit public benefit purpose clause; included as a positive example for the Stated Purpose Clause and Entity Type attributes."
}
```

### `evals.json` format

Each entry is a task prompt plus the document(s) it should be run against. See `skill-creator`'s eval schema (`references/schemas.md` in [anthropics/skills](https://github.com/anthropics/skills)) for the full spec — assertions are added incrementally.

## Adding to the corpus

1. Find a real Certificate/Articles of Incorporation on [SEC EDGAR full text search](https://www.sec.gov/edgar/search/) (or another public-record source).
2. When querying `sec.gov`/`efts.sec.gov`, send a descriptive `User-Agent` header with a contact email, and keep request rates low — see the [EDGAR fair access guidance](https://www.sec.gov/os/webmaster-faq#developers).
3. Save the unmodified document plus a `metadata.json` under `documents/<company-slug>-cert-of-incorporation/`.
4. Note in `metadata.json` which attribute(s) this document is meant to exercise.
5. Add or update the corresponding entry in `evals.json`.

## Running the Eval Loop

Use the workflow documented in Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill (spawn with-skill/without-skill runs per document, grade against assertions, review in the eval viewer). Point it at this repo's `skills/mission-lock/` and `evals/` directories.

### No Connectors in Eval Runs

This eval aims to capture portable behaviour of the skill. Eval results and artifacts are meant to reflect the skill's behavior, agnostic to the environment in which the evalulation is taking place.

Whoever orchestrates the with-skill/without-skill/grading subagents (a person or Claude) must restrict those subagents to local file tools (read/write/edit/bash) and public web fetches only. An eval-executor subagent that incidentally reaches into a connector could leak organization-specific context into results that live in this public repo, and would make the
benchmark reflect that account's environment rather than the skill's portable behavior.

This means (for example) no Slack, email, Google Drive, CRM, or any other connector/integration tool that might contain data or context that could affect the results of the eval, even if some are available in the environment running the eval.
