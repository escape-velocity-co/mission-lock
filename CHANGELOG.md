# Changelog

## [Unreleased]

- Eval corpus: Add *Incorruptible* examples: Veeva Systems, United Therapeutics, Warby Parker.
- Eval corpus: Capture which charters are featured in *Incorruptible*.
- Eval corpus: cache prompts by bundling into subagents in the eval runner (~50% faster, ~40% fewer tokens).
- Added "Amendment Supermajority Requirements for PBC/Purpose Article(s)" attribute (A5), capturing whether a supermajority is required to action on these declarations generally or specifically.
- Clarifying that our eval suite tests report generation (since that's deterministically verifiable).
- Added "Governing Jurisdiction" attribute, capturing the state (or country) under whose corporate statute the company is incorporated.
- Do not echo a user's claim as though it were a finding.
- Modified M3's Affirmative Condition to require the PBC-or-equivalent election be made in the certificate of incorporation itself (as the law requires).
- Removed negative test cases for source citation.

## [0.1.0]

Initial release.

- Core skill
- Manual invocation via `/mission-lock`
- Markdown and HTML report formats
- Eval harness
