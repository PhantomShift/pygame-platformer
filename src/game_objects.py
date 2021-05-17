import geometry
import pygame
from vector2 import Vector2, UP, DOWN, LEFT, RIGHT
from vector2 import ZERO as ZERO_VECTOR
from bindable_event import BindableEvent
from input_handler import InputHandler
from geometry import Ray_Result

GRAVITY = Vector2(0, 100)

class InteractiveRectangle(geometry.Rectangle):
    def __init__(self, x, y, w, h, color=None):
        super().__init__(x, y, w, h, color)
        self.on_touched = BindableEvent.new()
    
    def touch(self, player):
        self.on_touched.fire(player)

class Player:
    def __init__(self, object_list: dict, x=0, y=0, max_speed=200, acceleration=250, friction=400):
        self.pos = Vector2.new(x, y)
        self.vel = Vector2()
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.friction = friction
        self.rect = geometry.Rectangle(x, y, 40, 40, color=(230, 50, 50))
        self.jumped = False
        self.teleported = False
        self.alive = True
        self.object_list = object_list
        self.died = BindableEvent()

        self.connection_on_died = self.died.connect(self.on_died)
        self.connection_on_space = InputHandler.input_began.connect(self.on_space)

    def on_space(self, inputted):
        if inputted.key == pygame.K_SPACE:
            print("Space pressed")
            if not self.jumped:
                self.jumped = True
                self.vel = Vector2(self.vel.x, -100)
            elif not self.teleported:
                self.teleport()
    def on_died(self):
        self.alive = False
        print("died")

    def draw(self):
        self.rect.draw()
    
    def update(self, elapsedTime):
        if not self.alive:
            return
        pressed = pygame.key.get_pressed()
        input_vel = Vector2()
        if pressed[pygame.K_a]:
            input_vel += LEFT
        if pressed[pygame.K_d]:
            input_vel += RIGHT
        if input_vel != ZERO_VECTOR:
            vel = Vector2(self.vel.x, 0).move_toward(input_vel * self.max_speed, self.acceleration)
        else:
            vel = Vector2(self.vel.x, 0).move_toward(ZERO_VECTOR, self.friction)
        vel += GRAVITY
        self.vel += vel * elapsedTime
        self.rect.velocity = self.vel
        collisions = []
        for rectangle in self.object_list:
            result = geometry.dynamic_rect_vs_rect(self.rect, rectangle, elapsedTime)
            if isinstance(result, Ray_Result):
                collisions.append([rectangle, result.Time])
        collisions.sort(key=lambda s: s[1])
        for i in range(len(collisions)):
            rect = collisions[i][0]
            result = geometry.dynamic_rect_vs_rect(self.rect, rect, elapsedTime)
            if isinstance(result, Ray_Result):
                # print("Pos:", self.rect.position)
                # print("Size:", self.rect.size)
                # print("Target Pos:", rect.position)
                # print("Point:", result.Point)
                # print("Time:", result.Time)
                self.rect.velocity += result.Normal * Vector2(abs(self.rect.velocity.x), abs(self.rect.velocity.y)) * (1 - result.Time)
                if result.Normal == DOWN:
                    self.jumped = False
                    self.teleported = False
                if isinstance(rect, InteractiveRectangle):
                    rect.touch(self)
        self.vel = self.rect.velocity
        #print(self.vel)
        self.pos += self.vel * elapsedTime
        self.rect.position = self.pos
        if self.pos.y > pygame.display.get_surface().get_height():
            self.died.fire()

    def teleport(self):
        pressed = pygame.key.get_pressed()
        direction = ZERO_VECTOR
        if pressed[pygame.K_a]:
            direction += LEFT
        if pressed[pygame.K_d]:
            direction += RIGHT
        if pressed[pygame.K_s]:
            direction += UP
        if pressed[pygame.K_w]:
            direction += DOWN
        if direction == ZERO_VECTOR:
            return
        print("Teleported")
        direction = direction.unit * 80
        resolve = None
        for rect in self.object_list:
            if geometry.rect_vs_rect(self.rect.position + direction, self.rect.size, rect.position, rect.size):
                res = geometry.dynamic_rect_vs_rect(self.rect, rect, 1/60, direction=direction)
                if isinstance(res, Ray_Result):
                    if not resolve:
                        resolve = res
                    elif resolve.Time > res.Time:
                        resolve = res
                    #resolve = res if not resolve or resolve and resolve.Time < res.Time else resolve
                    #self.rect.position = res.Point - self.rect.size / 2
        if not resolve:
            self.rect.position += direction
        else:
            self.rect.position = resolve.Point - self.rect.size / 2
        self.pos = self.rect.position
        self.vel = self.vel * 0.5
        self.teleported = True
        self.jumped = False

class KillerRectangle(InteractiveRectangle):
    def __init__(self, x, y, w, h, color=(255, 0, 0)):
        super().__init__(x, y, w, h, color)
        
        self.on_touched.connect(self.touch)
    
    @staticmethod
    def touch(player: Player):
        player.died.fire()