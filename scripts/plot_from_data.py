"""Compatibility wrapper for tools/plot_from_data.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "tools" / "plot_from_data.py"
    runpy.run_path(str(target), run_name="__main__")
