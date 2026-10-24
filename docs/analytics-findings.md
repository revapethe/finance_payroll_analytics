# Snapshot findings

Source: PostgreSQL views over 50,000 synthetic employees, snapshot 2026-10-23.

Regenerate with `python -m etl.report --output docs/analytics-findings.md` after warehouse refresh.

- Annual salary run rate: **$2,971,278,556.07 USD**; monthly salary equivalent: **$247,606,546.34**. These are salary-based estimates, not paid payroll.
- Median salary: **$52,674.45 USD**; P90: **$129,813.10 USD**. Country-specific analysis is needed because this mixes two labor markets.
- Remote work accounts for **33.7%** of snapshot headcount; Hybrid is excluded from that share.
- **India** has **25,000 employees**. **Engineering** has the largest departmental salary allocation (**22.9%** of that country's annual run rate), reflecting the generated workforce mix rather than a measured staffing need.
- **United States** has **25,000 employees**. **Engineering** has the largest departmental salary allocation (**23.0%** of that country's annual run rate), reflecting the generated workforce mix rather than a measured staffing need.
- The within-country/department IQR rule flags **708 compensation review candidates**. These are not conclusions about pay fairness or data errors.

The data is synthetic, uses illustrative compensation ranges and fixed FX, and has no budget or payment history. No cost savings, attrition or time trends can be established.
