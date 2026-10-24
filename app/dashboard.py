"""Single Streamlit entry point for the payroll analytics demo."""

from pathlib import Path
import sys
import os
import time
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Streamlit executes this file directly; resolve the package independently of cwd.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.analytics import PayrollAnalyst, CompensationAdvisor, build_knowledge_base  # noqa: E402
from app.data import load_employee_data, DOCUMENTS  # noqa: E402

st.set_page_config(
    page_title="Payroll Analytics",
    page_icon=str(ROOT / "app/favicon.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("<style>" + (ROOT / "app/style.css").read_text() + "</style>", unsafe_allow_html=True)


@st.cache_resource
def load_chromadb():
    from app.documents import open_index

    try:
        collection = open_index()
        return collection, collection.count() if collection else 0
    except (ImportError, RuntimeError) as exc:
        st.warning(str(exc))
        return None, 0


def main():
    # Header
    st.markdown(
        "<p class='eyebrow'>WORKFORCE INTELLIGENCE / SYNTHETIC DATA LAB</p>", unsafe_allow_html=True
    )
    st.markdown("<h1>Finance Payroll Analytics</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='subtitle'>Understand your workforce. Explore compensation. Model what comes next.</p>",
        unsafe_allow_html=True,
    )

    source = st.sidebar.radio("Data source", ["CSV demo", "PostgreSQL warehouse"])
    workspace = st.sidebar.radio("Workspace", ["Analytics dashboard", "Question explorer"])
    df = None
    if source == "PostgreSQL warehouse":
        from app.database import load_warehouse_employees

        try:
            df = load_warehouse_employees()
            if df is None or df.empty:
                raise ValueError("Warehouse snapshot is empty")
            st.sidebar.success("Connected to PostgreSQL · latest snapshot")
        except Exception:
            st.info(
                "PostgreSQL is not available for this deployment. Showing the 50,000-record CSV demo instead; all analytics views remain available."
            )
            st.sidebar.caption("Active source: CSV demo · PostgreSQL unavailable")
            df = None
    if df is None:
        try:
            df = load_employee_data()
            if source == "CSV demo":
                st.sidebar.caption("Active source: versioned synthetic CSV")
        except Exception:
            st.error("The demo dataset could not be loaded. Please try again later.")
            return

    if df is None or df.empty:
        st.error("Data unavailable")
        st.stop()

    if workspace == "Analytics dashboard":
        from app.reporting import render_overview

        render_overview(df)
        return

    kb = build_knowledge_base(df)

    # Metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Workforce", f"{len(df):,}")
    with col2:
        usa_count = kb["countries"].get("United States", 0)
        st.metric("United States", f"{usa_count:,}")
    with col3:
        india_count = kb["countries"].get("India", 0)
        st.metric("India", f"{india_count:,}")
    with col4:
        st.metric("Mean Salary", f"${kb['avg_salary_global'] / 1000:.0f}K")

    st.markdown("---")

    collection, doc_count = load_chromadb()
    # Initialize deterministic analysis helpers
    analyst_agent = PayrollAnalyst(df, kb, collection)
    advisor_agent = CompensationAdvisor(kb)

    # Search interface
    st.markdown("## Search & Analysis")

    # Responsive buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Top 10 USA", width="stretch"):
            st.session_state.query = "Top 10 in USA"
    with col2:
        if st.button("Remote Policy", width="stretch"):
            st.session_state.query = "What is the remote work policy?"
    with col3:
        if st.button("Engineering", width="stretch"):
            st.session_state.query = "Analyze Engineering department"
    with col4:
        if st.button("Salary Ranges", width="stretch"):
            st.session_state.query = "Engineering salary ranges vs policy"

    user_query = st.text_input(
        "Payroll or policy question",
        value=st.session_state.get("query", ""),
        placeholder="Ask about employees or policies",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        search_btn = st.button("Analyze", type="primary", width="stretch")

    if search_btn and user_query:
        st.markdown("---")
        st.markdown("## Payroll Analysis")

        st.info(f"**Query:** {user_query}")

        # Payroll filtering
        st.markdown("### 📊 Payroll Analyst")
        with st.spinner("Searching..."):
            time.sleep(0.7)
            try:
                analyst_response = analyst_agent.respond(user_query)
            except RuntimeError as exc:
                st.error(str(exc))
                return

        st.markdown(
            f'<div class="agent-message analyst-message">{analyst_response["message"]}</div>',
            unsafe_allow_html=True,
        )

        # Policy source downloads
        doc_results = analyst_response.get("doc_data")
        if doc_results and doc_results["documents"] and len(doc_results["documents"][0]) > 0:
            st.markdown("### 📥 Source Documents")

            seen = set()
            download_cols = st.columns(min(len(doc_results["metadatas"][0]), 3))

            col_idx = 0
            for meta in doc_results["metadatas"][0]:
                doc_id = meta.get("doc_id")
                if doc_id and doc_id not in seen and col_idx < 3:
                    seen.add(doc_id)

                    pdf_file = (
                        str(DOCUMENTS / Path(meta["filename"]).name)
                        if meta.get("filename")
                        else None
                    )
                    if pdf_file and os.path.exists(pdf_file):
                        with open(pdf_file, "rb") as f:
                            pdf_data = f.read()

                        with download_cols[col_idx]:
                            st.markdown(f"**{meta['title']}**")
                            st.download_button(
                                label="Download policy text",
                                data=pdf_data,
                                file_name=os.path.basename(pdf_file),
                                mime="text/plain",
                                key=f"pdf_{doc_id}",
                                width="stretch",
                            )
                            col_idx += 1

        # Compensation summary
        st.markdown("### 💼 Compensation Summary")
        with st.spinner("Analyzing..."):
            time.sleep(0.5)
            advisor_response = advisor_agent.respond(analyst_response)

        st.markdown(
            f'<div class="agent-message advisor-message">{advisor_response["message"]}</div>',
            unsafe_allow_html=True,
        )

        # Visualizations
        if analyst_response.get("emp_data") is not None and len(analyst_response["emp_data"]) > 0:
            st.markdown("---")
            st.markdown("## Advanced Visualizations")

            results = analyst_response["emp_data"]

            viz1, viz2, viz3, viz4 = st.tabs(
                ["Distribution", "Rankings", "Geographic", "Data Table"]
            )

            with viz1:
                # Histogram
                fig = go.Figure()
                fig.add_trace(
                    go.Histogram(
                        x=results["annual_salary_usd"],
                        nbinsx=20,
                        marker=dict(color="#636efa", line=dict(color="#636efa", width=1)),
                        opacity=0.8,
                    )
                )

                fig.update_layout(
                    title="Salary Distribution",
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#ffffff",
                    font=dict(color="#24334a"),
                    height=450,
                    xaxis=dict(showgrid=True, gridcolor="#e5ecf6"),
                    yaxis=dict(showgrid=True, gridcolor="#e5ecf6"),
                )

                st.plotly_chart(fig, width="stretch")

                # Box plot by department
                if "department" in results.columns and len(results["department"].unique()) > 1:
                    fig2 = go.Figure()

                    for dept in results["department"].unique():
                        dept_data = results[results["department"] == dept]
                        fig2.add_trace(
                            go.Box(
                                y=dept_data["annual_salary_usd"],
                                name=dept,
                                marker=dict(color="#636efa"),
                            )
                        )

                    fig2.update_layout(
                        title="Department Comparison",
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        font=dict(color="#24334a"),
                        height=450,
                    )

                    st.plotly_chart(fig2, width="stretch")

            with viz2:
                # Top 10 bar chart
                top10 = results.nlargest(10, "annual_salary_usd")

                fig = go.Figure(
                    data=[
                        go.Bar(
                            y=top10["employee_id"],
                            x=top10["annual_salary_usd"],
                            orientation="h",
                            marker=dict(
                                color=top10["annual_salary_usd"],
                                colorscale="Blues",
                                line=dict(color="rgba(139,159,201,0.3)", width=1),
                            ),
                            text=top10["annual_salary_usd"].apply(lambda x: f"${x / 1000:.0f}K"),
                            textposition="outside",
                        )
                    ]
                )

                fig.update_layout(
                    title="Top 10 by Salary",
                    plot_bgcolor="#ffffff",
                    paper_bgcolor="#ffffff",
                    font=dict(color="#24334a"),
                    height=500,
                    showlegend=False,
                    xaxis=dict(showgrid=True, gridcolor="#e5ecf6"),
                    margin=dict(l=20, r=120, t=60, b=40),
                )

                st.plotly_chart(fig, width="stretch")

            with viz3:
                # Scatter plot by city
                if "city" in results.columns:
                    city_stats = (
                        results.groupby(["country", "city"])
                        .agg({"employee_id": "count", "annual_salary_usd": "mean"})
                        .reset_index()
                    )
                    city_stats.columns = ["Country", "City", "Employees", "Avg Salary"]

                    fig = px.scatter(
                        city_stats.head(20),
                        x="Employees",
                        y="Avg Salary",
                        size="Employees",
                        color="Country",
                        hover_name="City",
                        color_discrete_map={"United States": "#636efa", "India": "#EF553B"},
                    )

                    fig.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        font=dict(color="#24334a"),
                        height=500,
                    )

                    st.plotly_chart(fig, width="stretch")

                # Sunburst
                if len(results) > 15:
                    fig2 = px.sunburst(
                        results.head(100),
                        path=["country", "department", "job_title"],
                        values="annual_salary_usd",
                    )

                    fig2.update_layout(
                        plot_bgcolor="#ffffff",
                        paper_bgcolor="#ffffff",
                        font=dict(color="#24334a"),
                        height=500,
                    )

                    st.plotly_chart(fig2, width="stretch")

            with viz4:
                # Data table
                display_df = (
                    results[
                        [
                            "employee_id",
                            "job_title",
                            "department",
                            "city",
                            "country",
                            "annual_salary_usd",
                        ]
                    ]
                    .head(20)
                    .copy()
                )
                display_df["annual_salary_usd"] = display_df["annual_salary_usd"].apply(
                    lambda x: f"${x:,.0f}"
                )
                display_df.columns = ["ID", "Position", "Dept", "City", "Country", "Salary"]

                st.dataframe(display_df, width="stretch", height=600)

    # Sidebar
    with st.sidebar:
        st.markdown("### System Status")
        st.success(f"✅ {len(df):,} employees")

        if doc_count > 0:
            st.success(f"✅ {doc_count} doc chunks")
        else:
            st.info("Policy search is optional. See README for indexing instructions.")


if __name__ == "__main__":
    main()
