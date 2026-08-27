<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Mission-Lock Rules

This is the catalog of "Mission Lock" rules this skill checks for when analyzing a company's governing documents. These rules may make use of attributes defined in [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md).

## Confidence Requirement

This is the most important assessment instruction in this file, applying to every Rule in perpetuity:

  1. Every answer must be definitive.
  1. Never offer a best guess; guessing is not permissable.
  1. If you're uncertain, say "Could not determine."

Before assessing a Rule, you should be able to point to the sentence or section in the document that supports the answer. If the document's language is unclear, the relevant section is missing, illegible, or you're unsure how to read it then say "Could not determine" and explain why.

Whereas [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md) defines different response options per Attribute, Rules response options are universal:

  * Affirmative
  * Not affirmative
  * Could not determine

## Adding New Rules

Append a new `###` section following the template below.

```markdown
### Rule Name

**Positive Assertion:** What can be stated if evidence is found to support the Rule Name.

**Question:** What question this answers about the company.

**Affirmative Condition:** What condition(s) is/are required for this rule check to succeed.

**Categories of Evidence:** Examples of items whose presence would construe evidence of this making this assertion.

**Typically Found Location:** The documents and location(s) within a document this information typically resides. Legal documents are relatively standard and most information will be where we expect. 

**When to say "Could not determine:"** What condition(s) exist such that it is not possible for this skill to make an assertion.
```

## Rule Definitions

### Mission Existence and Breachability

**Positive Assertion:** A mission exists, is stated, and is specific enough to be breached.

**Question:** Is there a mission at all, in a form anyone could hold the company to?

**Affirmative Condition:**
  * A mission is stated in a durable document, identifies who benefits, and is specific enough that a breach of it could be identified by a third party. A mission naming no activity and no beneficiary, for example "any lawful act or activity", excludes no conduct and therefore cannot be departed from.
  * A breachable mission does not require metrics, thresholds, measurement periods, reporting obligations, third-party certification, or definitions of the evaluative words inside the mission itself.
  * You are not considering whether or not it is a "good" mission. A mission that cannot be breached is not a mission.

**Categories of Evidence:** Stated mission; assessor's breach-identification test; named beneficiary class

**Typically Found Location:** Articles of Incorporation

**When to say "Could not determine:"** You cannot locate a mission of any sort, or the document is missing, illegible, or truncated where the mission would be. Note that a mission whose wording is vague is not a case for "Could not determine" — apply the breachability bar above and answer definitively.