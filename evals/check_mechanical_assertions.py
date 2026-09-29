#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Pre-check the purely structural assertions in evals.json against a
report.md, so a human/LLM grader only has to spend judgment on the
assertions that actually require reading and reasoning about the document.

This does NOT replace grading. It only recognizes a handful of recurring
assertion *shapes* that are checkable by string/structure matching alone
(section presence, forbidden-keyword absence, "Could not determine" absence
when none is expected). Every other assertion is left "not automated" for
a human or grader agent to judge normally — this script is conservative on
purpose: a false PASS here would silently skip real grading, so any pattern
it isn't confident about is left unclassified rather than guessed at.

Usage:
    python3 check_mechanical_assertions.py <path/to/report.md> --eval-id <N>
    python3 check_mechanical_assertions.py <path/to/report.md> --assertions-file <path/to/eval_metadata.json>

Either --eval-id (looked up in this repo's evals/evals.json) or
--assertions-file (a JSON file with an "assertions" list, e.g. an
eval_metadata.json from a workspace run) must be given.
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
    "Amendment Supermajority Requirements",
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

    if args.json:
        print(json.dumps(results, indent=2))
        return

    mechanical = [r for r in results if r["mechanical"]]
    manual = [r for r in results if not r["mechanical"]]
    print(f"{len(assertions)} total assertions — {len(mechanical)} mechanically checked, {len(manual)} need manual/LLM grading\n")
    for r in mechanical:
        status = "PASS" if r["passed"] else ("NEEDS REVIEW" if r["passed"] is None else "FAIL")
        print(f"[{status}] {r['assertion'][:90]}")
        print(f"         {r['reason']}\n")
    print(f"--- {len(manual)} assertion(s) left for manual/LLM grading ---")
    for r in manual:
        print(f" - {r['assertion'][:100]}")


if __name__ == "__main__":
    main()
