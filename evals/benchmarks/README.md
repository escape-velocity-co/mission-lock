<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# Eval Suite Timing Benchmarks

How costly is the eval suite?

## Structure

```
evals/benchmarks/
├── README.md
├── history.md              — record of material timings
├── scripts/
│   ├── aggregate_timing.py — convert timing.json into summary
│   └── compare_timing.py   — diff two timing-summary.json files
└── versions/
    ├── unreleased/         - active development
    │   ├── timing-summary.json
    │   └── timing-summary.md
    └── <version>/          — e.g. 0.2.0
        ├── timing-summary.json
        └── timing-summary.md
```

## Maintaining the Benchmarks

1. As each with-skill subagent's completion notification arrives, save its `total_tokens`/`duration_ms`/`tool_uses` to `<eval-dir>/with_skill/run-1/timing.json` in that run's workspace directory. This is the only opportunity to capture this data — it isn't persisted anywhere else.
2. Once the run is graded, roll it up: `python3 evals/benchmarks/scripts/aggregate_timing.py skills/mission-lock-workspace/iteration-<N> --output evals/benchmarks/versions/unreleased`.
3. Update `evals/benchmarks/history.md`'s "In Development" row and its "Δ vs. previous" row with the new totals — `compare_timing.py --markdown-rows` (below) prints both, pre-formatted and ready to paste in.
4. If comparing against a prior run or a released version, use `evals/benchmarks/scripts/compare_timing.py`.

## Comparing Two Versions (or a Version Against Unreleased)

```bash
python3 evals/benchmarks/scripts/compare_timing.py evals/benchmarks/versions/0.2.0 evals/benchmarks/versions/unreleased
```

Accepts either a directory (containing `timing-summary.json`) or a path to the JSON file directly.
