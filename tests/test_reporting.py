import pytest
from app.data import load_employee_data
from app.reporting import summarize, department_summary, compensation_benchmarks
from streamlit.testing.v1 import AppTest
from app.data import ROOT


def test_metrics_reconcile():
    frame = load_employee_data()
    summary = summarize(frame)
    departments = department_summary(frame)
    assert summary["headcount"] == 50000
    assert departments.headcount.sum() == summary["headcount"]
    assert departments.annual_payroll_usd.sum() == pytest.approx(summary["annual_payroll_usd"])
    assert summary["monthly_salary_equivalent_usd"] * 12 == pytest.approx(
        summary["annual_payroll_usd"]
    )
    assert summary["p90_salary_usd"] >= summary["median_salary_usd"]
    assert 0 <= summary["remote_share"] <= 1
    assert summarize(frame.iloc[:0])["headcount"] == 0


def test_benchmarks_use_country_department_cohorts():
    import pandas as pd

    frame = pd.DataFrame(
        {
            "country": ["US"] * 5 + ["India"] * 3,
            "department": ["Engineering"] * 8,
            "annual_salary_usd": [10, 11, 12, 13, 100, 1, 2, 3],
        }
    )
    result = compensation_benchmarks(frame)
    assert result.cohort_median_salary_usd.tolist() == [12] * 5 + [2] * 3
    assert result.is_iqr_outlier.tolist() == [False, False, False, False, True, False, False, False]


def test_overview_filters_and_empty_selection():
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    assert not at.exception and not at.error
    next(w for w in at.multiselect if w.label == "Countries").set_value(["India"]).run()
    assert not at.exception and not at.error
    assert next(m for m in at.metric if m.label == "Filtered headcount").value == "25,000"
    summary = at.dataframe[0].value
    assert summary.country.eq("India").all()
    assert summary.headcount.sum() == 25000


def test_filter_combinations_and_scenario_math():
    from app.reporting import apply_filters, scenario_projection

    frame = load_employee_data()
    selected = apply_filters(
        frame,
        countries=["India"],
        departments=["Engineering"],
        arrangements=["Remote"],
        salary_range=(20000, 40000),
    )
    assert len(selected) > 0
    assert selected.country.eq("India").all()
    assert selected.department.eq("Engineering").all()
    assert selected.remote_status.eq("Remote").all()
    assert selected.annual_salary_usd.between(20000, 40000).all()
    result = scenario_projection(selected, 5)
    assert result["projected"] == pytest.approx(selected.annual_salary_usd.sum() * 1.05)
    assert result["annual_change"] == pytest.approx(selected.annual_salary_usd.sum() * 0.05)
    assert result["monthly_change"] * 12 == pytest.approx(result["annual_change"])
    with pytest.raises(ValueError):
        scenario_projection(selected, float("nan"))


def test_advanced_views_scenario_and_explorer():
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    for view in ["Workforce", "Compensation", "Scenario lab", "Employee explorer"]:
        next(w for w in at.radio if w.label == "Analysis view").set_value(view).run()
        assert not at.exception and not at.error
        if view == "Scenario lab":
            next(w for w in at.slider if w.label == "Salary adjustment (%)").set_value(5.0).run()
            assert not at.exception and not at.error
            expected = load_employee_data().annual_salary_usd.sum() * 0.05
            assert (
                next(m for m in at.metric if m.label == "Annual change (USD)").value
                == f"{expected:+,.0f}"
            )
        elif view == "Employee explorer":
            next(
                w for w in at.text_input if w.label == "Search employee ID or job title"
            ).set_value("USA0001").run()
            assert not at.exception and not at.error
            rows = at.dataframe[0].value
            assert len(rows) == 1 and rows.employee_id.iloc[0] == "USA0001"
            assert "email" not in rows and "first_name" not in rows


def test_empty_filter_and_reset():
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    next(w for w in at.multiselect if w.label == "Departments").set_value(["Engineering"])
    next(w for w in at.multiselect if w.label == "Job titles").set_value(["HR Specialist"]).run()
    assert not at.exception and not at.error
    assert any("No employees match" in x.value for x in at.info)
    next(w for w in at.button if w.label == "Reset filters").click().run()
    assert not at.exception and not at.error
    assert next(m for m in at.metric if m.label == "Filtered headcount").value == "50,000"


def test_existing_streamlit_deployment_entrypoint():
    at = AppTest.from_file(str(ROOT / "RESPONSIVE_PREMIUM.py"), default_timeout=30).run()
    assert not at.exception and not at.error
    assert next(m for m in at.metric if m.label == "Filtered headcount").value == "50,000"


@pytest.mark.parametrize(
    "failure", ["missing_configuration", "connection_failure", "empty_snapshot"]
)
def test_public_demo_survives_unavailable_postgres(monkeypatch, failure):
    from app import database

    def unavailable():
        if failure == "empty_snapshot":
            return load_employee_data().iloc[:0]
        if failure == "missing_configuration":
            raise ValueError("Missing configuration")
        raise ConnectionError("Service unreachable")

    monkeypatch.setattr(database, "load_warehouse_employees", unavailable)
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    next(w for w in at.radio if w.label == "Data source").set_value("PostgreSQL warehouse").run()
    assert not at.exception and not at.error
    assert next(m for m in at.metric if m.label == "Filtered headcount").value == "50,000"
    assert any("CSV demo instead" in item.value for item in at.info)
    assert not any("Connected to PostgreSQL" in item.value for item in at.success)
    next(w for w in at.radio if w.label == "Analysis view").set_value("Scenario lab").run()
    assert not at.exception and not at.error


def test_cohort_comparison_reconciles_and_renders():
    from app.reporting import cohort_comparison

    frame = load_employee_data()
    compared = cohort_comparison(frame, "Engineering")
    assert set(compared.country) == {"India", "United States"}
    assert compared.headcount.sum() == frame.department.eq("Engineering").sum()
    for row in compared.itertuples():
        salaries = frame.loc[
            frame.country.eq(row.country) & frame.department.eq("Engineering"), "annual_salary_usd"
        ]
        assert row.median_salary_usd == pytest.approx(salaries.median())
        assert row.p90_salary_usd == pytest.approx(salaries.quantile(0.9))
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    next(w for w in at.radio if w.label == "Analysis view").set_value("Cohort comparison").run()
    assert not at.exception and not at.error
    assert len(at.dataframe[0].value) == 2
    next(w for w in at.multiselect if w.label == "Countries").set_value(["India"]).run()
    assert not at.exception and not at.error
    assert any("Only one country" in x.value for x in at.info)


def test_overview_allocation_metrics():
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    for metric in ["Headcount", "Median salary", "Annual salary"]:
        next(w for w in at.selectbox if w.label == "Allocation metric").set_value(metric).run()
        assert not at.exception and not at.error
        assert at.dataframe[0].value.headcount.sum() == 50000
