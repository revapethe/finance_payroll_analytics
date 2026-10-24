# Payroll & Workforce Analytics

A data analytics project exploring **50,000 synthetic employee records** across the United States and India. It combines a PostgreSQL analytics warehouse, a Streamlit dashboard, and Power BI model definitions to examine workforce composition and compensation.

## Project objective

The project brings employee data into a consistent reporting model so analysts can explore salary allocation, compare compensation within country and department cohorts, and evaluate hypothetical salary adjustments. Its emphasis is on reliable data preparation, clear metric definitions, and interactive analysis.

## Dataset

The dataset contains **25,000 US employees and 25,000 Indian employees**, covering departments, job titles, cities, work arrangements, salaries, hire dates, tenure and performance labels.

The data represents a single snapshot dated **23 October 2026**. Salaries and policy documents are illustrative, and currency conversion uses a fixed synthetic assumption rather than live exchange rates.

## Analytics capabilities

- Headcount and workforce composition by country, department, city, job title and work arrangement.
- Annual salary allocation, monthly salary equivalents, median salaries and 90th-percentile salaries.
- Country-and-department compensation benchmarks and interquartile-range review candidates.
- Hypothetical salary adjustments with annual and monthly cost impacts.
- Filtered employee exploration and downloadable analysis tables.

## Streamlit dashboard

The dashboard uses a **flat navy blue theme** with shared filters, KPI cards and interactive charts. It supports both the versioned CSV dataset and the latest PostgreSQL warehouse snapshot.

| Workspace | Purpose |
|---|---|
| Overview | Summarizes selected headcount, salary allocation, compensation statistics and work arrangements. |
| Workforce | Explores employee distribution across cities, departments and job titles. |
| Compensation | Shows salary distributions, median salary comparisons and cohort-based review candidates. |
| Cohort comparison | Compares headcount, median salary and P90 salary for the same department across countries. |
| Scenario lab | Models hypothetical salary adjustments for the selected workforce without changing source records. |
| Employee explorer | Provides employee ID and job-title search, salary filters, sorting, pagination and exports without names or email addresses. |

A separate Question explorer supports keyword and regular-expression filtering, alongside optional retrieval from 25 synthetic policy documents. It does not use an LLM or translate natural language into SQL.

## PostgreSQL warehouse

The warehouse uses a star schema with employee, department, location and snapshot dimensions. The compensation fact table contains one row per employee per snapshot, while current reporting views select the latest snapshot.

The ETL pipeline validates required fields, employee identifiers, salaries, country/currency consistency and snapshot dates. It bulk-loads staging data, updates dimensions, refreshes snapshot facts and reconciles row counts and salary totals before committing. Failed refreshes roll back, and successful loads retain audit metadata and a source-data hash.

SQL reporting views provide workforce KPIs, departmental salary summaries and compensation benchmarks. A separate read-only reporting role supports BI access. Employee descriptive attributes use Type 1 updates, so the model is intended for current-state analysis rather than complete historical HR reporting.

## Power BI integration

The Power BI source files include a five-table semantic model, four dimension-to-fact relationships, PostgreSQL Power Query connections and **11 DAX measures**. A theme and report specification cover Executive Overview, Compensation Analysis and Workforce Profile pages.

CSV exports provide an alternative reporting source. Model structure, relationship keys and exports have been validated against PostgreSQL. Power BI Desktop execution and visual assembly remain a separate validation step; a completed `.pbix` report is not included.

## Technology stack

| Component | Technologies |
|---|---|
| Data preparation | Python, pandas |
| Analytics warehouse | PostgreSQL, SQL, SQLAlchemy, psycopg |
| Interactive application | Streamlit, Plotly |
| BI model definitions | Power Query, DAX, Power BI semantic model source |
| Optional policy retrieval | ChromaDB, local hashed token vectors |
| Quality assurance | pytest, Ruff, GitHub Actions |

## Data quality and validation

Automated checks cover reproducible generation, invalid-data rejection, filter correctness, dashboard interactions, scenario calculations, repeatable warehouse loads, transaction rollback, database constraints and read-only reporting access. Additional checks reconcile PostgreSQL KPIs with pandas calculations and verify Power BI exports and model relationships.

## Interpretation and limitations

This is a synthetic workforce analytics project. Annual salary run rate excludes benefits, taxes, bonuses and overtime; monthly salary equivalents are annual salaries divided by 12 rather than actual payroll payments. Compensation review flags identify descriptive outliers, not evidence of unfair pay or incorrect records.

The source does not support historical payroll trends, attrition, budget variance or measured business savings. More detail is available in the [analytics design and metric definitions](docs/analytics-design.md), [snapshot findings](docs/analytics-findings.md), and [data provenance](data/README.md).
