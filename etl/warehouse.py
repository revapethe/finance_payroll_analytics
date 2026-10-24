"""Transactional, idempotent PostgreSQL star-schema loading and reconciliation."""

import argparse
from datetime import date
import hashlib
from io import StringIO
import uuid
import pandas as pd
from sqlalchemy import text
from app.data import ROOT, load_employee_data
from app.database import create_payroll_engine

DEFAULT_SNAPSHOT = date(2026, 10, 23)
WAREHOUSE_COLUMNS = [
    "employee_id",
    "job_title",
    "remote_status",
    "performance",
    "hire_date",
    "country",
    "city",
    "department",
    "currency",
    "annual_salary_local",
    "annual_salary_usd",
    "years_of_service",
]


def validate_snapshot(frame, snapshot):
    missing = set(WAREHOUSE_COLUMNS) - set(frame.columns)
    if missing or frame[WAREHOUSE_COLUMNS].isna().any().any():
        raise ValueError("Warehouse columns must be present and non-null.")
    if not frame.remote_status.isin(["Remote", "Hybrid", "On-Site"]).all():
        raise ValueError("Unsupported remote status.")
    expected = frame.country.map({"United States": "USD", "India": "INR"})
    if expected.isna().any() or not expected.eq(frame.currency).all():
        raise ValueError("Country/currency mismatch.")
    for column in ["annual_salary_local", "years_of_service"]:
        values = pd.to_numeric(frame[column], errors="raise")
        import numpy as np

        if not np.isfinite(values).all() or values.lt(0).any():
            raise ValueError(f"Invalid {column}.")
    hire_dates = pd.to_datetime(frame.hire_date, errors="raise").dt.date
    if (hire_dates > snapshot).any():
        raise ValueError("Hire dates cannot be later than the snapshot.")


def load_warehouse(snapshot=DEFAULT_SNAPSHOT, source=None, engine=None):
    frame = load_employee_data(source)
    validate_snapshot(frame, snapshot)
    # Hash canonical source values, not a path or credentials.
    source_hash = hashlib.sha256(frame.to_csv(index=False).encode()).hexdigest()
    own_engine = engine is None
    engine = engine or create_payroll_engine()
    batch_id = str(uuid.uuid4())
    try:
        with engine.begin() as conn:
            # Serialize schema creation and writes, including concurrent refreshes.
            conn.execute(text("SELECT pg_advisory_xact_lock(7202601023)"))
            raw = conn.connection.driver_connection
            raw.execute((ROOT / "sql/warehouse.sql").read_text(), prepare=False)
            raw.execute(
                "CREATE TEMP TABLE payroll_stage (LIKE payroll_analytics.v_employee_snapshot INCLUDING DEFAULTS) ON COMMIT DROP"
            )
            data = frame[WAREHOUSE_COLUMNS].copy()
            data.insert(1, "snapshot_date", snapshot)
            buffer = StringIO(data.to_csv(index=False, header=False))
            columns = ", ".join(data.columns)
            with raw.cursor().copy(
                f"COPY payroll_stage ({columns}) FROM STDIN WITH (FORMAT CSV)"
            ) as copy:
                copy.write(buffer.getvalue())
            raw.execute(
                """
                INSERT INTO payroll_analytics.dim_department(department)
                SELECT DISTINCT department FROM payroll_stage ORDER BY department
                ON CONFLICT(department) DO NOTHING;
                INSERT INTO payroll_analytics.dim_location(country, city)
                SELECT DISTINCT country, city FROM payroll_stage ORDER BY country, city
                ON CONFLICT(country, city) DO NOTHING;
                INSERT INTO payroll_analytics.dim_employee(employee_id, job_title, remote_status, performance, hire_date)
                SELECT employee_id, job_title, remote_status, performance, hire_date FROM payroll_stage
                ON CONFLICT(employee_id) DO UPDATE SET job_title=EXCLUDED.job_title,
                  remote_status=EXCLUDED.remote_status, performance=EXCLUDED.performance, hire_date=EXCLUDED.hire_date;
            """,
                prepare=False,
            )
            conn.execute(
                text("""INSERT INTO payroll_analytics.dim_snapshot VALUES (:snapshot, :year, :month, :name)
                ON CONFLICT(snapshot_date) DO NOTHING"""),
                {
                    "snapshot": snapshot,
                    "year": snapshot.year,
                    "month": snapshot.month,
                    "name": snapshot.strftime("%B"),
                },
            )
            conn.execute(
                text(
                    "DELETE FROM payroll_analytics.fact_compensation WHERE snapshot_date=:snapshot"
                ),
                {"snapshot": snapshot},
            )
            raw.execute("""INSERT INTO payroll_analytics.fact_compensation
                SELECT s.snapshot_date, s.employee_id, d.department_key, l.location_key,
                       s.currency, s.annual_salary_local, s.annual_salary_usd, s.years_of_service
                FROM payroll_stage s
                JOIN payroll_analytics.dim_department d USING(department)
                JOIN payroll_analytics.dim_location l USING(country, city)""")
            result = conn.execute(
                text("""SELECT count(*) AS rows, sum(annual_salary_usd) AS total
                FROM payroll_analytics.fact_compensation WHERE snapshot_date=:snapshot"""),
                {"snapshot": snapshot},
            ).one()
            expected_cents = sum(round(float(x) * 100) for x in frame.annual_salary_usd)
            if result.rows != len(frame) or round(result.total * 100) != expected_cents:
                raise ValueError(
                    "Warehouse row count or salary reconciliation failed; transaction rolled back."
                )
            conn.execute(
                text("""INSERT INTO payroll_analytics.load_audit
                (batch_id, snapshot_date, source_sha256, row_count, annual_payroll_usd)
                VALUES (:batch, :snapshot, :sha, :rows, :total)"""),
                {
                    "batch": batch_id,
                    "snapshot": snapshot,
                    "sha": source_hash,
                    "rows": result.rows,
                    "total": result.total,
                },
            )
        return {
            "batch_id": batch_id,
            "rows": len(frame),
            "snapshot_date": snapshot.isoformat(),
            "source_sha256": source_hash,
        }
    finally:
        if own_engine:
            engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-date", type=date.fromisoformat, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--source")
    args = parser.parse_args()
    result = load_warehouse(args.snapshot_date, args.source)
    print(
        f"Reconciled {result['rows']:,} employees for {result['snapshot_date']}; batch {result['batch_id']}"
    )
