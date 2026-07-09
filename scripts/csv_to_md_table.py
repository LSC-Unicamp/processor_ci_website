"""Compatibility wrapper for tools/csv_to_md_table.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "tools" / "csv_to_md_table.py"),
        run_name="__main__",
    )
