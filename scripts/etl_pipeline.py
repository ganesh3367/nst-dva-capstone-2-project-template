"""ETL pipeline for Smartwatch Health Analytics — User Risk Segmentation.

Loads the raw unclean smartwatch dataset, applies all cleaning transformations
documented in notebooks/02_cleaning.ipynb, and exports the processed file to
data/processed/clean_smartwatch_health_data.csv.

Usage:
    python scripts/etl_pipeline.py \
        --input data/raw/unclean_smartwatch_health_data.csv \
        --output data/processed/clean_smartwatch_health_data.csv
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Step 1 — Load
# ---------------------------------------------------------------------------

def load_raw(input_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    log.info("Loaded %d rows × %d columns from %s", len(df), len(df.columns), input_path)
    return df


# ---------------------------------------------------------------------------
# Step 2 — Normalize column names
# ---------------------------------------------------------------------------

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )
    log.info("Columns normalized: %s", df.columns.tolist())
    return df


# ---------------------------------------------------------------------------
# Step 3 — Remove duplicates and rows with missing user_id
# ---------------------------------------------------------------------------

def remove_duplicates_and_null_ids(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(subset=["user_id"])
    log.info("Removed %d duplicate/null-ID rows (%d → %d)", before - len(df), before, len(df))
    return df


# ---------------------------------------------------------------------------
# Step 4 — Standardize activity_level categories
# ---------------------------------------------------------------------------

ACTIVITY_NORMALISATION = {
    "highly_active": "highly active",
    "actve": "active",
    "seddentary": "sedentary",
    "nan": np.nan,
}


def clean_activity_level(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["activity_level"] = (
        df["activity_level"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace(ACTIVITY_NORMALISATION)
    )
    df["activity_level"] = df["activity_level"].where(df["activity_level"] != "nan", other=np.nan)
    log.info("activity_level values: %s", df["activity_level"].value_counts(dropna=False).to_dict())
    return df


# ---------------------------------------------------------------------------
# Step 5 — Fix sleep_duration_hours (coerce 'ERROR' and similar to NaN)
# ---------------------------------------------------------------------------

def clean_sleep_duration(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    before_nulls = df["sleep_duration_hours"].isna().sum()
    df["sleep_duration_hours"] = pd.to_numeric(df["sleep_duration_hours"], errors="coerce")
    after_nulls = df["sleep_duration_hours"].isna().sum()
    log.info("sleep_duration_hours: coerced %d non-numeric values to NaN", after_nulls - before_nulls)
    return df


# ---------------------------------------------------------------------------
# Step 6 — Fix stress_level (coerce non-numeric strings to NaN)
# ---------------------------------------------------------------------------

def clean_stress_level(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    before_nulls = df["stress_level"].isna().sum()
    df["stress_level"] = pd.to_numeric(df["stress_level"], errors="coerce")
    after_nulls = df["stress_level"].isna().sum()
    log.info("stress_level: coerced %d non-numeric values to NaN", after_nulls - before_nulls)
    return df


# ---------------------------------------------------------------------------
# Step 7 — Cast step_count and user_id to integer
# ---------------------------------------------------------------------------

def cast_integer_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["step_count"] = df["step_count"].round().astype("Int64")
    df["user_id"] = df["user_id"].round().astype("Int64")
    log.info("step_count and user_id cast to Int64")
    return df


# ---------------------------------------------------------------------------
# Step 8 — Cap physiological outliers
# ---------------------------------------------------------------------------

def cap_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Cap heart rate to [30, 220] BPM and blood oxygen to [85, 100]%."""
    df = df.copy()
    hr_col = "heart_rate_bpm"
    spo2_col = "blood_oxygen_level"

    hr_outliers = ((df[hr_col] < 30) | (df[hr_col] > 220)).sum()
    df[hr_col] = df[hr_col].clip(lower=30, upper=220)
    log.info("Heart rate: capped %d outlier values to [30, 220] BPM", hr_outliers)

    spo2_outliers = ((df[spo2_col] < 85) | (df[spo2_col] > 100)).sum()
    df[spo2_col] = df[spo2_col].clip(lower=85, upper=100)
    log.info("Blood oxygen: capped %d outlier values to [85, 100]%%", spo2_outliers)

    return df


# ---------------------------------------------------------------------------
# Step 9 — Impute remaining missing values with column medians
# ---------------------------------------------------------------------------

def impute_medians(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_cols = ["heart_rate_bpm", "blood_oxygen_level", "step_count",
                    "sleep_duration_hours", "stress_level"]
    for col in numeric_cols:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            log.info("Imputed %d nulls in '%s' with median %.4f", n_missing, col, median_val)
    return df


# ---------------------------------------------------------------------------
# Pipeline orchestration
# ---------------------------------------------------------------------------

def run_pipeline(input_path: Path) -> pd.DataFrame:
    df = load_raw(input_path)
    df = normalize_columns(df)
    df = remove_duplicates_and_null_ids(df)
    df = clean_activity_level(df)
    df = clean_sleep_duration(df)
    df = clean_stress_level(df)
    df = cast_integer_columns(df)
    df = cap_outliers(df)
    df = impute_medians(df)
    log.info("Pipeline complete. Final shape: %d rows × %d columns", len(df), len(df.columns))
    return df


def save_processed(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    log.info("Processed dataset saved to: %s", output_path)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smartwatch Health ETL Pipeline")
    parser.add_argument("--input", required=True, type=Path,
                        help="Path to raw CSV (data/raw/unclean_smartwatch_health_data.csv)")
    parser.add_argument("--output", required=True, type=Path,
                        help="Path for cleaned CSV output (data/processed/clean_smartwatch_health_data.csv)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_df = run_pipeline(args.input)
    save_processed(cleaned_df, args.output)
    print(f"\nRows: {len(cleaned_df):,} | Columns: {len(cleaned_df.columns)}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
