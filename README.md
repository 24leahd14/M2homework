# M2homework

This repository now includes a deterministic workflow to rank courses from the anonymized MAcc exit survey dataset.

## Question answered

> Rank order the programs or courses based on student ratings or preferences in this dataset.

The ranked output is generated in:

- `results/course_rankings.md` (human-readable ranking table)
- `results/course_rankings.csv` (machine-readable ranking table)

## Deterministic methodology

The script `scripts/rank_courses.py` parses the `.xlsx` file directly using Python standard library XML/ZIP support and computes rankings from **finished responses only** (`Finished == 1`).

For each course mention in each finished response:

- **Most Beneficial**: score from `+2` to `+3` (higher if ranked closer to #1 within that respondent's Most group)
- **Neutral**: score `0`
- **Least Beneficial**: score from `-2` to `-3` (more negative if ranked closer to #1 within that respondent's Least group)
- **Did not take**: excluded from scoring

Courses are rank-ordered by descending average score (with deterministic tie-breakers).

## Run locally

```bash
python scripts/rank_courses.py
```

## GitHub Actions

Workflow: `.github/workflows/rank-courses.yml`

It runs on `workflow_dispatch`, `push` to `main`, and `pull_request`, then uploads ranking artifacts.
