"""Descriptive workforce analytics for a single compensation snapshot."""


def summarize(frame):
    salaries = frame.annual_salary_usd
    return {
        "headcount": len(frame),
        "annual_payroll_usd": float(salaries.sum()),
        "monthly_salary_equivalent_usd": float(salaries.sum() / 12),
        "median_salary_usd": float(salaries.median()) if len(frame) else 0,
        "p90_salary_usd": float(salaries.quantile(0.9)) if len(frame) else 0,
        "remote_share": float(frame.remote_status.eq("Remote").mean()) if len(frame) else 0,
    }


def department_summary(frame):
    return (
        frame.groupby(["country", "department"], as_index=False)
        .agg(
            headcount=("employee_id", "count"),
            annual_payroll_usd=("annual_salary_usd", "sum"),
            mean_salary_usd=("annual_salary_usd", "mean"),
            median_salary_usd=("annual_salary_usd", "median"),
        )
        .sort_values("annual_payroll_usd", ascending=False)
    )


def compensation_benchmarks(frame):
    groups = frame.groupby(["country", "department"])["annual_salary_usd"]
    result = frame.copy()
    result["cohort_median_salary_usd"] = groups.transform("median")
    q1, q3 = (
        groups.transform(lambda values: values.quantile(0.25)),
        groups.transform(lambda values: values.quantile(0.75)),
    )
    result["salary_to_cohort_median"] = result.annual_salary_usd.div(
        result.cohort_median_salary_usd.replace(0, float("nan"))
    )
    result["is_iqr_outlier"] = (result.annual_salary_usd < q1 - 1.5 * (q3 - q1)) | (
        result.annual_salary_usd > q3 + 1.5 * (q3 - q1)
    )
    return result


def apply_filters(
    frame, countries=(), departments=(), arrangements=(), roles=(), salary_range=None
):
    result = frame
    for column, selected in [
        ("country", countries),
        ("department", departments),
        ("remote_status", arrangements),
        ("job_title", roles),
    ]:
        if selected:
            result = result[result[column].isin(selected)]
    if salary_range is not None:
        result = result[result.annual_salary_usd.between(*salary_range)]
    return result.copy()


def scenario_projection(frame, adjustment):
    import math

    if not math.isfinite(adjustment) or not -100 <= adjustment <= 100:
        raise ValueError("Adjustment must be between -100 and 100 percent.")
    baseline = float(frame.annual_salary_usd.sum())
    change = baseline * adjustment / 100
    return {
        "headcount": len(frame),
        "baseline": baseline,
        "projected": baseline + change,
        "annual_change": change,
        "monthly_change": change / 12,
    }


def compact_money(value):
    if abs(value) >= 1e9:
        return f"${value / 1e9:.2f}B"
    if abs(value) >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"


def cohort_comparison(frame, department):
    selected = frame[frame.department.eq(department)]
    return selected.groupby("country", as_index=False).agg(
        headcount=("employee_id", "count"),
        annual_payroll_usd=("annual_salary_usd", "sum"),
        mean_salary_usd=("annual_salary_usd", "mean"),
        median_salary_usd=("annual_salary_usd", "median"),
        p90_salary_usd=("annual_salary_usd", lambda values: values.quantile(0.9)),
    )


def chart(figure):
    import streamlit as st

    figure.update_layout(
        paper_bgcolor="#10243f",
        plot_bgcolor="#10243f",
        font={"color": "#c8daf1", "family": "Segoe UI, Arial"},
        title_font={"size": 17, "color": "#e8f2ff"},
        margin={"l": 70, "r": 25, "t": 62, "b": 30},
        height=365,
        colorway=["#739bc7", "#a9bfd8", "#4875a6", "#c1d2e5", "#345a83"],
        legend={"orientation": "h", "y": -0.2, "title_text": ""},
    )
    figure.update_xaxes(gridcolor="#223b59", zerolinecolor="#223b59")
    figure.update_yaxes(gridcolor="#223b59", zerolinecolor="#223b59")
    st.plotly_chart(figure, width="stretch", theme=None)


