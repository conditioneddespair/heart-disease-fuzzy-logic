from membership_functions import triangular

OUTPUT_SETS = {
    "Healthy": (0, 2, 4),
    "LowRisk": (2, 4, 6),
    "MediumRisk": (4, 6, 8),
    "HighRisk": (6, 8, 10),
}

def calculate_output_memberships(x):
    return {
        risk: triangular(x, *parameters)
        for risk, parameters in OUTPUT_SETS.items()
    }

def build_aggregated_output(aggregated, step=0.01):
    if step <= 0:
        raise ValueError("step pozitif olmalı.")

    import numpy as np

    x_values = np.linspace(0, 10, int(round(10 / step)) + 1)
    output_values = []

    for x in x_values:
        memberships = calculate_output_memberships(x)

        clipped_values = [
            min(aggregated[risk], memberships[risk])
            for risk in OUTPUT_SETS
        ]

        output_values.append(max(clipped_values))

    return x_values, np.array(output_values)

if __name__ == "__main__":
    aggregated = {
        "Healthy": 0.0,
        "LowRisk": 0.0,
        "MediumRisk": 0.0,
        "HighRisk": 0.7,
    }

    x_values, output_values = build_aggregated_output(aggregated)

    for x in [6, 7, 8, 9, 10]:
        index = int(round(x * 100))
        print(f"x = {x}, üyelik = {output_values[index]:.2f}")
