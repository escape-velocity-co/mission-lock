# Mission Lock Analyzer

This is the development repository for the "Mission Lock Analyzer" (MLA) skill.

MLA analyzes a company's governing documents and assesses conditions related to the concept of "Mission Lock": qualities that affect how durably a company's mission is protected. These are mechanisms like Public Benefit Corporation status, purpose declaration and amendment thresholds.

***This skill produces summaries for informational purposes. It is not legal advice, and its output should not be relied on as a substitute for review by a qualified attorney.***

## 🟡 Prototype 🟡
This is an early release meant as a proof-of-concept to collect feedback. What's released is thoroughly tested, though early in functionality as we continue to evolve the standard.

## Installation Options

* Stable release: [Escape Velocity Claude Plugin Marketplace](https://github.com/escape-velocity-co/claude-plugins)
* Stable release: [Skill archive](https://github.com/escape-velocity-co/mission-lock/releases)
* In development: [Skill source](https://github.com/escape-velocity-co/mission-lock/tree/main/skills/mission-lock)

## Structure

```
mission-lock/
├── README.md               👋
├── CITATION.cff            Metadata supporting repo citation
├── CLAUDE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE                 MPL-2.0
├── THIRD_PARTY_NOTICES.md  
├── .claude/
│   ├── agents/             Placeholder for eval runner subagent(s)
│   └── skills/             Skills for MLA development change workflows
├── .github/
│   └── ISSUE_TEMPLATE/     Issue submission templates for GitHub
├── evals/                  Eval harness
│   ├── evals.json          Assertions checked per assessment
│   ├── documents/          Sample governing documents
│   └── benchmarks/         Eval run history (to monitor/optimize performance)
└── skills/   
    └── mission-lock/       MLA
        ├── SKILL.md   
        ├── LICENSE.txt     Copy of LICENSE (packaged with the MLA)
        ├── definitions/    Assessment descriptions
        └── assets/         Report templates
```

## License and Attribution

MLA is licensed under the [Mozilla Public License 2.0](LICENSE), Copyright © 2026 Escape Velocity.

We develop Mission Lock Analyzer in the open to help companies protect themselves and their missions. We chose its license deliberately, and we hope others building in this space will do the same.

If you build on Mission Lock Analyzer, whether its files or its ideas, we'd love to hear from you!
