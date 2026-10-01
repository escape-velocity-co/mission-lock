<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Mission-Lock Attributes

This is the catalog of Mission Lock attributes this skill considers when analyzing a company's governing documents.

## Confidence Requirements and Conflict Resolution

Confidence requirements and  and conflict resolution guidelines are present in [confidence-requirement.md](confidence-requirement.md). As these are likely to update over time as new types of confidence and conflicts surface, you should read this file at each usage; do not rely on memory of it.

## Adding New Attributes

Append a new `###` section following the template below.

```markdown
### <Attribute Name>

**ID:** Identifier used to cross-reference attributes.

**Definition:** One or two sentences defining what this attribute captures.

**Response Options:** The set of results an answer can take (e.g. "Yes / No / Could not determine", or "the exact legal name / Could not determine"). A relatively short list of specifics or types of responses helps ensure greater accuracy.

**What to Look For:** Concrete language patterns, section names, or defined terms that signal the answer.

**Typically Found In:** The documents and location(s) within a document this information typically resides.

**Could not Determine:** This is an optional template field that catalogs **specific** scenarios in which "Could not determine" is an appropriate response. The **general** scenarios for "Could not determine" are defined in the "Confidence Requirement" section above.
```

## Attribute Definitions

### Company Name

**ID:** A1

**Definition:** The entity's exact legal name.

**Response Options:** The exact legal name as written (including suffix, e.g. "Inc.", "Corp.").

**What to Look For:** Usually the first thing stated in the document, often in the introductory paragraph or Article I (e.g. "The name of the corporation is ___").

**Typically Found In:** The opening paragraph or Article I.

### Public Benefit Corporation Status

**ID:** A2

**Definition:** Whether the company is incorporated as a public benefit corporation (PBC) or equivalent statutory benefit-corporation form, as opposed to a standard for-profit corporation.

**Response Options:** Yes / No.

**What to Look For:** Explicit statutory language — e.g. "...is a public benefit corporation" or a citation to the relevant statute (in Delaware, Subchapter XV / Section 362 of the General Corporation Law). Don't infer PBC status from mission-sounding language elsewhere in the document (e.g. a values statement in a preamble) — it must be the actual statutory designation.

**Typically Found In:** The introductory article, immediately after the company name, or wherever the entity's statutory form is declared.

### Stated Purpose

**ID:** A3

**Definition:** The clause defining what the company exists to do.

**Response Options:** A quote or close paraphrase of the purpose clause / Could not determine.

**What to Look For:** Compare boilerplate ("to engage in any lawful act or activity for which corporations may be organized") against a specific, substantive statement of mission or public benefit purpose.

**Typically Found In:** Article II or III, often titled "Purpose" or "Objects."

**Could not Determine:** When no purpose clause or equivalent article can be located in the document at all.

### Governing Jurisdiction

**ID:** A4

**Definition:** The US state, or similar granularity of jurisdiction outside of the US, under whose corporate statute the company is incorporated.

**Response Options:** The exact jurisdiction as stated (e.g. "Delaware") / Could not determine.

**What to Look For:** A statement of incorporation in the introductory paragraph (e.g. "a Delaware corporation," "organized and existing under the laws of the State of ___"); a citation to the state's corporate statute (e.g. "the General Corporation Law of the State of Delaware"); a Secretary of State (or equivalent) filing stamp or certification page naming the jurisdiction.

**Typically Found In:**
* Certificate/Articles of Incorporation
* Filing stamp
* Certification page
* Statutory citation

**Could not Determine:** When no statement of incorporation, statutory citation, or filing stamp naming a jurisdiction appears anywhere in the open documents. A registered agent's address alone is not evidence of jurisdiction.

### Supermajority/Veto Requirements for PBC/Purpose Article(s) Amendments

**ID:** A5

**Definition:** Whether amending, altering, repealing, or waiving the article(s) that state the corporation's PBC status or purpose (A2, A3 respectively) requires greater than the amendment default (e.g. DGCL §242 if A4 is Delaware) in the relevant jurisdiction's (A4) statute.

**Response Options:**
* Yes (Specifically) - When the amendment is covered specifically by an increased threshold. Respond with a concise quote or close paraphrase of the elevated threshold and the voting group it applies to
* Yes (Generally) - When the amendment is covered generally by an increased threshold. Respond with a concise quote or close paraphrase of the elevated threshold and the voting group it applies to
* No — the article is amendable at the jurisdiction's ordinary default
* Could not determine - (see below for possible scenarios)

**What to Look For:** An elevated-vote provision (above the jurisdiction's ordinary amendment default) that reaches the article(s) already identified by A2 and A3. It shows up in one of two shapes, which is what distinguishes the two "Yes" response options above:
* **Yes (Specifically):** the clause names which article(s) it protects — e.g. "the affirmative vote of at least [X]%... shall be required to amend, alter, or repeal Articles III, V, VI..." — and the article(s) already identified by A2/A3 are among those named.
* **Yes (Generally):** the clause reaches every provision of the certificate with no named-article list and no carve-out — e.g. "...shall be required to amend, alter, or repeal any provision of this Certificate of Incorporation," or a separate-class protective-provision veto (a "Preferred Majority" or "Requisite Investors" consent right) phrased as "shall not... amend this corporation's Certificate of Incorporation or Bylaws" with no qualifying language. Because it reaches everything with no exception, it exceeds the ordinary default for the PBC/purpose article too, even though it wasn't drafted with that article specifically in mind.

Distinguish either of these from a separate-class vote that only triggers when an amendment adversely affects that class's own rights or preferences (e.g. "...in a manner that adversely affects the powers, preferences or rights of the Series X Preferred Stock") — that narrower, conditioned form doesn't reach an unrelated purpose/PBC article and doesn't by itself satisfy A5.

**Typically Found In:** Certificate of Incorporation, usually in the same article as the general amendment-reservation clause, or in a dedicated protective-provisions article.

**Could not Determine:** When the certificate's amendment mechanics reference an external document and that document wasn't provided.

### Supermajority/Veto Requirements for Mergers, Consolidations, or Reorganizations

**ID:** A6

**Definition:** Whether approving a merger, consolidation, reorganization, or sale/lease/exchange of substantially all assets requires greater than the jurisdiction's ordinary default (e.g. DGCL §251/§271 if A4 is Delaware) in the relevant jurisdiction's (A4) statute.

**Response Options:**
* Yes — the clause names merger, consolidation, reorganization, or a sale/lease/exchange of substantially all assets as requiring an elevated threshold or separate consent. Respond with a concise quote or close paraphrase of the elevated threshold and the voting group it applies to.
* No — these transactions are approvable at the jurisdiction's ordinary default
* Could not determine — (see below for possible scenarios)

**What to Look For:** An elevated-vote or separate-consent provision that names merger, consolidation, reorganization, or a sale/lease/exchange of substantially all assets directly — often via a defined term such as "Liquidation Event," "Change in Control Transaction," or a DGCL §203-style "Business Combination." The term alone isn't enough if it's paired only with a proceeds-allocation rule rather than an actual "shall not consummate without [vote/consent]" requirement — only the latter satisfies this attribute.

**Typically Found In:** Certificate of Incorporation, in a protective-provisions article or a dedicated "Mergers, Consolidations, and Sales of Assets" article.

**Could not Determine:** When the certificate's merger/reorganization-approval mechanics reference an external document and that document wasn't provided.
