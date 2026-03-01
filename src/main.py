from math import pi
from light_source import LightSource
from pair import Pair
from vector import Vector


def get_intensity(light, point):
    """Сила излучения от источника света, до выбранной точки (в глобальных координатах)"""
    n = light.n.normalize()
    s = point - light.point  # вектор от источника до точки
    cos_theta = max(0.0, s.normalize().dot(n))
    return light.intensity * cos_theta


def get_illuminance(light, point, p0, p1, p2):
    """Освещенность выбранной точки (в глобальных координатах) от источника света"""
    i = get_intensity(light, point)

    s = point - light.point  # вектор от источника до точки
    r = s.length()  # расстояние от точки до источника

    n = get_surface_norm(p0, p1, p2)  # нормаль поверхности

    cos_alpha = max(0.0, s.normalize().dot(n))

    return (i * cos_alpha) / (r * r)


def loc_to_global(x, y, p0, p1, p2):
    """Перевести локальные координаты в глобальные"""
    v1 = p1 - p0
    v2 = p2 - p0

    # Нормализованные векторы
    e1 = v1.normalize()
    e2 = v2.normalize()

    return p0 + (e1 * x + e2 * y)


def get_surface_norm(p0, p1, p2):
    """Нормаль к поверхности, заданной тремя точками"""
    v1 = p1 - p0
    v2 = p2 - p0

    numerator = v2.vec_mul(v1)
    denominator = v1.vec_mul(v2).length()
    return numerator / denominator


def brightness(lights, point, p0, p1, p2, v, color, k_d, k_s, k_e):
    """Яркость точки"""
    s = 0
    n = get_surface_norm(p0, p1, p2)
    for light in lights:
        s += get_illuminance(light, point, p0, p1, p2) * brdf(color, k_d, k_s, k_e, v, n, light, point)
    return (1 / pi) * s


def brdf(color, k_d, k_s, k_e, v, n, light, point):
    """Двунаправленная функция отражения (BRDF)"""
    s = point - light.point  # вектор от источника до точки
    return color * (k_d + k_s * (get_h(v, s).dot(n)) ** k_e)


def get_h(v, s):
    """Средний вектор (между наблюдателем и источником света)"""
    return (v + s).normalize()


def input_vec(name):
    """Ввод вектора вида (x, y, z)"""
    while True:
        try:
            x, y, z = map(float, input(f"{name}: ").split())
            return Vector(x, y, z)
        except ValueError:
            print("Ошибка ввода")


def input_float(name, min_value=None, max_value=None):
    """Ввод вещественного числа"""
    while True:
        try:
            x = float(input(f"{name}: "))
            if min_value is not None and x < min_value:
                print(f"Значение должно быть не меньше {min_value}")
            elif max_value is not None and x > max_value:
                print(f"Значение должно быть не больше {max_value}")
            else:
                return x
        except ValueError:
            print("Ошибка ввода")


def input_dots(count):
    """Ввод набора точек вида (x, y)"""
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

k_d = input_float("k_d", min_value=0, max_value=1)
k_s = input_float("k_s", min_value=0, max_value=1)
k_e = input_float("k_e", min_value=0, max_value=1)
