from math import sqrt


class Point:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Point(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Point(x, y, z)

    def __mul__(self, number: float):
        x = self.x * number
        y = self.y * number
        z = self.z * number
        return Point(x, y, z)

    def __rmul__(self, number: float):
        return self * number

    def __truediv__(self, number: float):
        x = self.x / number
        y = self.y / number
        z = self.z / number
        return Point(x, y, z)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def norm(self):
        length = self.length()
        if length == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / length
