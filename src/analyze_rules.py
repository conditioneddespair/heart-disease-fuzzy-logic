from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

train_path = BASE_DIR / "data" / "processed" / "inference_rules_cleaned.csv"
test_path = BASE_DIR / "data" / "raw" / "testing_data_set.csv"

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

condition_col = "Antecedent (If Condition)"
output_col = "Consequent (Output)"

print("KURAL DOSYASI:")
print("Toplam kayıt:", len(train_df))

print("\nEksik çıktı etiketi:")
print(train_df[output_col].isna().sum())

print("\nÇıktı sınıfları:")
print(train_df[output_col].value_counts(dropna=False))

print("\nTekrarlanan giriş kombinasyonları:")
print(train_df[condition_col].duplicated().sum())

print("\nTEST DOSYASI:")
print("Toplam kayıt:", len(test_df))

print("\nÇıktı sınıfları:")
print(test_df[output_col].value_counts(dropna=False))

print("\nTekrarlanan giriş kombinasyonları:")
print(test_df[condition_col].duplicated().sum())


print("\nTEST VERİSİNDE ETİKET ÇELİŞKİLERİ:")


label_counts = (
    test_df.groupby(condition_col)[output_col]
    .nunique()
)


conflicting_conditions = label_counts[label_counts > 1]

print("Çelişkili giriş kombinasyonu sayısı:",
      len(conflicting_conditions))


conflicting_rows = test_df[
    test_df[condition_col].isin(conflicting_conditions.index)
]

print("Çelişkili kombinasyonlara ait toplam kayıt:",
      len(conflicting_rows))


RESULTS_DIR = BASE_DIR / "results" / "tables"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

output_file = RESULTS_DIR / "conflicting_test_rows.csv"

conflicting_rows.to_csv(output_file, index=False)

print("Çelişki raporu:", output_file)


maximum_correct = (
    test_df.groupby(condition_col)[output_col]
    .value_counts()
    .groupby(level=0)
    .max()
    .sum()
)

upper_bound = maximum_correct / len(test_df) * 100

print("Teorik maksimum doğru sayısı:", maximum_correct)
print(f"Teorik maksimum accuracy: %{upper_bound:.2f}")
