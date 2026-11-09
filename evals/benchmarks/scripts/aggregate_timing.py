#!/usr/bin/env python3
"""Roll up one eval-suite run's per-eval timing.json files into a single
timing-summary.json + timing-summary.md, for evals/benchmarks/.

Reads timing data from a workspace iteration directory (e.g.
skills/mission-lock-workspace/iteration-11/eval-*/with_skill/run-1/timing.json
— gitignored, ephemeral) and writes the rolled-up summary to an output
directory under evals/benchmarks/ (tracked) — normally
evals/benchmarks/versions/unreleased/, per CLAUDE.md's "Maintaining the
Changelog" workflow. That output directory only ever holds the latest
snapshot; this script overwrites it in place rather than accumulating one
per run.

Usage:
    python3 aggregate_timing.py <path/to/iteration-N> --output <path/to/evals/benchmarks/versions/unreleased>
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def read_skill_version():
    skill_md = REPO_ROOT / "skills" / "mission-lock" / "SKILL.md"
    text = skill_md.read_text()
    m = re.search(r"^\s*version:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def friendly_name(eval_dir_name):
    # "eval-vital-farms-pbc" -> "Vital Farms Pbc"; good enough for a table,
    # not worth maintaining a separate display-name registry.
    return eval_dir_name.removeprefix("eval-").replace("-", " ").title()


def collect(iteration_dir: Path):
    evals = []
    for eval_dir in sorted(iteration_dir.glob("eval-*/")):
        timing_path = eval_dir / "with_skill" / "run-1" / "timing.json"
        if not timing_path.exists():
            print(f"WARNING: no timing.json for {eval_dir.name}, skipping")
            continue
        timing = json.loads(timing_path.read_text())

        eval_id = None
        meta_path = eval_dir / "eval_metadata.json"
        if meta_path.exists():
            eval_id = json.loads(meta_path.read_text()).get("eval_id")

        evals.append({
            "name": eval_dir.name,
            "id": eval_id,
            "tokens": timing["total_tokens"],
            "duration_ms": timing["duration_ms"],
            "tool_uses": timing["tool_uses"],
            "model": timing.get("model"),
            "effort": timing.get("effort"),
        })

    evals.sort(key=lambda e: (e["id"] is None, e["id"]))
    return evals


def summarize_model_effort(evals):
    """Roll up per-eval model/effort into one run-level value. Older
    timing.json files (pre-model/effort capture) have these as None — in
    that case, or when the run genuinely mixed models/efforts, report
    "unknown"/"mixed" rather than silently picking one eval's value, since
    a mixed or unrecorded run is itself important context for anyone
    comparing timings later."""
    models = {e["model"] for e in evals}
    efforts = {e["effort"] for e in evals}

    if models == {None}:
        model = "unknown"
    elif len(models) > 1:
        model = "mixed (" + ", ".join(sorted(m or "unknown" for m in models)) + ")"
        print(f"WARNING: this run mixed models across evals: {model}")
    else:
        model = next(iter(models))

    if efforts == {None}:
        effort = "unknown"
    elif len(efforts) > 1:
        effort = "mixed (" + ", ".join(sorted(e or "unknown" for e in efforts)) + ")"
        print(f"WARNING: this run mixed effort levels across evals: {effort}")
    else:
        effort = next(iter(efforts))

    return model, effort


def build_summary(iteration_dir: Path):
    evals = collect(iteration_dir)
    if not evals:
        raise SystemExit(f"No timing.json files found under {iteration_dir}")

    totals = {
        "tokens": sum(e["tokens"] for e in evals),
        "duration_ms": sum(e["duration_ms"] for e in evals),
        "tool_uses": sum(e["tool_uses"] for e in evals),
    }
    wall_clock_ms = max(e["duration_ms"] for e in evals)
    model, effort = summarize_model_effort(evals)

    m = re.search(r"iteration-(\d+)", iteration_dir.name)
    iteration_number = int(m.group(1)) if m else None

    return {
        "iteration": iteration_number,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "skill_version": read_skill_version(),
        "model": model,
        "effort": effort,
        "evals": evals,
        "totals": totals,
        "wall_clock_ms": wall_clock_ms,
    }


def render_markdown(summary):
    lines = [
        f"# Timing Summary — iteration {summary['iteration']} (skill v{summary['skill_version']})",
        "",
        f"Generated {summary['generated_utc']}",
        f"Model: {summary['model']} (effort: {summary['effort']})",
        "",
        "| Eval | Tokens | Tool Uses | Duration |",
        "|---|---:|---:|---:|",
    ]
    for e in summary["evals"]:
        dur_s = e["duration_ms"] / 1000
        lines.append(f"| {friendly_name(e['name'])} | {e['tokens']:,} | {e['tool_uses']} | {dur_s:.1f}s |")

    t = summary["totals"]
    lines.append(f"| **Total** | **{t['tokens']:,}** | **{t['tool_uses']}** | **{t['duration_ms']/1000:.1f}s** |")
    lines.append("")
    lines.append(f"Wall-clock (slowest single run): {summary['wall_clock_ms']/1000:.1f}s")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("iteration_dir", type=Path, help="e.g. skills/mission-lock-workspace/iteration-11")
    ap.add_argument("--output", type=Path, required=True, help="e.g. evals/benchmarks/versions/unreleased")
    args = ap.parse_args()

    summary = build_summary(args.iteration_dir)

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "timing-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (args.output / "timing-summary.md").write_text(render_markdown(summary))

    print(f"Wrote {args.output / 'timing-summary.json'}")
    print(f"Wrote {args.output / 'timing-summary.md'}")
    t = summary["totals"]
    print(f"\n{len(summary['evals'])} evals — {t['tokens']:,} tokens, {t['duration_ms']/1000:.1f}s total, "
          f"{t['tool_uses']} tool calls, {summary['wall_clock_ms']/1000:.1f}s wall-clock "
          f"— model: {summary['model']} (effort: {summary['effort']})")


if __name__ == "__main__":
    main()
