CREATE SCHEMA IF NOT EXISTS payroll_analytics;

CREATE TABLE IF NOT EXISTS payroll_analytics.dim_department (
    department_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department text NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS payroll_analytics.dim_location (
    location_key bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    country text NOT NULL,
    city text NOT NULL,
    UNIQUE(country, city)
);
CREATE TABLE IF NOT EXISTS payroll_analytics.dim_employee (
    employee_id text PRIMARY KEY,
    job_title text NOT NULL,
    remote_status text NOT NULL CHECK (remote_status IN ('Remote', 'Hybrid', 'On-Site')),
    performance text NOT NULL,
    hire_date date NOT NULL
);
CREATE TABLE IF NOT EXISTS payroll_analytics.dim_snapshot (
    snapshot_date date PRIMARY KEY,
    calendar_year integer NOT NULL,
    calendar_month integer NOT NULL CHECK (calendar_month BETWEEN 1 AND 12),
    month_name text NOT NULL
);
CREATE TABLE IF NOT EXISTS payroll_analytics.fact_compensation (
    snapshot_date date NOT NULL REFERENCES payroll_analytics.dim_snapshot,
    employee_id text NOT NULL REFERENCES payroll_analytics.dim_employee,
    department_key bigint NOT NULL REFERENCES payroll_analytics.dim_department,
    location_key bigint NOT NULL REFERENCES payroll_analytics.dim_location,
    currency text NOT NULL CHECK (currency IN ('USD', 'INR')),
    annual_salary_local numeric(16,2) NOT NULL CHECK (annual_salary_local >= 0),
    annual_salary_usd numeric(16,2) NOT NULL CHECK (annual_salary_usd >= 0),
    years_of_service numeric(6,1) NOT NULL CHECK (years_of_service >= 0),
    PRIMARY KEY(snapshot_date, employee_id)
);
CREATE INDEX IF NOT EXISTS fact_department_location_idx
    ON payroll_analytics.fact_compensation (department_key, location_key);
CREATE TABLE IF NOT EXISTS payroll_analytics.load_audit (
    batch_id uuid PRIMARY KEY,
    snapshot_date date NOT NULL,
    loaded_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    source_sha256 text NOT NULL,
    row_count bigint NOT NULL CHECK (row_count > 0),
    annual_payroll_usd numeric(20,2) NOT NULL
);

-- Current reporting views always use the latest loaded snapshot.
CREATE OR REPLACE VIEW payroll_analytics.v_employee_snapshot AS
SELECT f.employee_id, f.snapshot_date, d.department, l.country, l.city,
       e.job_title, e.remote_status, e.performance, e.hire_date,
       f.currency, f.annual_salary_local, f.annual_salary_usd, f.years_of_service
FROM payroll_analytics.fact_compensation f
JOIN payroll_analytics.dim_employee e USING(employee_id)
JOIN payroll_analytics.dim_department d USING(department_key)
JOIN payroll_analytics.dim_location l USING(location_key)
WHERE f.snapshot_date = (SELECT max(snapshot_date) FROM payroll_analytics.fact_compensation);

CREATE OR REPLACE VIEW payroll_analytics.v_payroll_kpis AS
SELECT snapshot_date, count(*) AS headcount,
       sum(annual_salary_usd) AS annual_payroll_usd,
       sum(annual_salary_usd) / 12 AS monthly_salary_equivalent_usd,
       avg(annual_salary_usd) AS mean_salary_usd,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY annual_salary_usd) AS median_salary_usd,
       percentile_cont(0.9) WITHIN GROUP (ORDER BY annual_salary_usd) AS p90_salary_usd,
       avg((remote_status = 'Remote')::integer)::numeric AS remote_share
FROM payroll_analytics.v_employee_snapshot
GROUP BY snapshot_date;

CREATE OR REPLACE VIEW payroll_analytics.v_department_country AS
SELECT snapshot_date, country, department, count(*) AS headcount,
       sum(annual_salary_usd) AS annual_payroll_usd,
       avg(annual_salary_usd) AS mean_salary_usd,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY annual_salary_usd) AS median_salary_usd,
       percentile_cont(0.9) WITHIN GROUP (ORDER BY annual_salary_usd) AS p90_salary_usd,
       avg(years_of_service) AS mean_tenure_years,
       avg((remote_status = 'Remote')::integer)::numeric AS remote_share
FROM payroll_analytics.v_employee_snapshot
GROUP BY snapshot_date, country, department;

CREATE OR REPLACE VIEW payroll_analytics.v_compensation_benchmarks AS
WITH bands AS (
    SELECT country, department,
           percentile_cont(0.25) WITHIN GROUP (ORDER BY annual_salary_usd) AS q1,
           percentile_cont(0.5) WITHIN GROUP (ORDER BY annual_salary_usd) AS median,
           percentile_cont(0.75) WITHIN GROUP (ORDER BY annual_salary_usd) AS q3
    FROM payroll_analytics.v_employee_snapshot
    GROUP BY country, department
)
SELECT e.*, b.median AS cohort_median_salary_usd,
       e.annual_salary_usd / NULLIF(b.median, 0) AS salary_to_cohort_median,
       (e.annual_salary_usd < b.q1 - 1.5 * (b.q3 - b.q1)
        OR e.annual_salary_usd > b.q3 + 1.5 * (b.q3 - b.q1)) AS is_iqr_outlier
FROM payroll_analytics.v_employee_snapshot e
JOIN bands b USING(country, department);

-- Power BI imports one snapshot, preventing duplicate headcount across snapshots.
CREATE OR REPLACE VIEW payroll_analytics.bi_fact_compensation AS
SELECT * FROM payroll_analytics.fact_compensation
WHERE snapshot_date = (SELECT max(snapshot_date) FROM payroll_analytics.fact_compensation);
