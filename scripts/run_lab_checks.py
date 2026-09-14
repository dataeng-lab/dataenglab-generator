import argparse
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = (
    "lab-spec.md",
    "page-content.md",
    "validate.json",
    "student-lab/README.md",
    "instructor/instructor-guide.md",
    "instructor/troubleshooting.md",
)
REQUIRED_DIRS = (
    "student-lab/starter",
    "student-lab/datasets",
    "student-lab/tests",
    "instructor/solution",
)


def format_command(argv):
    return " ".join(str(item) for item in argv)


def run(argv):
    print("\n$", format_command(argv), flush=True)
    result = subprocess.run(argv, check=False)
    status = "PASS" if result.returncode == 0 else f"FAIL ({result.returncode})"
    print(status + ":", format_command(argv), flush=True)
    return result.returncode == 0


def check_required_paths(lab_output_dir):
    errors = []

    for relative_path in REQUIRED_FILES:
        path = lab_output_dir / relative_path
        if not path.is_file() or path.stat().st_size == 0:
            errors.append("Missing or empty: " + relative_path)

    for relative_path in REQUIRED_DIRS:
        if not (lab_output_dir / relative_path).is_dir():
            errors.append("Missing directory: " + relative_path)

    for error in errors:
        print("ERROR:", error, flush=True)

    return not errors


def main():
    parser = argparse.ArgumentParser(description="Run validation checks for a standalone DataEngLab lab output.")
    parser.add_argument("lab_output_dir", type=Path)
    args = parser.parse_args()

    lab_output_dir = args.lab_output_dir
    scripts_dir = Path(__file__).resolve().parent
    py = sys.executable

    if not lab_output_dir.is_dir():
        print("ERROR: missing lab output directory", lab_output_dir, flush=True)
        return 1

    commands = [
        [py, str(scripts_dir / "validate_lab.py"), str(lab_output_dir / "student-lab")],
        [py, str(scripts_dir / "validate_lab_execution.py"), str(lab_output_dir)],
    ]

    lab_page = lab_output_dir / "elementor" / "labs-page.json"
    if lab_page.is_file():
        commands.append([py, str(scripts_dir / "validate_elementor_json.py"), str(lab_page)])

    ok = check_required_paths(lab_output_dir)
    for command in commands:
        ok = run(command) and ok

    print("ALL LAB CHECKS PASSED" if ok else "LAB CHECKS FAILED", flush=True)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
