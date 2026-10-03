#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
This script checks the structural assertions in evals.json against a
report.md; an optimization in the eval process to reduce reliance on
an LLM.

Usage:
    python3 check_mechanical_assertions.py <path/to/report.md> --eval-id <N>
    python3 check_mechanical_assertions.py <path/to/report.md> --assertions-file <path/to/eval_metadata.json>
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CURRENT_ATTRIBUTES = [
    "Company Name",
    "Public Benefit Corporation",
    "Stated Purpose",
    "Governing Jurisdiction",
    "Supermajority/Veto Requirements for PBC/Purpose Article(s) Amendments",
    "Supermajority/Veto Requirements for Mergers",
]
CURRENT_RULE_HEADINGS = [
    "Mission Beyond Financial Profit",
    "Mission Breachability",
    "Mission is Paramount",
]


def heading_lines(report_text, level_prefix):
    return [
        line.strip().lstrip("#").strip()
        for line in report_text.splitlines()
        if line.strip().startswith(level_prefix)
    ]


def check_attribute_sections(assertion, report_text):
    if "section for every attribute currently in" not in assertion:
        return None
    h3 = heading_lines(report_text, "###")
    missing = [a for a in CURRENT_ATTRIBUTES if not any(a in h for h in h3)]
    if missing:
        return False, f"Missing attribute section heading(s): {missing}"
    return True, "All attribute headings present (### level)."


def _quoted_words_after(marker, text):
    """Extract 'word' tokens after `marker`, to dodge stray apostrophes
    earlier in the sentence (e.g. "company's") desyncing naive quote-pairing
    across the whole string. Returns [] (not a whole-text fallback) if
    `marker` isn't found — falling back to the unrestricted text would
    silently reintroduce the exact desync bug this function exists to avoid."""
    m = re.search(re.escape(marker) + r"\s*(.+)$", text)
    if not m:
        return []
    return re.findall(r"'([^']+)'", m.group(1))


def check_no_evaluative_language(assertion, report_text):
    if "no evaluative or judgmental language" not in assertion and "no evaluative language" not in assertion:
        return None
    words = _quoted_words_after("such as", assertion)
    if not words:
        return None
    found = []
    for w in words:
        if re.search(r"\b" + re.escape(w) + r"\b", report_text, re.IGNORECASE):
            found.append(w)
    if found:
        return None, (
            f"Word(s) {found} appear somewhere in the report — could be a real "
            "violation or a false positive (e.g. inside a quoted document clause). "
            "Needs manual read, not auto-failed."
        )
    return True, f"None of {words} appear anywhere in the report."


def check_no_hedging(assertion, report_text):
    if "hedged with confidence language" not in assertion and "hedged as a" not in assertion and "hedged as though" not in assertion:
        return None
    words = _quoted_words_after("such as", assertion) or _quoted_words_after("as a", assertion)
    if not words:
        words = ["close call", "narrow margin"]
    found = [w for w in words if w.lower() in report_text.lower()]
    if found:
        return None, f"Hedging phrase(s) {found} found — needs manual read to confirm context."
    return True, f"None of {words} appear anywhere in the report."


def check_analysis_subsections(assertion, report_text):
    if "'# Analysis' section with a subsection for every rule" not in assertion:
        return None
    if "# Analysis" not in report_text:
        return False, "No '# Analysis' heading found."
    h2 = heading_lines(report_text, "##")
    missing = [r for r in CURRENT_RULE_HEADINGS if not any(r in h for h in h2)]
    if missing:
        return False, f"Missing rule subsection heading(s): {missing}"
    return True, "'# Analysis' present with all 3 current rule subsections (## level)."


