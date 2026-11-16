from pathlib import Path
import pandas as pd

TABLES = Path("results/tables")

large = pd.read_csv(TABLES / "large_scale_results.csv")
sigma = pd.read_csv(TABLES / "sigma_sensitivity_results.csv")
multi = pd.read_csv(TABLES / "multi_variable_robustness.csv")
summary = pd.read_csv(TABLES / "multi_variable_summary.csv")
paired = pd.read_csv(TABLES / "all_sigma_paired_comparison.csv")

systems = [
    "Baseline",
    "Gaussian_0.5",
    "Gaussian_1.0",
    "Gaussian_1.5",
    "Gaussian_2.0",
]

variables = [
    "BloodPressure",
    "LDL",
    "HDL",
    "HeartRate",
    "HbA1c",
    "Age",
]

checks = []


def check(name, condition):
    passed = bool(condition)
    checks.append(passed)
    print(f"{'PASS' if passed else 'FAIL'} | {name}")


print("DENEY VERILERININ DOGRULANMASI")
print("-" * 55)

check(
    "Large-scale deney: 64 kayit",
    len(large) == 64,
)

check(
    "Sigma deneyi: 128 kayit",
    len(sigma) == 128,
)

check(
    "Multi-variable deney: 1920 kayit",
    len(multi) == 1920,
)

check(
    "Multi-variable ozet: 30 kayit",
    len(summary) == 30,
)

large_ids = set(large["patient_id"])
sigma_ids = set(sigma["patient_id"])
multi_ids = set(multi["patient_id"])

check(
    "Tum deneylerde ayni 32 profil",
    len(large_ids) == 32
    and large_ids == sigma_ids == multi_ids,
)

check(
    "Her sistem icin 384 perturbasyon",
    all(
        len(multi[multi["system"] == system]) == 384
        for system in systems
    ),
)

check(
    "Her sigma icin 32 profil",
    all(
        len(sigma[sigma["sigma_scale"] == scale]) == 32
        for scale in [0.5, 1.0, 1.5, 2.0]
    ),
)

check(
    "Her degisken icin 48 ortak durum",
    all(
        int(
            summary[summary["variable"] == variable][
                "common_cases"
            ].iloc[0]
        ) == 48
        for variable in variables
    ),
)

check(
    "Bes sistemin ortak profil sayisi: 24",
    len(paired) == 24,
)

expected_combinations = {
    (patient_id, system, variable, direction)
    for patient_id in large_ids
    for system in systems
    for variable in variables
    for direction in [-1, 1]
}

actual_combinations = set(
    zip(
        multi["patient_id"],
        multi["system"],
        multi["variable"],
        multi["direction"],
    )
)

check(
    "Tum perturbasyon kombinasyonlari eksiksiz",
    actual_combinations == expected_combinations,
)

print()
print("OZET ORTALAMALARIN KONTROLU")
print("-" * 55)

all_averages_correct = True

for variable in variables:
    subset = multi[multi["variable"] == variable]

    valid_ids = []

    for patient_id in large_ids:
        for direction in [-1, 1]:
            group = subset[
                (subset["patient_id"] == patient_id)
                & (subset["direction"] == direction)
            ]

            if (
                len(group) == 5
                and group["absolute_score_change"].notna().all()
            ):
                valid_ids.append((patient_id, direction))

    for system in systems:
        values = []

        for patient_id, direction in valid_ids:
            row = subset[
                (subset["patient_id"] == patient_id)
                & (subset["direction"] == direction)
                & (subset["system"] == system)
            ]

            values.append(
                float(row["absolute_score_change"].iloc[0])
            )

        calculated = (
            sum(values) / len(values)
            if values else None
        )

        stored = summary[
            (summary["variable"] == variable)
            & (summary["system"] == system)
        ]["mean_absolute_change"].iloc[0]

        if calculated is None:
            correct = pd.isna(stored)
        else:
            correct = abs(calculated - stored) < 1e-9

        if not correct:
            all_averages_correct = False
            print("Uyusmazlik:", variable, system)

check(
    "Multi-variable ozet ortalamalari dogru",
    all_averages_correct,
)

large_gaussian = large[
    large["system"] == "Gaussian"
].set_index("patient_id")

sigma_one = sigma[
    sigma["sigma_scale"] == 1.0
].set_index("patient_id")

same_scores = all(
    (
        pd.isna(large_gaussian.loc[patient_id, "score"])
        and pd.isna(sigma_one.loc[patient_id, "score"])
    )
    or abs(
        large_gaussian.loc[patient_id, "score"]
        - sigma_one.loc[patient_id, "score"]
    ) < 1e-9
    for patient_id in large_ids
)

check(
    "Gaussian 1.0 skorlari iki deneyde ayni",
    same_scores,
)

print()
print("GENEL SONUC")
print("-" * 55)

passed = sum(checks)
total = len(checks)

print(f"Basarili kontrol: {passed}/{total}")

if passed == total:
    print("Tum otomatik tutarlilik kontrolleri basarili.")
else:
    print("Bazi kontroller basarisiz. Rapor oncesi incelenmeli.")
    raise SystemExit(1)
