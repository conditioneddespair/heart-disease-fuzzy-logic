from membership_functions import trapezoidal

def young_age(x):
    if x < 20 or x > 45:
        return 0.0

    if x <= 40:
        return 1.0

    return (45 - x) / 5


def mid_age(x):
    return trapezoidal(x, 40, 45, 60, 65)


def old_age(x):
    return trapezoidal(x, 60, 65, 80, 85)


def very_old_age(x):
    if x < 80:
        return 0.0

    if x >= 85:
        return 1.0

    return (x - 80) / 5


def calculate_age_memberships(x):
    return {
        "Young": young_age(x),
        "Mid": mid_age(x),
        "Old": old_age(x),
        "VeryOld": very_old_age(x),
    }


if __name__ == "__main__":
    for value in [40, 42.5, 45, 60, 62.5, 65, 80, 82.5, 85]:
        print(value, calculate_age_memberships(value))
