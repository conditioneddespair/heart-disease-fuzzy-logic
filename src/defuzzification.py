import numpy as np

from fuzzification import fuzzify_patient
from rule_evaluation import evaluate_all_rules
from aggregation import aggregate_rules
from output_memberships import build_aggregated_output, OUTPUT_SETS
from membership_functions import triangular


def centroid(x_values, memberships):
    area = np.trapezoid(memberships, x_values)

    if area == 0:
        raise ValueError("Birleşik çıktı alanı sıfır.")

    moment = np.trapezoid(x_values * memberships, x_values)

    return moment / area


def mean_of_maxima(x_values, memberships):
    maximum = np.max(memberships)

    if maximum <= 0:
        raise ValueError("Aktif çıktı üyeliği bulunamadı.")

    maximum_points = x_values[
        np.isclose(memberships, maximum)
    ]

    return np.mean(maximum_points)

    
def weighted_average(aggregated):
    numerator = 0.0
    denominator = 0.0

    for risk, strength in aggregated.items():
        center = OUTPUT_SETS[risk][1]

        numerator += strength * center
        denominator += strength

    if denominator == 0:
        raise ValueError("Aktif kural bulunamadı.")

    return numerator / denominator


def sum_of_area(aggregated, step=0.01):
    x_values = np.linspace(0, 10, int(round(10 / step)) + 1)

    numerator = 0.0
    denominator = 0.0

    for risk, strength in aggregated.items():
        if strength == 0:
            continue

        parameters = OUTPUT_SETS[risk]

        original = np.array([
            triangular(x, *parameters)
            for x in x_values
        ])

        clipped = np.minimum(original, strength)

        area = np.trapezoid(clipped, x_values)
        center = centroid(x_values, clipped)

        numerator += area * center
        denominator += area

    if denominator == 0:
        raise ValueError("Aktif çıktı alanı bulunamadı.")

    return numerator / denominator



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

    x_values, output_values = build_aggregated_output(aggregated)

    score = centroid(x_values, output_values)
    mm_score = mean_of_maxima(x_values, output_values)

    print("Centroid risk skoru:", round(score, 4))
    print("Mean of Maxima skoru:", round(mm_score, 4))

    
    paper_aggregated = {
        "Healthy": 0.0,
        "LowRisk": 0.0,
        "MediumRisk": 0.7,
        "HighRisk": 0.3,
    }

    paper_x, paper_output = build_aggregated_output(
        paper_aggregated
    )

    paper_centroid = centroid(paper_x, paper_output)
    paper_mm = mean_of_maxima(paper_x, paper_output)

    print("\nMakaledeki örnek kurallarla:")
    print("Centroid:", round(paper_centroid, 4))
    print("Mean of Maxima:", round(paper_mm, 4))

    
    paper_wa = weighted_average(paper_aggregated)
    paper_sa = sum_of_area(paper_aggregated)

    paper_final = (
        paper_wa + paper_sa + paper_mm
    ) / 3

    print("\nReferans örneği - üç yöntem:")
    print("WA:", round(paper_wa, 4))
    print("SA:", round(paper_sa, 4))
    print("MM:", round(paper_mm, 4))
    print("Nihai skor:", round(paper_final, 4))


