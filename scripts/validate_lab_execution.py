import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


TIMEOUT = 300
IGNORE_PATTERNS = shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc", "*.pyo")


def command_text(argv):
    return " ".join(str(item) for item in argv)


def validate_command_list(value, label, errors, required):
    if value in (None, []):
        if required:
            errors.append(f"{label} must contain at least one command")
        return []

    if not isinstance(value, list):
        errors.append(f"{label} must be a list of argv lists")
        return []

    commands = []
    for index, command in enumerate(value, start=1):
        command_label = f"{label}[{index}]"
        if not isinstance(command, list) or not command:
            errors.append(f"{command_label} must be a non-empty argv list")
            continue
        if not all(isinstance(arg, str) and arg for arg in command):
            errors.append(f"{command_label} must contain only non-empty strings")
            continue
        commands.append(command)
    return commands


def load_manifest(course_dir, errors):
    manifest_path = course_dir / "validate.json"
    if not manifest_path.is_file():
        errors.append(f"missing validate.json in {course_dir}")
        return None

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid validate.json: {exc}")
        return None

    if not isinstance(manifest, dict):
        errors.append("validate.json must contain a JSON object")
        return None
    return manifest


def run_cmds(commands, cwd, errors, label):
    for argv in commands:
        try:
            result = subprocess.run(
                argv,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
                check=False,
            )
        except FileNotFoundError as exc:
            errors.append(f"{label} command not found: {command_text(argv)} ({exc})")
            return False
        except subprocess.TimeoutExpired:
            errors.append(f"{label} command timed out after {TIMEOUT}s: {command_text(argv)}")
            return False

        if result.returncode != 0:
            tail = (result.stdout + result.stderr)[-2000:]
            errors.append(f"{label} failed (exit {result.returncode}): {command_text(argv)}\n{tail}")
            return False
    return True


def overlay_solution(course_dir, tmp_lab, errors):
    solution_dir = course_dir / "instructor" / "solution"
    if not solution_dir.is_dir():
        errors.append("Missing instructor/solution; cannot verify the lab is solvable")
        return False

    applied = False
    for source in solution_dir.rglob("*"):
        if not source.is_file() or source.suffix in {".pyc", ".pyo"} or "__pycache__" in source.parts:
            continue
        rel = source.relative_to(solution_dir)
        target = tmp_lab / "starter" / rel
        if not target.is_file():
            errors.append(f"instructor/solution file has no matching starter file: {rel}")
            continue
        shutil.copyfile(source, target)
        applied = True

    if not applied:
        errors.append("No instructor solution files were applied over the starter")
    return applied and not errors


def main():
    parser = argparse.ArgumentParser(description="Execute a lab validate.json against the instructor solution.")
    parser.add_argument("course_dir", type=Path)
    args = parser.parse_args()

    course_dir = args.course_dir
    errors = []
    lab_dir = course_dir / "student-lab"
    if not lab_dir.is_dir():
        print("ERROR: missing student-lab in", course_dir)
        return 1

    manifest = load_manifest(course_dir, errors)
    if manifest is None:
        for error in errors:
            print("ERROR:", error)
        return 1

    setup_commands = validate_command_list(manifest.get("setup", []), "validate.json.setup", errors, required=False)
    validate_commands = validate_command_list(manifest.get("validate"), "validate.json.validate", errors, required=True)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    ok = False
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_lab = Path(temp_dir) / "student-lab"
        shutil.copytree(lab_dir, tmp_lab, ignore=IGNORE_PATTERNS)
        if overlay_solution(course_dir, tmp_lab, errors):
            ok = run_cmds(setup_commands, tmp_lab, errors, "setup")
            if ok:
                ok = run_cmds(validate_commands, tmp_lab, errors, "validate")

    for error in errors:
        print("ERROR:", error)
    if not ok:
        return 1
    print("OK: instructor solution passes the lab tests -", course_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
