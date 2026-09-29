# Mission Lock Analyzer

This project contains the "Mission Lock Analyzer" (aka "MLA") Skill and its eval harness, developed using Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator). See [`SKILL.md`](skills/mission-lock/SKILL.md) for what the skill does, and [`evals/README.md`](evals/README.md) for the eval harness.

## Glossary

**Docket**: the eval iteration results page. The Docket is built from [`evals/docket-template.html`](evals/docket-template.html) and saved as `docket.html` in a run's workspace directory. It contains one page per eval run, consisting of a grid of every eval against every rule. It is used by developers of the skill to grade eval runs.

**Report**: the per-document analysis MLA produces for an end user, in either [`Markdown`](skills/mission-lock/assets/report-template.md) or [HTML](skills/mission-lock/assets/report-template.html).

**Report Template**: see "Report".

### Disambiguation

When encountering a word in the Glossary whose meaning you're unable to discern from context, do not guess; ask which is meant before taking action. For example, "docket"'s use is clear however since a docket is a type of report, using "report" without context may not be clear. In that case, prompt the user for guidance.

## Previewing the Markdown Report as an Artifact

When asked to publish the Markdown report (`report-template.md`, or a generated instance of it) as an Artifact, render it as plain CommonMark would.

## Report Template Change Workflow

Whenever a rule's or attribute's write-up fields change in `report-template.md` or `report-template.html`:

1. Check `docket-template.html`'s for every field name that changed.
1. Update all of them together in the same change.
1. Remove mentions of fields no longer present.
1. Regenerate the current iteration's `docket.html` from the corrected template.

## Assessment Catalog Change Workflow

Whenever a rule in [`skills/mission-lock/references/rules.md`](skills/mission-lock/references/rules.md) is added, edited, or removed, work through this checklist before considering the change done.

### Adding a Rule

