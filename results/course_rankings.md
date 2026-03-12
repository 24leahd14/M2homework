# Course Ranking from MAcc Exit Survey

Ranking uses only completed responses (`Finished == 1`). Scoring is deterministic: Most Beneficial = +2 to +3 based on rank, Neutral = 0, Least Beneficial = -2 to -3 based on rank, and Did not take is excluded.

Final ranking uses `weighted_score = avg_score * (responses_used / max_responses_used)` to factor in how many completed responses contributed to each course.

To keep values non-negative for reporting, avg and weighted scores are shifted upward by a constant offset equal to the absolute value of each metric's minimum.

| Rank | Course | Weighted score | Avg score | Response weight | Responses used | Most | Neutral | Least |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | ACC 6060 Professionalism and Leadership | 2.7453 | 2.8023 | 1.0000 | 53 | 39 | 12 | 2 |
| 2 | ACC 6400 Advanced Tax Business Entities | 2.5440 | 2.9717 | 0.8113 | 43 | 32 | 11 | 0 |
| 3 | ACC 6150 Info Sys Audit | 2.0148 | 3.4606 | 0.4340 | 23 | 21 | 1 | 1 |
| 4 | ACC 6300 Data Analytics | 1.8585 | 2.5117 | 0.6038 | 32 | 19 | 13 | 0 |
| 5 | ACC 6560 Financial Theory & Research I | 1.5796 | 1.6487 | 0.9811 | 52 | 24 | 18 | 10 |
| 6 | ACC 6600 Business Law for Accountants | 1.5126 | 2.7609 | 0.3208 | 17 | 13 | 2 | 2 |
| 7 | ACC 6420 Corporate Tax | 1.5003 | 2.5421 | 0.3585 | 19 | 12 | 6 | 1 |
| 8 | ACC 6030 Financial Accounting Reporting | 1.4085 | 1.5470 | 0.8491 | 45 | 15 | 24 | 6 |
| 9 | ACC 6350 Managment Control Systems | 1.3868 | 1.4609 | 0.9623 | 51 | 24 | 13 | 14 |
| 10 | ACC 6600 Business Law for Accountants (if taken as an elective) | 1.3538 | 2.7903 | 0.2264 | 12 | 9 | 2 | 1 |
| 11 | ACC 6410 Tax Research & Procedure | 1.3494 | 2.6352 | 0.2453 | 13 | 9 | 3 | 1 |
| 12 | ACC 6140 Fraud Exam & Forensic Acc | 1.2393 | 1.8140 | 0.3585 | 19 | 9 | 7 | 3 |
| 13 | ACC 6350 Mgmt Control Sys (if taken as an elective) | 1.2292 | 1.9320 | 0.3019 | 16 | 8 | 5 | 3 |
| 14 | ACC 6250 Financial Reporting and Analysis | 1.2220 | 1.8550 | 0.3208 | 17 | 6 | 10 | 1 |
| 15 | ACC 6440 Partnership Tax | 1.1701 | 1.7848 | 0.2830 | 15 | 8 | 3 | 4 |
| 16 | ACC 679R Special Topics | 1.0066 | 4.0070 | 0.0189 | 1 | 1 | 0 | 0 |
| 17 | ACC 6510 Financial Audit | 0.8443 | 0.8993 | 0.9811 | 52 | 13 | 22 | 17 |
| 18 | ACC 6610 Finance Statement Research | 0.7934 | 0.5920 | 0.3774 | 20 | 7 | 3 | 10 |
| 19 | ACC 6540 Professional Ethics | 0.0000 | 0.0000 | 0.9434 | 50 | 8 | 13 | 29 |
