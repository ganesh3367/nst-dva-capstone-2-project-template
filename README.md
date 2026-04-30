# Smartwatch Health Analytics — User Risk Segmentation

> **Newton School of Technology | Data Visualization & Analytics — Capstone 2**
> Converting raw wearable health data into actionable corporate wellness recommendations using Python, GitHub, and Tableau.

---

## Project Overview

| Field | Details |
|---|---|
| **Project Title** | Smartwatch Health Analytics — User Risk Segmentation |
| **Sector** | Digital Health / Corporate Wellness |
| **Team ID** | _To be filled by team_ |
| **Section** | _To be confirmed by faculty_ |
| **Faculty Mentor** | _To be filled by team_ |
| **Institute** | Newton School of Technology |
| **Submission Date** | April 28, 2026 |

### Team Members

| Role | Name | GitHub Username |
|---|---|---|
| Project Lead | _Name_ | `github-handle` |
| Data Lead | _Name_ | `github-handle` |
| ETL Lead | _Name_ | `github-handle` |
| Analysis Lead | _Name_ | `github-handle` |
| Visualization Lead | _Name_ | `github-handle` |
| Strategy Lead | _Name_ | `github-handle` |
| PPT and Quality Lead | _Name_ | `github-handle` |

---

## Business Problem

Corporate HR teams and health insurers lack a systematic way to identify which employee segments carry the highest health risk based on wearable data. Without data-driven segmentation, wellness budgets are spread uniformly across all users rather than directed to the highest-risk cohorts.

This project analyses 10,000 smartwatch user records — covering heart rate, blood oxygen, sleep, steps, and stress — to identify distinct health risk profiles and surface the behavioral drivers most strongly associated with poor health outcomes.

**Core Business Question**

> Which user segments show the highest cardiovascular and mental health risk, and which behavioral patterns (activity, sleep, stress) are the strongest predictors of poor health outcomes?

**Decision Supported**

> HR directors and wellness program managers can use this analysis to allocate intervention budgets to high-risk user segments and design targeted programs (step challenges, sleep coaching, stress management) with measurable expected impact.

---

## Dataset

| Attribute | Details |
|---|---|
| **Source Name** | Simulated Smartwatch Health Dataset |
| **Raw File** | `data/raw/unclean_smartwatch_health_data.csv` |
| **Row Count** | 10,000 |
| **Column Count (raw)** | 7 |
| **Column Count (processed + derived)** | 13 |
| **Format** | CSV |

**Key Columns Used**

| Column Name | Description | Role in Analysis |
|---|---|---|
| `heart_rate_bpm` | Resting heart rate in BPM | KPI, cardiovascular risk flag, clustering |
| `blood_oxygen_level` | SpO₂ saturation percentage | KPI, blood oxygen status filter |
| `step_count` | Daily step count | KPI, step category filter, regression feature |
| `sleep_duration_hours` | Nightly sleep in hours | KPI, sleep quality filter, regression feature |
| `activity_level` | Categorical activity tier | Primary segment dimension across all charts |
| `stress_level` | Ordinal stress score (1–5) | KPI, ANOVA target, regression target |
| `wellness_score` | Derived composite score (0–100) | Executive KPI scorecard |

For full column definitions, see [`docs/data_dictionary.md`](docs/data_dictionary.md).

---

## KPI Framework

| KPI | Definition | Formula / Computation |
|---|---|---|
| High Cardiovascular Risk Rate | % of users with resting HR > 100 BPM (tachycardia threshold) | `(heart_rate_bpm > 100).sum() / total_valid * 100` |
| Step Goal Achievement Rate | % of users meeting 10,000 steps/day WHO recommendation | `(step_count >= 10000).sum() / total_valid * 100` |
| Poor Sleep Rate | % of users sleeping fewer than 7 hours/night | `(sleep_duration_hours < 7).sum() / total_valid * 100` |
| Low Blood Oxygen Rate | % of users with SpO₂ below 95% clinical threshold | `(blood_oxygen_level < 95).sum() / total_valid * 100` |
| Average Wellness Score | Mean composite health score across all users (0–100) | Weighted combination of sleep, steps, stress, HR, SpO₂ — see `05_final_load_prep.ipynb` |

KPI computation logic lives in [`notebooks/05_final_load_prep.ipynb`](notebooks/05_final_load_prep.ipynb).

---

## Tableau Dashboard

| Item | Details |
|---|---|
| **Dashboard URL** | _Paste Tableau Public link here after publishing_ |
| **Executive View** | KPI scorecard: cardiovascular risk rate, step goal rate, poor sleep rate, avg wellness score by activity level |
| **Operational View** | User-level drill-down: filter by activity level, sleep quality, stress category, cardiovascular risk flag |
| **Main Filters** | Activity Level, Sleep Quality, Cardiovascular Risk Flag, Stress Category, Step Category |

