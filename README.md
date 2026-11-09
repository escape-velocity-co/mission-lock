# Mission Lock Analyzer

This is the development repository for the "Mission Lock Analyzer" (MLA) skill. If you're looking for the skill itself, here too, but [a little further on in](skills/mission-lock).

MLA analyzes a company's governing documents and assesses conditions related to the concept of "Mission Lock": qualities that affect how durably a company's mission is protected. These are mechanisms like Public Benefit Corporation status, purpose declaration and amendment thresholds.

***This skill produces summaries for informational purposes. It is not legal advice, and its output should not be relied on as a substitute for review by a qualified attorney.***

## Installation

TODO 

## Structure

```
mission-lock/
├── README.md            👋
├── CLAUDE.md            
├── CHANGELOG.md         
├── skills/
│   └── mission-lock/    MLA
│       ├── SKILL.md     
│       ├── definitions/ Assessment descriptions
│       └── assets/      Report templates
│
├── evals/               Eval harness
│   ├── evals.json       Assertions checked per assessment
│   ├── documents/       Sample governing documents
│   └── benchmarks/      Eval run history (to monitor/optimize performance)
│
└── .claude/
    ├── agents/          Placeholder for eval runner subagent(s)
    └── skills/          Skill change workflows
```

## License

MLA is licensed under the [Mozilla Public License 2.0](LICENSE), Copyright © 2026 Escape Velocity.

We develop Mission Lock Analyzer in the open to help companies protect themselves and their missions. We chose its license deliberately, and we hope others building in this space will do the same:

- **Use it freely.** Use it, build on it, and combine it with your own work, including commercially. Your own additions can be under any license you like.
- **Share your changes to our files.** If you distribute a modified version of any of this project's files, publish those changes under the MPL too. Improvements to the core stay open for everyone.
- **Keep the credit.** If you distribute these files, keep them under the MPL and keep our copyright and license notices with them. We also ask that you link back to this project (see [Credit](#credit)).

We treat the skill's instructions and definitions as source code (an LLM is simply the runtime that executes them), so we chose a software license, as we would for any other program.

## Credit

If you build on Mission Lock Analyzer, whether its files or its ideas, please credit *Mission Lock Analyzer by Escape Velocity* and link back to [this repository](https://github.com/escape-velocity-co/mission-lock).
