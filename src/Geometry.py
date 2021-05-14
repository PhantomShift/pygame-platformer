from numpy import sign
import pygame
import math
from Vector2 import Vector2, UP, DOWN, LEFT, RIGHT
from numbers import Number
from typing import Union
from pygame import Rect

def clamp(number, minimum, maximum) -> Number:
    return max(minimum, min(number, maximum))

Objects = {}
ID = 0

class Circle:
    def __init__(self, x, y, radius):
        self.position = Vector2(x, y)
        self.radius = radius
    def __str__(self):
        return f"Circle Position: {self.position}, Radius: {self.radius}"
class Rectangle:
    def __init__(self, x, y, w, h, color=(255,255,255)):
        self.position = Vector2(x, y)
        self.size = Vector2(w, h)
        self.velocity = Vector2()
        self.color = color
        global ID
        self.ID = ID
        ID += 1
    def __str__(self):
        return f"Rectangle Position: {self.position}, Size: {self.size}"
    def __hash__(self) -> int:
        return hash(("Rectangle", ID, ID - 1))
    
    def as_tuple(self):
        return (self.position.x, self.position.y, self.size.x, self.size.y)
    def pygame_rect(self):
        """returns pygame.Rect representation of the rectangle object"""
        return Rect(self.as_tuple())
    def draw(self):
        pygame.draw.rect(pygame.display.get_surface(), self.color, self.pygame_rect())
    def destroy(self):
        del Objects[self]

    @staticmethod
    def from_vectors(pos: Vector2, size: Vector2):
        return Rectangle(pos.x, pos.y, size.x, size.y)

def point_vs_rect(point: Vector2, rect_pos: Vector2, rect_size:Vector2) -> bool:
    return True if point.X >= rect_pos.X and point.Y >= rect_pos.Y and point.X < rect_pos.X + rect_size.X and point.Y < rect_pos.Y + rect_size.Y else False

def rect_vs_rect(rect_pos1: Vector2, rect_size1: Vector2, rect_pos2: Vector2, rect_size2: Vector2) -> bool:
    return True if (rect_pos1.X < rect_pos2.X + rect_size2.X and rect_pos1.X + rect_size1.X > rect_pos2.X and
                    rect_pos1.Y < rect_pos2.Y + rect_size2.Y and rect_pos1.Y + rect_size1.Y > rect_pos2.Y) else False

class Ray_Result:
    def __init__(self, Point, Normal, Time):
        self.Point = Point
        self.Normal = Normal
        self.Time = Time
    def __repr__(self):
        return f"Ray_Result (Normal: {self.Normal}, Point: {self.Point}, Time: {self.Time}"

def ray_vs_rect(origin: Vector2, direction: Vector2, target: Rectangle) -> Union[Ray_Result, bool]:
    if direction.x == 0:
        t_near = Vector2(int(sign(target.position.x - origin.x))*math.inf, (target.position.y - origin.y) / direction.y)
        t_far = Vector2(int(sign(target.position.x + target.size.x - origin.x))*math.inf, (target.position.y + target.size.y - origin.y) / direction.y)
    elif direction.y == 0:
        t_near = Vector2((target.position.x - origin.x) / direction.x, int(sign(target.position.y - origin.y))*math.inf)
        t_far = Vector2((target.position.x + target.size.x - origin.x) / direction.x, int(sign(target.position.y + target.size.y - origin.y))*math.inf)
    else:
        t_near = (target.position - origin) / direction
        t_far = (target.position + target.size - origin) / direction
    if t_near.x > t_far.x:
        t_near, t_far = Vector2(t_far.x, t_near.y), Vector2(t_near.x, t_far.y)
    if t_near.y > t_far.y:
        t_near, t_far = Vector2(t_near.x, t_far.y), Vector2(t_far.x, t_near.y)
    
    if t_near.x > t_far.y or t_near.y > t_far.x:
        return False
    
    t_hit_near = max(t_near.x, t_near.y)
    t_hit_far = min(t_far.x, t_far.y)

    # if t_hit_near < -10:
    #     print("origin:", origin)
    #     print("direction:", direction)
    #     print("t_near", t_near)
    #     print("t_hit_near:", t_hit_near)

    if t_hit_far < 0 or t_hit_near < -3: # this seems to fix collision for now?
        return False
    # if t_hit_near < -1:
    #     print("origin:", origin)
    #     print("direction:", direction)
    #     print("t_near", t_near)
    #     print("t_hit_near:", t_hit_near)

    point = origin + direction * t_hit_near
    if t_near.x > t_near.y:
        if direction.x < 0:
            normal = RIGHT
        else:
            normal = LEFT
    elif t_near.x < t_near.y:
        if direction.y < 0:
            normal = UP
        else:
            normal = DOWN
    else:
        normal = Vector2(- sign(direction.x), - sign(direction.y)).Unit
    #print("normal", normal)
    return Ray_Result(point, normal, t_hit_near)

def dynamic_rect_vs_rect(rect: Rectangle, target: Rectangle, elapsedTime: float, direction: Vector2 = None) -> Union[Ray_Result, bool]:
    if not direction and rect.velocity.x == 0 and rect.velocity.y == 0:
        return False
    vector = direction if direction else rect.velocity * elapsedTime
    expanded_target = Rectangle.from_vectors(
        target.position - rect.size / 2,
        rect.size + target.size
    )
    #expanded_target.color = pygame.Color(120, 120, 120, 120)
    result = ray_vs_rect(rect.position + rect.size / 2, vector, expanded_target)
    if isinstance(result, Ray_Result) and result.Time <= 1:
        return result
    return False