from math import sqrt


class Vector:
    def __init__(self, x: float, y: float, z: float):
        """Конструктор вектора"""
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        """Сложение векторов"""
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    def __sub__(self, other):
        """Вычитание векторов"""
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    def __mul__(self, number: float):
        """Умножение вектора на число"""
        x = self.x * number
        y = self.y * number
        z = self.z * number
        return Vector(x, y, z)

    def __rmul__(self, number: float):
        """Умножение числа на вектор"""
        return self * number

    def __truediv__(self, number: float):
        """Деление вектора на число"""
        x = self.x / number
        y = self.y / number
        z = self.z / number
        return Vector(x, y, z)

    def __eq__(self, other):
        """Проверка эквивалентности векторов"""
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        """Представление в виде строки"""
        return f"Vector({self.x}, {self.y}, {self.z})"

    def vec_mul(self, other):
        """Векторное умножение"""
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    def dot(self, other):
        """Скалярное умножение векторов"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def length(self):
        """Длина вектора (норма вектора)"""
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        """Нормализованный вектор"""
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / length
