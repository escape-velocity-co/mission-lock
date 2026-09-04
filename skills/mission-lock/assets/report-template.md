<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

<!--
  mission-lock Markdown report template.

  How to use this file:

  1. Copy this file's full contents as the starting point for the output
     file.
  2. Replace every {{PLACEHOLDER}} token with real content from the
     analysis. Never leave a placeholder token in the output.
  3. Blocks marked "REPEAT" contain one example iteration. Duplicate the
     block once per item (once per rule, once per attribute, once per
     document), in the same order the source reference file lists them,
     then delete the REPEAT/END REPEAT comment lines themselves from the
     output.
  4. Blocks marked "OMIT IF EMPTY" should be removed entirely (heading
     included) if there is nothing to put in them — never render an empty
     list or an empty section.
  5. Insert the disclaimer verbatim, do not paraphrase or shorten it.
  6. {{RULE_RESULT}} (Analysis section only): translate the rule's
     canonical response into reader-facing wording — Affirmative →
     "Mission-lock more likely", Not affirmative → "Mission-lock less
     likely", Could not determine → "Mission-lock uncertain". These are
     the only three values; never invent a fourth. This applies only to
     the Analysis section's per-rule Result field — the Appendix's
     {{ATTRIBUTE_ANSWER}} values are a separate concept (see
     attributes.md) and keep their own response options unchanged.
  7. The prototype banner (the line of 🟡 PROTOTYPE emoji above the
     title) is fixed content, not a placeholder — carry it through
     unchanged, verbatim, on its own line. Remove this whole step, and
     the banner line below, once the skill is out of development.
-->

🟡 PROTOTYPE 🟡 PROTOTYPE 🟡 PROTOTYPE 🟡 PROTOTYPE 🟡 

# Mission Lock Analysis — {{COMPANY_NAME}}

*This report is generated for informational purposes only and does not
constitute legal advice. Corporate governance law varies by jurisdiction
and changes over time. Please consult a licensed attorney before relying
on this analysis for any legal, investment, or governance decision.*

# Analysis

<!-- REPEAT: one block per rule in references/rules.md, in the order they
     appear there. -->
## {{RULE_NAME}}
**Assertion:** {{RULE_POSITIVE_ASSERTION}}

**Result:** {{RULE_RESULT}}

**Evidence:** {{RULE_EVIDENCE}}

**Location:** {{RULE_LOCATION}}
<!-- END REPEAT -->

# Appendix

## Documents Used in this Analysis
<!-- REPEAT: one line per document that was cited as evidence for at
     least one attribute or rule above. The line is {{DOCUMENT_NAME}} and
     nothing else — no trailing clause, dash, or parenthetical of any
     kind after it. -->
- {{DOCUMENT_NAME}}
<!-- END REPEAT -->

<!-- OMIT IF EMPTY: this entire subsection (heading included) if every
     document provided was used in the analysis. Do not show an empty
     "Documents Considered and not Used" list. -->
## Documents Considered and not Used
<!-- REPEAT: one line per document that was reviewed but not cited
     anywhere above — e.g. a bundled exhibit with no mission-lock content.
     The line is {{DOCUMENT_NAME}} and nothing else — no trailing
     clause, dash, or parenthetical explaining why it wasn't used, even a
     short one. If the bare name doesn't convey enough to distinguish it,
     make the name itself more descriptive instead (e.g. "Series A
     Preferred Stock Certificate of Designations" rather than just
     "Exhibit A") — that is the only lever available here, never added
     prose after the name. -->
- {{DOCUMENT_NAME}}
<!-- END REPEAT -->

## Data Points

<!-- REPEAT: one block per attribute in references/attributes.md, in the
     order they appear there. -->
### {{ATTRIBUTE_NAME}}
**Answer:** {{ATTRIBUTE_ANSWER}}

**Evidence:** {{ATTRIBUTE_EVIDENCE}}

**Location:** {{ATTRIBUTE_LOCATION}}
<!-- END REPEAT -->
