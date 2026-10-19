from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed" / "inference_rules_cleaned.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "data" / "processed" / "parsed_rules.csv"
)

INPUTS = [
    "ChestPain",
    "HbA1c",
    "HDL",
    "LDL",
    "HeartRate",
    "Age",
    "BloodPressure",
]

df = pd.read_csv(INPUT_FILE)

parsed_rows = []
invalid_rows = []

for index, row in df.iterrows():
    antecedent = row["Antecedent (If Condition)"]

    if pd.isna(antecedent):
        invalid_rows.append(index + 2)
        continue

    parsed_rule = {}

    try:
        for condition in antecedent.split(" AND "):
            name, value = condition.split(" = ", 1)
            name = name.strip()
            value = value.strip()

            if name not in INPUTS:
                raise ValueError(f"Bilinmeyen değişken: {name}")

            if name in parsed_rule:
                raise ValueError(f"Tekrarlanan değişken: {name}")

            parsed_rule[name] = value

        if set(parsed_rule) != set(INPUTS):
            raise ValueError("Eksik giriş değişkeni")

        parsed_rule["Risk"] = row["Consequent (Output)"]
        parsed_rows.append(parsed_rule)

    except ValueError as error:
        invalid_rows.append(index + 2)
        print(f"Satır {index + 2} ayrıştırılamadı: {error}")

parsed_df = pd.DataFrame(parsed_rows, columns=INPUTS + ["Risk"])
parsed_df.to_csv(OUTPUT_FILE, index=False)

print("Toplam kaynak kural:", len(df))
print("Başarıyla ayrıştırılan:", len(parsed_df))
print("Ayrıştırılamayan satırlar:", invalid_rows)
print("Eksik risk etiketi:", parsed_df["Risk"].isna().sum())
print("\nİlk üç kural:")
print(parsed_df.head(3).to_string(index=False))
print("\nDosya oluşturuldu:", OUTPUT_FILE)
