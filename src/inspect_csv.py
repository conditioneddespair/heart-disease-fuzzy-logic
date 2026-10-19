from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = (
    BASE_DIR
    / "data"
    / "raw"
    / "inference_rules_or_training_data_set.csv"
)

with open(file_path, "r", encoding="utf-8-sig") as file:
    for line_number, line in enumerate(file, start=1):
        if 995 <= line_number <= 1010:
            print(f"{line_number}: {line.rstrip()!r}")
