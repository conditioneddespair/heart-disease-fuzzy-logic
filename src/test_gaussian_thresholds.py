from gaussian_memberships import fuzzify_patient_gaussian
from rule_evaluation import evaluate_all_rules


patient = {
    "ChestPain": 7,
    "HbA1c": 10,
    "HDL": 25,
    "LDL": 185,
    "HeartRate": 110,
    "Age": 75,
    "BloodPressure": 210,
}

memberships = fuzzify_patient_gaussian(patient)
active_rules = evaluate_all_rules(memberships)

thresholds = [
    0,
    0.000001,
    0.00001,
    0.0001,
    0.001,
    0.01,
    0.05,
    0.1,
    0.3,
    0.5,
]

print("Toplam aktif kural:", len(active_rules))
print()

for threshold in thresholds:
    filtered_rules = [
        rule
        for rule in active_rules
        if rule["Strength"] > threshold
    ]

    print(
        f"Esik: {threshold:.6f} | "
        f"Kalan kural: {len(filtered_rules)}"
    )

print()
print(
    "En yuksek etkinlik:",
    max(rule["Strength"] for rule in active_rules)
)
