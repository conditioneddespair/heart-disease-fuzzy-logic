from membership_functions import trapezoidal

def very_healthy_ldl(x):
    if x < 40 or x > 80:
        return 0.0

    if x <= 70:
        return 1.0

    return (80 - x) / 10

def healthy_ldl(x):
    return trapezoidal(x, 70, 80, 100, 110)

def high_ldl(x):
    return trapezoidal(x, 100, 110, 130, 140)

def very_high_ldl(x):
    return trapezoidal(x, 130, 140, 160, 170)

def extra_high_ldl(x):
    if x < 160:
        return 0.0

    if x >= 170:
        return 1.0

    return (x - 160) / 10

def calculate_ldl_memberships(x):
    return {
        "VeryHealthy": very_healthy_ldl(x),
        "Healthy": healthy_ldl(x),
        "High": high_ldl(x),
        "VeryHigh": very_high_ldl(x),
        "ExtraHigh": extra_high_ldl(x),
    }

if __name__ == "__main__":
    for value in [70, 75, 80, 105, 110, 135, 140, 165, 170, 190]:
        print(value, calculate_ldl_memberships(value))
