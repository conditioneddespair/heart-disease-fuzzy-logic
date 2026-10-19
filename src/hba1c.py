from membership_functions import trapezoidal

def very_healthy_hba1c(x):
    if x < 3 or x > 7:
        return 0.0

    if x <= 6.5:
        return 1.0

    return (7 - x) / 0.5

def healthy_hba1c(x):
    return trapezoidal(x, 6.5, 7, 8.5, 9)

def high_hba1c(x):
    if x < 8.5:
        return 0.0

    if x >= 9:
        return 1.0

    return (x - 8.5) / 0.5

def calculate_hba1c_memberships(x):
    return {
        "VeryHealthy": very_healthy_hba1c(x),
        "Healthy": healthy_hba1c(x),
        "High": high_hba1c(x),
    }

if __name__ == "__main__":
    for value in [3, 6.5, 6.75, 7, 8.5, 8.75, 9, 10]:
        print(value, calculate_hba1c_memberships(value))
