"""Export the current PostgreSQL star model to CSV for Power BI file import."""

import json
from datetime import datetime, timezone
from app.data import DATA
from app.database import create_payroll_engine
import pandas as pd
from sqlalchemy import text

TABLES = {
    "dim_department": "dim_department",
    "dim_location": "dim_location",
    "dim_employee": "dim_employee",
    "dim_snapshot": "dim_snapshot",
    "fact_compensation": "bi_fact_compensation",
    "department_country": "v_department_country",
    "compensation_benchmarks": "v_compensation_benchmarks",
    "payroll_kpis": "v_payroll_kpis",
}


def export_model(destination=None, engine=None):
    destination = destination or DATA / "generated/powerbi"
    from pathlib import Path

    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    own_engine = engine is None
    engine = engine or create_payroll_engine()
    try:
        # All exports see one consistent database snapshot during concurrent ETL.
        with engine.connect().execution_options(isolation_level="REPEATABLE READ") as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ ONLY"))
                counts = {}
                for name, relation in TABLES.items():
                    frame = pd.read_sql(text(f'SELECT * FROM payroll_analytics."{relation}"'), conn)
                    frame.to_csv(destination / f"{name}.csv", index=False)
                    counts[name] = len(frame)
        manifest = {
            "exported_at_utc": datetime.now(timezone.utc).isoformat(),
            "tables": counts,
            "grain": "one employee per latest compensation snapshot",
        }
        (destination / "manifest.json").write_text(json.dumps(manifest, indent=2))
        return manifest
    finally:
        if own_engine:
            engine.dispose()


if __name__ == "__main__":
    result = export_model()
    print(
        f"Exported {result['tables']['fact_compensation']:,} compensation facts and supporting Power BI tables"
    )
