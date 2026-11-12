"""Recreate before/after logs without modifying the submitted fixed module."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "evidence" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")


def run(name, args, cwd, input_text=None, expected=0):
    result = subprocess.run(args, cwd=cwd, input=input_text, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=ENV)
    (LOGS / name).write_text(result.stdout, encoding="utf-8")
    print(result.stdout)
    if result.returncode != expected:
        raise SystemExit("Unexpected exit status: " + str(result.returncode))


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as folder:
        baseline = Path(folder)
        shutil.copyfile(ROOT / "original" / "coupon_validator.py", baseline / "coupon_validator.py")
        shutil.copyfile(ROOT / "test_coupon_validator.py", baseline / "test_coupon_validator.py")
        run("01_original_application.txt", [sys.executable, "coupon_validator.py"], baseline,
            "save-20\n199,49.5,320\n2024-03-01\n")
        run("01b_original_crash.txt", [sys.executable, "coupon_validator.py"], baseline,
            "bad\n", expected=1)
        run("02_failing_tests.txt", [sys.executable, "-m", "pytest", "test_coupon_validator.py",
            "-k", "no_crash", "--tb=short", "-q"], baseline, expected=1)
    run("03_fixed_application.txt", [sys.executable, "processor.py"], ROOT,
        "save-20\n199,49.5,320\n2024-03-01\n")
    run("03b_fixed_invalid.txt", [sys.executable, "processor.py"], ROOT,
        "bad\nnan\n2024-02-30\n")
    run("04_fixed_tests.txt", [sys.executable, "-m", "pytest", "test_processor.py", "-q"], ROOT)
