"""Validated, repeatable CSV loads. Run: python -m etl.load [--postgres]."""

import argparse
import sqlite3
from pathlib import Path
from app.data import DATA, load_employee_data


def load_sqlite(destination=None):
    frame = load_employee_data()
    destination = Path(destination or DATA / "generated/employees.db")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(destination) as connection:
        frame.to_sql("employees", connection, if_exists="replace", index=False)
        connection.execute("CREATE UNIQUE INDEX employee_id_idx ON employees(employee_id)")
    return len(frame)


def load_postgres():
    from etl.warehouse import load_warehouse

    return load_warehouse()["rows"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--postgres",
        action="store_true",
        help="Load and reconcile the PostgreSQL analytics warehouse",
    )
    args = parser.parse_args()
    print(f"Loaded {load_postgres() if args.postgres else load_sqlite():,} employees")
