# Eval Corpus

This corpus is expected to grow over time as new assessment concepts are added. These concepts will be located in definition documents in [`../skills/mission-lock/definitions/`](../skills/mission-lock/definitions/); for example `attributes.md`. Every new attribute, rule, etc. should have at least one document in this corpus that exercises it and one that clearly lacks it, for contrast. Test cases can do double-duty, serving as positive and negative assertions for many tests.

## Why This Corpus?

This corpus uses multiple tactics:

  1. Publicly available governance documents (e.g. Certificate/Articles of Incorporation), mostly sourced as exhibits (typically "Exhibit 3.1") to SEC EDGAR filings. Using filed documents allows us to test real-life variations.
  1. Fixtures, present in the the `*-synthetic-*` document folders (e.g. `slifka-and-sons-movers-synthetic-draft-conflict/`). They exist to test behaviors that public documents can't exercise, for example unresolvable precedence between two conflicting documents. This cannot happen because filings are dated and sequenced, by law. Synthetic test cases are marked as such: a folder name containing `synthetic`, a `"synthetic": true` field and note in `metadata.json`, along with a fictional company name.

## Structure

```
evals/
├── documents/
│   └── <company-slug>-cert-of-incorporation/
│       ├── <original-exhibit-file>.txt   # plain-text extraction, committed
│       └── metadata.json
└── evals.json                            # test prompts, referencing documents/
```

`<original-exhibit-file>.txt` is generated from the filed `.htm`/`.txt` exhibit by [`extract_text.py`](extract_text.py) when the document is added (see "Adding to the corpus" below). The raw `.htm` download is never committed — only the extraction is. If extraction looks wrong for some document (a mangled table, dropped text), fix `extract_text.py` and regenerate; don't hand-edit the `.txt`.

### `metadata.json` format

```json
{
  "company_name": "Example Inc.",
  "featured": false,
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

`featured` is `true` if the company appears in the book *Incorruptible*, `false` if it does not.

### `evals.json` format

Each entry is a task prompt plus the document(s) it should be run against. See `skill-creator`'s eval schema (`references/schemas.md` in [anthropics/skills](https://github.com/anthropics/skills)) for the full spec — assertions are added incrementally.

### Prompts Test Report Generation, Not Request Interpretation

This corpus exists to validate report generation deterministically against a standard output format across a variety of charters. It is not designed to test conversational requests. We trust that responding to those requests will be handled adequately at query time, given the skill will have been validated against retrieving the underlying accurate information.

* Every eval prompt should read as a variation on a request for the report.
* An eval prompt can motivate *why* the user is asking.
* An eval prompt should not explicitly name or request a narrower slice of the report.

## Adding to the Corpus

1. Find a Certificate/Articles of Incorporation on [SEC EDGAR full text search](https://www.sec.gov/edgar/search/) (or another public-record source).
1. When querying `sec.gov`/`efts.sec.gov`, send a `User-Agent` header with a contact email, and keep request rates low.
1. Save the downloaded `.htm` plus a `metadata.json` under `documents/<company-slug>-cert-of-incorporation/`.
1. Run `python3 extract_text.py documents/<company-slug>-cert-of-incorporation/<file>.htm` to generate the `.txt` extraction.
1. Delete the `.htm`.
1. Note in `metadata.json` which attribute(s) this document is meant to exercise.
1. Add or update the corresponding entry in `evals.json`, referencing the `.txt` file.

## Running the Eval Loop

Use the workflow documented in Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill (spawn with-skill/without-skill runs per document, grade against assertions, review in the eval viewer). Point it at this repo's `skills/mission-lock/` and `evals/` directories.

### What Counts as a Failure

A graded run's divergence from an eval's `expectations` is a failure only if the **result itself is wrong, unsupported by any evidence, or hedged when it shouldn't be**. If the Result is correct and with evidence, but the write-up organizes or distributes its reasoning differently than an assertion anticipated - that is not a skill defect. It likely means the assertion needs to be re-examined and called to the attention of the author. Fix or remove the assertion in that case.

### Grounding Expected-Output Reasoning

When drafting an eval's `expected_output` or `expectations` text, ground the reasoning in facts the source document itself states, not in a supporting legal or factual generalization you supply to justify the conclusion. A generalization offered only to explain *why* a result should hold is a separate claim from the result itself, and it can be wrong even when the result is right. For example, an eval once justified excluding a Bylaws provision from a certificate-only rule by asserting "bylaws are ordinarily amendable by the board alone" — a legal claim that isn't reliably true (DGCL §109(a) defaults bylaw-amendment power to stockholders unless the certificate grants it to the board) — when the document-grounded reason was simply that the statute requires the election to be made in the certificate itself.

Before writing an assertion that leans on a rule of thumb you haven't verified against the actual statute or document text, check it, the same way you'd verify a "should be a failure" call against the source document per "What Counts as a Failure" above.

### Generate the Results Docket After Every Run

Once a run is graded, generate the results docket. This is a standing deliverable of running the eval suite, not a one-off request. Produce it every time an eval run completes, without being asked again.

Use [`docket-template.html`](docket-template.html) as the starting point; it carries its own fill-in instructions as an HTML comment at the top. For the rule-definition popover content specifically, use [`parse_rules.py`](parse_rules.py)'s `parse_rules_md()` function to pull it straight from `rules.md` rather than retyping it — see the template's own instructions for the exact fields it returns. Save the filled-in copy as `docket.html` inside that run's workspace directory (e.g. `skills/mission-lock-workspace/iteration-<N>/docket.html`), then show it to the user — serve it over http and open it in the browser preview, rather than just reporting a pass/fail table in chat. A bare `file://` preview outside the project folder renders as a static snapshot with no JavaScript, which breaks the hover popover.

