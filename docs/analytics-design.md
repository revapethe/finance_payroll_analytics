# Analytics design and data dictionary

## Business questions

1. How is annual salary cost distributed across countries, departments and cities?
2. What are the median and P90 salaries within comparable country/department cohorts?
3. How do remote, hybrid and on-site headcount differ across those cohorts?
4. Which salaries warrant descriptive review using an IQR rule?
5. Does the warehouse reconcile with the source after each refresh?

This project answers descriptive questions. It does not establish causality, discriminatory pay, budget savings or staffing recommendations.

## Warehouse grain and keys

| Table | Grain/key | Contents |
|---|---|---|
| dim_employee | employee_id | Job title, work arrangement, performance label, hire date. Names and email are excluded. Type 1 attributes. |
| dim_department | department_key; unique department | Six departments |
| dim_location | location_key; unique country + city | Country/city combinations |
| dim_snapshot | snapshot_date | Calendar year/month and month name |
| fact_compensation | snapshot_date + employee_id | Department/location keys, currency, annual local/USD salary and tenure |
| load_audit | batch_id | Snapshot, UTC load time, canonical source SHA-256, reconciled count and annual USD total |

Facts reference all four dimensions. Employee and date keys are natural keys; department/location keys are generated surrogate keys. Different snapshot dates can coexist, but current reporting uses only the latest. Employee attributes are not Type 2, so historical slices of job title or work arrangement would reflect the current employee dimension. A full historical model would require effective-dated source data and SCD2 dimensions.

The default snapshot is 2026-10-23. `annual_salary_usd` and `annual_salary_local` are fixed-precision decimal amounts; `currency` must match country; salaries and tenure must be finite/nonnegative. IDs must be unique and required fields non-null. Hire dates cannot be after the snapshot. The loader stages with PostgreSQL COPY, checks constraints, then reconciles row count and aggregate USD salary before committing an audit row. A transaction-scoped advisory lock serializes refreshes.

## KPI dictionary

| Metric | Definition | Interpretation |
|---|---|---|
| Headcount | Count of latest snapshot facts | Snapshot employees, not full-time-equivalent staffing |
| Annual salary run rate USD | Sum annual_salary_usd | Annual base salary only; no paid transactions, bonuses, benefits or taxes |
| Monthly salary equivalent | Annual run rate / 12 | Analytical equivalent, not monthly paid payroll |
| Median salary | Exact 50th percentile over filtered facts | Recalculate after filtering; never average group medians |
| P90 salary | Continuous 90th percentile | SQL percentile_cont; pandas quantile; DAX PERCENTILEX.INC |
| Remote share | Remote headcount / filtered headcount | Hybrid is separate from Remote |
| Average tenure | Mean source years_of_service | Synthetic tenure, not actual retention rate |
| Cohort salary ratio | Salary / country+department median | Broad descriptive cohort that mixes job levels |
| IQR candidate | Salary outside Q1 − 1.5×IQR to Q3 + 1.5×IQR | Review flag, not evidence of incorrect/unfair pay |

Do not add local INR and USD salaries together. USD conversion uses a fixed synthetic assumption, not historical FX data. Country-wide compensation comparisons reflect different role mixes and purchasing power and should not be interpreted as pay-equity evidence. There are no gender, termination, budget or actual payroll-payment fields, so pay-gap, attrition, budget-variance and paid-payroll trends are unavailable.

## Reporting and operations

- Streamlit offers Overview, Workforce, Compensation, Scenario lab and Employee explorer views with shared filters and a dark blue theme. Salary scenarios are hypothetical and do not write to the database. Compensation review flags use full-snapshot country/department cohorts, preserving the reference benchmark when a display filter changes. Streamlit can analyze either CSV or the latest PostgreSQL employee view. Top cards describe the full source; cards within the analytics workspace reflect its filters.
- `v_payroll_kpis` provides exact SQL totals and percentiles; `v_department_country` supports allocation analysis; `v_compensation_benchmarks` computes within-cohort comparisons.
- Power BI imports a latest-only fact view and related dimensions, with one-way filtering from dimensions to fact. Summary exports are disconnected reconciliation inputs, not additional join paths.
- Exports use one repeatable-read database transaction. Generated files/indexes are ignored; the CSV fixture and BI source definitions are versioned.
- The local ETL owner and BI reader are separate roles. The BI role has SELECT and schema USAGE only; credentials stay in ignored local configuration, never M/DAX/model source.
- Failed transactions leave the last successful warehouse snapshot intact. Failure logs in an external scheduler are future work; committed audit rows represent successful loads only.

## Validation boundaries

PostgreSQL, SQL view calculations, SQL/pandas reconciliation, read-only access, rollback and CSV exports were exercised locally. The semantic model's columns and relationship keys are checked against those exports. Power BI Desktop's M/DAX engine, visual layout and refresh remain unverified until opened on Windows. A BI model source file is not evidence of a deployed Power BI report.
