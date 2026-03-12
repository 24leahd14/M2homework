#!/usr/bin/env python3
"""Generate a PR-friendly (text) SVG rank-order figure from course rankings."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "results" / "course_rankings.csv"
SVG_PATH = ROOT / "outputs" / "rank_order.svg"


def read_rows() -> list[tuple[int, str, float]]:
    rows: list[tuple[int, str, float]] = []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append((int(row["rank"]), row["course"], float(row["weighted_score"])))
    return sorted(rows, key=lambda item: item[0])


def generate_svg(rows: list[tuple[int, str, float]]) -> str:
    width = 1400
    height = 980
    left_label = 330
    chart_left = 520
    chart_right = width - 80
    top = 110
    row_h = 36
    gap = 8

    min_score = 0.0
    max_score = max(score for _, _, score in rows)
    span = max(max_score - min_score, 1e-9)
    zero_x = chart_left

    parts: list[str] = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )
    parts.append('<rect width="100%" height="100%" fill="#f8fafc"/>')
    parts.append(
        '<text x="40" y="52" font-family="Arial, Helvetica, sans-serif" font-size="30" '
        'fill="#19315a" font-weight="700">Course Rank Order by Weighted Score</text>'
    )
    parts.append(
        f'<line x1="{zero_x:.1f}" y1="90" x2="{zero_x:.1f}" y2="{top + len(rows) * (row_h + gap)}" '
        'stroke="#9ca3af" stroke-width="2"/>'
    )

    for idx, (rank, course, score) in enumerate(rows):
        y = top + idx * (row_h + gap)
        x_end = chart_left + (score - min_score) / span * (chart_right - chart_left)
        x = zero_x
        bar_w = max(1.0, x_end - zero_x)
        color = "#3b82f6"
        course_label = course.replace("&", "&amp;")

        parts.append(
            f'<text x="40" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="20" fill="#1f2937">'
            f'#{rank} {course_label}</text>'
        )
        parts.append(
            f'<rect x="{x:.1f}" y="{y}" width="{bar_w:.1f}" height="{row_h}" fill="{color}" rx="3"/>'
        )
        parts.append(
            f'<text x="{chart_right + 10}" y="{y + 24}" font-family="Arial, Helvetica, sans-serif" font-size="18" '
            f'fill="#374151">{score:.3f}</text>'
        )

    legend_y = height - 35
    parts.append('<rect x="40" y="940" width="18" height="18" fill="#3b82f6"/>')
    parts.append(
        f'<text x="66" y="{legend_y}" font-family="Arial, Helvetica, sans-serif" font-size="18" fill="#374151">Positive score</text>'
    )
    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    rows = read_rows()
    SVG_PATH.parent.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(generate_svg(rows), encoding="utf-8")
    print(f"Wrote {SVG_PATH}")


if __name__ == "__main__":
    main()
