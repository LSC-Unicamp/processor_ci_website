"""Compatibility wrapper for tools/plot_from_data.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "tools" / "plot_from_data.py"), run_name="__main__")
