from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

input_file = RAW_DIR / "inference_rules_or_training_data_set.csv"
output_file = PROCESSED_DIR / "inference_rules_cleaned.csv"

removed_lines = []

with open(input_file, "r", encoding="utf-8-sig") as source:
    with open(output_file, "w", encoding="utf-8", newline="") as target:
        for line_number, line in enumerate(source, start=1):

         
            if line.strip() == '"':
                removed_lines.append(line_number)
                continue

            target.write(line)

print("Temizlenmiş dosya:", output_file)
print("Kaldırılan satırlar:", removed_lines)
