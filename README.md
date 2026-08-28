# Mission Lock Analyzer

A [Claude Skill](https://www.agentskills.io/) that analyzes a company's governing documents and assesses conditions related to Mission Lock. These are mechanisms like public benefit corporation status, a purpose clause, supermajority amendment thresholds, or governance safeguards; things that affect how durably a company's founding mission protected.

## Repository Structure

```
mission-lock/
├── skills/
│   └── mission-lock/
│       ├── SKILL.md              
│       └── references/
│           ├── attributes.md   # Mission-lock attribute definitions
|           └── rules.md        # Mission-lock rule definitions
|             
├── evals/                      # Testing                    
│   ├── documents/              # Public-record incorporation documents
│   └── evals.json              # Test prompts
├── LICENSE
└── README.md
```

## Evals

This skill is tested against publicly filed governance documents from sources like SEC's [EDGAR](https://www.sec.gov/edgar/search/). See [`evals/README.md`](evals/README.md) for the corpus and how to run the eval loop.

## Disclaimer

This skill produces analytical summaries for informational purposes. It is not legal advice, and its output should not be relied on as a substitute for review by a qualified attorney.
