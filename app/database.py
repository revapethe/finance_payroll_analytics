"""Database configuration, never logged or embedded in tracked files."""

import os
from app.data import ROOT


def database_url():
    from dotenv import dotenv_values

    value = os.environ.get("PAYROLL_DATABASE_URL") or dotenv_values(ROOT / ".env").get(
        "PAYROLL_DATABASE_URL"
    )
    if not value:
        import streamlit as st
        from streamlit.errors import StreamlitSecretNotFoundError

        if st.runtime.exists():
            try:
                value = st.secrets.get("PAYROLL_DATABASE_URL")
            except (StreamlitSecretNotFoundError, FileNotFoundError):
                pass
    if not value:
        raise ValueError(
            "Configure PAYROLL_DATABASE_URL or run python -m etl.dev_database for a local demo."
        )
    return value


def create_payroll_engine():
    from sqlalchemy import create_engine

    engine = create_engine(
        database_url(),
        pool_pre_ping=True,
        hide_parameters=True,
        connect_args={"connect_timeout": 5},
    )
    if engine.dialect.name != "postgresql":
        engine.dispose()
        raise ValueError("PAYROLL_DATABASE_URL must use PostgreSQL.")
    return engine


def load_warehouse_employees():
    import pandas as pd
    from sqlalchemy import text

    engine = create_payroll_engine()
    try:
        with engine.connect() as conn:
            return pd.read_sql(text("SELECT * FROM payroll_analytics.v_employee_snapshot"), conn)
    finally:
        engine.dispose()
