import sqlite3
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest
from app.analytics import PayrollAnalyst, build_knowledge_base
from app.data import ROOT, load_employee_data
from etl.load import load_sqlite


def test_fixture_and_rankings():
    data = load_employee_data()
    assert len(data) == 50000
    assert data.country.value_counts().to_dict() == {"United States": 25000, "India": 25000}
    analyst = PayrollAnalyst(data, build_knowledge_base(data))
    rows, _ = analyst.search_employees("top 10 in USA")
    expected = data[data.country == "United States"].nlargest(10, "annual_salary_usd")
    pd.testing.assert_frame_equal(rows.reset_index(drop=True), expected.reset_index(drop=True))
    rows, _ = analyst.search_employees("Engineering in India over 20k")
    assert not rows.empty
    assert rows.country.eq("India").all()
    assert rows.department.eq("Engineering").all()
    assert rows.annual_salary_usd.gt(20000).all()


@pytest.mark.parametrize("defect", ["duplicate", "negative", "null", "missing", "infinite"])
def test_rejects_invalid_data(tmp_path, defect):
    frame = load_employee_data().head(2).copy()
    if defect == "duplicate":
        frame.loc[1, "employee_id"] = frame.loc[0, "employee_id"]
    elif defect == "negative":
        frame.loc[0, "annual_salary_usd"] = -1
    elif defect == "null":
        frame.loc[0, "department"] = None
    elif defect == "missing":
        frame = frame.drop(columns="country")
    else:
        frame.loc[0, "annual_salary_usd"] = float("inf")
    path = tmp_path / "bad.csv"
    frame.to_csv(path, index=False)
    with pytest.raises(ValueError):
        load_employee_data(path)


def test_sqlite_load_is_repeatable(tmp_path):
    database = tmp_path / "employees.db"
    assert load_sqlite(database) == 50000
    assert load_sqlite(database) == 50000
    with sqlite3.connect(database) as conn:
        assert conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 50000
        assert (
            conn.execute("SELECT COUNT(DISTINCT employee_id) FROM employees").fetchone()[0] == 50000
        )


def test_dashboard():
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    assert not at.exception and not at.error
    assert at.metric[0].value == "50,000"
    next(r for r in at.radio if r.label == "Workspace").set_value("Question explorer").run()
    for query in ["Top 10 in USA", "Analyze Engineering department"]:
        at.text_input[0].set_value(query)
        next(b for b in at.button if b.label == "Analyze").click().run()
        assert not at.exception and not at.error
        rows = at.dataframe[0].value
        if "USA" in query:
            assert len(rows) == 10 and rows.Country.eq("United States").all()
        else:
            assert not rows.empty and rows.Dept.eq("Engineering").all()


def test_document_failure_is_visible():
    class BrokenIndex:
        def query(self, **kwargs):
            raise OSError("unavailable")

    frame = load_employee_data()
    analyst = PayrollAnalyst(frame, build_knowledge_base(frame), BrokenIndex())
    with pytest.raises(RuntimeError, match="Policy search failed"):
        analyst.respond("remote policy")


def test_policy_download_ui(tmp_path, monkeypatch):
    pytest.importorskip("chromadb")
    from app import documents
    from etl import index_documents

    monkeypatch.setattr(documents, "INDEX", tmp_path / "index")
    monkeypatch.setattr(index_documents, "INDEX", tmp_path / "index")
    index_documents.build_index()
    # Streamlit cache keys do not include the index directory.
    import streamlit as st

    st.cache_resource.clear()
    at = AppTest.from_file(str(ROOT / "app/dashboard.py"), default_timeout=30).run()
    next(r for r in at.radio if r.label == "Workspace").set_value("Question explorer").run()
    at.text_input[0].set_value("remote work policy")
    next(b for b in at.button if b.label == "Analyze").click().run()
    assert not at.exception and not at.error
    assert len(at.get("download_button")) > 0
    assert any("doc chunks" in value.value for value in at.success)
    st.cache_resource.clear()