1. Ensure at least one eval in `evals/evals.json` exercises the Affirmative case.
1. Ensure at least one eval in `evals/evals.json` exercises the Not affirmative case.
1. If the rule's Affirmative Condition has more than one independent clause (e.g. M3's "PBC-or-equivalent status" *and* "directors permitted/required to prioritize"), make sure the evals collectively cover a Not-affirmative result for **each clause failing on its own** (i.e. not the same failure mode twice). A two-condition rule with only one tested failure path has an would not constitute a verified Condition.
1. If the corpus has no document that exercises a needed case, you're permitted to pull documents from SEC EDGAR's full-text search (see `evals/README.md`'s "Adding to the corpus" section for fetch etiquette). Create synthetic fixtures only for scenarios no public filing can demonstrate (e.g. an unresolvable draft conflict).
1. If the new rule shares underlying evidence with an existing rule (both read the Stated Purpose attribute, both depend on PBC status, etc.), add or confirm an eval where the two rules land on **different** results for the same document. Two rules that always co-vary across the whole corpus is not evidence they're assessed independently — it's equally consistent with one being silently copied from the other. For example, the Meridian Robotics eval: M1 and M2 don't require PBC status, M3 does, and the corpus needed a document where that split actually shows up.

### Editing a Rule

1. For every existing eval whose expected result could plausibly change under the new wording, re-read the source document and re-derive the expected answer. Don't assume the previous expectations still hold, and don't assume what one document contains transfers to a similar-looking one.
1. Update every `evals.json` expectation that names the rule — including `expected_output` prose, not just the `expectations` array.
1. Check `skills/mission-lock/SKILL.md` for any rule-specific example (e.g. the "reuse an attribute answer instead of re-deriving it" example) that names this rule. If the edit changes which attribute the rule depends on, or whether it depends on one at all, the example may now be wrong.

### Removing a Rule

1. Strip every `evals.json` expectation and `expected_output` sentence naming the removed rule, across every eval, including evals that are not "about" the edited rule.
1. Check `skills/mission-lock/SKILL.md` and `evals/docket-template.html`'s instructions comment for any mention of the removed rule by name or ID.

### Always, Regardless of Add / Edit / Remove

1. Run `python3 evals/parse_rules.py` and confirm `rules.md` still parses cleanly, e.g. malformed bullet or missing fields.
1. Check [`evals/check_mechanical_assertions.py`](evals/check_mechanical_assertions.py)'s `CURRENT_RULE_HEADINGS` list matches the current rule names in `rules.md`. A stale list doesn't error or fail loudly — it just silently stops checking for whatever changed, which is worse than a loud failure since nothing draws attention to the gap.
1. Run the full eval suite (see `evals/README.md`'s "Running the Eval Loop"), not only the ones touching the changed rule. A rule edit can change what a shared attribute means for every eval that reads it.
1. When a result looks like a shortfall, verify against the source document before concluding it's a model failure. An assumption about what a document "should" contain is not evidence about what it does contain.
1. Generate the results docket (per `evals/README.md`) and confirm the changed rule's column and popover render correctly.
1. Surface the run's pass rate and any findings to the user, and wait for an explicit go-ahead before committing. A rule catalog change and the eval updates it required should land together in one reviewed commit, not be split across separate silent ones.

## Attribute Catalog Change Workflow

Whenever an attribute in [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md) is added, edited, or removed, work through this checklist before considering the change done.

### Adding an Attribute

1. Ensure at least one eval in `evals/evals.json` exercises a document where the attribute has a clear, determinate answer.
1. Ensure the corpus includes at least one document whose answer for this attribute genuinely differs from whatever the "default" or most common answer is elsewhere in the corpus (e.g. a non-Delaware jurisdiction, when most of the corpus is Delaware). Without that contrast, there's no way to tell a model that actually read the attribute from one that just defaulted to the common case out of habit.
1. If the attribute has a genuine "Could not determine" case (e.g. conflicting values across multiple documents, or the attribute being altogether absent), ensure at least one eval exercises it, with Evidence that names the specific conflicting or missing language rather than a vague "could not determine."
1. Check whether any existing rule in `rules.md` reads the same underlying fact this attribute now captures. If so, per `SKILL.md`'s attribute-reuse instruction, that rule should cite this attribute's answer instead of re-deriving the fact independently — update `SKILL.md`'s rule-walking guidance to name the new attribute as a reuse target if appropriate.
1. Update every relevant `evals.json` entry: add the attribute to the "section for every attribute" enumeration in `expectations`, and add a specific value-check assertion for that document.
1. Check `skills/mission-lock/assets/report-template.md` and `report-template.html` for whether their Data Points block needs anything new for this attribute (it's meant to be generic enough to add a section per current attribute automatically — confirm that's still true rather than assuming it).

### Editing an Attribute

1. For every existing eval whose expected value for this attribute could plausibly change under the new definition, re-read the source document and re-derive the expected answer. Don't assume the previous expectations still hold, and don't assume what one document contains transfers to a similar-looking one.
1. Update every `evals.json` expectation that names the attribute — including `expected_output` prose, not just the `expectations` array.
1. Check `SKILL.md` and `rules.md` for any rule that reuses this attribute's answer (per the attribute-reuse instruction) — if the edit changes what the attribute answers, or how confidently, the dependent rule's reasoning may now be wrong too.

### Removing an Attribute

1. Strip every `evals.json` expectation and `expected_output` sentence naming the removed attribute, across every eval.
1. Check `SKILL.md` for any mention of the removed attribute by name or ID, and check `rules.md` for any rule that named it as a reuse target.
1. Check `report-template.md`/`report-template.html` for placeholders tied to this attribute.

### Always, Regardless of Add / Edit / Remove

1. Run `python3 evals/parse_attributes.py` and confirm `attributes.md` parses cleanly.
1. Check [`evals/check_mechanical_assertions.py`](evals/check_mechanical_assertions.py)'s `CURRENT_ATTRIBUTES` list matches the current attribute names in `attributes.md`.
1. Run the full eval suite (see `evals/README.md`'s "Running the Eval Loop").
1. Surface the run's pass rate and any findings to the user, and wait for an explicit go-ahead before committing. An attribute catalog change and the eval updates it required should land together in one reviewed commit, not be split across separate silent ones.

## Packaging the Skill

Packaging is performed via Anthropic's "skill-creator" skill.

  1. Package the contents of `skills/mission-lock/`.
  1. Package from the `skill-creator` plugin's `skills/skill-creator/` directory:
  
  ```
  python3 -m scripts.package_skill /path/to/skills/mission-lock /path/to/mission-lock/dist
  ```
  3. Rename the output file to `mla-<version>.skill` where `<version>` is the value from `SKILL.md`'s `metadata.version` field.
  1. Place the output file in `dist/` at the repo root.

## Maintaining the Changelog

[`CHANGELOG.md`](CHANGELOG.md) tracks what's changed between versions.

1. Add a bullet under `[Unreleased]` for any notable change as it's made (new/edited/removed rule or attribute, report format change, eval harness change, etc.). *Only add bullets for notable changes; not for every commit.*
1. When `metadata.version` is bumped: rename `[Unreleased]` to the new version (adding today's date) and start a fresh empty `[Unreleased]` above it.
1. When `metadata.version` is bumped: rename `evals/benchmarks/versions/unreleased/` to `evals/benchmarks/versions/<new-version>/`, add a row for that version to `evals/benchmarks/history.md`, and start a new `unreleased/` snapshot from the next eval suite run.
