"""Real PostgreSQL integration checks; opt in with PAYROLL_TEST_POSTGRES=1."""

import json
import os
from decimal import Decimal
from datetime import date

import pandas as pd
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError

from app.data import ROOT, load_employee_data
from app.database import create_payroll_engine
from app.reporting import summarize, compensation_benchmarks
from etl.warehouse import DEFAULT_SNAPSHOT, load_warehouse, validate_snapshot
from etl.export_bi import export_model


@pytest.fixture(scope="module")
def warehouse():
    if os.environ.get("PAYROLL_TEST_POSTGRES") != "1":
        pytest.skip(
            "Set PAYROLL_TEST_POSTGRES=1 with an isolated payroll_test database to run live PostgreSQL checks"
        )
    base = create_payroll_engine()
    url = base.url.set(database="payroll_test")
    base.dispose()
    engine = create_engine(url, hide_parameters=True)
    assert engine.url.database.endswith("_test")
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS payroll_analytics CASCADE"))
    load_warehouse(engine=engine)
    yield engine
    with engine.begin() as conn:
        conn.execute(text("DROP SCHEMA payroll_analytics CASCADE"))
    engine.dispose()


def test_postgres_repeatability_and_kpi_reconciliation(warehouse):
    frame = load_employee_data()
    first = load_warehouse(engine=warehouse)
    second = load_warehouse(engine=warehouse)
    assert first["source_sha256"] == second["source_sha256"]
    with warehouse.connect() as conn:
        assert (
            conn.scalar(text("SELECT count(*) FROM payroll_analytics.fact_compensation")) == 50000
        )
        assert conn.scalar(text("SELECT count(*) FROM payroll_analytics.dim_employee")) == 50000
        assert conn.scalar(text("SELECT count(*) FROM payroll_analytics.dim_department")) == 6
        kpi = conn.execute(text("SELECT * FROM payroll_analytics.v_payroll_kpis")).mappings().one()
        expected = summarize(frame)
        for key in [
            "headcount",
            "annual_payroll_usd",
            "monthly_salary_equivalent_usd",
            "median_salary_usd",
            "p90_salary_usd",
            "remote_share",
        ]:
            assert float(kpi[key]) == pytest.approx(expected[key])
        grouped = pd.read_sql(text("SELECT * FROM payroll_analytics.v_department_country"), conn)
        assert grouped.headcount.sum() == len(frame)
        assert float(grouped.annual_payroll_usd.sum()) == pytest.approx(
            expected["annual_payroll_usd"]
        )
        outliers = conn.scalar(
            text(
                "SELECT count(*) FROM payroll_analytics.v_compensation_benchmarks WHERE is_iqr_outlier"
            )
        )
        assert outliers == compensation_benchmarks(frame).is_iqr_outlier.sum()
        assert conn.scalar(text("SELECT count(*) FROM payroll_analytics.load_audit")) >= 3


def test_postgres_transaction_rolls_back_on_reconciliation_failure(warehouse, tmp_path):
    frame = load_employee_data()
    frame.loc[0, "annual_salary_usd"] += 0.001  # staging rounds to numeric(16,2)
    path = tmp_path / "fractional_cents.csv"
    # Force an audit/reconciliation failure after the fact rows have been replaced.
    with warehouse.begin() as conn:
        conn.execute(
            text(
                "ALTER TABLE payroll_analytics.load_audit ADD CONSTRAINT test_reject_audit CHECK (row_count < 50000) NOT VALID"
            )
        )
    frame.to_csv(path, index=False)
    try:
        with pytest.raises(DBAPIError):
            load_warehouse(source=path, engine=warehouse)
        with warehouse.connect() as conn:
            assert (
                conn.scalar(text("SELECT count(*) FROM payroll_analytics.fact_compensation"))
                == 50000
            )
            actual = conn.scalar(
                text("SELECT sum(annual_salary_usd) FROM payroll_analytics.fact_compensation")
            )
            expected = sum(Decimal(str(x)) for x in load_employee_data().annual_salary_usd)
            assert actual == expected
    finally:
        with warehouse.begin() as conn:
            conn.execute(
                text("ALTER TABLE payroll_analytics.load_audit DROP CONSTRAINT test_reject_audit")
            )


