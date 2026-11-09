---
name: mission-lock
description: Analyzes a company's governing documents (e.g. articles of incorporation, certificate of incorporation) for likelihood of "mission lock" - how protected the company's mission is. Use this whenever the user provides or references articles of incorporation, a certificate of incorporation, corporate charter, or formation documents (PDF, DOCX, plain text, or pasted content) and has questions regarding its mission, purpose and related concepts (e.g. PBC status) even if they don't say "mission lock" explicitly.
license: MPL-2.0
metadata:
  author: Escape Velocity
  version: 0.2.0
---

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
and explain why in that item's Evidence field. This matters more than it
might seem: the catalogs start
small and simple deliberately, and more complex checks will only be added
once the simple ones are proven reliable. A confident wrong answer (or a
guess dressed up as a finding) on an easy check undermines trust in
everything this skill will eventually be asked to evaluate. See
[definitions/confidence-requirement.md](definitions/confidence-requirement.md)
for the full rule.

**Attributes vs. rules — a distinction worth keeping straight:**
`definitions/attributes.md` holds pure fact-extraction (a name, a yes/no, a
quoted clause) — no interpretive judgment beyond reading the document.
`definitions/rules.md` holds compound checks that require judgment to apply
(e.g. "is the stated purpose specific enough that a third party could
identify a breach of it") but stay strictly non-evaluative about *quality*
— a rule may ask whether a mission is specific enough to be breached, never
whether it's a *good* mission. Don't let rule assessments drift into rating
how good, strong, or admirable something is — that line matters as much for
rules as it does for attributes.

## Workflow

1. **Get the source document.** Accept whatever the user provides — PDF,
   DOCX, plain text, or pasted content.

   - **Manual invocation (`/mission-lock`):** If invoked with arguments
     (e.g. `/mission-lock contract.pdf`), treat `$ARGUMENTS` as identifying
     which document(s) to use. If invoked with no arguments, and no
     document is otherwise attached, pasted, or already present in the
     conversation, stop and ask the user to provide one rather than
     proceeding. Do not fabricate or assume a document, and do not treat
     this as a "Could not determine" analysis of a document that was
     never given.
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

2. **Walk the attribute catalog.** Always read
   [definitions/attributes.md](definitions/attributes.md) fresh for the current
   list of mission-lock attributes. For each attribute:
   - Give a definitive answer using that attribute's specific "Answer
     options" (see the reference file) — or "Could not determine" if you
     can't support an answer with specific document text. Read each
     attribute's "Could not Determine" guidance carefully: a
     confident negative or "this is generic boilerplate" is a valid,
     definitive answer and should NOT be reported as "Could not determine."
   - Quote or closely paraphrase the relevant language as evidence, with an
     article/section reference if the document has numbered sections.
   - Every attribute gets reported, even if the answer is "Could not
     determine" — never silently skip one.

3. **Walk the rule catalog.** Read
   [definitions/rules.md](definitions/rules.md) fresh for the current list of
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
   - When a rule's Affirmative Condition relies on a fact the attribute
     catalog captures (e.g., Mission Beyond Financial Profit
     (M1)'s "purpose is stated" and "purpose is not the default
     any-lawful-purpose formulation" conditions, and Mission
     Breachability (M2)'s "identifies a domain and a direction" condition,
     are all read off the same underlying text as the Stated Purpose
     attribute), reuse that attribute's already-determined answer and
     citation.
     If the depended-on attribute came back "Could not determine," the
     rule usually can't be more confident than that either — but check
     the rule's own "When to say Could not determine" guidance first,
     since a rule may have its own path to a definitive answer even when
     the attribute it draws on doesn't.
   - Cite the specific document language that supports the answer, the same
     way you would for an attribute. A rule answer without evidence is not
     acceptable.
   - Stay within what the rule actually asks. `rules.md`'s rules are
     phrased as compound-but-neutral tests (e.g. specificity/breachability),
     not quality judgments — answer only the question asked, and don't let
     your own opinion of whether something is a *good* mission leak in.
   - Every rule gets reported, even if the answer is "Could not determine."

4. **Track document usage.** If more than one document was provided, note
   which ones ended up cited as evidence for at least one attribute or rule,
   and which were reviewed but never cited (e.g. an unrelated bundled
   exhibit). Both report formats need this split.

5. **Write the report.** Default to the Markdown structure below. If the
   user asks for HTML, a webpage, or something to open in a browser
   instead, use the HTML template described in "HTML report format"
   further down. Either way: no preamble narrating what was read or
   confirming completeness before the report, and nothing after it.
   Every report stamps {{SKILL_VERSION}} — read the `metadata.version`
   field from this file's own frontmatter at the top, never hardcode or
   recall a previous value, since it changes as the skill does.

   The template's own instructions are authoritative, but these are
   the ones most often broken, so apply them explicitly:
   - The prototype banner is the very first line of the report, above the
     title, not below it.
   - In the Analysis section each rule's Result is exactly one of
     "Mission-lock more likely", "Mission-lock less likely", or
     "Mission-lock uncertain" — never "Affirmative", "Not affirmative", or
     "Could not determine" there (those are for the attribute/rule
     catalogs, not the report's Result field).
   - Each line under "Documents Used in this Analysis" and "Documents
     Considered and not Used" is the file name exactly as provided, and
     nothing else (e.g. `d841617dex32.htm`) — no description, exhibit label,
     parenthetical, dash, or colon, and never a description plus the file
     name. Only for a document that has no file name of its own, such as an
     exhibit bundled inside another file, use a descriptive name instead
     (e.g. "Series A Preferred Stock Certificate of Designations").
   - Each rule's block holds only its italic query, Result, Evidence, and
     Location. If the user asked a specific question (e.g. whether a
     provision is legally binding), answer it through those fields — in the
     Evidence text of the rule it bears on — and do not add a paragraph,
     note, or heading to the report for it.
   - The report ends with the last attribute's Location line. Nothing
     follows it: no closing summary, no "answer to your question" section,
     no note.

## Markdown Report Structure

Use [assets/report-template.md](assets/report-template.md) as the default
report format. It contains detailed instructions (as an HTML comment near
the top) on filling in placeholders and repeating blocks.

## HTML Report Structure

If the user asks for HTML, a webpage, or something to open in a browser,
use [assets/report-template.html](assets/report-template.html) instead of
the Markdown structure above. It contains detailed instructions (as an
HTML comment near the top) on filling in placeholders and repeating blocks.

Save the result as a `.html` file rather than inlining raw HTML into a
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
  provides multiple documents with overlapping information — e.g. both
  original articles and a later amendment — analyze the current (most
  recently amended and restated) version, and call out in the affected
  attribute's or rule's Evidence field if comparing the documents shows an
  amendment changed the answer from the original. This is a
  comparison you can only make when you actually hold more than one
  document. If multiple documents *are* provided but
  you can't tell which one is the current, controlling version, that's the
  conflicting-documents case in the Confidence Requirement section of
  attributes.md/rules.md — the affected attribute(s) or rule(s) should come
  back "Could not determine" rather than guessing which document to trust.
- **Current v. prospective documents:** This skill will often be used
  when the user is drafting governance documents (e.g. in preparation
  for a financing round, restatement or IPO) in which case you may
  detect several conflicting copies of the same document. If the user
  is asking what's about to be filed or adopted, analyze that
  prospective draft on its own terms (noting it isn't yet effective)
  rather than defaulting to whatever's currently in force. If they're
  asking what currently governs, prefer the document that's presently
  in force over a draft. If you're uncertain and in a conversation where you
  can ask, ask the user which document should be treated as authoritative.
  Only fall back to reporting "Could not determine" for the affected
  items if you can't ask (a non-interactive or batch context) or the user
  can't say either.
- **Non-US entities:** The attribute and rule catalogs are written with US
  (mostly Delaware) corporate law patterns in mind. For other
  jurisdictions, apply the same attributes/rules where the underlying
  concept translates (e.g. a "memorandum of association" purpose clause), a
  PBC-equivalent statutory form, etc. If the concept doesn't map cleanly
  enough to answer confidently, that's a legitimate "Could not determine" —
  say so and explain the mismatch in that item's Evidence field.
- **Incomplete documents:** If the provided document is missing pages or
  clearly truncated, say so up front before the report. Missing the section
  that would answer a given attribute or rule is exactly the kind of case
  where "Could not determine" is the correct, honest answer.
