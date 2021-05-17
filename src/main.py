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

class GameGlobals:
    def __init__(self):
        self.objects: list[object] = []
        self.drawables: list[object] = []
        self.player: game_objects.Player = None
    
    def level_changed(self, new_level: level_manager.LevelObject):
        self.objects = new_level.objects
        self.drawables = new_level.drawables
        print(self.objects)
        if isinstance(self.player, game_objects.Player):
            self.player.connection_on_died.disconnect()
            self.player.connection_on_space.disconnect()
        game_globals.player = new_level.player
        game_globals.player.died.connect(level_manager.reset_level)
        self.drawables.append(game_globals.player)
    
    def update(self, elapsedTime):
        if isinstance(self.player, game_objects.Player):
            self.player.update(elapsedTime)
    
    def draw(self):
        DISPLAYSURF.fill(BG_COLOR)
        for drawable in self.drawables:
            drawable.draw()
        

game_globals = GameGlobals()
level_manager.on_level_changed.connect(game_globals.level_changed)

test = user_interface.TextBox(text="Start Game", anchor_point=Vector2(0.5,0.5),
                            size=user_interface.UDim2.from_offset(200, 100),
                            pos=user_interface.UDim2.from_scale(0.5,0.5), font_size=24)
title = user_interface.TextBox(text="Pygame Platformer", anchor_point=Vector2(0.5, 0.5),
                            pos=user_interface.UDim2(Vector2(0.5, 0.5), Vector2(0, -100)),
                            size=user_interface.UDim2(),
                            color=(0, 0, 0), text_color=(255, 255, 255),
                            font_size=48)
def start(inputted):
    for drawable in game_globals.drawables:
        drawable.visible = False
    start_connection.disconnect()
    game_globals.drawables.clear()
    level_manager.change_level(level_manager.test_level)
start_connection = test.mouse_clicked.connect(start)
game_globals.drawables.append(test)
game_globals.drawables.append(title)


def test_input(inputted: InputObject):
    if inputted.input_type == pygame.MOUSEBUTTONDOWN:
        (pos_x, pos_y) = pygame.mouse.get_pos()
        print(pos_x, pos_y)
InputHandler.input_began.connect(test_input)
InputHandler.input_ended.connect(test_input)

def main():
    timer = Timer()
    pygame_clock = pygame.time.Clock()

    # Game loop
    looping = True
    while looping:
        # update phase
        game_globals.update(timer.update())

        # display phase
        game_globals.draw()
        pygame.display.update()

        # event phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
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
        pygame_clock.tick(60)

main()