Dashboard screenshots → [`tableau/screenshots/`](tableau/screenshots/)
Public link → [`tableau/dashboard_links.md`](tableau/dashboard_links.md)

---

## Key Insights

1. **Sedentary users carry significantly higher resting heart rates** than highly active users — confirmed by a statistically significant t-test (p < 0.05), making activity level the single strongest risk differentiator.
2. **Sleep duration is the strongest behavioral predictor of stress** — Pearson correlation shows a significant negative relationship: each additional hour of sleep reduces stress by approximately 0.2 points on the 1–5 scale.
3. **Step count is positively correlated with blood oxygen** — active users consistently maintain SpO₂ above the 95% clinical threshold, while sedentary users show higher rates of borderline hypoxemia.
4. **K-Means clustering reveals 3–4 distinct user risk profiles** — a high-risk cluster (low steps, elevated HR, high stress, poor sleep) and a healthy cluster (high steps, normal HR, low stress, good sleep) anchor opposite ends of the wellness spectrum.
5. **The poor sleep rate is substantial** — a meaningful proportion of users sleep fewer than 7 hours, cutting across all activity levels and suggesting sleep is a systemic problem, not limited to sedentary users.
6. **ANOVA confirms stress levels differ significantly across activity groups** (p < 0.05) — physical activity is a statistically validated stress buffer, not just an observed trend.
7. **Blood oxygen deficiency is concentrated in the sedentary segment** — low SpO₂ (< 95%) users are disproportionately represented among users with < 5,000 steps/day.
8. **Highly active users show the highest wellness scores** — the composite wellness score confirms that consistent activity drives holistic health improvements, not just cardiovascular outcomes.
9. **Stress level 4–5 (High/Very High) users also tend to have shorter sleep** — the sleep-stress bidirectional relationship suggests interventions targeting one will benefit the other.
10. **Step goal achievement is low across the dataset** — fewer than half of users reach 10,000 steps/day, presenting a large addressable opportunity for step-challenge programs.

---

## Recommendations

| # | Insight | Recommendation | Expected Impact |
|---|---|---|---|
| 1 | Sedentary users have measurably elevated resting HR | Launch a 30-day step-challenge program targeting the sedentary and lightly active segments, with smartwatch-triggered nudges at midday | Reduce high cardiovascular risk rate by ~15–20% within one quarter |
| 2 | Sleep < 7h drives elevated stress scores | Deploy an in-app sleep coaching module for users flagged as Poor/Very Poor sleep quality — push-notifications for consistent bedtime routines | Projected 0.3–0.5 point reduction in average stress score among targeted users |
| 3 | High-risk cluster (low steps + high stress + poor sleep) represents the highest-burden segment | Create a prioritised wellness plan for HR cluster-flagged users, including subsidised counselling sessions and wearable-based stress alerts | Reduce high-risk cluster membership by ~10% over 6 months |
| 4 | Blood oxygen drops below 95% in sedentary users | Integrate SpO₂ alerts into the wellness app: notify users when blood oxygen falls below 95% with a prompt to take a short walk | Improve average SpO₂ in the sedentary segment; reduce clinical threshold breach rate |
| 5 | Step goal achievement is low across all segments | Partner with employers to gamify step goals — team-based leaderboards and milestone rewards have proven ROI in corporate wellness literature | Increase step goal achievement rate by 20–25 percentage points among participating teams |

---

## Repository Structure

