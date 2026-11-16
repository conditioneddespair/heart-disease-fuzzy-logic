import csv
import random
from pathlib import Path
from statistics import mean

from fuzzy_system import evaluate_patient
from gaussian_fuzzy_system import evaluate_patient_gaussian

SEED = 42
SAMPLES_PER_PROFILE = 8
MINIMUM_STRENGTH = 0.001

OUTPUT_DIR = Path("results/tables")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random_generator = random.Random(SEED)

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

systems = {
    "Baseline": evaluate_patient,
    "Gaussian": evaluate_patient_gaussian,
}


def generate_patients():
    patients = []

    for profile_name, original in profiles.items():
        for index in range(SAMPLES_PER_PROFILE):
            patient = original.copy()

            if index > 0:
                for variable, variation in variations.items():
                    change = random_generator.uniform(
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


def evaluate(evaluate_function, patient):
    try:
        result = evaluate_function(patient)
    except ValueError:
        return {
            "score": None,
            "maximum_strength": 0.0,
            "active_rules": 0,
            "covered": False,
        }

    maximum_strength = max(
        result["aggregated"].values()
    )

    return {
        "score": result["final_score"],
        "maximum_strength": maximum_strength,
        "active_rules": result["active_rule_count"],
        "covered": maximum_strength > MINIMUM_STRENGTH,
    }


def calculate_mean(values):
    return mean(values) if values else None


def format_number(value):
    return "N/A" if value is None else f"{value:.4f}"


patients = generate_patients()
rows = []

for patient_id, patient in patients:
    for system_name, evaluate_function in systems.items():
        original = evaluate(evaluate_function, patient)

        modified_patient = patient.copy()
        modified_patient["BloodPressure"] += 3

        modified = evaluate(
            evaluate_function,
            modified_patient,
        )

        score_change = None

        if original["covered"] and modified["covered"]:
            score_change = abs(
                modified["score"] - original["score"]
            )

        rows.append({
            "patient_id": patient_id,
            "system": system_name,
            "score": original["score"],
            "maximum_strength": original["maximum_strength"],
            "active_rules": original["active_rules"],
            "covered": original["covered"],
            "modified_covered": modified["covered"],
            "absolute_score_change": score_change,
        })


output_path = OUTPUT_DIR / "large_scale_results.csv"

with output_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=rows[0].keys(),
    )
    writer.writeheader()
    writer.writerows(rows)


print("Toplam sentetik profil:", len(patients))
print("Toplam sistem degerlendirmesi:", len(rows))

for system_name in systems:
    system_rows = [
        row for row in rows
        if row["system"] == system_name
    ]

    covered_rows = [
        row for row in system_rows
        if row["covered"]
    ]

    changes = [
        row["absolute_score_change"]
        for row in system_rows
        if row["absolute_score_change"] is not None
    ]

    coverage = len(covered_rows) / len(system_rows)

    print(f"\n{system_name}")
    print(
        "Kapsanan profil:",
        f"{len(covered_rows)}/{len(system_rows)}"
    )
    print("Kapsama orani:", f"{coverage:.2%}")
    print("Karsilastirilabilir degisim:", len(changes))
    print(
        "Ortalama mutlak skor degisimi:",
        format_number(calculate_mean(changes)),
    )


paired_differences = []

for patient_id, patient in patients:
    baseline = evaluate(evaluate_patient, patient)
    gaussian = evaluate(evaluate_patient_gaussian, patient)

    if baseline["covered"] and gaussian["covered"]:
        paired_differences.append(
            abs(baseline["score"] - gaussian["score"])
        )

print("\nIki sistemin de kapsadigi profil:", len(paired_differences))
print(
    "Ortalama sistemler arasi skor farki:",
    format_number(calculate_mean(paired_differences)),
)
print("\nSonuclar kaydedildi:", output_path)
