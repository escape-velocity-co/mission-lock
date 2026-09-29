#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Parse skills/mission-lock/references/attributes.md into structured data.

Mirrors parse_rules.py for the attribute catalog. There's no docket
consumer for this today (the results docket's columns are rules, not
attributes — see CLAUDE.md's "Attribute Catalog Change Workflow"), so
this exists mainly as the same kind of structural-sanity check
parse_rules.py gives rules.md: a malformed bullet, a missing field, or a
duplicate/skipped attribute ID will surface here rather than fail
silently. Read fresh every time it's used — this content changes as the
attribute catalog evolves.
"""

import re


def parse_attributes_md(path):
    """Return {attribute_id: {name_plain, definition, response_options,
    what_to_look_for, typically_found_in, when_to_say_cnd}} for every
    attribute under the "## Attribute Definitions" heading.

    Each field is returned as the raw field text, verbatim (including any
    typos — this mirrors the live attribute text exactly, it is not a
    paraphrase). Unlike rules.md's fields, attributes.md's "Typically
    Found In" is sometimes prose and sometimes a bulleted list, so no
    field is forced into a bullet list here — callers that want a bullet
    list back out of a given field can split on "\\n* " themselves.

    Only the "## Attribute Definitions" section onward is scanned, so the
    "### <Attribute Name>" template example earlier in the file (under
    "## Adding New Attributes") is never mistaken for a real attribute.
    """
    with open(path) as f:
        content = f.read()

    defs_start = content.index("## Attribute Definitions")
    body = content[defs_start:]

    sections = re.split(r"\n### ", body)[1:]  # drop the heading preamble
    attributes = {}
    for section in sections:
        lines = section.split("\n")
        name_plain = lines[0].strip()
        section_text = "\n".join(lines[1:])

        def field(label):
            # Case-insensitive: attributes.md's own field labels aren't
            # consistently capitalized (e.g. "Could not Determine" vs.
            # "Could not determine") across existing entries.
            pattern = rf"\*\*{label}:\*\*\s*\n?(.*?)(?=\n\*\*|\Z)"
            m = re.search(pattern, section_text, re.DOTALL | re.IGNORECASE)
            return m.group(1).strip() if m else ""

        attribute_id = field("ID")
        attributes[attribute_id] = dict(
            name_plain=name_plain,
            definition=field("Definition"),
            response_options=field("Response Options"),
            what_to_look_for=field("What to Look For"),
            typically_found_in=field("Typically Found In"),
            when_to_say_cnd=field("Could not Determine"),
        )
    return attributes


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
            "references",
            "attributes.md",
        )
    )
    path = sys.argv[1] if len(sys.argv) > 1 else default_path
    print(json.dumps(parse_attributes_md(path), indent=2))
