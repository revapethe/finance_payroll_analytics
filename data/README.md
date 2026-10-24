# Demo data

`employee_data.csv` contains **50,000 synthetic employees**, split evenly between the United States and India (25,000 each).

`seed_employees.csv` preserves the original 2,000-row fixture. `python -m etl.generate --rows 50000 --seed 42` retains those records and adds 48,000 employees with unique IDs and synthetic identities. The additions use job titles aligned to departments, fixed illustrative salary ranges, and a reference date of 2026-10-23. INR salaries are converted with the illustrative fixed factor 0.012 USD/INR. These are not surveyed compensation figures or real employee records. Original seed rows retain their original field values and generation assumptions.

Generation is deterministic and does not run at app startup. `--output` writes a separate experiment; `--rows` must be at least 2,000. The tests verify repeatability, preservation of the original rows, unique IDs, country balance and consistency with the checked-in dataset.

`documents/` contains text extracted from the original 25 synthetic policy PDF fixtures. They are retrieval examples, not real company policies. The index command never rewrites these sources.

`generated/` is ignored. Rebuild the SQLite export with `python -m etl.load` after modifying the CSV; rebuild policy indexes separately with `python -m etl.index_documents`.
