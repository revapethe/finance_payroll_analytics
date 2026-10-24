"""Create a local read-only Power BI role; store its password only in ignored .env."""

import os
import secrets
from dotenv import dotenv_values, set_key
from psycopg import sql
from app.data import ROOT
from app.database import create_payroll_engine


def configure_reader():
    path = ROOT / ".env"
    # The local dev setup creates .env with restricted permissions.
    if not path.exists():
        raise ValueError("Run python -m etl.dev_database first.")
    values = dotenv_values(path)
    username = "payroll_bi_reader"
    password = values.get("PAYROLL_BI_PASSWORD") or secrets.token_urlsafe(32)
    engine = create_payroll_engine()
    try:
        with engine.begin() as connection:
            raw = connection.connection.driver_connection
            exists = raw.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (username,)).fetchone()
            if not exists:
                raw.execute(sql.SQL("CREATE ROLE {} LOGIN").format(sql.Identifier(username)))
            raw.execute(
                sql.SQL(
                    "ALTER ROLE {} WITH PASSWORD {} NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION"
                ).format(sql.Identifier(username), sql.Literal(password))
            )
            raw.execute(
                sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
                    sql.Identifier(connection.engine.url.database), sql.Identifier(username)
                )
            )
            raw.execute(
                sql.SQL("GRANT USAGE ON SCHEMA payroll_analytics TO {}").format(
                    sql.Identifier(username)
                )
            )
            raw.execute(
                sql.SQL("GRANT SELECT ON ALL TABLES IN SCHEMA payroll_analytics TO {}").format(
                    sql.Identifier(username)
                )
            )
    finally:
        engine.dispose()
    os.chmod(path, 0o600)
    set_key(path, "PAYROLL_BI_USER", username)
    set_key(path, "PAYROLL_BI_PASSWORD", password)
    print(
        "Read-only Power BI user configured. Find PAYROLL_BI_USER and PAYROLL_BI_PASSWORD in ignored .env; do not commit or share that file."
    )


if __name__ == "__main__":
    configure_reader()
