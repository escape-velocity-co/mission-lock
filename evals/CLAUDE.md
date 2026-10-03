# Eval Harness

Corpus structure, formats, and the operational rules Claude follows when working with the eval suite.

## Structure

```
evals/
├── evals.json                                # test prompts and expectations
├── documents/
│   ├── <company-slug>-cert-of-incorporation/ # documents, per company
│   │   ├── <extracted-exhibit-file>.txt      # plain-text extraction of source docs (for optimization)
│   │   └── metadata.json
│   └── <company-slug>-synthetic-<scenario>/  # fixtures, per company
│       ├── <document>.txt                    # plain-text fixtures
│       └── metadata.json
├── benchmarks/                               # timing history; see benchmarks/README.md
│   ├── README.md
│   ├── history.md
│   ├── scripts/                              # utilities to capture timings
│   └── versions/<version>/                   # timing snapshots for posterity
├── docket-template.html                      # template for the per-run results docket
├── extract_text.py                           # .htm/.txt exhibit -> plain-text extraction
├── build_bundled_runner.py                   # generates .claude/agents/mission-lock-eval-runner.md
├── check_mechanical_assertions.py            # mechanical assertion checks
├── parse_attributes.py                       # processes/validates attributes.md
└── parse_rules.py                            # processes/validates rules.md
```

## Adding a Document to the Corpus

1. Find a Certificate/Articles of Incorporation on [SEC EDGAR full text search](https://www.sec.gov/edgar/search/).
1. When querying `sec.gov`/`efts.sec.gov`, send a `User-Agent` header with a contact email, and keep request rates low.
1. Save the downloaded `.htm` under `documents/<company-slug>-cert-of-incorporation/`.
1. Extract the plain text via `python3 extract_text.py documents/<company-slug>-cert-of-incorporation/<file>.htm`.
1. Delete the `.htm` file.
1. Create `metadata.json` under `documents/<company-slug>-cert-of-incorporation/` (see format guidance below).
1. Add or update the corresponding entry in `evals.json`, referencing the `.txt` file.

### `metadata.json` Format

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

## Test Creation

Tests are created following the pattern from Anthropic's `skill-creator`. Prompts and expectations are present in [evals.json](evals.json), as well as the documents those prompts are evaluating. See the eval schema (`references/schemas.md` in [anthropics/skills](https://github.com/anthropics/skills)) for the full spec.

### Guidance for Creating Prompts and Expectations

Tests should validate assessments via report generation, as that provides a standard output format across a variety of charters. At the moment, tests should not be written to validate conversational requests. We trust that responding to those requests will be handled adequately at query time, given the skill will have been validated against retrieving the underlying information, accurately and consistently.

* Every eval prompt should read as a variation on a request for the report.
* An eval prompt can motivate why the user is asking, to retain the conversational interaction style.
* An eval prompt should not explicitly name or request a narrower slice of the report.
* When drafting an eval's `expected_output` or `expectations`, ensure any reasoning is based in facts the source document states.

## Running the Eval Loop

### Step 1 - Generate the Subagent Runner

In order to save tokens and eval time, we generate the subagent declaration `.claude/agents/mission-lock-eval-runner.md` at each eval invocation. It bundles context into the subagent system prompt so they don't have to all rediscover that context. The subagent runner also codifies our desire to test in a sandbox sans connectors, to maximize portability of the skill. Additionally, it decides on the model such that we can track performance changes over time.

Run `python3 evals/build_bundled_runner.py` after any change under `skills/mission-lock/` and before every eval run.

### Step 2 - Run the Eval Suite

#### Workspace Setup

Create a new `skills/mission-lock-workspace/iteration-<N>/` directory (gitignored), where `<N>` is the next unused iteration number. For each eval, create:

- `eval-<name>/eval_metadata.json`, built from that eval's `evals.json` entry: `id` becomes `eval_id`, `expectations` becomes `assertions`, and `eval_name` is added. Reuse an existing eval's `<name>` slug from the previous iteration; choose a short descriptive one for a new eval.
- `eval-<name>/with_skill/run-1/outputs/`, where the orchestrator writes each run's `report.md`. A requested without-skill run uses `without_skill/run-1/outputs/` instead.

#### Running the Evals

Use the workflow documented in Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill. Point it at this repo's `skills/mission-lock/` and `evals/` directories.

Every run is a with-skill run, one per eval in `evals.json`, using the `mission-lock-eval-runner` subagent. Without-skill baseline runs are only done on request.

#### Output Filename and the Subagent Write-Guard

Structure with-skill/without-skill subagent prompts around **"return the full content as text, orchestrator writes the file"**:

- Ask each subagent to produce its report and return the complete text in its final message, rather than instructing it to save the file itself.
- Whoever is orchestrating then writes that returned text to the run's `outputs/` path directly.

#### Timing

As each with-skill run completes, capture its timing (see [`benchmarks/README.md`](benchmarks/README.md)) before moving on; the data comes from the completion notification and isn't recoverable later.

### Step 3 - Grading

Claude grades each run's `report.md` against that eval's assertions and writes the results to `grading.json` alongside it, with `text`, `passed` and `evidence` for each assertion. The docket and timing roll-up build on these files.

#### Structural Checks

Before grading a `report.md` against an eval's assertions, run `check_mechanical_assertions.py` against it:

`python3 evals/check_mechanical_assertions.py <path/to/report.md> --eval-id <N>`

#### Judgment-Based Assertions

The script reports every assertion it can't check mechanically as "not automated". Grading is complete when each of those has been read against the report and the source document, and has a pass/fail verdict backed by evidence.

#### Identifying Failures

A run is a failure when its results diverge from an eval's `expectations` in one or more of the following ways:

* The result itself is wrong
* The result is unsupported by any evidence
* The result is "hedged" (inconclusively written)

If the result is correct and with evidence but has been returned in an unexpected way, ask the user. Historically this tends to mean that the assertion needs to be re-examined.

### Step 4 - Results

#### Generate the Docket

After every eval run is graded, generate the results docket. This is a standing deliverable of running the eval suite, not a one-off request; produce it without being asked.

Follow the instructions in [`docket-template.html`](docket-template.html)'s header comment. Save the result as `docket.html` in that run's workspace directory (e.g. `skills/mission-lock-workspace/iteration-<N>/docket.html`), then show it to the user rather than only reporting a pass/fail table in chat.

#### Roll Up Timing

Once the run is graded, roll up the per-run timing captured in Step 2. See [`benchmarks/README.md`](benchmarks/README.md) for instructions on how to maintain the benchmarks.
