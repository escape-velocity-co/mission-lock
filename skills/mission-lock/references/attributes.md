<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Mission-Lock Attributes

This is the catalog of Mission Lock attributes this skill considers when analyzing a company's governing documents.

## Confidence Requirement

Attribute assessment confidence is necessary to ensure the foundation for later assessments is built with integrity.

This is the most important rule in this file, applying to every Attribute in perpetuity:

  1. Every answer must be definitive.
  1. Never hedge a definitive answer with confidence language (e.g. "close call", "narrow margin").
  1. Never offer a best guess; guessing is not permissable.
  1. If you're uncertain, say "Could not determine."

Before assessing an Attribute, you should be able to point to the sentence or section in the document that supports the answer. If the document's language is unclear, the relevant section is missing, illegible, or you're unsure how to read it then say "Could not determine" and explain why.

## Adding New Attributes

Append a new `###` section following the template below.

```markdown
### <Attribute Name>

**Definition:** One or two sentences defining what this attribute captures.

**Response Options:** The set of results an answer can take (e.g. "Yes / No / Could not determine", or "the exact legal name / Could not determine"). A relatively short list of specifics or types of responses helps ensure greater accuracy.

**What to Look For:** Concrete language patterns, section names, or defined terms that signal the answer.

**Typically Found In:** The documents and location(s) within a document this information typically resides.

**When to Say "Could not determine":** Specific situations in which "Could not determine" is an appropriate response. The general case for "Could not determine" is defined in the "Confidence Requirement" section above.
```

## Attribute Definitions

### Company Name

**Definition:** The entity's exact legal name.

**Response Options:** The exact legal name as written (including suffix, e.g. "Inc.", "Corp.").

**What to Look For:** Usually the first thing stated in the document, often in the introductory paragraph or Article I (e.g. "The name of the corporation is ___").

**Typically Found In:** The opening paragraph or Article I.

**When to Say "Could not Determine":** Only if the document is missing its opening section, or the name is illegible/corrupted in extraction. A name that appears but seems unusual or hard to read cleanly should still be reported as-is with a note, not withheld.

### Public Benefit Corporation (PBC) Status

**Definition:** Whether the company is incorporated as a public benefit corporation (PBC) or equivalent statutory benefit-corporation form, as opposed to a standard for-profit corporation.

**Response Options:** Yes / No.

**What to Look For:** Explicit statutory language — e.g. "...is a public benefit corporation" or a citation to the relevant statute (in Delaware, Subchapter XV / Section 362 of the General Corporation Law). Don't infer PBC status from mission-sounding language elsewhere in the document (e.g. a values statement in a preamble) — it must be the actual statutory designation.

**Typically Found In:** The introductory article, immediately after the company name, or wherever the entity's statutory form is declared.

**When to Say "Could not determine":** When the relevant introductory section is missing, illegible, or genuinely doesn't state the entity's statutory form one way or the other. A document that declares itself a standard corporation under the general corporation law, with no PBC language anywhere, supports a confident "No" — that is not a case for "Could not determine."

### Stated Purpose

**Definition:** The clause defining what the company exists to do.

**Response Options:** A quote or close paraphrase of the purpose clause / Could not determine.

**What to Look For:** Compare boilerplate ("to engage in any lawful act or activity for which corporations may be organized") against a specific, substantive statement of mission or public benefit purpose.

**Typically Found In:** Article II or III, often titled "Purpose" or "Objects."

**When to Say "Could not Determine":** Only when no purpose clause or equivalent article can be located in the document at all. Generic boilerplate language is itself a definitive, reportable answer — quote it as-is. Don't confuse "the purpose clause is generic" (a confident finding) with "I couldn't find a purpose clause" (genuine uncertainty) — these are different answers and should never be conflated.
