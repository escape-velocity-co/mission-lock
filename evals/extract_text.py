#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Extract plain text from a SEC EDGAR exhibit .htm file.

Unlike parse_attributes.py/parse_rules.py, which re-read their source
fresh on every call, this script's output is meant to be generated once
and committed: when a document is added to the corpus, run this against
the downloaded exhibit, review the .txt it produces, then delete the
.htm and commit only the .txt (plus metadata.json). The raw .htm is a
transient download, never a repo artifact — see "Adding to the corpus"
in evals/README.md. If extraction turns out wrong for some document,
fix this script and regenerate; never hand-edit a .txt directly.
"""

import html
import re
from html.parser import HTMLParser

BLOCK_TAGS = {
    "p", "div", "br", "tr", "table", "li", "ul", "ol",
    "h1", "h2", "h3", "h4", "h5", "h6", "hr", "section",
}
SKIP_TAGS = {"script", "style", "head"}


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._parts = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        elif tag in BLOCK_TAGS:
            self._parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        if tag in BLOCK_TAGS:
            self._parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag in BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data):
        if not self._skip_depth:
            self._parts.append(data)

    def get_text(self):
        return "".join(self._parts)


def extract_text(html_path):
    """Return the visible text of a SEC EDGAR exhibit .htm file.

    Block-level tags (paragraphs, table rows, headings, list items) are
    turned into line breaks so a document's section/article structure
    survives; everything inside <script>/<style>/<head> is dropped.
    Entities are unescaped (including &nbsp;, normalized to a plain
    space) and runs of blank lines/horizontal whitespace are collapsed,
    but no other normalization (casing, wording) is applied — this
    mirrors the filed document's visible text exactly, it is not a
    paraphrase.
    """
    with open(html_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    parser = _TextExtractor()
    parser.feed(content)
    parser.close()
    text = parser.get_text().replace("\xa0", " ")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


if __name__ == "__main__":
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parent.parent
    args = sys.argv[1:]
    if args:
        html_paths = [Path(a) for a in args]
    else:
        html_paths = sorted((repo_root / "evals" / "documents").glob("*/*.htm"))

    for html_path in html_paths:
        txt_path = html_path.with_suffix(".txt")
        txt_path.write_text(extract_text(html_path))
        print(f"wrote {txt_path}")
