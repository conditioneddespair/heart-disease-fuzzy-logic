import pandas as pd

baseline_df = pd.read_csv(
    "results/tables/large_scale_results.csv"
)

sigma_df = pd.read_csv(
    "results/tables/sigma_sensitivity_results.csv"
)


def get_valid_changes(df):
    valid = df[
        (df["covered"] == True)
        & (df["modified_covered"] == True)
    ]

    return valid.set_index("patient_id")[
        "absolute_score_change"
    ]


baseline = get_valid_changes(
    baseline_df[baseline_df["system"] == "Baseline"]
).rename("Baseline")

series = [baseline]

for scale in [0.5, 1.0, 1.5, 2.0]:
    subset = sigma_df[
        sigma_df["sigma_scale"] == scale
    ]

    changes = get_valid_changes(subset).rename(
        f"Gaussian_{scale}"
    )

    series.append(changes)

comparison = pd.concat(series, axis=1).dropna()

print("Tum sistemlerde ortak kapsanan profil:", len(comparison))
print()

if not comparison.empty:
    print("Ayni profillerde ortalama mutlak skor degisimi:")

    averages = comparison.mean().sort_values()

    for system, value in averages.items():
        print(f"{system}: {value:.6f}")

    comparison.to_csv(
        "results/tables/all_sigma_paired_comparison.csv"
    )

    print()
    print("Sonuclar kaydedildi.")
else:
    print("Ortak karsilastirilabilir profil bulunamadi.")
