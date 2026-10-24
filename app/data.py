"""Load the versioned synthetic fixture and validate it before analysis."""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCUMENTS = DATA / "documents"
REQUIRED = {"employee_id", "country", "department", "job_title", "city", "annual_salary_usd"}


def load_employee_data(path=None):
    frame = pd.read_csv(path or DATA / "employee_data.csv")
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Missing employee columns: {sorted(missing)}")
    if frame.empty or frame["employee_id"].isna().any() or frame["employee_id"].duplicated().any():
        raise ValueError("Employee IDs must be present and unique; data must not be empty.")
    if frame[list(REQUIRED)].isna().any().any():
        raise ValueError("Required employee fields must not contain nulls.")
    salary = pd.to_numeric(frame["annual_salary_usd"], errors="raise")
    import numpy as np

    if not np.isfinite(salary).all() or (salary < 0).any():
        raise ValueError("Salaries must be finite and nonnegative.")
    frame["annual_salary_usd"] = salary
    return frame
