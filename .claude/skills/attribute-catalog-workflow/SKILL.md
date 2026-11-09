---
name: attribute-catalog-workflow
description: Checklist to run whenever an attribute in skills/mission-lock/definitions/attributes.md is added, edited, or removed. Covers evals.json coverage, SKILL.md's attribute-reuse guidance, and the parse/check scripts. Use this before considering any Attribute catalog change done.
metadata:
  internal: true
---

# Attribute Catalog Change Workflow

Whenever an Attribute in [attributes.md](../../../skills/mission-lock/definitions/attributes.md) is added, edited, or removed, work through this checklist before considering the change done.

If only the Name of the Attribute has changed (i.e. the text after `###` that describes the Attribute) you can ignore these steps. That is a cosmetic change that will not affect assessment.

## Adding or Editing an Attribute

During this workflow you may discover the corpus lacks a document exercising a needed case. If so, follow the guidance in the "Adding to the corpus" section of [README.md](../../../evals/README.md).

1. Ensure at least one eval in [evals.json](../../../evals/evals.json) exercises a document where the Attribute has an answer (i.e. not a "Could not determine").
1. If the Attribute has a "Could not determine" case, ensure at least one eval exercises it.
1. Ensure at least one eval exercises the case where the answer for this Attribute differs from whatever the "default" or most common answer is elsewhere in the corpus.
1. Check whether any existing Rule in [rules.md](../../../skills/mission-lock/definitions/rules.md) reads the same underlying fact this Attribute captures. If so, that Rule should cite this Attribute's answer via it's ID.
1. Check whether any existing Attribute in [attributes.md](../../../skills/mission-lock/definitions/attributes.md) reads the same underlying fact this Attribute captures. If so, that Attribute should cite this Attribute's answer via it's ID.
1. Update every relevant `evals.json` entry: add the attribute to the "section for every attribute" enumeration in `expectations`, and add a specific value-check assertion for that document.

## Removing an Attribute

1. Strip every `evals.json` expectation and `expected_output` sentence citing the removed Attribute by name or ID.
1. Check `SKILL.md` and all files in the [definitions](../../../skills/mission-lock/definitions/) folder for any mention of the removed Attribute by name or ID and prompt the user for how to proceed.

## Always, Regardless of Add / Edit / Remove

1. Run `python3 evals/parse_attributes.py` and confirm `attributes.md` parses cleanly.
1. Ensure that the `CURRENT_ATTRIBUTES` list in [check_mechanical_assertions.py](../../../evals/check_mechanical_assertions.py) matches the Attribute names in `attributes.md`.
1. Consider which portions of the eval suite need to be rerun (see [evals/README.md](../../../evals/README.md)'s "Running the Eval Loop") and rerun only those portions. Any eval that depends on this Attribute directly or transitively is a candidate.
1. Surface the run's pass rate and any findings to the user.
1. Wait for an explicit go-ahead before committing.
