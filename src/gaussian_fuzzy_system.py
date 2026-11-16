from gaussian_memberships import fuzzify_patient_gaussian
from rule_evaluation import evaluate_all_rules
from aggregation import aggregate_rules
from output_memberships import build_aggregated_output
from defuzzification import (
    centroid,
    mean_of_maxima,
    weighted_average,
    sum_of_area,
)


def evaluate_patient_gaussian(patient, sigma_scale=1.0):
    memberships = fuzzify_patient_gaussian(patient, sigma_scale)

    active_rules = evaluate_all_rules(memberships)

    if not active_rules:
        raise ValueError("Gaussian sisteminde aktif kural bulunamadi.")

    aggregated = aggregate_rules(active_rules)

    x_values, output_memberships = build_aggregated_output(
        aggregated
    )

    centroid_score = centroid(x_values, output_memberships)
    wa_score = weighted_average(aggregated)
    sa_score = sum_of_area(aggregated)
    mm_score = mean_of_maxima(x_values, output_memberships)

    final_score = (wa_score + sa_score + mm_score) / 3

    return {
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
        "ChestPain": 7,
        "HbA1c": 10,
        "HDL": 25,
        "LDL": 185,
        "HeartRate": 110,
        "Age": 75,
        "BloodPressure": 210,
    }

    result = evaluate_patient_gaussian(patient)

    print("Gaussian aktif kural sayisi:", result["active_rule_count"])
    print()

    print("Risk dagilimi:")
    for risk, strength in result["aggregated"].items():
        print(f"{risk}: {strength:.8f}")

    print()
    print("Centroid:", round(result["centroid"], 4))
    print("Weighted Average:", round(result["wa"], 4))
    print("Sum of Area:", round(result["sa"], 4))
    print("Mean of Maxima:", round(result["mm"], 4))
    print()
    print("Nihai risk skoru:", round(result["final_score"], 4))
