from chest_pain import calculate_chest_pain_memberships
from hba1c import calculate_hba1c_memberships
from hdl import calculate_hdl_memberships
from ldl import calculate_ldl_memberships
from heart_rate import calculate_hr_memberships
from age import calculate_age_memberships
from blood_pressure import calculate_bp_memberships

def fuzzify_patient(patient):
    return {
        "ChestPain": calculate_chest_pain_memberships(patient["ChestPain"]),
        "HbA1c": calculate_hba1c_memberships(patient["HbA1c"]),
        "HDL": calculate_hdl_memberships(patient["HDL"]),
        "LDL": calculate_ldl_memberships(patient["LDL"]),
        "HeartRate": calculate_hr_memberships(patient["HeartRate"]),
        "Age": calculate_age_memberships(patient["Age"]),
        "BloodPressure": calculate_bp_memberships(patient["BloodPressure"]),
    }

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

    for variable, values in memberships.items():
        print(variable, values)