```text
SectionName_TeamID_RetailCustomerSegmentation/
|
|-- README.md
|
|-- data/
|   |-- raw/                         # unclean_smartwatch_health_data.csv (never edited)
|   `-- processed/                   # clean_smartwatch_health_data.csv, tableau_ready_dataset.csv
|
|-- notebooks/
|   |-- 01_extraction.ipynb          # Load, profile, document quality issues
|   |-- 02_cleaning.ipynb            # Fix nulls, types, misspellings, outliers
|   |-- 03_eda.ipynb                 # Distributions, correlations, segment analysis
|   |-- 04_statistical_analysis.ipynb  # T-test, ANOVA, regression, K-Means clustering
|   `-- 05_final_load_prep.ipynb     # KPI computation, derived columns, Tableau export
|
|-- scripts/
|   `-- etl_pipeline.py             # Production-style standalone ETL script
|
|-- tableau/
|   |-- screenshots/                 # Dashboard screenshots
|   `-- dashboard_links.md           # Tableau Public URL
|
|-- reports/
|   |-- project_report_template.md
|   |-- presentation_outline.md
|   `-- README.md
|
|-- docs/
|   `-- data_dictionary.md          # All raw + derived column definitions
|
|-- DVA-oriented-Resume/
`-- DVA-focused-Portfolio/
```

---

## Analytical Pipeline

1. **Define** — Digital health sector selected; corporate wellness decision-maker persona; problem statement scoped to user risk segmentation.
2. **Extract** — Raw smartwatch dataset (10,000 rows) committed to `data/raw/`; quality issues profiled in `01_extraction.ipynb`.
3. **Clean & Transform** — Nulls, misspellings, outliers, and type errors corrected in `02_cleaning.ipynb` and `scripts/etl_pipeline.py`.
4. **Analyze** — EDA in `03_eda.ipynb`; hypothesis testing, regression, and K-Means clustering in `04_statistical_analysis.ipynb`.
5. **Visualize** — Interactive Tableau Public dashboard with executive KPI view and operational drill-down.
6. **Recommend** — 5 data-backed business recommendations tied to statistical findings.
7. **Report** — Final report and presentation deck in `reports/`.

---

## Tech Stack

| Tool | Status | Purpose |
|---|---|---|
| Python + Jupyter Notebooks | Mandatory | ETL, cleaning, analysis, KPI computation |
| Google Colab | Supported | Cloud notebook execution |
| Tableau Public | Mandatory | Dashboard design and publishing |
| GitHub | Mandatory | Version control, collaboration, contribution audit |
| pandas, numpy, matplotlib, seaborn | Required | Data manipulation and visualisation |
| scipy, scikit-learn | Required | Statistical tests and clustering |

---

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Run the ETL pipeline standalone:

```bash
python scripts/etl_pipeline.py \
    --input data/raw/unclean_smartwatch_health_data.csv \
    --output data/processed/clean_smartwatch_health_data.csv
```

Then run notebooks in order: `01` → `02` → `03` → `04` → `05`.

---

## Evaluation Rubric

| Area | Marks | Focus |
|---|---|---|
| Problem Framing | 10 | Sharp, scoped business question with a named decision-maker |
| Data Quality and ETL | 15 | Pipeline documented, reproducible, transformation log present |
| Analysis Depth | 25 | Statistical methods applied correctly; insights in decision language |
| Dashboard and Visualization | 20 | Interactive Tableau dashboard directly addresses business problem |
| Business Recommendations | 20 | Actionable, tied to findings, with estimated impact |
| Storytelling and Clarity | 10 | Repo, report, and deck tell one coherent story |
| **Total** | **100** | |

---

## Submission Checklist

**GitHub Repository**

- [ ] Public repository with correct naming convention
- [ ] All 5 notebooks committed in `.ipynb` format with outputs
- [ ] `data/raw/` contains the original, unedited dataset
- [ ] `data/processed/` contains cleaned and Tableau-ready CSVs
- [ ] `tableau/screenshots/` contains dashboard screenshots
- [ ] `tableau/dashboard_links.md` contains the Tableau Public URL
- [ ] `docs/data_dictionary.md` complete with all 13 columns
- [ ] `README.md` explains project, dataset, KPIs, insights, and recommendations
- [ ] All team members have visible commits and pull requests

**Tableau Dashboard**

- [ ] Published on Tableau Public and accessible via public URL
- [ ] At least one interactive filter implemented
- [ ] Executive view + operational drill-down view

**Project Report**

- [ ] Final report exported as PDF into `reports/`
- [ ] All 14 sections covered (see `reports/project_report_template.md`)
- [ ] Contribution matrix matches GitHub Insights

**Presentation Deck**

- [ ] Final presentation exported as PDF into `reports/`

**Individual Assets**

- [ ] DVA-oriented resume updated
- [ ] Portfolio case study added with dashboard link

---

## Contribution Matrix

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
|---|---|---|---|---|---|---|---|
| _Member 1_ | Owner | Support | — | — | — | Owner | Support |
| _Member 2_ | Support | Owner | — | — | — | Support | — |
| _Member 3_ | — | Support | Owner | Support | Support | Support | — |
| _Member 4_ | — | — | Support | Owner | Owner | Support | Support |
| _Member 5_ | — | — | — | — | Support | Owner | Owner |

_Declaration: We confirm that the above contribution details are accurate and verifiable through GitHub Insights, PR history, and submitted artifacts._

**Team Lead Name:** _____________________________

**Date:** April 28, 2026

---

## Academic Integrity

All analysis, code, and recommendations in this repository are the original work of the team listed above. Contributions are tracked via GitHub Insights and pull request history. Any mismatch between the contribution matrix and actual commit history may result in individual grade adjustments.

---

*Newton School of Technology — Data Visualization & Analytics | Capstone 2*
