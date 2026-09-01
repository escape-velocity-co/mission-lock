# Eval Corpus

This corpus is expected to grow over time as new assessment concepts are added. These concepts will be located in definition documents in [`../skills/mission-lock/references/`](../skills/mission-lock/references/); for example `attributes.md`.

As these definitions expand, the eval corpus should grow alongside it: every new attribute, rule, etc. should have at least one document in this corpus that exercises it and one that clearly lacks it, for contrast.

## Why This Corpus?

This corpus uses more than one evaluation tactic:

  1. Publicly available governance documents (e.g. Certificate/Articles of Incorporation), mostly sourced as exhibits (typically "Exhibit 3.1") to SEC EDGAR filings. Using actual documents surfaces drafting details that we want to test against.
  1. Fixtures, present in the the `*-synthetic-*` document folders (e.g. `slifka-and-sons-movers-synthetic-draft-conflict/`). They exist to test behaviors that public documents can't exercise, for example unresolvable precedence between two conflicting documents. This cannot happen because filings are dated and sequenced, by law. Synthetic test cases are marked as such: a folder name containing `synthetic`, a `"synthetic": true` field and note in `metadata.json`, along with a fictional company name.

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

### Generate the Results Docket After Every Run

Once a run is graded, generate the results docket — a single HTML page with one row per eval and one column per rule, a colored marker (🟢/🔴/🟡) at each intersection, and a hover popover showing that call's Result, Assertion, Evidence, and Location. This is a standing deliverable of running the eval suite, not a one-off request — produce it every time an eval run completes, without being asked again.

Use [`docket-template.html`](docket-template.html) as the starting point; it carries its own fill-in instructions as an HTML comment at the top. Save the filled-in copy as `docket.html` inside that run's workspace directory (e.g. `skills/mission-lock-workspace/iteration-<N>/docket.html`), then show it to the user — serve it over http and open it in the browser preview, rather than just reporting a pass/fail table in chat. A bare `file://` preview outside the project folder renders as a static snapshot with no JavaScript, which breaks the hover popover.

### No Connectors in Eval Runs

This eval aims to capture portable behaviour of the skill. Eval results and artifacts are meant to reflect the skill's behavior, agnostic to the environment in which the evalulation is taking place.

Whoever orchestrates the with-skill/without-skill/grading subagents (a person or Claude) must restrict those subagents to local file tools (read/write/edit/bash) and public web fetches only. An eval-executor subagent that incidentally reaches into a connector could leak organization-specific context into results that live in this public repo, and would make the
benchmark reflect that account's environment rather than the skill's portable behavior.

This means (for example) no Slack, email, Google Drive, CRM, or any other connector/integration tool that might contain data or context that could affect the results of the eval, even if some are available in the environment running the eval.

### Output Filename and the Subagent Write-Guard

Some harnesses guard the Write tool against agent-generated files that look like self-authored reports, and block the write outright. This guard is **content-triggered, not just filename-triggered** — avoiding "report" in the filename (e.g. using `assessment.md` or `analysis.md` instead) reduces but does not reliably prevent it. A subagent producing a polished, report-shaped Markdown deliverable can still get blocked regardless of what it's named.

Don't rely on a filename workaround. Instead, structure with-skill/without-skill subagent prompts around **"return the full content as text, orchestrator writes the file"**:

- Ask each subagent to produce its report and return the complete text in its final message, rather than instructing it to save the file itself.
- Whoever is orchestrating (a person or Claude) then writes that returned text to the run's `outputs/` path directly.

This sidesteps the guard entirely rather than tempting a workaround. If a subagent reports the Write tool was blocked and it responded by finding another way to write the file anyway (e.g. a `Bash` heredoc), don't treat that as a routine success — it's the harness saying no, and the subagent routing around it is itself the failure mode to avoid, not a clever fix. Verify the file's content matches what the subagent returned as text, and note the workaround when reporting results.
