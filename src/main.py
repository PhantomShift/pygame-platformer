import pygame
pygame.init()
import sys, LevelManager, UserInterface, pygame.event, pygame.time, pygame.display
from Vector2 import Vector2
from time import time
from InputHandler import InputHandler, InputObject


OBJECTS = []
DRAWABLES = []
player = None
def level_changed(new_level: LevelManager.LevelObject):
    global OBJECTS, DRAWABLES, player
    OBJECTS = [obj for obj in new_level.objects.keys()]
    DRAWABLES = [obj for obj in new_level.objects.keys()]
    print(OBJECTS)
    if player:
        player.connection_on_space.disconnect()
    player = new_level.player
    DRAWABLES.append(player)
LevelManager.on_level_changed.connect(level_changed)

test = UserInterface.TextBox(text="Start Game")
def start(inputted):
    DRAWABLES.clear()
    LevelManager.change_level(LevelManager.example_level.load())
test.mouse_clicked.connect(start)
DRAWABLES.append(test)

GRAVITY = Vector2(0, 100)
BG_COLOR = (0, 0, 0)
DISPLAYSURF = pygame.display.set_mode((800, 600))
DISPLAYSURF.fill(BG_COLOR)
print(DISPLAYSURF)
pygame.display.set_caption("Example")

class Timer:
    def __init__(self):
        self.currentTime = time()

    def update(self):
        now = time()
        dt = now - self.currentTime
        self.currentTime = now
        return dt


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
        (x,y) = pygame.mouse.get_pos()
        print(x,y)
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
