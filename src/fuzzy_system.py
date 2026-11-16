
from fuzzification import fuzzify_patient
from rule_evaluation import evaluate_all_rules
from aggregation import aggregate_rules
from output_memberships import build_aggregated_output
from defuzzification import (
    centroid,
    mean_of_maxima,
    weighted_average,
    sum_of_area,
)


def evaluate_patient(patient):
    memberships = fuzzify_patient(patient)

    active_rules = evaluate_all_rules(memberships)

    if not active_rules:
        raise ValueError("Bu hasta için aktif bir kural bulunamadı.")

    aggregated = aggregate_rules(active_rules)

    x_values, output_memberships = build_aggregated_output(aggregated)

    centroid_score = centroid(x_values, output_memberships)

    wa_score = weighted_average(aggregated)
    sa_score = sum_of_area(aggregated)
    mm_score = mean_of_maxima(x_values, output_memberships)

    final_score = (wa_score + sa_score + mm_score) / 3

    return {
        "memberships": memberships,
        "active_rule_count": len(active_rules),
        "aggregated": aggregated,
        "centroid": centroid_score,
        "wa": wa_score,
        "sa": sa_score,
        "mm": mm_score,
        "final_score": final_score,
    }


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

    result = evaluate_patient(patient)

    print("Aktif kural sayısı:", result["active_rule_count"])
    print()

    print("Risk seviyelerine göre birleşim:")
    for risk, strength in result["aggregated"].items():
        print(f"{risk}: {strength:.4f}")

    print()
    print("Centroid:", round(result["centroid"], 4))
    print("Weighted Average:", round(result["wa"], 4))
    print("Sum of Area:", round(result["sa"], 4))
    print("Mean of Maxima:", round(result["mm"], 4))
    print()
    print("Nihai risk skoru:", round(result["final_score"], 4))
