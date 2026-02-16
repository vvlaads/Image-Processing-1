from math import pi
from light_source import LightSource
from pair import Pair
from vector import Vector


def get_intensity(light, Vector):
    o = light.n.normalize()
    s = (Vector - light.Vector).normalize()
    cos_theta = max(0.0, o * s)
    return light.intensity * cos_theta


def illumination(intensity, cos_alpha, r):
    return (intensity * cos_alpha) / (r * r)


def loc_to_global(x, y, p0, p1, p2):
    v1 = p1 - p0
    v2 = p2 - p0

    # Нормализованные векторы
    e1 = v1.normalize()
    e2 = v2.normalize()

    return p0 + (e1 * x + e2 * y)


def get_normal(p0, p1, p2):
    v1 = p1 - p0
    v2 = p2 - p0

    numerator = v2.vec_mul(v1)
    denominator = v1.vec_mul(v2).length()
    return numerator / denominator


def brightness(Vector, v, light_sources):
    s = 0
    for light in light_sources:
        s += illumination(Vector.intensity, light.intensity, v)
    return (1 / pi) * s


def brdf(color, k_d, k_s, k_e, h, n):
    return color * (k_d + k_s * (h * n) ** k_e)


def get_s(light, Vector):
    return Vector - light


def get_h(v, s):
    return (v + s).normalize()


def input_vec(name):
    while True:
        try:
            x, y, z = map(float, input(f"{name}: ").split())
            return Vector(x, y, z)
        except ValueError:
            print("Ошибка ввода")


def input_float(name):
    while True:
        try:
            x = float(input(f"{name}: "))
            return x
        except ValueError:
            print("Ошибка ввода")


def input_dots(count):
    pairs = []
    for i in range(count):
        while True:
            try:
                x, y = map(float, input(f"x_{i + 1}, y_{i + 1}: ").split())
                pairs.append(Pair(x, y))
                break
            except ValueError:
                print("Ошибка ввода")
    return pairs


i1 = input_vec("I_O1 (RGB)")
i2 = input_vec("I_O2 (RGB)")

o1 = input_vec("O1")
o2 = input_vec("O2")

pl1 = input_vec("PL1")
pl2 = input_vec("PL2")

light1 = LightSource(pl1, i1, o1)
light2 = LightSource(pl2, i2, o2)
lights = [light1, light2]

p0 = input_vec("P0")
p1 = input_vec("P1")
p2 = input_vec("P2")

dots = input_dots(5)

v = input_vec("V")
color = input_vec("K (RGB)")

k_d = input_float("k_d")
k_s = input_float("k_s")
k_e = input_float("k_e")
