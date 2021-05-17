import sys
from time import time
import pygame
pygame.init()
import pygame.event
import pygame.time
import pygame.display
import level_manager
import user_interface
import game_objects
from vector2 import Vector2
from input_handler import InputHandler, InputObject


OBJECTS = []
DRAWABLES = []
player = None
def level_changed(new_level: level_manager.LevelObject):
    global OBJECTS, DRAWABLES, player
    OBJECTS = list(new_level.objects.keys())
    DRAWABLES = list(new_level.objects.keys())
    print(OBJECTS)
    if isinstance(player, game_objects.Player):
        player.connection_on_died.disconnect()
        player.connection_on_space.disconnect()
    player = new_level.player
    player.died.connect(level_manager.reset_level)
    DRAWABLES.append(player)
level_manager.on_level_changed.connect(level_changed)

test = user_interface.TextBox(text="Start Game", anchor_point=Vector2(0.5,0.5),
                            size=user_interface.UDim2.from_offset(200, 100),
                            pos=user_interface.UDim2.from_scale(0.5,0.5), font_size=24)
title = user_interface.TextBox(text="Pygame Platformer", anchor_point=Vector2(0.5, 0.5),
                            pos=user_interface.UDim2(Vector2(0.5, 0.5), Vector2(0, -100)),
                            size=user_interface.UDim2(),
                            color=(0, 0, 0), text_color=(255, 255, 255),
                            font_size=48)
def start(inputted):
    for drawable in DRAWABLES:
        drawable.visible = False
    start_connection.disconnect()
    DRAWABLES.clear()
    level_manager.change_level(level_manager.test_level)
start_connection = test.mouse_clicked.connect(start)
DRAWABLES.append(test)
DRAWABLES.append(title)

GRAVITY = Vector2(0, 100)
BG_COLOR = (0, 0, 0)
DISPLAYSURF = pygame.display.set_mode((800, 600))
DISPLAYSURF.fill(BG_COLOR)
print(DISPLAYSURF)
pygame.display.set_caption("Pygame Platformer")

class Timer:
    def __init__(self):
        self.current_time = time()

    def update(self) -> float:
        now = time()
        delta_time = now - self.current_time
        self.current_time = now
        return delta_time


timer = Timer()
Pygame_Clock = pygame.time.Clock()


def update(elapsedTime):
    if player:
        player.update(elapsedTime)

def draw():
    DISPLAYSURF.fill(BG_COLOR)
    for drawable in DRAWABLES:
        drawable.draw()


def test_input(inputted: InputObject):
    if inputted.input_type == pygame.MOUSEBUTTONDOWN:
        (pos_x, pos_y) = pygame.mouse.get_pos()
        print(pos_x, pos_y)
InputHandler.input_began.connect(test_input)
InputHandler.input_ended.connect(test_input)


# Game loop
LOOPING = True
while LOOPING:
    # update phase
    update(timer.update())
   
    # display phase
    draw()
    pygame.display.update()

    # event phase
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            LOOPING = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            InputHandler.parse_input(event.type, event.key, InputHandler.BEGAN)
        elif event.type == pygame.KEYUP:
            InputHandler.parse_input(event.type, event.key, InputHandler.ENDED)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            InputHandler.parse_input(event.type, event.button, InputHandler.BEGAN)
        elif event.type == pygame.MOUSEBUTTONUP:
            InputHandler.parse_input(event.type, event.button, InputHandler.BEGAN)
    Pygame_Clock.tick(60)
