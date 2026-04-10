# """runs the full pipeline end-to-end"""

import subprocess
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")


def run_script(script_name):
    script_path = os.path.join(SRC_DIR, script_name)

    if not os.path.exists(script_path):
        print(f"Skipping {script_name} (not found)")
        return

    print(f"\nRunning {script_name}...")
    result = subprocess.run([sys.executable, script_path])

    if result.returncode != 0:
        print(f"Error running {script_name}")
        sys.exit(1)


def main():
    print("Starting automated pipeline...")

    # Step 1: Clean dataset (if applicable)
    run_script("02_clean_reviews.py")

    # Step 2: Generate review groups + personas
    run_script("05_personas_auto.py")

    # Step 3: Generate specifications
    run_script("06_spec_generate.py")

    # Step 4: Generate validation tests
    run_script("07_tests_generate.py")

    # Step 5: Compute automated metrics
    run_script("08_metrics.py")

    print("\nAutomated pipeline completed successfully.")


if __name__ == "__main__":
    main()
