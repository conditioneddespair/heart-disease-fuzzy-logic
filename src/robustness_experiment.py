from fuzzy_system import evaluate_patient
from gaussian_fuzzy_system import evaluate_patient_gaussian

patients = {
    "Dusuk risk": {
        "ChestPain": 1,
        "HbA1c": 5.5,
        "HDL": 60,
        "LDL": 65,
        "HeartRate": 55,
        "Age": 30,
        "BloodPressure": 110,
    },
    "Orta risk": {
        "ChestPain": 3,
        "HbA1c": 7.5,
        "HDL": 45,
        "LDL": 115,
        "HeartRate": 80,
        "Age": 53,
        "BloodPressure": 145,
    },
    "Yuksek risk": {
        "ChestPain": 7,
        "HbA1c": 10,
        "HDL": 25,
        "LDL": 185,
        "HeartRate": 110,
        "Age": 75,
        "BloodPressure": 210,
    },
    "Makaledeki ornek": {
        "ChestPain": 5,
        "HbA1c": 10,
        "HDL": 30,
        "LDL": 141,
        "HeartRate": 60,
        "Age": 59,
        "BloodPressure": 126,
    },
}

perturbations = [
    ("BloodPressure", -5),
    ("BloodPressure", 5),
    ("LDL", -5),
    ("LDL", 5),
    ("HbA1c", -0.2),
    ("HbA1c", 0.2),
]

systems = {
    "Baseline": evaluate_patient,
    "Gaussian": evaluate_patient_gaussian,
}

minimum_strength = 0.001


def run_system(evaluate_function, patient):
    try:
        result = evaluate_function(patient)
    except ValueError:
        return None, False

    maximum_strength = max(result["aggregated"].values())

    if maximum_strength <= minimum_strength:
        return result["final_score"], False

    return result["final_score"], True


for name, patient in patients.items():
    print(f"\n{name}")
    print("-" * 55)

    for system_name, evaluate_function in systems.items():
        original_score, original_valid = run_system(
            evaluate_function,
            patient,
        )

        differences = []
        covered_count = 0

        for variable, change in perturbations:
            modified_patient = patient.copy()
            modified_patient[variable] += change

            new_score, new_valid = run_system(
                evaluate_function,
                modified_patient,
            )

            if new_valid:
                covered_count += 1

            if original_valid and new_valid:
                differences.append(
                    abs(new_score - original_score)
                )

        if original_score is None:
            score_text = "Hesaplanamadi"
        else:
            score_text = f"{original_score:.4f}"

        if differences:
            average_change = sum(differences) / len(differences)
            change_text = f"{average_change:.4f}"
        else:
            change_text = "Hesaplanamadi"

        print(f"\n{system_name}")
        print("Orijinal skor:", score_text)
        print("Orijinal kapsama:", original_valid)
        print("Perturbasyon kapsama:", f"{covered_count}/6")
        print("Karsilastirilabilir cift:", len(differences))
        print("Ortalama mutlak skor degisimi:", change_text)
