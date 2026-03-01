class LightSource:
    """Источник света с заданным положением, направлением и силой излучения"""

    def __init__(self, point, illumination, n):
        """
        Конструктор источника света.

        :param point: Точка расположения источника света.
        :param illumination: Сила излучения вдоль оси источника.
        :param n: Нормаль (ось) источника света — направление максимального излучения.
        """
        self.point = point
        self.illumination = illumination
        self.n = n
