from point import Point


def loc_to_global(x, y, p0, p1, p2):
    v1 = p1 - p0
    v2 = p2 - p0

    # Нормализованные векторы
    e1 = v1.norm()
    e2 = v2.norm()

    return p0 + (e1 * x + e2 * y)


print("Start")