def test_postgres_constraints_and_read_only_role(warehouse):
    with warehouse.begin() as conn:
        conn.execute(
            text(
                "DO $$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='payroll_test_reader') THEN CREATE ROLE payroll_test_reader NOLOGIN; END IF; END $$"
            )
        )
        conn.execute(text("GRANT USAGE ON SCHEMA payroll_analytics TO payroll_test_reader"))
        conn.execute(
            text("GRANT SELECT ON ALL TABLES IN SCHEMA payroll_analytics TO payroll_test_reader")
        )
    with warehouse.connect() as conn:
        with conn.begin():
            conn.execute(text("SET LOCAL ROLE payroll_test_reader"))
            assert (
                conn.scalar(text("SELECT count(*) FROM payroll_analytics.bi_fact_compensation"))
                == 50000
            )
            with pytest.raises(DBAPIError):
                conn.execute(text("DELETE FROM payroll_analytics.fact_compensation"))
            # PostgreSQL aborts the transaction on denied writes.
    with warehouse.connect() as conn:
        with pytest.raises(DBAPIError):
            with conn.begin():
                conn.execute(
                    text(
                        "UPDATE payroll_analytics.fact_compensation SET department_key=-1 WHERE employee_id='USA0001'"
                    )
                )


def test_powerbi_exports_and_semantic_model(warehouse, tmp_path):
    result = export_model(tmp_path, warehouse)
    assert result["tables"]["fact_compensation"] == 50000
    fact = pd.read_csv(tmp_path / "fact_compensation.csv")
    assert not fact.employee_id.duplicated().any()
    assert "first_name" not in fact and "email" not in fact
    model = json.loads((ROOT / "powerbi/PayrollAnalytics.bim").read_text())["model"]
    tables = {t["name"]: t for t in model["tables"]}
    assert len(tables) == 5
    for table, definition in tables.items():
        data = pd.read_csv(tmp_path / f"{table}.csv")
        assert set(c["sourceColumn"] for c in definition["columns"]) == set(data.columns)
    for relationship in model["relationships"]:
        dimension = pd.read_csv(tmp_path / f"{relationship['toTable']}.csv")
        key = relationship["toColumn"]
        assert dimension[key].notna().all() and dimension[key].is_unique
        assert fact[relationship["fromColumn"]].isin(dimension[key]).all()
        assert relationship["crossFilteringBehavior"] == "oneDirection"
    assert len(tables["fact_compensation"]["measures"]) == 11


def test_invalid_warehouse_snapshot_is_rejected():
    frame = load_employee_data().head(2).copy()
    with pytest.raises(ValueError, match="Hire dates"):
        validate_snapshot(frame, date(2000, 1, 1))
    frame.loc[0, "currency"] = "INR"
    with pytest.raises(ValueError, match="Country/currency"):
        validate_snapshot(frame, DEFAULT_SNAPSHOT)


def test_postgres_dashboard_uses_warehouse(warehouse, monkeypatch):
    from app import database
    from streamlit.testing.v1 import AppTest

    monkeypatch.setattr(database, "create_payroll_engine", lambda: warehouse)
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    next(w for w in at.radio if w.label == "Data source").set_value("PostgreSQL warehouse").run()
    assert not at.exception and not at.error
    assert at.metric[0].value == "50,000"
    assert any("Connected to PostgreSQL" in value.value for value in at.success)
    next(w for w in at.multiselect if w.label == "Countries").set_value(["India"]).run()
    assert not at.exception and not at.error
    assert next(m for m in at.metric if m.label == "Filtered headcount").value == "25,000"


def test_snapshot_refresh_removes_departed_facts(warehouse, tmp_path):
    path = tmp_path / "smaller_snapshot.csv"
    load_employee_data().head(10).to_csv(path, index=False)
    try:
        assert load_warehouse(source=path, engine=warehouse)["rows"] == 10
        with warehouse.connect() as conn:
            assert (
                conn.scalar(text("SELECT count(*) FROM payroll_analytics.bi_fact_compensation"))
                == 10
            )
    finally:
        load_warehouse(engine=warehouse)
