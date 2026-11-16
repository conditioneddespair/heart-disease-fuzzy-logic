from gaussian_fuzzy_system import evaluate_patient_gaussian


patients = {
    "Makaledeki ornek": {
        "ChestPain": 5,
        "HbA1c": 10,
        "HDL": 30,
        "LDL": 141,
        "HeartRate": 60,
        "Age": 59,
        "BloodPressure": 126,
    },
    "Yuksek risk profili": {
        "ChestPain": 7,
        "HbA1c": 10,
        "HDL": 25,
        "LDL": 185,
        "HeartRate": 110,
        "Age": 75,
        "BloodPressure": 210,
    },
}

sigma_scales = [0.5, 1.0, 1.5, 2.0]
minimum_strength = 0.001


for name, patient in patients.items():
    print(f"\n{name}")
    print("-" * 70)

    for scale in sigma_scales:
        try:
            result = evaluate_patient_gaussian(
                patient,
                sigma_scale=scale,
            )

            maximum_strength = max(
                result["aggregated"].values()
            )

            covered = maximum_strength > minimum_strength

            print(
                f"Sigma: {scale:.1f} | "
                f"Kural: {result['active_rule_count']:4d} | "
                f"Max: {maximum_strength:.6f} | "
                f"Kapsama: {covered} | "
                f"Skor: {result['final_score']:.4f}"
            )

        except ValueError as error:
            print(
                f"Sigma: {scale:.1f} | "
                f"Sonuc hesaplanamadi: {error}"
            )
