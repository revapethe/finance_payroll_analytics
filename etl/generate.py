"""Expand the original 2,000-row synthetic fixture deterministically."""

import argparse
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
from app.data import DATA, load_employee_data

SEED_FILE = DATA / "seed_employees.csv"
AS_OF = date(2026, 10, 23)
# Illustrative ranges and conversion assumptions, not a compensation survey.
USD_PER_INR = 0.012
ROLES = {
    "Engineering": [("Software Engineer", 90000, 140000), ("Engineering Manager", 140000, 210000)],
    "Product": [("Product Manager", 110000, 160000), ("Product Analyst", 75000, 115000)],
    "Sales": [("Sales Representative", 55000, 95000), ("Sales Manager", 70000, 120000)],
    "Marketing": [("Marketing Analyst", 60000, 100000), ("Marketing Manager", 85000, 135000)],
    "HR": [("HR Specialist", 55000, 85000), ("HR Manager", 80000, 120000)],
    "Finance": [("Financial Analyst", 65000, 105000), ("Finance Manager", 95000, 145000)],
}
CITIES = {
    "United States": ["San Francisco", "New York", "Seattle", "Austin", "Boston"],
    "India": ["Bangalore", "Mumbai", "Hyderabad", "Pune", "Delhi"],
}


def generate_employees(rows=50000, seed=42):
    baseline = load_employee_data(SEED_FILE)
    if rows < len(baseline):
        raise ValueError(f"rows must be at least {len(baseline)} to retain the original fixture")
    rng = random.Random(seed)
    additions = []
    counts = baseline.country.value_counts().to_dict()
    for offset in range(rows - len(baseline)):
        country = "United States" if offset % 2 == 0 else "India"
        counts[country] += 1
        number = counts[country]
        prefix = "USA" if country == "United States" else "IND"
        department = rng.choice(list(ROLES))
        title, low, high = rng.choice(ROLES[department])
        # Indian ranges are illustrative local INR amounts derived from US ranges.
        local_salary = rng.randint(low, high) * (10 if country == "India" else 1)
        usd_salary = round(local_salary * USD_PER_INR, 2) if country == "India" else local_salary
        hire_date = AS_OF - timedelta(days=rng.randint(0, 3650))
        additions.append(
            {
                "employee_id": f"{prefix}{number:05d}",
                "first_name": f"Synthetic{prefix}{number}",
                "last_name": f"Employee{number}",
                "email": f"{prefix.lower()}{number}@example.invalid",
                "country": country,
                "city": rng.choice(CITIES[country]),
                "job_title": title,
                "department": department,
                "currency": "INR" if country == "India" else "USD",
                "annual_salary_local": local_salary,
                "annual_salary_usd": usd_salary,
                "hire_date": hire_date.isoformat(),
                "years_of_service": round((AS_OF - hire_date).days / 365.25, 1),
                "performance": rng.choice(["Satisfactory", "Good", "Excellent", "Outstanding"]),
                "remote_status": rng.choice(["Remote", "Hybrid", "On-Site"]),
            }
        )
    if not additions:
        return baseline.copy()
    return pd.concat([baseline, pd.DataFrame(additions)], ignore_index=True)[baseline.columns]


def write_dataset(rows=50000, seed=42, output=None):
    frame = generate_employees(rows, seed)
    destination = Path(output or DATA / "employee_data.csv")
    if destination.resolve() == SEED_FILE.resolve():
        raise ValueError("The original seed fixture must not be overwritten")
    destination.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(destination, index=False, float_format="%.2f", lineterminator="\n")
    return len(frame)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=50000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(f"Wrote {write_dataset(args.rows, args.seed, args.output):,} synthetic employees")
