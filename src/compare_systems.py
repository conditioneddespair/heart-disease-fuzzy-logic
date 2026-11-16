from fuzzy_system import evaluate_patient
from gaussian_fuzzy_system import evaluate_patient_gaussian
from fuzzification import fuzzify_patient
from gaussian_memberships import fuzzify_patient_gaussian
from rule_evaluation import evaluate_all_rules

patients = {
    "Dusuk risk profili": {
        "ChestPain": 1,
        "HbA1c": 5.5,
        "HDL": 60,
        "LDL": 65,
        "HeartRate": 55,
        "Age": 30,
        "BloodPressure": 110,
    },
    "Orta risk profili": {
        "ChestPain": 3,
        "HbA1c": 7.5,
        "HDL": 45,
        "LDL": 115,
        "HeartRate": 80,
        "Age": 53,
        "BloodPressure": 145,
    },
    "Yuksek risk profili": {
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

def analyze_system(patient, fuzzify_function, evaluate_function):
    memberships = fuzzify_function(patient)
    rules = evaluate_all_rules(memberships)

    maximum_strength = max(
        (rule["Strength"] for rule in rules),
        default=0.0,
    )

    try:
        result = evaluate_function(patient)
        score = round(result["final_score"], 4)
    except ValueError:
        score = None

    return {
        "active_rules": len(rules),
        "maximum_strength": maximum_strength,
        "score": score,
    }

for name, patient in patients.items():
    baseline = analyze_system(
        patient,
        fuzzify_patient,
        evaluate_patient,
    )

    gaussian = analyze_system(
        patient,
        fuzzify_patient_gaussian,
        evaluate_patient_gaussian,
    )

    print(f"\n{name}")

    print(
        f"Baseline | Kural: {baseline['active_rules']} | "
        f"Max: {baseline['maximum_strength']:.8f} | "
        f"Skor: {baseline['score']}"
    )

    print(
        f"Gaussian | Kural: {gaussian['active_rules']} | "
        f"Max: {gaussian['maximum_strength']:.8f} | "
        f"Skor: {gaussian['score']}"
    )
