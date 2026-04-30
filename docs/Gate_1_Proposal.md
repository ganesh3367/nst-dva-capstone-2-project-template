# Gate 1 Proposal

## Problem Statement
The aim of this project is to analyze raw smartwatch health data to uncover patterns and actionable insights regarding users' daily habits, such as their sleep duration, step count, activity levels, heart rate, and stress levels. By conducting exploratory data analysis and statistical modeling, the project will identify the correlation between lifestyle habits and health indicators.

## Dataset Link
[Smartwatch Health Data (Kaggle or relevant source) - Represented by local file](data/raw/unclean_smartwatch_health_data.csv)

## Initial Data Dictionary
| Column Name | Data Type | Description | Example Value | Used In | Cleaning Notes |
|---|---|---|---|---|---|
| `user_id` | Int64 | Unique identifier for each user | 4174 | EDA / Tableau | Deduplicated, handled nulls |
| `heart_rate_bpm` | float | Average heart rate in beats per minute | 58.94 | EDA / KPI / Tableau | Kept as float |
| `blood_oxygen_level` | float | Blood oxygen percentage | 98.81 | EDA / KPI / Tableau | Kept as float |
| `step_count` | Int64 | Total steps taken in a day | 5450 | EDA / KPI / Tableau | Casted to Integer |
| `sleep_duration_hours` | float | Hours of sleep recorded | 7.17 | EDA / KPI / Tableau | Converted 'ERROR' to NaN |
| `activity_level` | string | Categorical classification of activity | highly active | EDA / KPI / Tableau | Standardized strings |
| `stress_level` | float | Self-reported or inferred stress | 1.0 | EDA / KPI / Tableau | Converted 'Very High' to NaN |
