from gaussian_memberships import fuzzify_patient_gaussian
from rule_evaluation import evaluate_all_rules
from aggregation import aggregate_rules
from output_memberships import build_aggregated_output
from defuzzification import (
    weighted_average,
    sum_of_area,
    mean_of_maxima,
)

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

thresholds = [0, 0.0001, 0.001, 0.01, 0.1]

def calculate_score(rules):
    if not rules:
        return None

    aggregated = aggregate_rules(rules)

    x_values, output = build_aggregated_output(aggregated)

    wa = weighted_average(aggregated)
    sa = sum_of_area(aggregated)
    mm = mean_of_maxima(x_values, output)

    return (wa + sa + mm) / 3

for name, patient in patients.items():
    memberships = fuzzify_patient_gaussian(patient)
    rules = evaluate_all_rules(memberships)

    print(f"\n{name}")
    print("-" * 55)

    for threshold in thresholds:
        filtered = [
            rule
            for rule in rules
            if rule["Strength"] > threshold
        ]

        score = calculate_score(filtered)

        if score is None:
            score_text = "Hesaplanamadi"
        else:
            score_text = f"{score:.4f}"

        print(
            f"Esik: {threshold:.4f} | "
            f"Kural: {len(filtered):4d} | "
            f"Skor: {score_text}"
        )
