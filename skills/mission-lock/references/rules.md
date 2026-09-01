<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Mission-Lock Rules

This is the catalog of "Mission Lock" rules this skill checks for when analyzing a company's governing documents. These rules may make use of attributes defined in [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md).

## Confidence Requirements and Conflict Resolution

Confidence requirements and conflict resolution guidelines are present in [confidence-requirement.md](confidence-requirement.md). As these are likely to update over time as new types of confidence and conflicts surface, you should read this file at each usage; do not rely on memory of it.

## Adding New Rules

Append a new section to "Rule Definitions" following the template below.

There is no "Response Options" field in the template.  Whereas [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md) defines different response options per Attribute, Rules response options are the same for all Rules:

  * Affirmative
  * Not affirmative
  * Could not determine

```markdown
### Rule Name

**ID:** Identifier used to cross-reference rules.

**Query:** What question does this analysis answer?

**Affirmative Condition:** What condition(s) is/are required for this rule check to succeed.

**Categories of Evidence:** Examples of items whose presence would construe evidence of this making this assertion.

**Typically Found Location:** The documents and location(s) within a document this information typically resides. Legal documents are relatively standard and most information will be where we expect. 

**When to say "Could not determine:"** This presence of this in the template is optional. It is provided when conditions exist in the governance documents such that it is not possible for this skill to make an assertion.
```

## Rule Definitions

### Mission Beyond Financial Profit

**ID:** M1

**Query:** Does a mission with more than financial benefits exist?

**Affirmative Condition:** 
* A purpose is stated in a durable document
* The purpose is not the jurisdiction's default any-lawful-purpose formulation
* The purpose Is not solely financial return
* The purpose identifies who or what benefits beyond the owners
* You are not considering whether or not it is a ""good"" mission

**Categories of Evidence:**
* Stated mission
* Named beneficiary class

**Typically Found Location:** 
Articles of Incorporation
