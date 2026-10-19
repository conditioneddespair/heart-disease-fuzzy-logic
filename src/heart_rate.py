from membership_functions import trapezoidal

def very_healthy_hr(x):
    if x < 40 or x > 70:
        return 0.0

    if x <= 60:
        return 1.0

    return (70 - x) / 10


def healthy_hr(x):
    return trapezoidal(x, 60, 70, 90, 100)


def high_hr(x):
    if x < 90:
        return 0.0

    if x >= 100:
        return 1.0

    return (x - 90) / 10


def calculate_hr_memberships(x):
    return {
        "VeryHealthy": very_healthy_hr(x),
        "Healthy": healthy_hr(x),
        "High": high_hr(x),
    }


if __name__ == "__main__":
    for value in [60, 65, 70, 80, 90, 95, 100, 120]:
        print(value, calculate_hr_memberships(value))
