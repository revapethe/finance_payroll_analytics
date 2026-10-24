"""Build a native PBIP/PBIR report with a CSV-backed semantic model."""

import copy
import hashlib
import json
from pathlib import Path
from app.data import ROOT

PROJECT = ROOT / "powerbi/PayrollAnalytics"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/"


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def literal(value):
    return {
        "expr": {
            "Literal": {
                "Value": str(value).lower()
                if isinstance(value, bool)
                else str(value)
                if isinstance(value, (int, float))
                else "'" + value.replace("'", "''") + "'"
            }
        }
    }


def fill(color):
    return {"solid": {"color": literal(color)}}


def projection(table, name, measure=False):
    return {
        "field": {
            "Measure" if measure else "Column": {
                "Expression": {"SourceRef": {"Entity": table}},
                "Property": name,
            }
        },
        "queryRef": f"{table}.{name}",
    }


def build_project(destination=None):
    root = Path(destination or PROJECT)
    report = root / "PayrollAnalytics.Report"
    semantic = root / "PayrollAnalytics.SemanticModel"
    save(
        root / "PayrollAnalytics.pbip",
        {
            "$schema": SCHEMA + "pbip/pbipProperties/1.0.0/schema.json",
            "version": "1.0",
            "artifacts": [{"report": {"path": "PayrollAnalytics.Report"}}],
            "settings": {"enableAutoRecovery": True},
        },
    )
    save(
        report / "definition.pbir",
        {
            "$schema": SCHEMA + "item/report/definitionProperties/2.0.0/schema.json",
            "version": "4.0",
            "datasetReference": {"byPath": {"path": "../PayrollAnalytics.SemanticModel"}},
        },
    )
    save(
        semantic / "definition.pbism",
        {
            "$schema": SCHEMA + "item/semanticModel/definitionProperties/1.0.0/schema.json",
            "version": "1.0",
            "settings": {},
        },
    )
    model = copy.deepcopy(json.loads((ROOT / "powerbi/PayrollAnalytics.bim").read_text()))
    model["model"]["expressions"] = [
        {
            "name": "DataFolder",
            "kind": "m",
            "expression": '"C:\\PayrollAnalytics\\data" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]',
        }
    ]
    for table in model["model"]["tables"]:
        types = {
            "int64": "Int64.Type",
            "string": "type text",
            "dateTime": "type date",
            "decimal": "Currency.Type",
            "double": "type number",
        }
        conversions = ", ".join(
            '{"' + column["sourceColumn"] + '", ' + types[column["dataType"]] + "}"
            for column in table["columns"]
        )
        table["partitions"][0]["source"]["expression"] = [
            "let",
            f'    Source = Csv.Document(File.Contents(DataFolder & "/{table["name"]}.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            "    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
            f'    Typed = Table.TransformColumnTypes(Headers, {{{conversions}}}, "en-US")',
            "in",
            "    Typed",
        ]
    save(semantic / "model.bim", model)
    theme = {
        "name": "PayrollNavyTeal",
        "dataColors": ["#01B8AA", "#374649", "#FD625E", "#F2C80F", "#5F6B6D", "#8AD4EB"],
        "background": "#FFFFFF",
        "foreground": "#073867",
        "tableAccent": "#08B9B6",
    }
    save(report / "StaticResources/RegisteredResources/PayrollNavyTeal.json", theme)
    save(
        report / "definition/report.json",
        {
            "$schema": SCHEMA + "item/report/definition/report/3.0.0/schema.json",
            "themeCollection": {
                "customTheme": {
                    "name": "PayrollNavyTeal",
                    "reportVersionAtImport": {
                        "visual": "2.0.0",
                        "page": "2.0.0",
                        "report": "3.0.0",
                    },
                    "type": "RegisteredResources",
                }
            },
            "resourcePackages": [
                {
                    "name": "RegisteredResources",
                    "type": "RegisteredResources",
                    "items": [
                        {
                            "name": "PayrollNavyTeal",
                            "path": "PayrollNavyTeal.json",
                            "type": "CustomTheme",
                        }
                    ],
                }
            ],
        },
    )
    pages = [
        ("executive", "Executive Overview"),
        ("compensation", "Compensation Analysis"),
        ("workforce", "Workforce Profile"),
    ]
    save(
        report / "definition/pages/pages.json",
        {
            "$schema": SCHEMA + "item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": [p[0] for p in pages],
            "activePageName": "executive",
        },
    )

    def measure(name):
        return projection("fact_compensation", name, True)

    def column(table, name):
        return projection(table, name)

    total_visuals = 0
    for page_id, title in pages:
        page = report / "definition/pages" / page_id
        save(
            page / "page.json",
            {
                "$schema": SCHEMA + "item/report/definition/page/2.0.0/schema.json",
                "name": page_id,
                "displayName": title,
                "displayOption": "FitToPage",
                "width": 1280,
                "height": 900,
                "objects": {
                    "background": [
                        {"properties": {"color": fill("#041E38"), "transparency": literal(0)}}
                    ]
                },
            },
        )
        counter = 0

        def add(kind, title, roles, position, header=False):
            nonlocal counter, total_visuals
            counter += 1
            total_visuals += 1
            name = hashlib.sha256(f"{page_id}:{counter}:{title}".encode()).hexdigest()[:20]
            visual = {
                "visualType": kind,
                "visualContainerObjects": {
                    "title": [
                        {
                            "properties": {
                                "show": literal(True),
                                "text": literal(title),
                                "fontSize": literal(12),
                                "fontColor": fill("#073867"),
                            }
                        }
                    ],
                    "background": [
                        {
                            "properties": {
                                "show": literal(True),
                                "color": fill("#FFFFFF"),
                                "transparency": literal(0),
                            }
                        }
                    ],
                },
            }
            if roles:
                visual["query"] = {
                    "queryState": {role: {"projections": fields} for role, fields in roles.items()}
                }
            if header:
                visual["objects"] = {
                    "general": [
                        {
                            "properties": {
                                "paragraphs": [
                                    {
                                        "textRuns": [
                                            {
                                                "value": title,
                                                "textStyle": {
                                                    "fontFamily": "Segoe UI",
                                                    "fontSize": "22pt" if counter == 1 else "9pt",
                                                    "fontWeight": "bold",
                                                    "color": "#FFFFFF",
                                                },
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
                visual["visualContainerObjects"] = {
                    "title": [{"properties": {"show": literal(False)}}],
                    "background": [{"properties": {"show": literal(False)}}],
                }
            x, y, w, h = position
            save(
                page / "visuals" / name / "visual.json",
                {
                    "$schema": SCHEMA + "item/report/definition/visualContainer/2.0.0/schema.json",
                    "name": name,
                    "position": {
                        "x": x,
                        "y": y,
                        "width": w,
                        "height": h,
                        "z": counter,
                        "tabOrder": counter,
                    },
                    "visual": visual,
                },
            )

        add("textbox", title + " | Synthetic workforce snapshot", {}, (24, 12, 1232, 55), True)
        for index, (label, table, field) in enumerate(
            [
                ("Country", "dim_location", "country"),
                ("Department", "dim_department", "department"),
                ("Work arrangement", "dim_employee", "remote_status"),
            ]
        ):
            add(
                "slicer",
                label,
                {"Values": [column(table, field)]},
                (24 + index * 416, 76, 400, 125),
            )
        for index, name in enumerate(
            ["Headcount", "Annual Salary Run Rate USD", "Median Salary USD", "Remote Share"]
        ):
            add("card", name, {"Values": [measure(name)]}, (24 + index * 312, 215, 296, 110))
        if page_id == "executive":
            add(
                "clusteredBarChart",
                "Annual salary by department",
                {
                    "Category": [column("dim_department", "department")],
                    "Y": [measure("Annual Salary Run Rate USD")],
                    "Series": [column("dim_location", "country")],
                },
                (24, 340, 760, 295),
            )
            add(
                "donutChart",
                "Work arrangement mix",
                {
                    "Category": [column("dim_employee", "remote_status")],
                    "Y": [measure("Headcount")],
                },
                (800, 340, 448, 295),
            )
            details = [
                column("dim_location", "country"),
                column("dim_department", "department"),
                measure("Headcount"),
                measure("Median Salary USD"),
                measure("P90 Salary USD"),
            ]
        elif page_id == "compensation":
            add(
                "clusteredBarChart",
                "Average salary by job title",
                {
                    "Category": [column("dim_employee", "job_title")],
                    "Y": [measure("Average Salary USD")],
                    "Series": [column("dim_location", "country")],
                },
                (24, 340, 760, 295),
            )
            add(
                "clusteredColumnChart",
                "Median and P90 by country",
                {
                    "Category": [column("dim_location", "country")],
                    "Y": [measure("Median Salary USD"), measure("P90 Salary USD")],
                },
                (800, 340, 448, 295),
            )
            details = [
                column("dim_employee", "employee_id"),
                column("dim_employee", "job_title"),
                measure("Average Salary USD"),
                measure("Average Tenure Years"),
            ]
        else:
            add(
                "barChart",
                "Department workforce composition",
                {
                    "Category": [column("dim_department", "department")],
                    "Y": [measure("Headcount")],
                    "Series": [column("dim_employee", "remote_status")],
                },
                (24, 340, 760, 295),
            )
            add(
                "clusteredColumnChart",
                "Performance rating distribution",
                {"Category": [column("dim_employee", "performance")], "Y": [measure("Headcount")]},
                (800, 340, 448, 295),
            )
            details = [
                column("dim_location", "country"),
                column("dim_location", "city"),
                measure("Headcount"),
                measure("Average Salary USD"),
                measure("Average Tenure Years"),
            ]
        add("tableEx", "Workforce details", {"Values": details}, (24, 650, 1224, 215))
        add(
            "textbox",
            "Synthetic snapshot · Annual salary is a run rate, not paid payroll · No benefits, taxes or historical trends",
            {},
            (24, 866, 1224, 30),
            True,
        )
    return {"pages": len(pages), "visuals": total_visuals, "path": str(root)}


if __name__ == "__main__":
    print(json.dumps(build_project(), indent=2))
