---
name: rule-catalog-workflow
description: Checklist to run whenever a Rule in skills/mission-lock/definitions/rules.md is added, edited, or removed. Covers evals.json coverage, SKILL.md's rule-reuse guidance, and the parse/check scripts. Use this before considering any Rule catalog change done.
---

# Rule Catalog Change Workflow

Whenever a Rule in [rules.md](../../../skills/mission-lock/definitions/rules.md) is added, edited, or removed, work through this checklist before considering the change done.

If only the Name of the Rule has changed (i.e. the text after `###` that describes the Rule) you can ignore these steps. That is a cosmetic change that will not affect assessment.

## Adding or Editing a Rule

During this workflow you may discover the corpus lacks a document exercising a needed case. If so, follow the guidance in the "Adding to the corpus" section of [README.md](../../../evals/README.md).

1. Ensure at least one eval in [evals.json](../../../evals/evals.json) exercises the Affirmative case.
1. Ensure at least one eval in [evals.json](../../../evals/evals.json) exercises the Not affirmative case.
1. If the Rule's Affirmative Condition has more than one independent clause, make sure the evals collectively cover a Not-affirmative result for each clause failing on its own.
1. If the Rule shares underlying evidence with an existing Rule (e.g. both read the same Attribute), ensure an eval exists where the two land on different results for the same document.
1. Check for existing evals whose expected results could change (generally, anyone naming or using the result of this Rule directly or transitively). Re-read the source document and re-derive their expected answers.

## Removing a Rule

1. Check every `evals.json` expectation and `expected_output` sentence citing the removed Rule by name or ID. If the expectation or expected output test only that removed Rule, strip it. If it tests more than that Rule, prompt the user for how to proceed.
1. Check `SKILL.md` and all files in the [definitions](../../../skills/mission-lock/definitions/) folder for any mention of the removed Rule by name or ID and prompt the user for how to proceed.

## Always, Regardless of Add / Edit / Remove

1. Run `python3 evals/parse_rules.py` and confirm `rules.md` parses cleanly.
1. Ensure that the `CURRENT_RULE_HEADINGS` list in [check_mechanical_assertions.py](../../../evals/check_mechanical_assertions.py) matches the Rule names in `rules.md`.
1. Consider which portions of the eval suite need to be rerun (see [evals/README.md](../../../evals/README.md)'s "Running the Eval Loop") and rerun only those portions. Any eval that depends on this Rule directly or transitively is a candidate.
1. Generate the results docket (per `evals/README.md`).
1. Surface the run's pass rate and any findings to the user.
1. Wait for an explicit go-ahead before committing.
