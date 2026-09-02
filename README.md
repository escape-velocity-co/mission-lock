# Mission Lock Analyzer

This repository contains the "Mission Lock Analyzer" (MLA) Skill and its eval harness, developed using Anthropic's [`skill-creator`](https://github.com/anthropics/skills/tree/main/skills/skill-creator).

MLA analyzes a company's governing documents and assesses conditions related to the concept of "Mission Lock": things that affect how durably a company's mission is protected. These are mechanisms like public benefit corporation status, a purpose clause, amendment thresholds and other governance safeguards, etc.

***This skill produces summaries for informational purposes. It is not legal advice, and its output should not be relied on as a substitute for review by a qualified attorney.***

See [`skills/mission-lock/SKILL.md`](skills/mission-lock/SKILL.md) for what the skill does, and [`evals/README.md`](evals/README.md) for the eval corpus and eval loop.

## Testing and Verification

MLA is primarily tested with publicly filed governance documents from SEC's [EDGAR](https://www.sec.gov/edgar/search/) as well as synthetic documents designed to capture edge-case behaviour (conflicts, degrees of confidence, etc.). See [`evals/README.md`](evals/README.md) for more information about how MLA is tested.

## Repository Structure

```
mission-lock/
├── evals/                      # Testing                    
│   ├── documents/              # Incorporation documents
│   └── evals.json              # Test prompts
├── skills/
│   └── mission-lock/
│       ├── SKILL.md            # MLA
│       └── references/
│           ├── attributes.md   # Mission-lock attribute definitions
|           └── rules.md        # Mission-lock rule definitions
├── CLAUDE.md
├── LICENSE
└── README.md
└── THIRD_PARTY_NOTICES.md      
```
