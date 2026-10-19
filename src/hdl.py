def low_hdl(x):
    if x < 10 or x > 50:
        return 0.0

    if x <= 40:
        return 1.0

    return (50 - x) / 10

def healthy_hdl(x):
    if x < 40:
        return 0.0

    if x >= 50:
        return 1.0

    return (x - 40) / 10

def calculate_hdl_memberships(x):
    return {
        "Low": low_hdl(x),
        "Healthy": healthy_hdl(x),
    }

if __name__ == "__main__":
    for value in [10, 30, 40, 45, 50, 60, 80]:
        print(value, calculate_hdl_memberships(value))
