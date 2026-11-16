import csv
import random
from pathlib import Path
from statistics import mean

from fuzzy_system import evaluate_patient
from gaussian_fuzzy_system import evaluate_patient_gaussian


SEED = 42
SAMPLES_PER_PROFILE = 8
MINIMUM_STRENGTH = 0.001
SIGMA_SCALES = [0.5, 1.0, 1.5, 2.0]

PROFILES = {
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

VARIATIONS = {
    "HbA1c": 0.3,
    "HDL": 5,
    "LDL": 7,
    "HeartRate": 5,
    "Age": 3,
    "BloodPressure": 7,
}

PERTURBATIONS = {
    "BloodPressure": 5,
    "LDL": 5,
    "HDL": 5,
    "HeartRate": 5,
    "HbA1c": 0.2,
    "Age": 2,
}

SYSTEMS = [
    "Baseline",
    "Gaussian_0.5",
    "Gaussian_1.0",
    "Gaussian_1.5",
    "Gaussian_2.0",
]


def generate_patients():
    rng = random.Random(SEED)
    patients = []

    for profile_name, original in PROFILES.items():
        for index in range(SAMPLES_PER_PROFILE):
            patient = original.copy()

            if index > 0:
                for variable, variation in VARIATIONS.items():
                    change = rng.uniform(
                        -variation,
                        variation,
                    )

                    patient[variable] = max(
                        0.01,
                        original[variable] + change,
                    )

            patients.append(
                (f"{profile_name}_{index + 1}", patient)
            )

    return patients



def evaluate(system, patient):
    if system == "Baseline":
        evaluate_function = evaluate_patient
        kwargs = {}
    else:
        evaluate_function = evaluate_patient_gaussian
        kwargs = {
            "sigma_scale": float(system.split("_")[1])
        }

    try:
        result = evaluate_function(patient, **kwargs)
    except ValueError as error:
        if "aktif bir kural bulunamadı" in str(error).lower():
            return None, 0.0, False

        if "aktif kural bulunamadi" in str(error).lower():
            return None, 0.0, False

        raise

    maximum_strength = max(result["aggregated"].values())

    return (
        result["final_score"],
        maximum_strength,
        maximum_strength > MINIMUM_STRENGTH,
    )


patients = generate_patients()
rows = []

for system in SYSTEMS:
    print("Degerlendiriliyor:", system, flush=True)

    for patient_id, patient in patients:
        original_score, _, original_covered = evaluate(
            system,
            patient,
        )

        for variable, magnitude in PERTURBATIONS.items():
            for direction in [-1, 1]:
                modified_patient = patient.copy()
                modified_patient[variable] += direction * magnitude

                modified_score, _, modified_covered = evaluate(
                    system,
                    modified_patient,
                )

                change = None

                if original_covered and modified_covered:
                    change = abs(
                        modified_score - original_score
                    )

                rows.append({
                    "patient_id": patient_id,
                    "system": system,
                    "variable": variable,
                    "direction": direction,
                    "original_covered": original_covered,
                    "modified_covered": modified_covered,
                    "absolute_score_change": change,
                })


output_dir = Path("results/tables")
output_dir.mkdir(parents=True, exist_ok=True)

output_path = output_dir / "multi_variable_robustness.csv"

with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(rows)


print("\nToplam profil:", len(patients))
print("Toplam perturbasyon degerlendirmesi:", len(rows))
print("\nTum sistemlerin ortak kapsadigi durumlar:")
print("-" * 65)

summary_rows = []

for variable in PERTURBATIONS:
    variable_rows = [
        row for row in rows
        if row["variable"] == variable
    ]

    grouped = {}

    for row in variable_rows:
        key = (row["patient_id"], row["direction"])

        if key not in grouped:
            grouped[key] = {}

        grouped[key][row["system"]] = row

    common_keys = [
        key
        for key, values in grouped.items()
        if all(
            system in values
            and values[system]["absolute_score_change"] is not None
            for system in SYSTEMS
        )
    ]

    print(f"\n{variable}")
    print("Ortak karsilastirilabilir durum:", len(common_keys))

    for system in SYSTEMS:
        changes = [
            grouped[key][system]["absolute_score_change"]
            for key in common_keys
        ]

        average = mean(changes) if changes else None

        average_text = (
            f"{average:.6f}"
            if average is not None
            else "Hesaplanamadi"
        )

        summary_rows.append({
            "variable": variable,
            "system": system,
            "common_cases": len(common_keys),
            "mean_absolute_change": average,
        })

        print(f"{system:15s}: {average_text}")


summary_path = output_dir / "multi_variable_summary.csv"

with summary_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=summary_rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(summary_rows)

print("\nDetayli sonuclar:", output_path)
print("Ozet sonuclar:", summary_path)
