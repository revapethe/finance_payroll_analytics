"""Deterministic payroll filtering and compensation summaries; no LLM or SQL generation."""

import re


def build_knowledge_base(df):
    kb = {
        "total_employees": len(df),
        "countries": df["country"].value_counts().to_dict(),
        "avg_salary_global": df["annual_salary_usd"].mean(),
        "by_department": {},
    }

    for dept in df["department"].unique():
        dept_df = df[df["department"] == dept]
        kb["by_department"][dept] = {
            "count": len(dept_df),
            "avg_salary": dept_df["annual_salary_usd"].mean(),
            "min_salary": dept_df["annual_salary_usd"].min(),
            "max_salary": dept_df["annual_salary_usd"].max(),
        }

    return kb


class PayrollAnalyst:
    def __init__(self, df, kb, doc_collection=None):
        self.df = df
        self.knowledge_base = kb
        self.doc_collection = doc_collection
        self.name = "Payroll Analyst"

    def search_employees(self, query):
        q = query.lower()
        filtered = self.df.copy()
        filters = []

        if "usa" in q or "united states" in q:
            filtered = filtered[filtered["country"] == "United States"]
            filters.append("USA")
        elif "india" in q:
            filtered = filtered[filtered["country"] == "India"]
            filters.append("India")

        for dept in ["Engineering", "HR", "Sales", "Marketing", "Finance", "Product"]:
            if dept.lower() in q:
                filtered = filtered[filtered["department"] == dept]
                filters.append(dept)
                break

        if "manager" in q:
            filtered = filtered[filtered["job_title"].str.contains("Manager", case=False, na=False)]
            filters.append("Manager")

        over_match = re.search(r"over\s+(\d+)k?", q)
        if over_match:
            amount = int(over_match.group(1)) * 1000
            filtered = filtered[filtered["annual_salary_usd"] > amount]
            filters.append(f">${amount:,}")

        filtered = filtered.sort_values("annual_salary_usd", ascending=False)

        top_match = re.search(r"top\s+(\d+)", q)
        if top_match:
            filtered = filtered.head(int(top_match.group(1)))
        elif "top" in q:
            filtered = filtered.head(10)

        return filtered, filters

    def search_documents(self, query):
        if not self.doc_collection:
            return None
        try:
            return self.doc_collection.query(query_texts=[query], n_results=3)
        except Exception as exc:
            raise RuntimeError("Policy search failed; rebuild the document index.") from exc

    def respond(self, query):
        emp_results, filters = self.search_employees(query)
        doc_results = self.search_documents(query)

        message = ""

        if len(emp_results) > 0:
            message += "**Workforce Analysis**\n\n"
            message += f"Identified **{len(emp_results):,} employees**"
            if filters:
                message += f" — {' · '.join(filters)}"

            message += "\n\n**Compensation:**\n"
            message += f"• Mean: ${emp_results['annual_salary_usd'].mean():,.0f}\n"
            message += f"• Range: ${emp_results['annual_salary_usd'].min():,.0f}–${emp_results['annual_salary_usd'].max():,.0f}\n\n"

            message += "**Top Five:**\n"
            for idx, (_, emp) in enumerate(emp_results.head(5).iterrows(), 1):
                message += f"{idx}. {emp['employee_id']} — {emp['job_title']} — ${emp['annual_salary_usd']:,.0f}\n"

        if doc_results and doc_results["documents"] and len(doc_results["documents"][0]) > 0:
            message += "\n\n**Policy Documentation:**\n\n"
            for i, (doc, meta) in enumerate(
                zip(doc_results["documents"][0], doc_results["metadatas"][0])
            ):
                message += f"*{meta['title']}* — {doc[:140]}...\n\n"

        return {
            "agent": self.name,
            "message": message,
            "emp_data": emp_results,
            "doc_data": doc_results,
        }


class CompensationAdvisor:
    def __init__(self, kb):
        self.knowledge_base = kb
        self.name = "Compensation Advisor"

    def respond(self, analyst_response):
        emp_data = analyst_response.get("emp_data")

        message = "**Descriptive Compensation Summary**\n\n"
        if emp_data is not None and len(emp_data) > 0:
            average = emp_data["annual_salary_usd"].mean()
            message += f"Selected employees: **{len(emp_data):,}**\n\n"
            message += f"Mean annual salary: **${average:,.2f} USD**\n\n"
            message += "Use the analytics workspace to compare country and department cohorts. "
            message += "This selection may mix roles and labor markets; its average does not establish pay fairness or staffing needs."

        return {"agent": self.name, "message": message}
