# Assembled Power BI Desktop project

`PayrollAnalytics/PayrollAnalytics.pbip` is a native editable Power BI project. Its report and semantic model are already defined; you do not need to manually create the visuals, relationships or measures.

## Included report

| Page | Visuals |
|---|---|
| Executive Overview | Country/department/work-arrangement slicers; headcount, salary run rate, median and remote-share cards; salary allocation chart; work-arrangement donut; summary table |
| Compensation Analysis | Shared slicers and KPI cards; average salary by job title; country median/P90 comparison; employee detail table |
| Workforce Profile | Shared slicers and KPI cards; department/work-arrangement stacked bars; performance distribution; city workforce table |

There are 36 visual containers across the three pages, including the page headings and data notes. The model includes five tables, four active one-to-many relationships and 11 DAX measures. It uses CSV Import mode for a standalone handoff, with no database credentials embedded.

## Open the packaged project on Windows

1. Install the current Power BI Desktop.
2. Download the `PayrollAnalytics_PowerBI.zip` handoff and extract **all files** into `C:\PayrollAnalytics`.
3. Open `PayrollAnalytics.pbip` from that folder. Enable project/PBIR support if your Desktop version prompts for it.
4. Select **Refresh** to import the included data.
5. If you extracted elsewhere, open **Transform data → Edit parameters**, set `DataFolder` to the full path of the extracted `data` folder, then Apply and Refresh.
6. Inspect the three report pages and save a `.pbix` using Save As.

The `.pbip`, `.Report`, `.SemanticModel` and `data` folders must stay together. A source-code checkout contains the project definitions; the handoff ZIP also includes the generated star-schema CSVs needed for refresh.

The latest GitHub Actions run uploads a `PayrollAnalytics-PowerBI-Desktop` artifact after its checks and export succeed. Its ZIP contains the Desktop handoff. Artifact availability depends on a successful workflow run; it has not been verified from this task.

## Rebuild and validate the handoff

From the repository root in the prepared development environment:

```bash
python -m etl.build_powerbi
python -m etl.validate_powerbi
python -m etl.warehouse
python -m etl.package_bi
```

The ZIP is written to `data/generated/PayrollAnalytics_PowerBI.zip`. Warehouse/package steps use the configured PostgreSQL database. Opening the resulting CSV-backed project in Desktop does not need that database. The build is deterministic and official schema files are vendored under `powerbi/schemas` for offline validation.

## PostgreSQL option

`PayrollSource.pq` and `PayrollAnalytics.bim` at the top of this folder retain PostgreSQL Import definitions. They are alternatives to the CSV-backed native project. Use a reachable PostgreSQL server and authenticate through Desktop's credential dialog, never inside M/DAX/model source. The local project helper creates a read-only BI role; credentials remain in ignored `.env`. Cloud localhost is not your PC's localhost.

## Model and KPI definitions

| Dimension key | Fact key |
|---|---|
| dim_employee.employee_id | fact_compensation.employee_id |
| dim_department.department_key | fact_compensation.department_key |
| dim_location.location_key | fact_compensation.location_key |
| dim_snapshot.snapshot_date | fact_compensation.snapshot_date |

Relationships filter from the dimension to the fact. The fact import contains only the latest snapshot, with one employee per row. Extra summary CSVs are disconnected reconciliation inputs, not additional join paths.

Annual salary run rate sums annual USD base salaries; monthly equivalent divides by 12 and does not represent paid payroll. Median/P90 recalculate over filtered facts. Remote share excludes Hybrid. Country comparisons mix synthetic role levels and fixed FX assumptions and do not establish pay fairness. There is no actual budget, attrition or payroll-payment history.

## Validation boundary

The native PBIP/PBIR metadata, pages and visual definitions pass Microsoft's official schemas. Tests also check every referenced model field/measure, visual bounds, relationship keys and package contents. SQL calculations and exports are exercised separately against PostgreSQL.

**Power BI Desktop cannot run in the Linux cloud task.** Desktop refresh, M/DAX compilation and visual rendering have not been verified. This is an assembled source project, not a tested `.pbix` or a deployed report. If Desktop produces an error, retain its exact message so the compatibility issue can be diagnosed.
