"""Write reproducible, aggregate findings from the current PostgreSQL snapshot."""

import argparse
from pathlib import Path
from sqlalchemy import text
from app.data import DATA
from app.database import create_payroll_engine


def write_report(output=None):
    engine = create_payroll_engine()
    try:
        with engine.connect().execution_options(isolation_level="REPEATABLE READ") as conn:
            with conn.begin():
                conn.execute(text("SET TRANSACTION READ ONLY"))
                kpi = (
                    conn.execute(text("SELECT * FROM payroll_analytics.v_payroll_kpis"))
                    .mappings()
                    .one()
                )
                countries = (
                    conn.execute(
                        text(
                            "SELECT country, count(*) AS headcount, sum(annual_salary_usd) AS total FROM payroll_analytics.v_employee_snapshot GROUP BY country ORDER BY country"
                        )
                    )
                    .mappings()
                    .all()
                )
                departments = (
                    conn.execute(
                        text(
                            "SELECT country, department, annual_payroll_usd, headcount FROM payroll_analytics.v_department_country ORDER BY country, annual_payroll_usd DESC"
                        )
                    )
                    .mappings()
                    .all()
                )
                candidates = conn.scalar(
                    text(
                        "SELECT count(*) FROM payroll_analytics.v_compensation_benchmarks WHERE is_iqr_outlier"
                    )
                )
        lines = [
            "# Snapshot findings",
            "",
            f"Source: PostgreSQL views over {kpi['headcount']:,} synthetic employees, snapshot {kpi['snapshot_date']}.",
            "",
            "Regenerate with `python -m etl.report --output docs/analytics-findings.md` after warehouse refresh.",
            "",
            f"- Annual salary run rate: **${kpi['annual_payroll_usd']:,.2f} USD**; monthly salary equivalent: **${kpi['monthly_salary_equivalent_usd']:,.2f}**. These are salary-based estimates, not paid payroll.",
            f"- Median salary: **${kpi['median_salary_usd']:,.2f} USD**; P90: **${kpi['p90_salary_usd']:,.2f} USD**. Country-specific analysis is needed because this mixes two labor markets.",
            f"- Remote work accounts for **{kpi['remote_share']:.1%}** of snapshot headcount; Hybrid is excluded from that share.",
        ]
        for country in countries:
            leading = next(d for d in departments if d["country"] == country["country"])
            share = leading["annual_payroll_usd"] / country["total"]
            lines.append(
                f"- **{country['country']}** has **{country['headcount']:,} employees**. **{leading['department']}** has the largest departmental salary allocation (**{share:.1%}** of that country's annual run rate), reflecting the generated workforce mix rather than a measured staffing need."
            )
        lines += [
            f"- The within-country/department IQR rule flags **{candidates:,} compensation review candidates**. These are not conclusions about pay fairness or data errors.",
            "",
            "The data is synthetic, uses illustrative compensation ranges and fixed FX, and has no budget or payment history. No cost savings, attrition or time trends can be established.",
        ]
        path = Path(output or DATA / "generated/analytics-findings.md")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n")
        return path
    finally:
        engine.dispose()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    path = write_report(args.output)
    print(f"Wrote aggregate findings to {path}")
