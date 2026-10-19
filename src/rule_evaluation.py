
from pathlib import Path
import pandas as pd
from fuzzification import fuzzify_patient



CATEGORY_ALIASES = {
    ("LDL", "HIgh"): "High",
    ("LDL", "VeryHIgh"): "VeryHigh",
    ("LDL", "XtraHigh"): "ExtraHigh",
    ("LDL", "XHigh"): "ExtraHigh",
    ("LDL", "XHIgh"): "ExtraHigh",
}


def evaluate_rule(rule, memberships):
    degrees = []

    for variable, category in rule.items():
        if variable == "Risk":
            continue

        category = CATEGORY_ALIASES.get(
            (variable, category),
            category
        )

        if category not in memberships[variable]:
            raise ValueError(
                f"Uyumsuz kategori: {variable} = {category}. "
                f"Geçerli kategoriler: {list(memberships[variable])}"
            )

        degrees.append(memberships[variable][category])

    return min(degrees)


def evaluate_all_rules(memberships):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "data" / "processed" / "parsed_rules.csv"

    df = pd.read_csv(file_path)
    df = df.dropna(subset=["Risk"])

    results = []

    for _, row in df.iterrows():
        rule = row.to_dict()
        strength = evaluate_rule(rule, memberships)

        if strength > 0:
            results.append({
                "Risk": rule["Risk"],
                "Strength": strength,
                "Rule": rule,
            })

    return results

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

    rule_1 = {
        "ChestPain": "Atypical",
        "HbA1c": "High",
        "HDL": "Low",
        "LDL": "VeryHigh",
        "HeartRate": "VeryHealthy",
        "Age": "Mid",
        "BloodPressure": "Normal",
        "Risk": "MediumRisk",
    }

    rule_2 = {
        **rule_1,
        "BloodPressure": "High",
        "Risk": "HighRisk",
    }

    print("Kural 1:", evaluate_rule(rule_1, memberships))
    print("Kural 2:", evaluate_rule(rule_2, memberships))

    active_rules = evaluate_all_rules(memberships)

    print("\nAktif kural sayısı:", len(active_rules))

    
    for result in active_rules:
        print("\nRisk:", result["Risk"])
        print("Etkinlik:", result["Strength"])
        print("Kural koşulları:")

        for variable, category in result["Rule"].items():
            if variable != "Risk":
                print(f"  {variable}: {category}")

