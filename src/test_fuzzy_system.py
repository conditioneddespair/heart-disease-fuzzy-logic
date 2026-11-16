
from fuzzy_system import evaluate_patient


patients = {
    "Test 1 - Dusuk risk profili": {
        "ChestPain": 1,
        "HbA1c": 5.5,
        "HDL": 60,
        "LDL": 65,
        "HeartRate": 55,
        "Age": 30,
        "BloodPressure": 110,
    },
    "Test 2 - Orta risk profili": {
        "ChestPain": 3,
        "HbA1c": 7.5,
        "HDL": 45,
        "LDL": 115,
        "HeartRate": 80,
        "Age": 53,
        "BloodPressure": 145,
    },
    "Test 3 - Yuksek risk profili": {
        "ChestPain": 7,
        "HbA1c": 10,
        "HDL": 25,
        "LDL": 185,
        "HeartRate": 110,
        "Age": 75,
        "BloodPressure": 210,
    },
}


for name, patient in patients.items():
    print(f"\n{name}")

    try:
        result = evaluate_patient(patient)

        print("Aktif kural sayisi:", result["active_rule_count"])
        print("Risk dagilimi:", result["aggregated"])
        print("Nihai risk skoru:", round(result["final_score"], 4))

    except ValueError as error:
        print("Hata:", error)


from fuzzification import fuzzify_patient

print("\nTest 3 - Uyelik dereceleri")

memberships = fuzzify_patient(patients["Test 3 - Yuksek risk profili"])

for variable, categories in memberships.items():
    active_categories = {
        category: round(value, 4)
        for category, value in categories.items()
        if value > 0
    }

    print(f"{variable}: {active_categories}")
