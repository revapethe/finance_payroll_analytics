"""Compatibility entry point for the existing Streamlit Community Cloud deployment."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parent / "app/dashboard.py"), run_name="__main__")