def check_no_could_not_determine(assertion, report_text):
    triggers = [
        "No attribute answer is 'Could not determine'",
        "None of the four attributes",
        "None of the three attributes",
    ]
    if not any(t in assertion for t in triggers):
        return None
    if "could not determine" not in assertion.lower():
        return None
    # Only fires when the assertion is a blanket NEGATIVE claim (nothing
    # should be CND). Conflict-resolution evals phrase it the opposite way
    # ("X answer is 'Could not determine'") and are deliberately excluded by
    # requiring one of the triggers above.
    if re.search(r"\*\*Answer:\*\*\s*Could not determine", report_text, re.IGNORECASE):
        return False, "Found a 'Could not determine' attribute answer despite assertion expecting none."
    return True, "No attribute Answer field reads 'Could not determine'."


# ---------------------------------------------------------------------------
# Template conformance: checks against report-template.md's own rules, run on
# every report regardless of which assertions the eval defines.
# ---------------------------------------------------------------------------
ALLOWED_RESULTS = {"Mission-lock more likely", "Mission-lock less likely", "Mission-lock uncertain"}
TEMPLATE_PATH = REPO_ROOT / "skills" / "mission-lock" / "assets" / "report-template.md"
BANNER_PREFIX = "🟡 PROTOTYPE"


def _section(report_text, heading):
    """Body of a top-level ('# ') section, up to the next top-level heading
    (so its own '## ' subsections stay inside it)."""
    m = re.search(r"^" + re.escape(heading) + r"[^\n]*\n(.*?)(?=^# |\Z)", report_text, re.S | re.M)
    return m.group(1) if m else None


def conformance_banner(report_text):
    # The banner is fixed content only while the template still carries it.
    if BANNER_PREFIX not in TEMPLATE_PATH.read_text():
        return True, "Template no longer carries the prototype banner; not checked."
    lines = [l for l in report_text.splitlines() if l.strip()]
    if not lines or not lines[0].startswith(BANNER_PREFIX):
        return False, f"First line should be the prototype banner; got: {lines[0][:60] if lines else '(empty)'!r}"
    return True, "Prototype banner is the first line."


def conformance_result_values(report_text):
    values = re.findall(r"^\*\*Result:\*\*\s*(.+?)\s*$", report_text, re.M)
    if not values:
        return False, "No '**Result:**' fields found."
    bad = [v for v in values if v not in ALLOWED_RESULTS]
    if bad:
        return False, f"Result value(s) outside the three allowed wordings: {bad}"
    return True, f"All {len(values)} Result values use an allowed wording."


def conformance_document_lines(report_text):
    problems = []
    for heading in ("## Documents Used in this Analysis", "## Documents Considered and not Used"):
        body = _section_h2(report_text, heading)
        if body is None:
            continue
        for line in body.splitlines():
            if not line.startswith("- "):
                continue
            if "(" in line or " — " in line or " - " in line[2:] or ": " in line:
                problems.append(line.strip())
    if problems:
        return False, f"Document line(s) with text beyond the bare name: {problems}"
    return True, "All document-list lines are bare names."


def _section_h2(report_text, heading):
    m = re.search(r"^" + re.escape(heading) + r"\s*\n(.*?)(?=^## |^# |\Z)", report_text, re.S | re.M)
    return m.group(1) if m else None


def conformance_rule_blocks(report_text):
    """Each rule block is: italic query, then the Result, Evidence and Location
    fields, in that order, and nothing else. Evidence may run to several
    paragraphs or bullets (that is where a user's specific question gets
    answered); what is not allowed is any other field or paragraph after
    Location, or anything between the query and Result."""
    analysis = _section(report_text, "# Analysis")
    if analysis is None:
        return False, "No '# Analysis' section."
    blocks = re.split(r"^## ", analysis, flags=re.M)[1:]
    problems = []
    for block in blocks:
        title, _, body = block.partition("\n")
        body = body.strip()
        m = re.match(r"\*[^*\n]+\*\n\n\*\*Result:\*\* [^\n]+\n\n\*\*Evidence:\*\* .*?\n\n\*\*Location:\*\* ([^\n]*)(.*)\Z", body, re.S)
        if not m:
            problems.append(f"{title.strip()}: not query / Result / Evidence / Location in order")
            continue
        trailing = re.sub(r"^\s*---\s*$", "", m.group(2), flags=re.M).strip()
        if trailing:
            problems.append(f"{title.strip()}: extra content after Location: {trailing[:60]!r}")
    if problems:
        return False, "; ".join(problems)
    return True, f"{len(blocks)} rule block(s), each query/Result/Evidence/Location only."


