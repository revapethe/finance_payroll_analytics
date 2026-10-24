"""Start an isolated local PostgreSQL demo with an ignored, randomly generated password."""

import argparse
import os
import secrets
import subprocess
from app.data import ROOT


def start(with_test_database=False):
    path = ROOT / ".env"
    if not path.exists():
        password = secrets.token_urlsafe(32)
        # Exclusive creation preserves existing user configuration and limits file access.
        with open(path, "x", opener=lambda name, flags: os.open(name, flags, 0o600)) as handle:
            handle.write(f"PAYROLL_POSTGRES_PASSWORD={password}\n")
            handle.write(
                f"PAYROLL_DATABASE_URL=postgresql+psycopg://payroll_owner:{password}@127.0.0.1:15432/payroll\n"
            )
    from dotenv import dotenv_values

    if not dotenv_values(path).get("PAYROLL_POSTGRES_PASSWORD"):
        raise ValueError(
            "Existing .env has no PAYROLL_POSTGRES_PASSWORD; configure local Docker credentials without overwriting other settings."
        )
    subprocess.run(
        [
            "docker",
            "compose",
            "--env-file",
            str(path),
            "-f",
            str(ROOT / "compose.yml"),
            "up",
            "-d",
            "--wait",
        ],
        cwd=ROOT,
        check=True,
    )
    if with_test_database:
        from sqlalchemy import create_engine, text
        from app.database import create_payroll_engine

        owner = create_payroll_engine()
        admin = create_engine(
            owner.url.set(database="postgres"), isolation_level="AUTOCOMMIT", hide_parameters=True
        )
        try:
            with admin.connect() as connection:
                if not connection.scalar(
                    text("SELECT 1 FROM pg_database WHERE datname='payroll_test'")
                ):
                    connection.execute(text("CREATE DATABASE payroll_test"))
        finally:
            admin.dispose()
            owner.dispose()
    print("Local PostgreSQL is healthy on port 15432. Credentials remain in ignored .env.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--with-test-db",
        action="store_true",
        help="Create the isolated payroll_test database if absent",
    )
    args = parser.parse_args()
    start(args.with_test_db)
