from pathlib import Path
import pandas as pd
from fuzzification import fuzzify_patient

BASE_DIR = Path(__file__).resolve().parent.parent

file_path = BASE_DIR / "data" / "processed" / "parsed_rules.csv"

df = pd.read_csv(file_path)

patient = {
    "ChestPain": 5,
    "HbA1c": 10,
    "HDL": 30,
    "LDL": 141,
    "HeartRate": 60,
    "Age": 59,
    "BloodPressure": 126,
}

memberships = fuzzify_patient(patient)

print("KATEGORİ DOĞRULAMA:")

total_invalid = 0

for variable, valid_categories in memberships.items():
    observed = df[variable].dropna().unique()

    for category in observed:
        if category not in valid_categories:
            count = (df[variable] == category).sum()

            print(
                f"{variable} = {category} "
                f"| Kayıt sayısı: {count} "
                f"| Geçerli: {list(valid_categories)}"
            )

            total_invalid += count

print("\nUyumsuz kategori içeren hücre sayısı:", total_invalid)
