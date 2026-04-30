# Data Dictionary — Smartwatch Health Analytics

## Dataset Summary

| Item | Details |
|---|---|
| Dataset name | Unclean Smartwatch Health Data |
| Source | Simulated wearable device telemetry dataset |
| Raw file name | `unclean_smartwatch_health_data.csv` |
| Cleaned file name | `clean_smartwatch_health_data.csv` |
| Tableau-ready file | `tableau_ready_dataset.csv` |
| Row count | 10,000 |
| Column count (raw) | 7 |
| Column count (processed + derived) | 13 |
| Granularity | One row per user reading (daily summary) |

---

## Raw Column Definitions

| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `User ID` → `user_id` | Integer | Unique identifier for each smartwatch user | `4174` | EDA, KPI | Rows with null user_id dropped; cast to Int64 |
| `Heart Rate (BPM)` → `heart_rate_bpm` | Float | Resting heart rate measured by the smartwatch in beats per minute | `72.4` | EDA, KPI, Tableau | Outliers > 220 or < 30 BPM capped; nulls imputed with median |
| `Blood Oxygen Level (%)` → `blood_oxygen_level` | Float | Blood oxygen saturation (SpO₂) as a percentage | `97.5` | EDA, KPI, Tableau | Values clipped to [85, 100]; nulls imputed with median |
| `Step Count` → `step_count` | Integer | Total daily step count recorded by the device | `8,234` | EDA, KPI, Tableau | Cast to Int64; nulls imputed with median |
| `Sleep Duration (hours)` → `sleep_duration_hours` | Float | Total sleep duration in hours for the night preceding the reading | `7.2` | EDA, KPI, Tableau | `ERROR` strings coerced to NaN; nulls imputed with median |
| `Activity Level` → `activity_level` | String (categorical) | Self-reported or device-inferred physical activity category | `active` | EDA, KPI, Tableau, clustering | Misspellings corrected (`Actve`→`active`, `Highly_Active`→`highly active`, `Seddentary`→`sedentary`); lowercased and stripped |
| `Stress Level` → `stress_level` | Integer (1–5) | Stress score on a 1–5 ordinal scale (1 = very low, 5 = very high) | `3` | EDA, KPI, Tableau | Non-numeric strings coerced to NaN; nulls imputed with median |

---

## Derived Column Definitions

| Derived Column | Logic | Business Meaning |
|---|---|---|
| `sleep_quality` | Binned from `sleep_duration_hours`: < 5h = Very Poor, 5–7h = Poor, 7–9h = Good, > 9h = Excessive | Enables Tableau filtering by sleep health category |
| `step_category` | Binned from `step_count`: < 5k = Low, 5k–7.5k = Moderate, 7.5k–10k = Active, > 10k = High | Segments users by WHO daily step targets |
| `cardiovascular_risk_flag` | `High Risk` if `heart_rate_bpm` > 100, else `Normal` | Flags users at tachycardia risk for priority intervention |
| `blood_oxygen_status` | Binned: < 90% = Critical, 90–95% = Low, ≥ 95% = Normal | Highlights users needing respiratory health support |
| `stress_category` | Maps `stress_level` 1–5 to labels: Very Low / Low / Moderate / High / Very High | Human-readable stress label for Tableau filters and tooltips |
| `wellness_score` | Composite 0–100: sleep (20 pts) + steps (25 pts) + low stress (25 pts) + normal HR (15 pts) + good SpO₂ (15 pts) | Single executive KPI summarising overall user health status |

---

## Activity Level Categories

| Category | Meaning | Expected Step Range |
|---|---|---|
| `sedentary` | Little to no physical activity | < 3,000 steps/day |
| `lightly active` | Light movement, mostly desk-based | 3,000–5,000 steps/day |
| `active` | Regular moderate activity | 5,000–10,000 steps/day |
| `highly active` | Vigorous daily physical activity | > 10,000 steps/day |

---

## Stress Level Scale

| Value | Label | Interpretation |
|---|---|---|
| 1 | Very Low | Minimal stress, optimal recovery |
| 2 | Low | Below-average stress load |
| 3 | Moderate | Average stress — monitor trends |
| 4 | High | Elevated — consider intervention |
| 5 | Very High | Critical stress level — priority for wellness program |

---

## Data Quality Notes

- **Missing User IDs:** Rows where `User ID` was blank were dropped — they cannot be attributed to any individual.
- **Heart Rate outliers:** Values above 220 BPM (physiologically impossible for a resting reading) and below 30 BPM were capped, not dropped, to preserve row count.
- **Sleep Duration `ERROR` values:** Approximately 1–2% of rows had the string `ERROR` in the sleep column, likely a device sync failure. These were coerced to NaN and then imputed.
- **Activity Level misspellings:** At least three distinct misspellings (`Actve`, `Highly_Active`, `Seddentary`) were found and corrected before analysis.
- **Imputation strategy:** Median imputation used for all numeric nulls to avoid distorting distributions in the presence of outliers.
- **No time dimension:** The dataset does not include a date or timestamp column — all analysis is cross-sectional (snapshot), not longitudinal.
