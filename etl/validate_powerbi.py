"""Validate native Power BI report files with offline official Microsoft JSON schemas."""

import json
from pathlib import Path
from urllib.parse import urlparse
from jsonschema import Draft7Validator
from referencing import Registry, Resource
from app.data import ROOT

SCHEMAS = ROOT / "powerbi/schemas"


def load_schema(uri):
    parsed = urlparse(uri)
    prefix = "/json-schemas/"
    if parsed.netloc != "developer.microsoft.com" or not parsed.path.startswith(prefix):
        raise ValueError(f"Unexpected schema URI: {uri}")
    path = SCHEMAS / parsed.path[len(prefix) :]
    # Microsoft uses both schema.embedded.json IDs and schema-embedded.json filenames.
    if not path.exists():
        path = Path(str(path).replace("schema.embedded.json", "schema-embedded.json"))
    return Resource.from_contents(json.loads(path.read_text()))


def validate_project(project=None):
    project = Path(project or ROOT / "powerbi/PayrollAnalytics")
    registry = Registry(retrieve=load_schema)
    checked = 0
    for path in project.rglob("*"):
        if path.suffix not in {".json", ".pbip", ".pbir", ".pbism"}:
            continue
        data = json.loads(path.read_text())
        uri = data.get("$schema")
        if not uri:
            continue
        schema = load_schema(uri).contents
        validator = Draft7Validator(schema, registry=registry)
        errors = list(validator.iter_errors(data))
        if errors:
            raise ValueError(
                f"{path.relative_to(project)}: {errors[0].message} at {list(errors[0].path)}"
            )
        checked += 1
    return checked


if __name__ == "__main__":
    print(f"Validated {validate_project()} project/report files against Microsoft schemas")
