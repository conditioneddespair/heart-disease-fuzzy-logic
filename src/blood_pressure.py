from membership_functions import trapezoidal

def normal_bp(x):
    if x < 80 or x > 140:
        return 0.0

    if x <= 120:
        return 1.0

    return (140 - x) / 20


def high_bp(x):
    return trapezoidal(x, 120, 140, 180, 200)


def very_high_bp(x):
    if x < 180:
        return 0.0

    if x >= 200:
        return 1.0

    return (x - 180) / 20


def calculate_bp_memberships(x):
    return {
        "Normal": normal_bp(x),
        "High": high_bp(x),
        "VeryHigh": very_high_bp(x),
    }


if __name__ == "__main__":
    for value in [120, 130, 140, 180, 190, 200]:
        print(value, calculate_bp_memberships(value))
