CHEST_PAIN_CODES = {
    1: "NoPain",
    3: "NonAnginal",
    5: "Atypical",
    7: "Typical",
}

def calculate_chest_pain_memberships(value):
    if isinstance(value, int) and value in CHEST_PAIN_CODES:
        value = CHEST_PAIN_CODES[value]

    if value not in CHEST_PAIN_CODES.values():
        raise ValueError(f"Geçersiz ChestPain değeri: {value}")

    return {
        name: float(value == name)
        for name in CHEST_PAIN_CODES.values()
    }

if __name__ == "__main__":
    for value in [1, 3, 5, 7, "Atypical"]:
        print(value, calculate_chest_pain_memberships(value))
