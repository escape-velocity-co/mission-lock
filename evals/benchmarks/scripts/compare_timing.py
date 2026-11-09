#!/usr/bin/env python3
"""Diff two timing-summary.json files (from aggregate_timing.py) and print
the delta: totals (tokens/duration/tool_uses), wall-clock, and a per-eval
breakdown, matched by eval id (so it still works if the eval corpus itself
changed between the two runs — an eval present in only one side is called
out rather than silently skipped or crashing).

Usage:
    python3 compare_timing.py <A: dir-or-timing-summary.json> <B: dir-or-timing-summary.json>
    python3 compare_timing.py <A> <B> --markdown-rows --label "In Development"

e.g.:
    python3 compare_timing.py evals/benchmarks/versions/0.2.0 evals/benchmarks/versions/unreleased

--markdown-rows prints the two lines evals/benchmarks/history.md actually
wants — B's data row and the "Δ vs. previous" row, using that file's own
formatting conventions (tokens truncated to millions at 2 decimals,
seconds rounded to whole numbers, delta percentages rounded to whole
numbers) — ready to paste in rather than hand-computed.
"""
import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


def load(path: Path):
    if path.is_dir():
        path = path / "timing-summary.json"
    return json.loads(path.read_text())


def model_effort_label(summary):
    """Older timing-summary.json files (pre-model/effort capture) won't
    have these keys at all — report "unknown" rather than crashing or
    silently omitting it, since an unrecorded model/effort is itself
    important context, not a missing detail to paper over."""
    model = summary.get("model") or "unknown"
    effort = summary.get("effort") or "unknown"
    return f"{model} (effort: {effort})"


def pct(a, b):
    if a == 0:
        return float("inf") if b else 0.0
    return (b - a) / a * 100


def fmt_delta_pct(a, b):
    p = pct(a, b)
    sign = "+" if p > 0 else ""
    return f"{sign}{p:.1f}%"


def fmt_delta_pct_whole(a, b):
    """Same as fmt_delta_pct but rounded to a whole number — history.md's
    own convention for the "Δ vs. previous" row."""
    p = pct(a, b)
    sign = "+" if p > 0 else ""
    return f"{sign}{round(p)}%"


def fmt_tokens_millions(n):
    """Truncate (not round) to 2 decimal places in millions — matches
    history.md's existing rows (e.g. 1,278,580 -> "1.27M", not "1.28M")."""
    truncated = math.floor(n / 1_000_000 * 100) / 100
    return f"{truncated:.2f}M"


def fmt_seconds_whole(ms):
    """Round (not truncate) to the nearest whole second — history.md's
    convention for Duration/Wall-clock."""
    return f"{round(ms / 1000)}s"


def markdown_data_row(label, date, summary):
    t = summary["totals"]
    model = summary.get("model") or "unknown"
    effort = summary.get("effort") or "unknown"
    return (f"| {label} | {date} | {len(summary['evals'])} | {model} | {effort} | {fmt_tokens_millions(t['tokens'])} | "
            f"{t['tool_uses']} | {fmt_seconds_whole(t['duration_ms'])} | {fmt_seconds_whole(summary['wall_clock_ms'])} |")