### Capture and Roll Up Timing After Every Run

See [`evals/benchmarks/README.md`](benchmarks/README.md) for instructions on how to maintain the benchmarks.

### No Connectors in Eval Runs

This eval aims to capture portable behaviour of the skill. Eval results and artifacts are meant to reflect the skill's behavior, agnostic to the environment in which the evalulation is taking place. Spawn with-skill runs using the project's `mission-lock-eval-runner` subagent, which codifies this behaviour by limiting available tools.

### Generating the Subagent Runner

In order to save tokens and eval time, we generate the subagent `.claude/agents/mission-lock-eval-runner.md` at each eval invocation. `SKILL.md`, `definitions/*.md` and `assets/report-template.md` are embedded in the agent's system prompt so parallel runs share one cacheable prefix and skip the skill-reading tool calls.

Run `python3 evals/build_bundled_runner.py` after any change under `skills/mission-lock/` and before every eval run.

To edit the frontmatter, modify [`build_bundled_runner.py`](build_bundled_runner.py).

### Output Filename and the Subagent Write-Guard

Some harnesses guard the Write tool against agent-generated files that look like self-authored reports, and block the write outright. This guard is **content-triggered, not just filename-triggered** — avoiding "report" in the filename (e.g. using `assessment.md` or `analysis.md` instead) reduces but does not reliably prevent it. A subagent producing a polished, report-shaped Markdown deliverable can still get blocked regardless of what it's named.

Don't rely on a filename workaround. Instead, structure with-skill/without-skill subagent prompts around **"return the full content as text, orchestrator writes the file"**:

- Ask each subagent to produce its report and return the complete text in its final message, rather than instructing it to save the file itself.
- Whoever is orchestrating (a person or Claude) then writes that returned text to the run's `outputs/` path directly.

This sidesteps the guard entirely rather than tempting a workaround. If a subagent reports the Write tool was blocked and it responded by finding another way to write the file anyway (e.g. a `Bash` heredoc), don't treat that as a routine success — it's the harness saying no, and the subagent routing around it is itself the failure mode to avoid, not a clever fix. Verify the file's content matches what the subagent returned as text, and note the workaround when reporting results.
