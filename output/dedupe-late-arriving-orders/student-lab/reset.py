"""Setup step for the lab: (re)creates an empty output/ directory.

Usage: python reset.py
Safe to re-run at any time — this is also the lab's reset procedure.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output"


def main():
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir()
    print(f"Reset {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
