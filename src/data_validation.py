from pathlib import Path
import pandas as pd 

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "raw"

TRAIN_FILE = BASE_DIR / "data" / "processed" / "inference_rules_cleaned.csv"
TEST_FILE = DATA_DIR / "testing_data_set.csv"

print("Proje klasörü:", BASE_DIR)

for file_path in [TRAIN_FILE, TEST_FILE]:
   print("\nDosya:", file_path.name)
   print("Dosya mevcut mu?", file_path.exists())

   if file_path.exists():
    try:
        df = pd.read_csv(file_path)
        print("Satır sayısı:", len(df))
        print("Sütün sayısı:", len(df.columns))
        print("Sütun adları:", df.columns.tolist())
        print(df.head(3).to_string(index=False))
    except Exception as error:
            print("CSV okuma hatası:", error)