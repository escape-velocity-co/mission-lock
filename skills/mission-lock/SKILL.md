---
name: mission-lock
description: Analyzes a company's articles of incorporation or certificate of incorporation for "mission lock" — both factual attributes (currently the company's legal name, whether it's incorporated as a public benefit corporation (PBC), and its stated purpose clause) and rules (compound checks like whether a specific, third-party-breachable mission exists at all) — each answered definitively or explicitly flagged as undeterminable, never guessed. This is a deliberately small, trust-first starting catalog (see references/attributes.md and references/rules.md) that will grow over time. Use this whenever the user provides or references articles of incorporation, a certificate of incorporation, corporate charter, or formation documents (PDF, DOCX, plain text, or pasted content) and wants to know its PBC status, purpose clause, whether it has a real/breachable mission, or basic entity facts — even if they don't say "mission lock" explicitly. This produces analytical, descriptive output only — it does not score, rate, or recommend.
---

<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Mission Lock

Analyze a company's articles/certificate of incorporation and report a
definitive answer for each "mission lock" attribute in the catalog, using
neutral, descriptive language.

**This skill is strictly analytical, not evaluative.** Never assign a score,
rating, verdict ("strong"/"weak" mission lock), or recommendation. The job is
to report what the document says and let the reader draw their own
conclusions. If a finding could be read as praise or criticism, rewrite it in
neutral terms (e.g. "requires a two-thirds vote to amend Article III" rather
than "has strong protection against amendment").

**Never guess.** Every attribute or rule answer must be definitive and
traceable to specific document text, or it must say "Could not determine"
and explain why. This matters more than it might seem: the catalogs start
small and simple deliberately, and more complex checks will only be added
once the simple ones are proven reliable. A confident wrong answer (or a
guess dressed up as a finding) on an easy check undermines trust in
everything this skill will eventually be asked to evaluate. See the
"Confidence Requirement" section at the top of both
[references/attributes.md](references/attributes.md) and
[references/rules.md](references/rules.md) for the full rule.

