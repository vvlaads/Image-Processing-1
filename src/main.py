import os
import json
from math import pi
from light_source import LightSource
from vector import Vector


def get_intensity(light, point):
    """Сила излучения от источника света, до выбранной точки (в глобальных координатах)"""
    o = light.n
    s = point - light.point  # вектор от источника до точки
    cos_theta = max(0.0, s.normalize().dot(o))
    return light.intensity * cos_theta


def get_illuminance(light, point, n):
    """Освещенность выбранной точки (в глобальных координатах) от источника света"""
    i = get_intensity(light, point)

    s = light.point - point  # вектор от точки до источника
    r = s.length()  # расстояние от точки до источника
    cos_alpha = abs(s.normalize().dot(n))
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


def get_brightness(lights, point, n, v, color, k_d, k_s, k_e):
    """Яркость точки"""
    s = 0
    for light in lights:
        s += get_illuminance(light, point, n).dot(brdf(color, k_d, k_s, k_e, v, n, light, point))
    return (1 / pi) * s


def brdf(color, k_d, k_s, k_e, v, n, light, point):
    """Двунаправленная функция отражения (BRDF)"""
    s = point - light.point  # вектор от источника до точки
    return color * (k_d + k_s * (get_h(v, s).dot(n)) ** k_e)


def get_h(v, s):
    """Средний вектор (между наблюдателем и источником света)"""
    return (v + s).normalize()


def input_vec(name, min_value=None):
    """Ввод вектора вида (x, y, z)"""
    while True:
        try:
            x, y, z = map(float, input(f"{name}: ").split())
            if min_value is not None and (x < min_value or y < min_value or z < min_value):
                print(f"Значения должны быть не меньше {min_value}")
            else:
                return Vector(x, y, z)
        except ValueError:
            print("Ошибка ввода")


def input_float(name, min_value=None, max_value=None):
    """Ввод вещественного числа"""
    while True:
        try:
            num = float(input(f"{name}: "))
            if min_value is not None and num < min_value:
                print(f"Значение должно быть не меньше {min_value}")
            elif max_value is not None and num > max_value:
                print(f"Значение должно быть не больше {max_value}")
            else:
                return num
        except ValueError:
            print("Ошибка ввода")


def input_int(name, min_value=None, max_value=None):
    """Ввод целого числа"""
    while True:
        try:
            num = int(input(f"{name}: "))
            if min_value is not None and num < min_value:
                print(f"Значение должно быть не меньше {min_value}")
            elif max_value is not None and num > max_value:
                print(f"Значение должно быть не больше {max_value}")
            else:
                return num
        except ValueError:
            print("Ошибка ввода")


def input_array(count, name):
    """Ввод набора чисел"""
    arr = []
    for i in range(count):
        number = input_float(f"{name}{i + 1}")
        arr.append(number)
    return arr


def vec_from_dict(d):
    """Создать Vector из словаря {x, y, z}"""
    return Vector(d["x"], d["y"], d["z"])


def print_table_matrix(xs, ys, values, fmt="{:6.2f}", title=None):
    """
    xs - список значений по столбцам (X)
    ys - список значений по строкам (Y)
    values - двумерный массив размером len(ys) x len(xs)
             values[i][j] соответствует ys[i], xs[j]
    fmt - формат ячейки для чисел
    title - заголовок таблицы (опционально)
    """
    if title:
        print(title)
    # Заголовок
    header = "Y\\X | " + " | ".join(f"{x:6.2f}" for x in xs)
    print(header)
    print("-" * len(header))

    for y_idx, y in enumerate(ys):
        row_values = []
        for x_idx in range(len(xs)):
            val = values[y_idx][x_idx]
            if isinstance(val, Vector):
                row_values.append(f"({val.x:.2f},{val.y:.2f},{val.z:.2f})")
            else:
                row_values.append(fmt.format(val))
        print(f"{y:6.2f} | " + " | ".join(row_values))
    print()


# Папка с ресурсами
RESOURCES_DIR = "../resources"

print("Выберите тип ввода:")
print("1. Через файл")
print("2. Ввести вручную")
option = input_int("Тип ввода", min_value=1, max_value=2)

# --- Чтение из файла ---
if option == 1:
    filename = input("Введите имя файла (например, data.json): ").strip()
    path = os.path.join(RESOURCES_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл {filename} не найден в папке {RESOURCES_DIR}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Источники света
    i1 = vec_from_dict(data["i1"])
    i2 = vec_from_dict(data["i2"])
    o1 = vec_from_dict(data["o1"])
    o2 = vec_from_dict(data["o2"])
    pl1 = vec_from_dict(data["pl1"])
    pl2 = vec_from_dict(data["pl2"])

    light1 = LightSource(pl1, i1, o1)
    light2 = LightSource(pl2, i2, o2)
    lights = [light1, light2]

    # Треугольник
    p0 = vec_from_dict(data["p0"])
    p1 = vec_from_dict(data["p1"])
    p2 = vec_from_dict(data["p2"])

    # Проверка на совпадение точек
    while p0 == p1 or p0 == p2 or p1 == p2:
        raise ValueError("Точки треугольника не должны совпадать")

    # Координаты точек для расчета
    xs = data["xs"]
    ys = data["ys"]

    # Вектор наблюдателя и цвет
    v = vec_from_dict(data["v"])
    color = vec_from_dict(data["k"])

    # Параметры BRDF
    k_d = data["k_d"]
    k_s = data["k_s"]
    k_e = data["k_e"]

# --- Ввод вручную ---
else:
    i1 = input_vec("I_O1 (RGB)", min_value=0)
    i2 = input_vec("I_O2 (RGB)", min_value=0)

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
    while p0 == p1 or p0 == p2 or p1 == p2:
        print("Точки треугольника не должны совпадать")
        p0 = input_vec("P0")
        p1 = input_vec("P1")
        p2 = input_vec("P2")

    xs = input_array(5, "X")
    ys = input_array(5, "Y")

    v = input_vec("V")
    color = input_vec("K (RGB)", min_value=0)

    k_d = input_float("k_d", min_value=0, max_value=1)
    k_s = input_float("k_s", min_value=0, max_value=1)
    k_e = input_float("k_e", min_value=0)

# === Инициализация массивов ===
illuminance1 = [[0.0 for _ in range(len(xs))] for _ in range(len(ys))]
illuminance2 = [[0.0 for _ in range(len(xs))] for _ in range(len(ys))]
brightness = [[0.0 for _ in range(len(xs))] for _ in range(len(ys))]

# === Вычисление ===
n = get_surface_norm(p0, p1, p2)
for x_idx in range(len(xs)):
    for y_idx in range(len(ys)):
        x = xs[x_idx]
        y = ys[y_idx]
        point = loc_to_global(x, y, p0, p1, p2)
        illuminance1[y_idx][x_idx] = get_illuminance(light1, point, n)
        illuminance2[y_idx][x_idx] = get_illuminance(light2, point, n)
        brightness[y_idx][x_idx] = get_brightness(lights, point, n, v, color, k_d, k_s, k_e)

print_table_matrix(xs, ys, illuminance1, title="E1")
print_table_matrix(xs, ys, illuminance2, title="E2")
print_table_matrix(xs, ys, brightness, title="L")
