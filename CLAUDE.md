# Mission Lock Analyzer

This project contains the "Mission Lock Analyzer" (aka "MLA") skill and its eval harness, developed using Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator). See [`SKILL.md`](skills/mission-lock/SKILL.md) for what the skill does, and [`evals/README.md`](evals/README.md) for the eval harness.

## Glossary

- **Attribute**: An objective interpretation made by the MLA skill. For example, the governing jurisdiction of a document. Attributes can be built on the findings of previously other Attributes, for consistency and optimization.
- **Assessment**: Colloquially used to mean the results of a generating a full report against accessible governing documents.
- **Definition**: A single Rule, Attribute, etc. defined in the skill itself (i.e. any file under [definitions/](skills/mission-lock/definitions))
- **Docket**: The eval iteration results page. The Docket is built from [`evals/docket-template.html`](evals/docket-template.html) and saved as `docket.html` in a run's workspace directory. It contains one page per eval run, consisting of a grid of every eval against every rule. It is used by developers of the skill to grade eval runs.
- **Mission Lock Analyzer**: this skill this project is responsible for developing.
- **MLA**: See "Mission Lock Analyzer".
- **Report**: The per-document analysis MLA produces for an end user, in either [`Markdown`](skills/mission-lock/assets/report-template.md) or [HTML](skills/mission-lock/assets/report-template.html).
- **Report Template**: see "Report".
- **Rule**: A qualitative, subjective interpretation made by the MLA skill. For example, is the mission stated in a breachable way? Rules can be built on the findings of other definitions (e.g. Attributes, Rules) for consistency and optimization.

### Disambiguation

When encountering a word in the Glossary whose meaning you're unable to discern from context, do not guess. Prompt the user for feedback before taking action. For example, "docket"'s use is clear however since a docket is a type of report, using "report" without context may not be clear.

## Previewing the Markdown Report as an Artifact

When asked to publish the Markdown report (`report-template.md`, or a generated instance of it) as an Artifact, render it as plain CommonMark would.

## Definition Change Workflow

When a definition is changed (any file under [definitions/](skills/mission-lock/definitions)), consider which change workflow skill should be run.

- If a Rule in [`rules.md`](skills/mission-lock/definitions/rules.md) is added, edited, or removed, follow the [`rule-catalog-workflow`](.claude/skills/rule-catalog-workflow/SKILL.md) skill's checklist before considering the change done.
- If an Attribute in [`attributes.md`](skills/mission-lock/definitions/attributes.md) is added, edited, or removed, follow the [`attribute-catalog-workflow`](.claude/skills/attribute-catalog-workflow/SKILL.md) skill's checklist before considering the change done.

If there is a transitive change (e.g. a Rule didn't change, but it's underlying Attribute(s) did), consider that Rule as having changed.

## Maintaining the Changelog

All notable changes to this project will be documented in [`CHANGELOG.md`](CHANGELOG.md). The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

When a **notable** change is made:
1. Identify the proper `###` section for the change as per the Keep a Changelog standard.
1. If the section doesn't exist, create it.
1. Add a bullet for that change under the section.

When `metadata.version` is bumped:
1. Rename `[Unreleased]` to the new version (adding today's date) and start an empty `[Unreleased]` above it.
1. Rename `evals/benchmarks/versions/unreleased/` to `evals/benchmarks/versions/<new-version>/`, add a row for that version to `evals/benchmarks/history.md`, and start a new `unreleased/` snapshot from the next eval suite run.

## Packaging the Skill

Packaging is performed via Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator) skill.

1. Confirm that `skills/mission-lock/LICENSE.txt` is identical to the root `LICENSE` (e.g. `cmp LICENSE skills/mission-lock/LICENSE.txt`).
1. Package the contents of `skills/mission-lock/`.
1. Package from the `skill-creator` plugin's `skills/skill-creator/` directory: ```python3 -m scripts.package_skill /path/to/skills/mission-lock /path/to/mission-lock/dist```
1. Rename the output file to `mla-<version>.skill` where `<version>` is the value from `SKILL.md`'s `metadata.version` field.
1. Place the output file in `dist/` at the repo root.
