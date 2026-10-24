"""Package the native Power BI project with fresh warehouse CSVs and no credentials."""

import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED
from app.data import DATA, ROOT
from etl.export_bi import export_model
from etl.build_powerbi import build_project

START_HERE = """# Open the assembled Power BI report

1. Install the current Power BI Desktop on Windows.
2. Extract ALL files from this ZIP into C:\\PayrollAnalytics (not inside another nested folder).
3. Open PayrollAnalytics.pbip. If your Desktop version asks, enable Power BI project/PBIR support and restart Desktop.
4. Select Refresh. The three pages, 36 visual containers, 11 measures and relationships are already defined.
5. If you extracted elsewhere, select Transform data > Edit parameters, set DataFolder to the full path of the extracted data folder, Apply, then Refresh.
6. Use Save As to save a PBIX after checking the report in Desktop.

The included CSVs contain 50,000 synthetic employees. No PostgreSQL connection, cloud account or password is required for this CSV-backed project. Keep the .pbip, Report folder, SemanticModel folder and data folder together.

This is a native editable Power BI project, not a Desktop-generated PBIX or a rendered report. Its files pass official Microsoft JSON-schema validation, and fields/relationships/data exports have been checked. Power BI Desktop, the M/DAX engines and visual rendering cannot be executed in the Linux cloud task and remain unverified. If Desktop reports a compatibility error, retain its exact message for diagnosis.

Pages: Executive Overview; Compensation Analysis; Workforce Profile. The model contains one synthetic snapshot, not historical payroll payments. No benefits, taxes or actual company budgets are present.
"""


def package_model(output=None):
    destination = Path(output or DATA / "generated/PayrollAnalytics_PowerBI.zip")
    export_dir = DATA / "generated/powerbi"
    manifest = export_model(export_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="payroll-bi-") as temp:
        project = Path(temp) / "PayrollAnalytics"
        build_project(project)
        with ZipFile(destination, "w", ZIP_DEFLATED) as archive:
            for path in sorted(project.rglob("*")):
                if path.is_file():
                    archive.write(path, str(path.relative_to(project)))
            for path in sorted(export_dir.glob("*.csv")):
                archive.write(path, f"data/{path.name}")
            archive.write(export_dir / "manifest.json", "data/manifest.json")
            archive.writestr(
                "START_HERE.md",
                START_HERE.replace("50,000", f"{manifest['tables']['fact_compensation']:,}"),
            )
            for name in ["analytics-design.md", "analytics-findings.md"]:
                path = ROOT / "docs" / name
                if path.exists():
                    archive.write(path, f"docs/{name}")
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    print(f"Created {package_model(args.output)}")
