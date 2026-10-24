import pandas as pd
import pytest
from app.data import load_employee_data
from etl.generate import SEED_FILE, generate_employees, write_dataset


def test_generator_matches_versioned_fixture():
    generated = generate_employees()
    pd.testing.assert_frame_equal(generated, generate_employees())
    pd.testing.assert_frame_equal(generated, load_employee_data(), check_dtype=False)
    original = load_employee_data(SEED_FILE)
    pd.testing.assert_frame_equal(generated.head(len(original)), original)
    assert len(generated) == 50000
    assert generated.employee_id.nunique() == 50000
    assert generated.country.value_counts().to_dict() == {"United States": 25000, "India": 25000}


def test_generator_supports_other_sizes(tmp_path):
    path = tmp_path / "employees.csv"
    assert write_dataset(rows=2005, seed=7, output=path) == 2005
    frame = load_employee_data(path)
    assert frame.country.value_counts().to_dict() == {"United States": 1003, "India": 1002}
    first = path.read_bytes()
    write_dataset(rows=2005, seed=7, output=path)
    assert path.read_bytes() == first


def test_generator_protects_originals():
    with pytest.raises(ValueError, match="at least"):
        generate_employees(rows=1999)
    with pytest.raises(ValueError, match="must not be overwritten"):
        write_dataset(rows=2000, output=SEED_FILE)
