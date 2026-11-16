from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


output_dir = Path("results/figures")
output_dir.mkdir(parents=True, exist_ok=True)

sigma_df = pd.read_csv(
    "results/tables/sigma_sensitivity_results.csv"
)

paired_df = pd.read_csv(
    "results/tables/all_sigma_paired_comparison.csv"
)

coverage = (
    sigma_df.groupby("sigma_scale")["covered"]
    .mean()
    .mul(100)
    .sort_index()
)

plt.figure(figsize=(8, 5))
plt.bar(
    [f"{x:.1f}x" for x in coverage.index],
    coverage.values,
)
plt.ylim(0, 110)
plt.xlabel("Gaussian Sigma Multiplier")
plt.ylabel("Coverage (%)")
plt.title("Gaussian Sigma Sensitivity - Coverage")
plt.tight_layout()
plt.savefig(
    output_dir / "sigma_coverage.png",
    dpi=300,
)
plt.close()

columns = [
    "Gaussian_0.5",
    "Baseline",
    "Gaussian_2.0",
    "Gaussian_1.0",
    "Gaussian_1.5",
]

averages = paired_df[columns].mean()

plt.figure(figsize=(9, 5))
plt.bar(averages.index, averages.values)
plt.ylabel("Mean Absolute Score Change")
plt.title("Paired Robustness Comparison")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(
    output_dir / "paired_robustness.png",
    dpi=300,
)
plt.close()

print("Grafikler olusturuldu:")
print(output_dir / "sigma_coverage.png")
print(output_dir / "paired_robustness.png")
