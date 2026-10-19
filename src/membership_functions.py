import math

def triangular(x, a, b, c):
    if a >= b or b >= c:
        raise ValueError("a < b < c olmalı.")

    if x <= a or x >= c:
        return 0.0

    if x == b:
        return 1.0

    if x < b:
        return (x - a) / (b - a)

    return (c - x) / (c - b)

def trapezoidal(x, a, b, c, d):
    if not (a <= b <= c <= d):
        raise ValueError("a <= b <= c <= d olmalı.")

    if a == d:
        raise ValueError("Yamuk sıfır genişlikte olamaz.")

    if x < a or x > d:
        return 0.0

    if b <= x <= c:
        return 1.0

    if a < x < b:
        return (x - a) / (b - a)

    if c < x < d:
        return (d - x) / (d - c)

    return 0.0

def gaussian(x, c, sigma):
    if sigma <= 0:
        raise ValueError("sigma pozitif olmalı.")

    return math.exp(-((x - c) ** 2) / (2 * sigma ** 2))

if __name__ == "__main__":
    print("125:", triangular(125, 80, 120, 140))
    print("120:", triangular(120, 80, 120, 140))
    print("140:", triangular(140, 80, 120, 140))

    print("\nYamuksal üyelik testleri:")

    print("90:", trapezoidal(90, 80, 100, 120, 140))
    print("110:", trapezoidal(110, 80, 100, 120, 140))
    print("130:", trapezoidal(130, 80, 100, 120, 140))
    print("145:", trapezoidal(145, 80, 100, 120, 140))

    print("\nGaussian üyelik testleri:")

    print("120:", gaussian(120, 120, 10))
    print("130:", gaussian(130, 120, 10))
    print("140:", gaussian(140, 120, 10))
