import math

from chest_pain import calculate_chest_pain_memberships

def gaussian(x, center, sigma):
    if sigma <= 0:
        raise ValueError("Sigma sifirdan buyuk olmali.")

    return math.exp(-0.5 * ((x - center) / sigma) ** 2)


def gaussian_plateau(x, left, right, sigma):
    if left <= x <= right:
        return 1.0

    if x < left:
        return gaussian(x, left, sigma)

    return gaussian(x, right, sigma)


def gaussian_left_shoulder(x, end, sigma):
    if x <= end:
        return 1.0

    return gaussian(x, end, sigma)


def gaussian_right_shoulder(x, start, sigma):
    if x >= start:
        return 1.0

    return gaussian(x, start, sigma)


def calculate_gaussian_blood_pressure(x, sigma_scale=1.0):
    return {
        "Normal": gaussian_plateau(x, 80, 120, 10 * sigma_scale),
        "High": gaussian_plateau(x, 140, 180, 10 * sigma_scale),
        "VeryHigh": gaussian_right_shoulder(x, 200, 10 * sigma_scale),
    }


def calculate_gaussian_age(x, sigma_scale=1.0):
    return {
        "Young": gaussian_plateau(x, 20, 40, 2.5 * sigma_scale),
        "Mid": gaussian_plateau(x, 45, 60, 2.5 * sigma_scale),
        "Old": gaussian_plateau(x, 65, 80, 2.5 * sigma_scale),
        "VeryOld": gaussian_right_shoulder(x, 85, 2.5 * sigma_scale),
    }


def calculate_gaussian_heart_rate(x, sigma_scale=1.0):
    return {
        "VeryHealthy": gaussian_plateau(x, 40, 60, 5 * sigma_scale),
        "Healthy": gaussian_plateau(x, 70, 90, 5 * sigma_scale),
        "High": gaussian_right_shoulder(x, 100, 5 * sigma_scale),
    }


def calculate_gaussian_ldl(x, sigma_scale=1.0):
    return {
        "VeryHealthy": gaussian_plateau(x, 40, 70, 5 * sigma_scale),
        "Healthy": gaussian_plateau(x, 80, 100, 5 * sigma_scale),
        "High": gaussian_plateau(x, 110, 130, 5 * sigma_scale),
        "VeryHigh": gaussian_plateau(x, 140, 160, 5 * sigma_scale),
        "ExtraHigh": gaussian_right_shoulder(x, 170, 5 * sigma_scale),
    }


def calculate_gaussian_hdl(x, sigma_scale=1.0):
    return {
        "Low": gaussian_plateau(x, 10, 40, 5 * sigma_scale),
        "Healthy": gaussian_right_shoulder(x, 50, 5 * sigma_scale),
    }


def calculate_gaussian_hba1c(x, sigma_scale=1.0):
    return {
        "VeryHealthy": gaussian_plateau(x, 3, 6.5, 0.25 * sigma_scale),
        "Healthy": gaussian_plateau(x, 7, 8.5, 0.25 * sigma_scale),
        "High": gaussian_right_shoulder(x, 9, 0.25 * sigma_scale),
    }


def fuzzify_patient_gaussian(patient, sigma_scale=1.0):
    if not math.isfinite(sigma_scale) or sigma_scale <= 0:
        raise ValueError("Sigma katsayisi pozitif ve sonlu olmali.")

    return {
        "ChestPain": calculate_chest_pain_memberships(
            patient["ChestPain"]
        ),
        "HbA1c": calculate_gaussian_hba1c(
            patient["HbA1c"], sigma_scale
        ),
        "HDL": calculate_gaussian_hdl(
            patient["HDL"], sigma_scale
        ),
        "LDL": calculate_gaussian_ldl(
            patient["LDL"], sigma_scale
        ),
        "HeartRate": calculate_gaussian_heart_rate(
            patient["HeartRate"], sigma_scale
        ),
        "Age": calculate_gaussian_age(
            patient["Age"], sigma_scale
        ),
        "BloodPressure": calculate_gaussian_blood_pressure(
            patient["BloodPressure"], sigma_scale
        ),
    }
