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
-->

# Mission Lock Analysis — {{COMPANY_NAME}}

*This report is generated for informational purposes only and does not
constitute legal advice. Corporate governance law varies by jurisdiction
and changes over time. Please consult a licensed attorney before relying
on this analysis for any legal, investment, or governance decision.*

# Analysis

<!-- REPEAT: one block per rule in references/rules.md, in the order they
     appear there. -->
## {{RULE_NAME}}
**Result:** {{RULE_RESULT}}

**Assertion:** {{RULE_POSITIVE_ASSERTION}}

**Evidence:** {{RULE_EVIDENCE}}

**Location:** {{RULE_LOCATION}}
<!-- END REPEAT -->

# Appendix

## Documents Used in this Analysis
<!-- REPEAT: one line per document that was cited as evidence for at
     least one attribute or rule above. -->
- {{DOCUMENT_NAME}}
<!-- END REPEAT -->

<!-- OMIT IF EMPTY: this entire subsection (heading included) if every
     document provided was used in the analysis. Do not show an empty
     "Documents Considered and not Used" list. -->
## Documents Considered and not Used
<!-- REPEAT: one line per document that was reviewed but not cited
     anywhere above — e.g. a bundled exhibit with no mission-lock content.
     There is no field here to explain *why* — keep the name itself clear
     enough to be self-explanatory (e.g. "Series A Preferred Stock
     Certificate of Designations" rather than just "Exhibit A"). -->
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
