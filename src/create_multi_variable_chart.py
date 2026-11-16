from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv(
    "results/tables/multi_variable_summary.csv"
)

system_order = [
    "Baseline",
    "Gaussian_0.5",
    "Gaussian_1.0",
    "Gaussian_1.5",
    "Gaussian_2.0",
]

variable_order = [
    "BloodPressure",
    "LDL",
    "HDL",
    "HeartRate",
    "HbA1c",
    "Age",
]

pivot = df.pivot(
    index="variable",
    columns="system",
    values="mean_absolute_change",
)

pivot = pivot.reindex(
    index=variable_order,
    columns=system_order,
)

output_dir = Path("results/figures")
output_dir.mkdir(parents=True, exist_ok=True)

ax = pivot.plot(
    kind="bar",
    figsize=(12, 6),
    width=0.8,
)

ax.set_title("Multi-variable Robustness Comparison")
ax.set_xlabel("Input Variable")
ax.set_ylabel("Mean Absolute Score Change")
ax.legend(title="System")
ax.tick_params(axis="x", rotation=25)

plt.tight_layout()

output_path = output_dir / "multi_variable_robustness.png"

plt.savefig(output_path, dpi=300)
plt.close()

print("Grafik olusturuldu:", output_path)
