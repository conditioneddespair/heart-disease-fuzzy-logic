import csv
import random
from pathlib import Path
from statistics import mean

from gaussian_fuzzy_system import evaluate_patient_gaussian


SEED = 42
SAMPLES_PER_PROFILE = 8
MINIMUM_STRENGTH = 0.001
SIGMA_SCALES = [0.5, 1.0, 1.5, 2.0]

profiles = {
    "Low": {
        "ChestPain": 1,
        "HbA1c": 5.5,
        "HDL": 60,
        "LDL": 65,
        "HeartRate": 55,
        "Age": 30,
        "BloodPressure": 110,
    },
    "Medium": {
        "ChestPain": 3,
        "HbA1c": 7.5,
        "HDL": 45,
        "LDL": 115,
        "HeartRate": 80,
        "Age": 53,
        "BloodPressure": 145,
    },
    "High": {
        "ChestPain": 7,
        "HbA1c": 10,
        "HDL": 25,
        "LDL": 185,
        "HeartRate": 110,
        "Age": 75,
        "BloodPressure": 210,
    },
    "PaperExample": {
        "ChestPain": 5,
        "HbA1c": 10,
        "HDL": 30,
        "LDL": 141,
        "HeartRate": 60,
        "Age": 59,
        "BloodPressure": 126,
    },
}

variations = {
    "HbA1c": 0.3,
    "HDL": 5,
    "LDL": 7,
    "HeartRate": 5,
    "Age": 3,
    "BloodPressure": 7,
}


def generate_patients():
    rng = random.Random(SEED)
    patients = []

    for name, original in profiles.items():
        for index in range(SAMPLES_PER_PROFILE):
            patient = original.copy()

            if index > 0:
                for variable, variation in variations.items():
                    change = rng.uniform(-variation, variation)
                    patient[variable] = max(
                        0.01,
                        original[variable] + change,
                    )

            patients.append((f"{name}_{index + 1}", patient))

    return patients


def evaluate(patient, scale):
    try:
        result = evaluate_patient_gaussian(
            patient,
            sigma_scale=scale,
        )
    except ValueError as error:
        if "aktif kural bulunamadi" in str(error).lower():
            return None, 0.0, False
        raise

    maximum_strength = max(result["aggregated"].values())
    covered = maximum_strength > MINIMUM_STRENGTH

    return result["final_score"], maximum_strength, covered


patients = generate_patients()
rows = []

for scale in SIGMA_SCALES:
    for patient_id, patient in patients:
        score, strength, covered = evaluate(patient, scale)

        modified = patient.copy()
        modified["BloodPressure"] += 3

        modified_score, _, modified_covered = evaluate(
            modified,
            scale,
        )

        change = None

        if covered and modified_covered:
            change = abs(modified_score - score)

        rows.append({
            "patient_id": patient_id,
            "sigma_scale": scale,
            "score": score,
            "maximum_strength": strength,
            "covered": covered,
            "modified_covered": modified_covered,
            "absolute_score_change": change,
        })


output = Path("results/tables/sigma_sensitivity_results.csv")
output.parent.mkdir(parents=True, exist_ok=True)

with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)


print("Toplam sentetik profil:", len(patients))

for scale in SIGMA_SCALES:
    subset = [
        row for row in rows
        if row["sigma_scale"] == scale
    ]

    covered = sum(row["covered"] for row in subset)

    changes = [
        row["absolute_score_change"]
        for row in subset
        if row["absolute_score_change"] is not None
    ]

    coverage = covered / len(subset)

    change_text = (
        f"{mean(changes):.6f}"
        if changes else "Hesaplanamadi"
    )

    print(f"\nSigma: {scale:.1f}")
    print(f"Kapsama: {covered}/32 ({coverage:.2%})")
    print("Karsilastirilabilir cift:", len(changes))
    print("Ortalama mutlak skor degisimi:", change_text)

print("\nSonuclar kaydedildi:", output)
