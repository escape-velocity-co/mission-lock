# Mission Lock Analyzer

This is the development repository for the "Mission Lock Analyzer" (MLA) skill. If you're looking for the skill itself, that's [over here](https://github.com/rslifka/mission-lock/tree/main/skills/mission-lock).

MLA analyzes a company's governing documents and assesses conditions related to the concept of "Mission Lock": qualities that affect how durably a company's mission is protected. These are mechanisms like Public Benefit Corporation status, purpose declaration and amendment thresholds.

***This skill produces summaries for informational purposes. It is not legal advice, and its output should not be relied on as a substitute for review by a qualified attorney.***

## Installation

* Latest stable: found on the [Releases](https://github.com/rslifka/mission-lock/releases) page.
* In development: `https://github.com/rslifka/mission-lock/tree/main/skills/mission-lock` 

## Structure

```
mission-lock/
├── README.md            👋
├── CLAUDE.md            instructions for Claude Code
├── CHANGELOG.md         
├── skills/
│   └── mission-lock/    ← the installable skill
│       ├── SKILL.md     skill behaviour & metadata
│       ├── definitions/ assessment descriptions
│       └── assets/      report templates
│
├── evals/               eval harness
│   ├── evals.json       assertions checked per assessment
│   ├── documents/       sample governing documents
│   └── benchmarks/      eval run history
│
└── .claude/
    ├── agents/          placeholder for eval runner subagent
    └── skills/          change workflows
```
