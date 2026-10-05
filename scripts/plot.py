"""Compatibility wrapper for tools/plot.py."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parents[1] / "tools" / "plot.py"
    runpy.run_path(str(target), run_name="__main__")