def render_overview(frame):
    import streamlit as st
    import plotly.express as px

    snapshot = str(frame.snapshot_date.max()) if "snapshot_date" in frame else "2026-10-23"
    st.caption(
        f"SNAPSHOT {snapshot}  ·  {len(frame):,} synthetic employees  ·  All reporting amounts in USD"
    )
    with st.expander("Filter workforce", expanded=True):
        first, second, third = st.columns(3)
        countries = first.multiselect(
            "Countries", sorted(frame.country.unique()), key="filter_countries"
        )
        departments = second.multiselect(
            "Departments", sorted(frame.department.unique()), key="filter_departments"
        )
        arrangements = third.multiselect(
            "Work arrangements", sorted(frame.remote_status.unique()), key="filter_arrangements"
        )
        roles = st.multiselect("Job titles", sorted(frame.job_title.unique()), key="filter_roles")
        if st.button("Reset filters"):
            for key in [
                "filter_countries",
                "filter_departments",
                "filter_arrangements",
                "filter_roles",
            ]:
                st.session_state.pop(key, None)
            st.rerun()
    filtered = apply_filters(frame, countries, departments, arrangements, roles)
    if filtered.empty:
        st.info("No employees match these filters. Clear a filter to explore the workforce.")
        return
    metrics = summarize(filtered)
    cols = st.columns(4)
    cols[0].metric(
        "Filtered headcount",
        f"{metrics['headcount']:,}",
        help="Employees matching all active filters.",
    )
    cols[1].metric(
        "Annual salary run rate (USD)",
        compact_money(metrics["annual_payroll_usd"]),
        help=f"Exact total: {metrics['annual_payroll_usd']:,.2f} USD. Excludes taxes, benefits and bonuses.",
    )
    cols[2].metric("Median salary (USD)", f"${metrics['median_salary_usd']:,.0f}")
    cols[3].metric(
        "Remote share",
        f"{metrics['remote_share']:.1%}",
        help="Remote employees only; Hybrid is separate.",
    )
    st.caption(
        f"{len(filtered) / len(frame):.1%} of the source workforce selected · Monthly salary equivalent: {metrics['monthly_salary_equivalent_usd']:,.0f} USD · P90: {metrics['p90_salary_usd']:,.0f} USD"
    )
    view = st.radio(
        "Analysis view",
        [
            "Overview",
            "Workforce",
            "Compensation",
            "Cohort comparison",
            "Scenario lab",
            "Employee explorer",
        ],
        horizontal=True,
    )
    palette = {"United States": "#739bc7", "India": "#a9bfd8"}
    groups = department_summary(filtered)
    if view == "Overview":
        st.subheader("Workforce & compensation overview")
        metric_label = st.selectbox(
            "Allocation metric", ["Annual salary", "Headcount", "Median salary"]
        )
        metric_column = {
            "Annual salary": "annual_payroll_usd",
            "Headcount": "headcount",
            "Median salary": "median_salary_usd",
        }[metric_label]
        left, right = st.columns([1.3, 1])
        with left:
            order = groups.groupby("department")[metric_column].sum().sort_values().index.tolist()
            chart(
                px.bar(
                    groups,
                    y="department",
                    x=metric_column,
                    color="country",
                    orientation="h",
                    barmode="group",
                    color_discrete_map=palette,
                    category_orders={"department": order},
                    title=f"Department comparison · {metric_label.lower()}",
                    labels={
                        "department": "",
                        metric_column: "Employees" if metric_column == "headcount" else "USD",
                    },
                )
            )
        with right:
            composition = filtered.groupby("remote_status").size().reset_index(name="employees")
            chart(
                px.pie(
                    composition,
                    names="remote_status",
                    values="employees",
                    hole=0.7,
                    title="How the workforce works",
                    color_discrete_sequence=["#739bc7", "#a9bfd8", "#4875a6"],
                )
            )
        leading = groups.iloc[0]
        from html import escape

        share = leading["annual_payroll_usd"] / metrics["annual_payroll_usd"]
        st.markdown(
            f"<div class='insight-card'><strong>Allocation insight</strong><br>{escape(str(leading['department']))} · {escape(str(leading['country']))} represents <strong>{share:.1%}</strong> of the selected salary run rate — {compact_money(leading['annual_payroll_usd'])} across {leading['headcount']:,} employees.</div>",
            unsafe_allow_html=True,
        )
        st.dataframe(
            groups,
            width="stretch",
            hide_index=True,
            column_config={
                "annual_payroll_usd": st.column_config.NumberColumn(
                    "Annual salary · USD", format="$ %.2f"
                ),
                "mean_salary_usd": st.column_config.NumberColumn(
                    "Mean salary · USD", format="$ %.2f"
                ),
                "median_salary_usd": st.column_config.NumberColumn(
                    "Median salary · USD", format="$ %.2f"
                ),
            },
        )
        st.download_button(
            "Download department analysis",
            groups.to_csv(index=False),
            "department_analysis.csv",
            "text/csv",
        )
    elif view == "Workforce":
        st.subheader("People, places & roles")
        left, right = st.columns(2)
        with left:
            city = filtered.groupby(["country", "city"], as_index=False).agg(
                headcount=("employee_id", "count"), mean_salary=("annual_salary_usd", "mean")
            )
            chart(
                px.bar(
                    city.sort_values("headcount"),
                    x="headcount",
                    y="city",
                    color="country",
                    orientation="h",
                    color_discrete_map=palette,
                    title="Headcount by city",
                    labels={"headcount": "Employees", "city": ""},
                )
            )
        with right:
            mix = (
                filtered.groupby(["department", "remote_status"])
                .size()
                .reset_index(name="employees")
            )
            chart(
                px.bar(
                    mix,
                    x="department",
                    y="employees",
                    color="remote_status",
                    title="Work arrangement by department",
                    labels={"department": "", "employees": "Employees"},
                )
            )
        roles = (
            filtered.job_title.value_counts()
            .head(15)
            .rename_axis("Job title")
            .reset_index(name="Employees")
        )
        st.dataframe(roles, width="stretch", hide_index=True)
        st.download_button(
            "Download workforce profile",
            city.to_csv(index=False),
            "workforce_profile.csv",
            "text/csv",
        )
    elif view == "Compensation":
        st.subheader("Compensation distribution & review")
        left, right = st.columns(2)
        with left:
            chart(
                px.box(
                    filtered,
                    x="department",
                    y="annual_salary_usd",
                    color="country",
                    points=False,
                    color_discrete_map=palette,
                    title="Salary spread within each department",
                    labels={"department": "", "annual_salary_usd": "Annual salary · USD"},
                )
            )
        with right:
            medians = groups.pivot(
                index="department", columns="country", values="median_salary_usd"
            )
            chart(
                px.imshow(
                    medians,
                    text_auto=",.0f",
                    aspect="auto",
                    color_continuous_scale=["#102b4a", "#2467a0", "#58c7e8"],
                    title="Median salary by country & department",
                    labels={"color": "USD"},
                )
            )
        st.caption(
            "Review flags use full-snapshot country/department benchmarks, even when the display is filtered. Cohorts mix job levels; flags do not establish unfair pay or data errors."
        )
        benchmark = compensation_benchmarks(frame).loc[filtered.index]
        only_flags = st.checkbox("Show only IQR review candidates", value=True)
        reviewed = benchmark[benchmark.is_iqr_outlier] if only_flags else benchmark
        st.write(
            f"{int(benchmark.is_iqr_outlier.sum()):,} IQR review candidates among {len(filtered):,} selected employees"
        )
        columns = [
            "employee_id",
            "country",
            "department",
            "job_title",
            "annual_salary_usd",
            "cohort_median_salary_usd",
            "salary_to_cohort_median",
            "is_iqr_outlier",
        ]
        st.dataframe(reviewed[columns].head(1000), width="stretch", hide_index=True)
        st.caption(
            "Preview limited to 1,000 rows. The download contains the complete current review selection."
        )
        st.download_button(
            "Download compensation review",
            reviewed[columns].to_csv(index=False),
            "compensation_review.csv",
            "text/csv",
        )
    elif view == "Cohort comparison":
        st.subheader("Compare country cohorts")
        st.caption(
            "Compare the same department across countries within the active filters. Differences reflect synthetic role mixes and fixed currency conversion, not pay-equity findings."
        )
        department = st.selectbox("Comparison department", sorted(filtered.department.unique()))
        compared = cohort_comparison(filtered, department)
        left, right = st.columns(2)
        with left:
            chart(
                px.bar(
                    compared,
                    x="country",
                    y="median_salary_usd",
                    color="country",
                    color_discrete_map=palette,
                    title="Median salary · matched department",
                    labels={"country": "", "median_salary_usd": "USD"},
                )
            )
        with right:
            chart(
                px.bar(
                    compared,
                    x="country",
                    y="p90_salary_usd",
                    color="country",
                    color_discrete_map=palette,
                    title="P90 salary · matched department",
                    labels={"country": "", "p90_salary_usd": "USD"},
                )
            )
        if len(compared) < 2:
            st.info(
                "Only one country is in the current selection. Include both countries to compare cohorts."
            )
        st.dataframe(compared, width="stretch", hide_index=True)
        st.download_button(
            "Download cohort comparison",
            compared.to_csv(index=False),
            "cohort_comparison.csv",
            "text/csv",
        )
    elif view == "Scenario lab":
        st.subheader("Salary adjustment scenario")
        st.caption(
            "Applies a uniform hypothetical adjustment to the filtered workforce. This is a planning illustration, not an approved budget or a forecast. Taxes, benefits and bonuses are excluded."
        )
        adjustment = st.slider("Salary adjustment (%)", -10.0, 30.0, 3.0, 0.5)
        result = scenario_projection(filtered, adjustment)
        a, b, c = st.columns(3)
        a.metric("Projected annual salary", compact_money(result["projected"]))
        b.metric("Annual change (USD)", f"{result['annual_change']:+,.0f}")
        c.metric("Monthly change (USD)", f"{result['monthly_change']:+,.0f}")
        scenario = groups.copy()
        scenario["adjustment_percent"] = adjustment
        scenario["annual_change_usd"] = scenario.annual_payroll_usd * adjustment / 100
        scenario["projected_annual_usd"] = scenario.annual_payroll_usd + scenario.annual_change_usd
        chart(
            px.bar(
                scenario,
                x="department",
                y="annual_change_usd",
                color="country",
                barmode="group",
                color_discrete_map=palette,
                title="Annual scenario impact by department",
                labels={"department": "", "annual_change_usd": "Annual change · USD"},
            )
        )
        st.dataframe(scenario, width="stretch", hide_index=True)
        st.download_button(
            "Download scenario", scenario.to_csv(index=False), "salary_scenario.csv", "text/csv"
        )
    else:
        st.subheader("Employee explorer")
        st.caption(
            "Employee identifiers and job attributes only. Names and email addresses are excluded from this view and its exports."
        )
        needle = st.text_input("Search employee ID or job title")
        import math

        low, high = (
            math.floor(filtered.annual_salary_usd.min()),
            math.ceil(filtered.annual_salary_usd.max()),
        )
        salary_range = (
            st.slider("Annual salary range (USD)", low, high, (low, high))
            if low < high
            else (low, high)
        )
        selected = apply_filters(filtered, salary_range=salary_range)
        if needle.strip():
            selected = selected[
                selected.employee_id.str.contains(needle, case=False, regex=False)
                | selected.job_title.str.contains(needle, case=False, regex=False)
            ]
        order = st.selectbox(
            "Sort employees by", ["Highest salary", "Lowest salary", "Employee ID"]
        )
        selected = selected.sort_values(
            "employee_id" if order == "Employee ID" else "annual_salary_usd",
            ascending=order != "Highest salary",
        )
        columns = [
            "employee_id",
            "country",
            "city",
            "department",
            "job_title",
            "remote_status",
            "annual_salary_usd",
            "years_of_service",
        ]
        page_size = 100
        page_count = max(1, (len(selected) + page_size - 1) // page_size)
        page = st.number_input("Page", min_value=1, max_value=page_count, value=1, step=1)
        st.caption(f"{len(selected):,} matching employees · Page {page} of {page_count}")
        st.dataframe(
            selected[columns].iloc[(page - 1) * page_size : page * page_size],
            width="stretch",
            hide_index=True,
        )
        st.download_button(
            "Download matching employees",
            selected[columns].to_csv(index=False),
            "employee_selection.csv",
            "text/csv",
        )
    with st.expander("Metric definitions & data notes"):
        st.markdown(
            "**Annual salary run rate** sums base annual USD salaries. **Monthly equivalent** divides that total by 12; it is not paid payroll. **Median/P90** are computed over the selected employees. This is one synthetic snapshot using illustrative fixed FX, with no historical payments, benefits, taxes or budget data."
        )
