# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-11-10

### Added

- Attribute A4: "Governing Jurisdiction", capturing the state (or country) under whose corporate statutes the company is incorporated.
- Attribute A5: "Supermajority/Veto Requirements for PBC/Purpose Article(s) Amendments", capturing whether amendment voting rights require elevated privileges.
- Attribute A6: "Supermajority/Veto Requirements for Mergers, Consolidations, or Reorganizations", capturing whether liquidation actions require elevated privileges.
- Eval: Add *Incorruptible* examples: Veeva Systems, United Therapeutics, Warby Parker.

### Changed

- Eval: Cache reused prompts by bundling into subagents (~50% faster, ~40% fewer tokens).
- Eval: Convert charters to text, reducing eval overhead.

### Removed

- Negative test cases for source citation.

### Fixed

- Claims included in prompts should not be echoed back as though they were findings the skill derived.
- Modified M3's "Affirmative Condition" to require the PBC-or-equivalent election be made in the certificate of incorporation itself (as required by law).
- If a governance document is incomplete, provide a conversational warning (i.e. not part of the report).
- Corrected outdated field names and cross-references across the skill and evals.

## [0.1.0] - 2026-09-17

Initial release.

- Core skill
- Manual invocation via `/mission-lock`
- Markdown and HTML report formats
- Eval harness
