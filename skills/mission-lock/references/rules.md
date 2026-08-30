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

Append a new `###` section following the template below.

There is no "Response Options" field in the template.  Whereas [`skills/mission-lock/references/attributes.md`](skills/mission-lock/references/attributes.md) defines different response options per Attribute, Rules response options are the same for all Rules:

  * Affirmative
  * Not affirmative
  * Could not determine

```markdown
### Rule Name

**Positive Assertion:** What can be stated if evidence is found to support the Rule Name.

**Question:** What question this answers about the company.

**Affirmative Condition:** What condition(s) is/are required for this rule check to succeed.

**Categories of Evidence:** Examples of items whose presence would construe evidence of this making this assertion.

**Typically Found Location:** The documents and location(s) within a document this information typically resides. Legal documents are relatively standard and most information will be where we expect. 

**When to say "Could not determine:"** This presence of this in the template is optional. It is provided when conditions exist in the governance documents such that it is not possible for this skill to make an assertion.
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

### Paramount Purpose

**Positive Assertion:** Purpose is paramount in the constitutional documents.

**Question:** Is the mission legally binding, or merely aspirational?

**Affirmative Condition:** PBC or an equivalent legal form in the relevant jurisdiction. The stated purpose appears in the constitutional documents, and directors are permitted or required to prioritize it.

**Categories of Evidence:** Filed charter / articles of association

**Typically Found Location:** Articles of Incorporation

**When to say "Could not determine:"** You cannot locate a mission of any sort, or the document is missing, illegible, or truncated where the mission would be. Note that a mission whose wording is vague is not a case for "Could not determine" — apply the binding bar above and answer definitively.

### Mission Protection from Ordinary Majority

**Positive Assertion:** No ordinary majority can override the mission.

**Question:** Who can say no when everyone else says yes?

**Affirmative Condition:** Satisfied by any of the following:
  * A distinct lock-holding body - trust, foundation, golden share, employee ownership trust, cooperative member body - holding real power and owing a duty to the purpose;
  * A constitutionally distributed lock, where binding provisions sit across a federated or member constitution and cannot be amended by simple majority. Route (b) must be DEMONSTRATED provision by provision, not asserted

Advisory bodies satisfy none of the above.

**Categories of Evidence:** Charter, share class terms, trust deed, federation constitution and member bylaws, charter amendment/entrenchment provisions and the vote thresholds they set

**Typically Found Location:** Articles of Incorporation, particularly the amendment article (often titled "Amendment" or near the end of the document) and any article addressing supermajority voting requirements