def conformance_nothing_after_report(report_text):
    """The report ends with the last attribute's Location line; nothing
    (other than a TOOL_USE_COUNT line the eval runner appends) follows it."""
    idx = [m.end() for m in re.finditer(r"^\*\*Location:\*\* [^\n]*", report_text, re.M)]
    if not idx:
        return False, "No '**Location:**' fields found."
    tail = report_text[idx[-1]:]
    tail = re.sub(r"^TOOL_USE_COUNT:.*$", "", tail, flags=re.M)
    tail = re.sub(r"^\s*---\s*$", "", tail, flags=re.M).strip()
    if tail:
        return False, f"Content after the final attribute: {tail[:80]!r}"
    return True, "Nothing follows the final attribute."


CONFORMANCE_CHECKS = [
    ("Template: prototype banner is the first line", conformance_banner),
    ("Template: rule Results use only the three allowed wordings", conformance_result_values),
    ("Template: document-list lines are bare names", conformance_document_lines),
    ("Template: each rule block holds only query, Result, Evidence, Location", conformance_rule_blocks),
    ("Template: nothing follows the final attribute", conformance_nothing_after_report),
]


CHECKERS = [
    check_attribute_sections,
    check_no_evaluative_language,
    check_no_hedging,
    check_analysis_subsections,
    check_no_could_not_determine,
]


def check_one(assertion, report_text):
    for checker in CHECKERS:
        result = checker(assertion, report_text)
        if result is None:
            continue
        passed, reason = result
        return {"mechanical": True, "passed": passed, "reason": reason}
    return {"mechanical": False, "passed": None, "reason": "Not a recognized mechanical pattern — needs manual/LLM grading."}


def load_assertions(args):
    if args.assertions_file:
        data = json.loads(Path(args.assertions_file).read_text())
        return data["assertions"]
    evals_path = REPO_ROOT / "evals" / "evals.json"
    data = json.loads(evals_path.read_text())
    for e in data["evals"]:
        if e["id"] == args.eval_id:
            return e["expectations"]
    raise SystemExit(f"No eval with id {args.eval_id} in {evals_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report_path", type=Path)
    ap.add_argument("--eval-id", type=int)
    ap.add_argument("--assertions-file", type=Path)
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of a human-readable summary.")
    args = ap.parse_args()

    if not args.eval_id and not args.assertions_file:
        ap.error("pass --eval-id or --assertions-file")

    assertions = load_assertions(args)
    report_text = args.report_path.read_text()

    results = []
    for a in assertions:
        r = check_one(a, report_text)
        r["assertion"] = a
        results.append(r)
    for label, fn in CONFORMANCE_CHECKS:
        passed, reason = fn(report_text)
        results.append({"mechanical": True, "passed": passed, "reason": reason, "assertion": label, "conformance": True})

    if args.json:
        print(json.dumps(results, indent=2))
        return

    mechanical = [r for r in results if r["mechanical"]]
    manual = [r for r in results if not r["mechanical"]]
    print(f"{len(assertions)} eval assertions + {len(CONFORMANCE_CHECKS)} template-conformance checks — {len(mechanical)} mechanically checked, {len(manual)} need manual/LLM grading\n")
    for r in mechanical:
        status = "PASS" if r["passed"] else ("NEEDS REVIEW" if r["passed"] is None else "FAIL")
        print(f"[{status}] {r['assertion'][:90]}")
        print(f"         {r['reason']}\n")
    print(f"--- {len(manual)} assertion(s) left for manual/LLM grading ---")
    for r in manual:
        print(f" - {r['assertion'][:100]}")


if __name__ == "__main__":
    main()
