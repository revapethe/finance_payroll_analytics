import json
import shutil
from zipfile import ZipFile
import pytest
from etl.build_powerbi import build_project
from etl.validate_powerbi import validate_project


def test_native_project_schemas_fields_and_layout(tmp_path):
    result = build_project(tmp_path)
    assert result["pages"] == 3 and result["visuals"] == 36
    assert validate_project(tmp_path) == 44
    model = json.loads((tmp_path / "PayrollAnalytics.SemanticModel/model.bim").read_text())["model"]
    fields = {
        table["name"]: {
            "Column": {c["name"] for c in table["columns"]},
            "Measure": {m["name"] for m in table.get("measures", [])},
        }
        for table in model["tables"]
    }
    assert len(model["relationships"]) == 4
    assert len(fields["fact_compensation"]["Measure"]) == 11
    assert len(model["expressions"]) == 1 and model["expressions"][0]["name"] == "DataFolder"

    def check_fields(node):
        if isinstance(node, dict):
            for kind in ["Column", "Measure"]:
                if kind in node and "Expression" in node[kind]:
                    value = node[kind]
                    entity = value["Expression"]["SourceRef"]["Entity"]
                    assert value["Property"] in fields[entity][kind]
            for value in node.values():
                check_fields(value)
        elif isinstance(node, list):
            for value in node:
                check_fields(value)

    for visual in tmp_path.rglob("visual.json"):
        data = json.loads(visual.read_text())
        check_fields(data)
        position = data["position"]
        assert position["x"] >= 0 and position["y"] >= 0
        assert position["x"] + position["width"] <= 1280
        assert position["y"] + position["height"] <= 900


def test_official_schema_rejects_bad_visual(tmp_path):
    build_project(tmp_path)
    path = next(tmp_path.rglob("visual.json"))
    value = json.loads(path.read_text())
    value["position"]["width"] = "not-a-number"
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match="not-a-number"):
        validate_project(tmp_path)


def test_native_package_includes_report_and_data_without_credentials(tmp_path, monkeypatch):
    from etl import package_bi

    exported = tmp_path / "exports"
    exported.mkdir()
    for table in [
        "dim_employee",
        "dim_department",
        "dim_location",
        "dim_snapshot",
        "fact_compensation",
    ]:
        (exported / f"{table}.csv").write_text("placeholder\n")
    (exported / "manifest.json").write_text("{}")

    def fake_export(destination):
        for path in exported.iterdir():
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, destination / path.name)
        return {"tables": {"fact_compensation": 50000}}

    monkeypatch.setattr(package_bi, "DATA", tmp_path / "generated-root")
    monkeypatch.setattr(package_bi, "export_model", fake_export)
    target = package_bi.package_model(tmp_path / "report.zip")
    with ZipFile(target) as archive:
        names = archive.namelist()
        assert "PayrollAnalytics.pbip" in names
        assert "PayrollAnalytics.SemanticModel/model.bim" in names
        assert "PayrollAnalytics.Report/definition.pbir" in names
        assert len([name for name in names if name.endswith("/visual.json")]) == 36
        assert "data/fact_compensation.csv" in names
        assert "START_HERE.md" in names
        assert not any(".env" in name or "cache.abf" in name for name in names)
        assert archive.testzip() is None
