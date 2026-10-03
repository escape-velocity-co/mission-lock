# Eval Corpus

This is the eval suite for the Mission Lock Analyzer (MLA) skill.

It consists of a set of governing documents and test prompts, used to validate how how the MLA definitions are interpreted. It aims to have at least one positive and negative test case for every definition present in [`skills/mission-lock/definitions/`](../skills/mission-lock/definitions/), with many documents being used to test multiple definitions.

See [`evals.json`](evals.json) for prompts and expectations, and [`documents/`](documents/) for the governance documents they reference.

## Document Types and Sources

Initially for expediency, the documents we're testing against will be a mixture of public companies and synthetic documents derived from public examples.

**Public company documents** are sourced mostly as exhibits (typically "Exhibit 3.1") to SEC EDGAR filings. Relying primarily on filed documents means we're getting both commonly-used terms in practice and the natural variation present from the variety of methods by which they're derived/written.

**Fixtures (or "sythetics")** are used both to test behaviors that public documents can't exercise and less common scenarios for which a filed charter hasn't yet been incorporated into the corpus.
