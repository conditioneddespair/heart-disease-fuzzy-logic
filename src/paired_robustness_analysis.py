import pandas as pd

path = "results/tables/large_scale_results.csv"
df = pd.read_csv(path)

baseline = df[df["system"] == "Baseline"].set_index("patient_id")
gaussian = df[df["system"] == "Gaussian"].set_index("patient_id")

paired = baseline[
    ["covered", "modified_covered", "absolute_score_change"]
].join(
    gaussian[
        ["covered", "modified_covered", "absolute_score_change"]
    ],
    how="inner",
    lsuffix="_baseline",
    rsuffix="_gaussian",
)

valid = paired[
    (paired["covered_baseline"])
    & (paired["covered_gaussian"])
    & (paired["modified_covered_baseline"])
    & (paired["modified_covered_gaussian"])
].dropna(
    subset=[
        "absolute_score_change_baseline",
        "absolute_score_change_gaussian",
    ]
)

baseline_changes = valid["absolute_score_change_baseline"]
gaussian_changes = valid["absolute_score_change_gaussian"]

print("Ortak karsilastirilabilir profil:", len(valid))

if not valid.empty:
    print(
        "Baseline ortalama mutlak degisim:",
        round(baseline_changes.mean(), 6),
    )
    print(
        "Gaussian ortalama mutlak degisim:",
        round(gaussian_changes.mean(), 6),
    )

    print(
        "Baseline daha az degisti:",
        int((baseline_changes < gaussian_changes).sum()),
    )
    print(
        "Gaussian daha az degisti:",
        int((gaussian_changes < baseline_changes).sum()),
    )
    print(
        "Esit degisim:",
        int((baseline_changes == gaussian_changes).sum()),
    )

    output_path = "results/tables/paired_robustness_results.csv"
    valid.to_csv(output_path)

    print("Sonuclar kaydedildi:", output_path)
else:
    print("Karsilastirilabilir ortak profil bulunamadi.")
