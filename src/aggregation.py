from fuzzification import fuzzify_patient
from rule_evaluation import evaluate_all_rules


RISK_CLASSES = [
    "Healthy",
    "LowRisk",
    "MediumRisk",
    "HighRisk",
]


def aggregate_rules(active_rules):
    aggregated = {risk: 0.0 for risk in RISK_CLASSES}

    for result in active_rules:
        risk = result["Risk"]
        strength = result["Strength"]

        if risk not in aggregated:
            raise ValueError(f"Bilinmeyen risk kategorisi: {risk}")

        aggregated[risk] = max(aggregated[risk], strength)

    return aggregated


if __name__ == "__main__":
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
    active_rules = evaluate_all_rules(memberships)
    aggregated = aggregate_rules(active_rules)

    print("Aktif kural sayısı:", len(active_rules))
    print("\nBirleştirilmiş risk etkinlikleri:")

    for risk, strength in aggregated.items():
        print(f"{risk}: {strength}")
