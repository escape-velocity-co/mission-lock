#!/usr/bin/env python3

"""Parse skills/mission-lock/definitions/rules.md into structured data.

Used when generating the eval results docket (see docket-template.html's
own instructions) so each rule's Query / Affirmative Condition /
Categories of Evidence / Typically Found Location can be shown in a
hover popover without hand-transcribing rules.md's current wording into
a second, driftable copy. Read fresh every time the docket is generated —
this content changes as the rule catalog evolves.
"""

import re


def parse_rules_md(path):
    """Return {rule_id: {name_plain, query, condition, evidence_categories,
    location}} for every rule under the "## Rule Definitions" heading.

    - name_plain: the rule's ### heading text, no markup.
    - query: the "Query" field, verbatim.
    - condition: "Affirmative Condition" bullets, as a list of strings,
      in source order, verbatim (including any typos — this mirrors the
      live rule text exactly, it is not a paraphrase).
    - evidence_categories: "Categories of Evidence" bullets, same idea.
    - location: the "Typically Found Location" bullets, same idea.

    Only the "## Rule Definitions" section onward is scanned, so the
    "### Rule Name" template example earlier in the file (under
    "## Adding New Rules") is never mistaken for a real rule.
    """
    with open(path) as f:
        content = f.read()

    defs_start = content.index("## Rule Definitions")
    body = content[defs_start:]

    sections = re.split(r"\n### ", body)[1:]  # drop the heading preamble
    rules = {}
    for section in sections:
        lines = section.split("\n")
        name_plain = lines[0].strip()
        section_text = "\n".join(lines[1:])

        def field(label):
            pattern = rf"\*\*{label}:\*\*\s*\n?(.*?)(?=\n\*\*|\Z)"
            m = re.search(pattern, section_text, re.DOTALL)
            return m.group(1).strip() if m else ""

        def bullets(block):
            items = []
            for line in block.split("\n"):
                line = line.strip()
                if line.startswith("*"):
                    items.append(line[1:].strip())
            return items

        rule_id = field("ID")
        rules[rule_id] = dict(
            name_plain=name_plain,
            query=field("Query"),
            condition=bullets(field("Affirmative Condition")),
            evidence_categories=bullets(field("Categories of Evidence")),
            location=bullets(field("Typically Found Location")),
        )
    return rules


if __name__ == "__main__":
    import json
    import os
    import sys

    default_path = os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "skills",
            "mission-lock",
            "definitions",
            "rules.md",
        )
    )
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    print(json.dumps(parse_rules_md(path), indent=2))