**Attributes vs. rules — a distinction worth keeping straight:**
`references/attributes.md` holds pure fact-extraction (a name, a yes/no, a
quoted clause) — no interpretive judgment beyond reading the document.
`references/rules.md` holds compound checks that require judgment to apply
(e.g. "is the stated purpose specific enough that a third party could
identify a breach of it") but stay strictly non-evaluative about *quality*
— a rule may ask whether a mission is specific enough to be breached, never
whether it's a *good* mission. Don't let rule assessments drift into rating
how good, strong, or admirable something is — that line matters as much for
rules as it does for attributes.

## Workflow

1. **Get the source document.** Accept whatever the user provides — PDF,
   DOCX, plain text, or pasted content.

   - **PDF:** If a dedicated PDF skill is available in this environment, use
     it to extract the text — it will typically handle multi-page layout and
     OCR for scanned pages more reliably than ad hoc parsing. Otherwise,
     extract text directly (e.g. with a PDF text-extraction library). Either
     way, extract the *complete* document before analysis — articles of
     incorporation are usually short (a handful of pages), so there's rarely
     a reason to sample or truncate.
   - **DOCX:** If a dedicated DOCX skill is available, use it. Otherwise,
     extract the document body text directly (e.g. with a DOCX-parsing
     library), including any numbered headings — they're often the article/
     section references you'll cite in the report.
   - **Scanned PDFs with no text layer:** If extraction comes back empty or
     garbled and no OCR capability is available, say so explicitly and ask
     the user for OCR'd text or a text-based copy rather than guessing at
     content from a blank or corrupted extraction.

2. **Walk the attribute catalog.** Read
   [references/attributes.md](references/attributes.md) for the current
   list of mission-lock attributes — it starts deliberately small (currently
   just company name, PBC status, and stated purpose) and is expected to
   grow over time, so always read the reference file fresh rather than
   relying on memory of it. For each attribute:
   - Give a definitive answer using that attribute's specific "Answer
     options" (see the reference file) — or "Could not determine" if you
     can't support an answer with specific document text. Read each
     attribute's "When to say Could not determine" guidance carefully: a
     confident negative or "this is generic boilerplate" is a valid,
     definitive answer and should NOT be reported as "Could not determine."
   - Quote or closely paraphrase the relevant language as evidence, with an
     article/section reference if the document has numbered sections.
   - Every attribute gets reported, even if the answer is "Could not
     determine" — never silently skip one.

3. **Walk the rule catalog.** Read
   [references/rules.md](references/rules.md) fresh for the current list of
   rules. For each rule:
   - Answer the rule's stated "Question" using the universal response
     options defined at the top of `rules.md` — read them there rather than
     assuming them, since that file is the authority. As of this writing
     they are Affirmative / Not affirmative / Could not determine. Note that
     "Not affirmative" means the document's content lets you confidently
     conclude the Affirmative Condition is not met; it is a definitive
     answer, not a hedge. Read the rule's own "Affirmative Condition" and
     "When to say Could not determine" fields closely — they carry
     calibration about how demanding the test is meant to be, and applying
     a stricter bar than the rule sets will produce answers that look
     cautious but are actually wrong.
   - Cite the specific document language that supports the answer, the same
     way you would for an attribute. A rule answer without evidence is not
     acceptable.
   - Stay within what the rule actually asks. `rules.md`'s rules are
     phrased as compound-but-neutral tests (e.g. specificity/breachability),
     not quality judgments — answer only the question asked, and don't let
     your own opinion of whether something is a *good* mission leak in.
   - Every rule gets reported, even if the answer is "Could not determine."

4. **Write the report.** Default to the Markdown structure below. If the
   user asks for HTML, a webpage, or something to open in a browser
   instead, use the HTML template described in "HTML report format"
   further down. Either way: no preamble narrating what was read or
   confirming completeness before the report, and nothing after it.

## Report structure

Always use this structure:

```markdown
# Mission Lock Analysis — [Company Name, or "Unknown" if that attribute
itself came back Could not determine]

## Attributes

### [Attribute Name]
**Answer:** [one of that attribute's defined "Answer options" — never
freeform text here]
**Evidence:** [quoted or closely paraphrased document language supporting
the answer — required whenever the answer isn't "Could not determine"]
**Location:** [article/section reference, if available]

(repeat for every attribute in references/attributes.md, in the order they
appear there)

## Rules

### [Rule Name]
**Result:** [Affirmative / Not affirmative / Could not determine]
**Evidence:** [quoted or closely paraphrased document language supporting
the result — required whenever the result isn't "Could not determine"]
**Location:** [article/section reference, if available]

(repeat for every rule in references/rules.md, in the order they appear
there)

## Notes
[Anything that doesn't fit above: why an answer came back "Could not
determine," ambiguous drafting, unusual provisions that don't map to any
current attribute or rule, missing pages, illegible sections, etc. If you
notice a provision that looks like it should become its own tracked
attribute or rule but isn't in the reference files yet, flag it here and
suggest it as a candidate addition rather than folding it into an existing
one or inventing an ad hoc one.]
```

## HTML report format

If the user asks for HTML, a webpage, or something to open in a browser,
use [assets/report-template.html](assets/report-template.html) instead of
the Markdown structure above. Read that file fresh — it contains its own
detailed instructions (as an HTML comment near the top) on filling in
placeholders and repeating blocks, and it is the single source of truth
for the design; don't reconstruct it from memory or improvise styling.

A few things worth knowing before you open it:

- **The content is the same underlying analysis, reshaped — not a
  different analysis.** Walk the attribute and rule catalogs exactly as
  described above; only the output format changes.
- **This format has no Notes section.** Unlike the Markdown structure, the
  HTML template has nowhere to put "Could not determine" explanations or
  candidate-attribute flags. Don't invent a Notes section to hold them —
  if a document was reviewed but excluded from the analysis, its name in
  "Documents Considered and not Used" needs to be self-explanatory on its
  own, since nothing else in the report will explain why.
- **Every attribute and rule still gets reported** — the template's
  repeat-block instructions cover this, but the underlying rule from the
  Workflow section (never silently skip one) still applies.
- Save the result as a `.html` file rather than inlining raw HTML into a
  chat response.

## Edge cases

- **Comparing two or more companies:** Neutrality is hardest to hold in a
  comparison, and it fails in a specific way worth naming: describing one
  document's provision as a protection and the other as *lacking* it. "X has
  a 66⅔% amendment threshold while Y has no equivalent protection" carries
  the same verdict as "X is better protected," just in quieter words — it
  makes one document the standard and the other a shortfall against it.
  Instead, describe each document on its own terms, in mechanical language:
  "X's Article IX requires a 66⅔% vote to amend Article III; Y's purpose
  clause is subject to the ordinary amendment process." Both sentences are
  now factual statements about what each document does, and the reader can
  draw the comparison themselves — which is the point. Give each side its
  own affirmative description rather than leaving one as a bare absence.
- **Multiple documents / amended and restated charters:** If the user
  provides both original articles and later amendments, analyze the current
  (most recently amended and restated) version, but note in "Notes" if an
  amendment changed the answer to any attribute or rule from the original.
- **Non-US entities:** The attribute and rule catalogs are written with US
  (mostly Delaware) corporate law patterns in mind. For other
  jurisdictions, apply the same attributes/rules where the underlying
  concept translates (e.g. a "memorandum of association" purpose clause), a
  PBC-equivalent statutory form, etc. If the concept doesn't map cleanly
  enough to answer confidently, that's a legitimate "Could not determine" —
  say so and explain the mismatch in "Notes" rather than forcing a
  US-shaped answer onto a different legal system.
- **Incomplete documents:** If the provided document is missing pages or
  clearly truncated, say so up front before the report. Missing the section
  that would answer a given attribute or rule is exactly the kind of case
  where "Could not determine" is the correct, honest answer.
