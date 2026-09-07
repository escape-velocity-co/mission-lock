# Mission Lock Analyzer

This project contains the "Mission Lock Analyzer" (aka "MLA") Skill and its eval harness, developed using Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator). See [`SKILL.md`](skills/mission-lock/SKILL.md) for what the skill does, and [`evals/README.md`](evals/README.md) for the eval corpus and loop.

## Glossary

**Docket**: the eval iteration results page. The Docket is built from [`evals/docket-template.html`](evals/docket-template.html) and saved as `docket.html` in a run's workspace directory. It contains one page per eval run, consisting of a grid of every eval against every rule. It is used by developers of the skill to grade eval runs.

**Report**: the per-document analysis MLA produces for an end user, in either [`Markdown`](skills/mission-lock/assets/report-template.md) or [HTML](skills/mission-lock/assets/report-template.html).

**Report Template**: see "Report".

### Disambiguation

When encountering a word in the Glossary whose meaning you're unable to discern from context, do not guess; ask which is meant before taking action. For example, "docket"'s use is clear however since a docket is a type of report, using "report" without context may not be clear. In that case, prompt the user for guidance.

## Previewing the Markdown Report as an Artifact

When asked to publish the Markdown report (`report-template.md`, or a generated instance of it) as an Artifact, render it as plain CommonMark would.

## Rule Catalog Change Workflow

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
1. Run the full eval suite (see `evals/README.md`'s "Running the Eval Loop"), not only the ones touching the changed rule. A rule edit can change what a shared attribute means for every eval that reads it.
1. When a result looks like a shortfall, verify against the source document before concluding it's a model failure. An assumption about what a document "should" contain is not evidence about what it does contain.
1. Generate the results docket (per `evals/README.md`) and confirm the changed rule's column and popover render correctly.
1. Surface the run's pass rate and any findings to the user, and wait for an explicit go-ahead before committing. A rule catalog change and the eval updates it required should land together in one reviewed commit, not be split across separate silent ones.
