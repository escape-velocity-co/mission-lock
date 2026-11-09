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
* You are not considering whether or not it is a "good" mission

**Categories of Evidence:**
* Stated mission
* Named beneficiary class

**Typically Found Location:** 
* Articles of Incorporation

### Mission Breachability

**ID:** M2

**Query:** Can mission pursuit and violation be easily identified?

**Affirmative Condition:** 
* The mission is written so that it can be contradicted. It identifies a domain and a direction, and a course of conduct exists that would run against it.
* A mission that cannot be breached is not acceptable.
* You are not considering whether or not it is a "good" mission.

**Categories of Evidence:**
* Stated mission
* Named beneficiary class

**Typically Found Location:** 
* Articles of Incorporation

### Mission is Paramount

**ID:** M3

**Query:** Are Directors permitted or required to pursue the mission?

**Affirmative Condition:** 
* PBC-or-equivalent legal designation in the relevant jurisdiction, that allows for the prioritization of the mission described in M1.
* PBC-or-equivalent election must be made in the certificate of incorporation itself.
* Merely stating that directors are required or permitted to prioritize the mission, without the statutory election, does not satisfy this condition.

**Categories of Evidence:**
* Statutory definition allowing prioritization of mission

**Typically Found Location:** 
* Articles of Incorporation

### Mission Entrenchment Against Ordinary-Majority Amendment

**ID:** M4

**Query:** Does amending or removing the mission-related provisions (stated purpose, PBC-or-equivalent status, or any director mission-prioritization provision) require a two-thirds-or-greater shareholder vote, rather than being changeable by an ordinary-majority override?

**Affirmative Condition:**
* A mission-related provision exists: a stated purpose beyond the jurisdiction's default any-lawful-purpose formulation, a PBC-or-equivalent statutory election, or a director mission-prioritization provision. (In Delaware, the statutory election that also satisfies Mission is Paramount (M3) is the same provision that authorizes director prioritization, so a clause protecting the PBC-status article protects both at once — a separately named "benefit-director" article is not required.)
* An elevated-vote provision reaches the article(s) stating that content. Reuse the Amendment Supermajority Requirements attribute's answer for this: it must read "Yes (Specifically)," naming the article(s) in question, or "Yes (Generally)," a blanket clause with no carve-out that by that attribute's own definition reaches every article.
* The elevated threshold itself, as quoted or paraphrased in that attribute's evidence, is two-thirds (66⅔%) or greater of the shares or voting power entitled to vote generally — not merely "above the jurisdiction's ordinary default" if that margin still falls short of two-thirds, and not a majority confined to a single class or defined subset of shareholders (e.g. a "Preferred Majority" or "Requisite Investors" consent right defined as a majority of one series or class) standing in for an overall supermajority of the whole shareholder base.
* You are not considering how hard the threshold would be to assemble in practice, who currently holds enough shares to trigger or block it, or whether the entrenchment is "good" policy — only what the document's own amendment mechanics require.

**Categories of Evidence:**
* Amendment Supermajority Requirements attribute's quoted elevated-vote clause, its voting group, and whether it names the mission-related article(s) or sweeps in every provision
* The specific fraction or percentage the clause specifies, or, for a defined consent-right term (e.g. "Preferred Majority"), that term's own definition and the class it is confined to

**Typically Found Location:** 
* Certificate of Incorporation, usually in the same article as the general amendment-reservation clause, or in a dedicated protective-provisions article

**When to say "Could not determine:"**
* When the Amendment Supermajority Requirements attribute itself is "Could not determine"
* When an elevated-vote clause reaches the mission-related article but uses an undefined term for the required vote (e.g. "supermajority") without stating or cross-referencing an actual fraction, so whether it meets or exceeds two-thirds cannot be confirmed or ruled out
