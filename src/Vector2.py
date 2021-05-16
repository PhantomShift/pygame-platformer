import math
from math import sqrt
from numpy import sign

def vector_only(f):
    def wrapper(self, other, *args):
        if type(self) != Vector2 or type(other) != Vector2:
            raise TypeError("Argument must be another Vector2")
        return f(self, other, *args)
    return wrapper


class Vector2:
    def __init__(self, x=0, y=0):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Vector2s must be constructed with numbers.")
        self.x = x
        self.y = y
        self.X = x
        self.Y = y
        self.magnitude = sqrt(x*x + y * y)
        self.Magnitude = self.magnitude
        self.unit = self
        if self.magnitude > 0 and not math.isclose(self.magnitude, 1):
            self.unit = Vector2.new(x / self.magnitude, y / self.magnitude)
        self.Unit = self.unit

    def __hash__(self) -> int:
        return hash(("Vector2", self.x, self.y))

    def __setattr__(self, attribute, value):
        raise TypeError("Vector2s are immutable")

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Vector2s can only be added with other Vector2s")
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if type(self) != type(other):
            raise TypeError("Vector2s can only be subtracted by other Vector2s")
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if (type(self) == int or type(self) == float) and type(other) == Vector2:
            return Vector2(self * other.x, self * other.y)
        elif type(self) == Vector2 and (type(other) == int or type(other) == float):
            return Vector2(self.x * other, self.y * other)
        elif type(self) == type(other):
            return Vector2(self.x * other.x, self.y * other.y)
        raise TypeError("Vector2s must be multiplied with other Vector2s or a number")

    def __truediv__(self, other):
        if other == 0:
            return Vector2(math.inf, math.inf)
        if type(other) == int or type(other) == float:
            return Vector2(self.x / other, self.y / other)
        elif type(other) == Vector2:
            #print(f"self: {self}, other: {other}")
            return Vector2(self.x / other.x, self.y / other.y)
        raise ValueError("Vector2s must be divided by another Vector2 or a number")

    def __floordiv__(self, other):
        if other == 0:
            return Vector2(math.inf, math.inf)
        if type(other) == int or type(other) == float:
            return Vector2(self.x // other, self.y // 0)
        elif type(other) == Vector2:
            return Vector2(self.x // other.x, self.y // other.y)
        raise ValueError("Vector2s must be divided by another Vector2 or a number")

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def unpack(self):
        return (self.x, self.y)

    def rotate(self, angle, degrees=False):
        if degrees:
            angle = math.cos(angle)
        return Vector2.from_angle(math.atan2(self.y, self.x) + angle, self.magnitude)

    def move_toward(self, destination: Vector2, delta) -> Vector2:
        """inspired by Godot Vector2's move_toward method"""
        if destination == self:
            return self
        return self + (destination - self).unit * delta

    @vector_only
    def distance_to(self, other):
        return (self - other).magnitude

    @vector_only
    def dot(self, other):
        return self.x * other.x + self.y * other.y

    @vector_only
    def reflect(self, normal):
        return self - 2 * self.dot(normal) * normal

    @vector_only
    def angle_between(self, other, degrees=False):
        return math.degrees(math.acos(self.unit.dot(other.unit))) if degrees else math.acos(self.unit.dot(other.unit))

    @vector_only
    def project(self, other):
        return self.dot(other.unit) * other.unit

    @vector_only
    def lerp(self, other, a):
        if type(a) != int and type(a) != float:
            raise TypeError("a must be a number")
        a = max(0, min(a, 1))
        return self.x * (1 - a) + other * a

    @staticmethod
    def new(x=0, y=0):
        return Vector2(x, y)

    @staticmethod
    def from_angle(angle=0, magnitude=1, degrees=False):
        if degrees:
            angle = math.radians(angle)
        return Vector2(math.cos(angle) * magnitude, math.sin(angle) * magnitude)

ZERO = Vector2()
UP = Vector2(0, 1)
DOWN = Vector2(0, -1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
new = Vector2.new
from_angle = Vector2.from_angle
