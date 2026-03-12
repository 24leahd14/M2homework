#!/usr/bin/env python3
"""Deterministically rank MAcc courses from the exit survey workbook."""

from __future__ import annotations

import argparse
import csv
import re
import zipfile
from collections import defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

HEADER_PATTERN = re.compile(
    r"Ranks - (?P<group>Most Beneficial|Neutral|Least Beneficial|Did not take) - (?P<course>.+?) - Rank$"
)
NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="Grad Program Exit Survey Data.xlsx", help="Path to workbook")
    parser.add_argument("--csv-output", default="results/course_rankings.csv")
    parser.add_argument("--md-output", default="results/course_rankings.md")
    return parser.parse_args()


def load_shared_strings(zf: zipfile.ZipFile) -> list[str]:
    sst = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    out = []
    for si in sst.findall("a:si", NS):
        text = "".join((t.text or "") for t in si.findall(".//a:t", NS))
        out.append(text)
    return out


def col_to_index(ref: str) -> int:
    col = "".join(ch for ch in ref if ch.isalpha())
    idx = 0
    for ch in col:
        idx = idx * 26 + (ord(ch) - 64)
    return idx - 1


def read_sheet_rows(zf: zipfile.ZipFile, sheet_path: str) -> list[list[str]]:
    shared = load_shared_strings(zf)
    sheet = ET.fromstring(zf.read(sheet_path))

    rows: list[list[str]] = []
    for row in sheet.findall(".//a:sheetData/a:row", NS):
        cells: dict[int, str] = {}
        max_col = -1
        for cell in row.findall("a:c", NS):
            col_idx = col_to_index(cell.attrib["r"])
            max_col = max(max_col, col_idx)
            value_node = cell.find("a:v", NS)
            if value_node is None:
                cells[col_idx] = ""
                continue
            value = value_node.text or ""
            if cell.attrib.get("t") == "s":
                value = shared[int(value)]
            cells[col_idx] = value
        rows.append([cells.get(i, "") for i in range(max_col + 1)])
    return rows


def normalized_bonus(rank: int, max_rank: int) -> float:
    return 0.0 if max_rank <= 1 else (max_rank - rank) / (max_rank - 1)


def score_response(group: str, rank: int, max_rank: int) -> float | None:
    if group == "Did not take":
        return None
    if group == "Neutral":
        return 0.0
    bonus = normalized_bonus(rank, max_rank)
    if group == "Most Beneficial":
        return 2.0 + bonus
    if group == "Least Beneficial":
        return -2.0 - bonus
    raise ValueError(group)


def main() -> None:
    args = parse_args()

    with zipfile.ZipFile(args.input) as zf:
        rows = read_sheet_rows(zf, "xl/worksheets/sheet1.xml")

    headers = rows[0]
    finished_index = headers.index("Finished")

    rank_columns: dict[int, tuple[str, str]] = {}
    for idx, header in enumerate(headers):
        match = HEADER_PATTERN.search(header)
        if match:
            rank_columns[idx] = (match.group("group"), match.group("course"))

    scores_by_course: dict[str, list[float]] = defaultdict(list)
    mentions_by_course: dict[str, int] = defaultdict(int)
    group_counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for row in rows[2:]:
        if finished_index >= len(row) or str(row[finished_index]).strip() != "1":
            continue

        entries: list[tuple[str, str, int]] = []
        max_rank_by_group: dict[str, int] = defaultdict(int)

        for col_idx, (group, course) in rank_columns.items():
            if col_idx >= len(row):
                continue
            raw = str(row[col_idx]).strip()
            if not raw:
                continue
            rank = int(raw)
            entries.append((group, course, rank))
            if rank > max_rank_by_group[group]:
                max_rank_by_group[group] = rank

        for group, course, rank in entries:
            mentions_by_course[course] += 1
            group_counts[course][group] += 1
            score = score_response(group, rank, max_rank_by_group[group])
            if score is not None:
                scores_by_course[course].append(score)

    max_responses_used = max(len(scores) for scores in scores_by_course.values())

    ranked = []
    for course, scores in scores_by_course.items():
        responses_used = len(scores)
        avg_score = sum(scores) / responses_used
        response_weight = responses_used / max_responses_used
        weighted_score = avg_score * response_weight
        ranked.append(
            {
                "course": course,
                "responses_used": responses_used,
                "mentions_total": mentions_by_course[course],
                "most_beneficial": group_counts[course]["Most Beneficial"],
                "neutral": group_counts[course]["Neutral"],
                "least_beneficial": group_counts[course]["Least Beneficial"],
                "avg_score": round(avg_score, 4),
                "response_weight": round(response_weight, 4),
                "weighted_score": round(weighted_score, 4),
            }
        )

    ranked.sort(key=lambda item: (-item["weighted_score"], -item["avg_score"], -item["responses_used"], item["course"]))

    csv_path = Path(args.csv_output)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank",
        "course",
        "weighted_score",
        "avg_score",
        "response_weight",
        "responses_used",
        "mentions_total",
        "most_beneficial",
        "neutral",
        "least_beneficial",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for i, item in enumerate(ranked, start=1):
            writer.writerow({"rank": i, **item})

    md_path = Path(args.md_output)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Course Ranking from MAcc Exit Survey\n\n")
        f.write("Ranking uses only completed responses (`Finished == 1`). ")
        f.write(
            "Scoring is deterministic: Most Beneficial = +2 to +3 based on rank, Neutral = 0, "
            "Least Beneficial = -2 to -3 based on rank, and Did not take is excluded.\n\n"
        )
        f.write(
            "Final ranking uses `weighted_score = avg_score * (responses_used / max_responses_used)` "
            "to factor in how many completed responses contributed to each course.\n\n"
        )
        f.write("| Rank | Course | Weighted score | Avg score | Response weight | Responses used | Most | Neutral | Least |\n")
        f.write("| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
        for i, item in enumerate(ranked, start=1):
            f.write(
                f"| {i} | {item['course']} | {item['weighted_score']:.4f} | {item['avg_score']:.4f} "
                f"| {item['response_weight']:.4f} | {item['responses_used']} | "
                f"{item['most_beneficial']} | {item['neutral']} | {item['least_beneficial']} |\n"
            )


if __name__ == "__main__":
    main()