def markdown_delta_row(a, b):
    ta, tb = a["totals"], b["totals"]
    return (f"| Δ vs. previous | | | | | {fmt_delta_pct_whole(ta['tokens'], tb['tokens'])} | "
            f"{fmt_delta_pct_whole(ta['tool_uses'], tb['tool_uses'])} | "
            f"{fmt_delta_pct_whole(ta['duration_ms'], tb['duration_ms'])} | "
            f"{fmt_delta_pct_whole(a['wall_clock_ms'], b['wall_clock_ms'])} |")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a", type=Path, help="baseline: a timing-summary.json, or a directory containing one")
    ap.add_argument("b", type=Path, help="comparison: a timing-summary.json, or a directory containing one")
    ap.add_argument("--markdown-rows", action="store_true",
                    help="Print B's history.md data row plus the 'Δ vs. previous' row, instead of the full terminal report.")
    ap.add_argument("--label", default="In Development", help="Label for B's row in --markdown-rows output (default: 'In Development').")
    ap.add_argument("--date", default=None, help="Date for B's row in --markdown-rows output (default: today, UTC).")
    args = ap.parse_args()

    a = load(args.a)
    b = load(args.b)

    if args.markdown_rows:
        date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        if (a.get("model"), a.get("effort")) != (b.get("model"), b.get("effort")):
            print(
                f"WARNING: model/effort differ between A ({model_effort_label(a)}) and "
                f"B ({model_effort_label(b)}) — the Δ row below may reflect that "
                "difference rather than a real change.",
                file=sys.stderr,
            )
        print(markdown_data_row(args.label, date, b))
        print(markdown_delta_row(a, b))
        return

    label_a = f"iteration {a['iteration']} (v{a['skill_version']})"
    label_b = f"iteration {b['iteration']} (v{b['skill_version']})"

    print(f"Comparing {label_a}  ->  {label_b}\n")

    model_a, model_b = model_effort_label(a), model_effort_label(b)
    print(f"Model/effort — A: {model_a}   B: {model_b}")
    if (a.get("model"), a.get("effort")) != (b.get("model"), b.get("effort")):
        print(
            "WARNING: model and/or effort differ between these two runs — any timing "
            "delta below may reflect that difference rather than a change to the skill "
            "or eval suite. Treat this comparison as inconclusive until re-run under "
            "matching model/effort."
        )
    print()

    print(f"{'':22s} {label_a:>22s} {label_b:>22s} {'delta':>12s}")
    ta, tb = a["totals"], b["totals"]
    print(f"{'Total tokens':22s} {ta['tokens']:22,d} {tb['tokens']:22,d} {fmt_delta_pct(ta['tokens'], tb['tokens']):>12s}")
    print(f"{'Total duration':22s} {ta['duration_ms']/1000:21.1f}s {tb['duration_ms']/1000:21.1f}s {fmt_delta_pct(ta['duration_ms'], tb['duration_ms']):>12s}")
    print(f"{'Total tool calls':22s} {ta['tool_uses']:22,d} {tb['tool_uses']:22,d} {fmt_delta_pct(ta['tool_uses'], tb['tool_uses']):>12s}")
    print(f"{'Wall-clock (slowest)':22s} {a['wall_clock_ms']/1000:21.1f}s {b['wall_clock_ms']/1000:21.1f}s {fmt_delta_pct(a['wall_clock_ms'], b['wall_clock_ms']):>12s}")

    a_by_id = {e["id"]: e for e in a["evals"] if e["id"] is not None}
    b_by_id = {e["id"]: e for e in b["evals"] if e["id"] is not None}
    common_ids = sorted(set(a_by_id) & set(b_by_id))
    only_a = sorted(set(a_by_id) - set(b_by_id))
    only_b = sorted(set(b_by_id) - set(a_by_id))

    faster = sum(1 for i in common_ids if b_by_id[i]["duration_ms"] < a_by_id[i]["duration_ms"])
    fewer_tok = sum(1 for i in common_ids if b_by_id[i]["tokens"] < a_by_id[i]["tokens"])
    print(f"\nEvals present in both: {len(common_ids)} — {faster} faster, {fewer_tok} used fewer tokens")

    if only_a:
        print(f"Only in {label_a}: {[a_by_id[i]['name'] for i in only_a]}")
    if only_b:
        print(f"Only in {label_b}: {[b_by_id[i]['name'] for i in only_b]}")

    name_width = max([len("Eval")] + [len(a_by_id[i]["name"]) for i in common_ids]) + 2
    print(f"\n{'Eval':{name_width}s} {'tokens ' + label_a:>18s} {'tokens ' + label_b:>18s} {'delta':>10s}")
    for i in common_ids:
        ea, eb = a_by_id[i], b_by_id[i]
        print(f"{ea['name']:{name_width}s} {ea['tokens']:18,d} {eb['tokens']:18,d} {fmt_delta_pct(ea['tokens'], eb['tokens']):>10s}")


if __name__ == "__main__":
    main()
