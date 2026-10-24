-- Salary rankings per country and department; comparisons stay within each cohort.
SELECT employee_id, country, department, job_title, annual_salary_usd,
       dense_rank() OVER (PARTITION BY country, department ORDER BY annual_salary_usd DESC) AS salary_rank
FROM payroll_analytics.v_employee_snapshot;

-- Department allocation as a percentage of each country's annual salary run rate.
SELECT country, department, headcount, annual_payroll_usd,
       round(100 * annual_payroll_usd / NULLIF(sum(annual_payroll_usd) OVER (PARTITION BY country), 0), 2) AS country_salary_share_pct
FROM payroll_analytics.v_department_country
ORDER BY country, annual_payroll_usd DESC;

-- Review candidates, not proof of pay inequity or data errors.
SELECT employee_id, country, department, annual_salary_usd,
       cohort_median_salary_usd, salary_to_cohort_median
FROM payroll_analytics.v_compensation_benchmarks
WHERE is_iqr_outlier
ORDER BY salary_to_cohort_median DESC;

-- Auditable load reconciliation, not claims of actual paid payroll.
SELECT loaded_at, snapshot_date, row_count, annual_payroll_usd, source_sha256
FROM payroll_analytics.load_audit
ORDER BY loaded_at DESC;
