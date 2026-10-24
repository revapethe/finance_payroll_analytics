"""Create a credential-free Power BI Desktop handoff ZIP from a fresh warehouse export."""

import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from app.data import DATA, ROOT
from etl.export_bi import export_model


def package_model(output=None):
    destination = Path(output or DATA / "generated/PayrollAnalytics_PowerBI.zip")
    export_dir = DATA / "generated/powerbi"
    export_model(export_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
        for path in sorted(export_dir.glob("*.csv")):
            archive.write(path, f"data/{path.name}")
        archive.write(export_dir / "manifest.json", "data/manifest.json")
        for path in sorted((ROOT / "powerbi").iterdir()):
            if path.is_file() and path.suffix in {".md", ".pq", ".bim", ".dax", ".json"}:
                archive.write(path, f"powerbi/{path.name}")
        for name in ["analytics-design.md", "analytics-findings.md", "dashboard.png"]:
            path = ROOT / "docs" / name
            if path.exists():
                archive.write(path, f"docs/{name}")
        archive.writestr(
            "START_HERE.md",
            """# Power BI Desktop handoff

This package contains 50,000 synthetic employee compensation facts plus dimensions and reporting tables. It does not include credentials, a live database or a finished PBIX.

On Windows, unzip this archive. In Power BI Desktop select Get data > Text/CSV and import data/dim_department.csv, dim_location.csv, dim_employee.csv, dim_snapshot.csv and fact_compensation.csv. Set keys to Whole Number or Text as appropriate, salaries to Fixed Decimal, and dates to Date. Follow powerbi/README.md to create four relationships, add the measures from powerbi/measures.dax and build the pages from powerbi/report-spec.json. Save the result as PayrollAnalytics.pbix on your PC.

The extra summary CSVs are reconciliation inputs; do not join them into the star model. The model is one synthetic snapshot, not historical payment records. PostgreSQL connection files require a reachable PostgreSQL instance; cloud localhost is not your PC's localhost. Power BI Desktop execution/visual assembly has not been validated in the Linux task.
""",
        )
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(f"Created {package_model(args.output)}")
