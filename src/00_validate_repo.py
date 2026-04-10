# """checks required files/folders exist"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


REQUIRED_FILES = [
    "data/reviews_clean.jsonl",
    "data/review_groups_auto.json",
    "data/review_groups_hybrid.json",
    "personas/personas_manual.json",
    "personas/personas_auto.json",
    "personas/personas_hybrid.json",
    "spec/spec_auto.md",
    "spec/spec_hybrid.md",
    "tests/tests_auto.json",
    "tests/tests_hybrid.json",
    "metrics/metrics_manual.json",
    "metrics/metrics_auto.json",
    "metrics/metrics_hybrid.json",
    "metrics/metrics_summary.json",
    "prompts/prompt_auto.json",
]


def main():
    print("Checking repository structure...\n")

    all_good = True

    for file_path in REQUIRED_FILES:
        full_path = os.path.join(BASE_DIR, file_path)

        if os.path.exists(full_path):
            print(f"{file_path} found")
        else:
            print(f"{file_path} MISSING")
            all_good = False

    print("\nRepository validation complete")

    if not all_good:
        print("Some files are missing.")
    else:
        print("All required files are present.")


if __name__ == "__main__":
    main()
