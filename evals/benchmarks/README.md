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

1. Regenerate the runner (`python3 evals/build_bundled_runner.py`; see [`evals/CLAUDE.md`](../CLAUDE.md)'s "Step 1 - Generate the Subagent Runner"), then spawn with-skill runs using the `mission-lock-eval-runner` subagent. Snapshots recorded before the runner embedded the skill (i.e. that read it from disk) aren't comparable with later ones. As each completion notification arrives, save its `total_tokens`/`duration_ms`/`tool_uses` (from the notification's usage data) plus the pinned `model`/`effort` from the subagent frontmatter, to `<eval-dir>/with_skill/run-1/timing.json` in that run's workspace directory.
2. Once the run is graded, roll it up: `python3 evals/benchmarks/scripts/aggregate_timing.py skills/mission-lock-workspace/iteration-<N> --output evals/benchmarks/versions/unreleased`.
3. Update `evals/benchmarks/history.md`'s "In Development" row with the new totals — `compare_timing.py --markdown-rows` (below) prints it pre-formatted and ready to paste in. See "history.md Format" below for what belongs in that row.

## history.md Format

`history.md` is used to capture and compare historical results. It consists of a table only, with no description.

- The table consists of one row per released version, in order of release date.
- There is also a single "In Development" row for the current unreleased snapshot.
- Finally, include a "Δ vs. previous" row comparing the "In Development" run to the most recently released run.

## Comparing Two Versions (or a Version Against Unreleased)

```bash
python3 evals/benchmarks/scripts/compare_timing.py evals/benchmarks/versions/0.2.0 evals/benchmarks/versions/unreleased
```

Accepts either a directory (containing `timing-summary.json`) or a path to the JSON file directly.
