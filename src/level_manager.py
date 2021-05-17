import sys
import pygame
from pygame import Color, error, event
import game_objects
import geometry
from vector2 import Vector2
from bindable_event import BindableEvent
from game_objects import Player
from user_interface import TextBox, Frame, UDim2

CURRENT_LEVEL = None
on_level_changed = BindableEvent.new()
class LevelObject:
    def __init__(self, player: Player, objects, drawables):
        self.player = player
        self.objects = list(objects)
        self.drawables = list(drawables)
        for drawable in self.drawables:
            if isinstance(drawable, TextBox):
                drawable.visible = True

class Level:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.objects = []
        self.drawables = []
    
    def load(self) -> LevelObject:
        return LevelObject(Player(self.objects, self.start_x, self.start_y), self.objects, self.drawables)

    def add_object(self, obj):
        self.objects.append(obj)
        self.drawables.append(obj)

    def add_rect(self, x, y, w, h):
        rect = geometry.Rectangle(x, y, w, h)
        self.objects.append(rect)
        self.drawables.append(rect)
    
    def add_drawable(self, drawable):
        self.drawables.append(drawable)

def change_level(new_level: Level):
    #print("Hey level should be changed?")
    global CURRENT_LEVEL
    if CURRENT_LEVEL:
        for drawable in CURRENT_LEVEL.drawables:
            if isinstance(drawable, TextBox):
                drawable.visible = False
    CURRENT_LEVEL = new_level
    on_level_changed.fire(CURRENT_LEVEL.load())

def reset_level():
    global CURRENT_LEVEL
    if not CURRENT_LEVEL:
        raise error("CURRENT_LEVEL not initialized when attempted to reset level")
    change_level(CURRENT_LEVEL)

example_level = Level(50, 50)
def construct_platform(x, y, w, h):
    example_level.add_object(geometry.Rectangle(x, y, w, h))
construct_platform(0, 200, 200, 20)
construct_platform(100, 220, 200, 20)
construct_platform(600, 220, 200, 20)
construct_platform(640, 300, 200, 20)
construct_platform(640, 240, 20, 80)
construct_platform(400, 50, 20, 200)

BLUE = (50, 40, 240)

goal = game_objects.InteractiveRectangle(760, 260, 40, 40, color=BLUE)
def goal_touched(player):
    #print(test_level)
    change_level(end_level)
goal.on_touched.connect(goal_touched)
example_level.add_object(goal)

test_level = Level(50, 520)
base = geometry.Rectangle(0, 580, 800, 120)
goal2 = game_objects.InteractiveRectangle(760, 540, 40, 40, color=BLUE)
def goal_touched2(player):
    change_level(level2)
test_level.add_object(base)
test_level.add_object(goal2)
goal2.on_touched.connect(goal_touched2)
level1_text = TextBox(size=UDim2(), pos=UDim2.from_scale(0.5, 0.5), anchor_point=Vector2(0.5, 0.5),
                    text_color=(255, 255, 255), font_size=24, text="Press A and D to move")
test_level.add_drawable(level1_text)

level2 = Level(50, 520)
level2.add_object(geometry.Rectangle(0, 580, 800, 120))
level2.add_object(game_objects.KillerRectangle(400, 540, 20, 60))
level2_goal = game_objects.InteractiveRectangle(760, 540, 40, 40, color=BLUE)
level2.add_object(level2_goal)
def level2_goal_touched(player):
    change_level(level3)
level2_goal.on_touched.connect(level2_goal_touched)
level2_text = TextBox(size=UDim2(), pos=UDim2.from_scale(0.5, 0.5), anchor_point=Vector2(0.5, 0.5),
                    text_color=(255, 255, 255), font_size=24, text="Press Space to jump")
level2.add_drawable(level2_text)

level3 = Level(50, 520)
level3.add_object(geometry.Rectangle(0, 580, 800, 120))
level3.add_object(geometry.Rectangle(400, 0, 20, 800))
level3_goal = game_objects.InteractiveRectangle(760, 540, 40, 40, color=BLUE)
level3.add_object(level3_goal)
def level3_goal_touched(player):
    change_level(level4)
level3_goal.on_touched.connect(level3_goal_touched)
level3_text = TextBox(size=UDim2(), pos=UDim2.from_offset(185, 100), text_color=(255, 255, 255), 
                    font_size=24, text="Press space in the air to teleport!")
level3.add_drawable(level3_text)

level4 = Level(50, 520)
level4.add_rect(0, 580, 800, 120)
level4.add_rect(700, 480, 100, 20)
level4.add_rect(700, 400, 100, 20)
level4.add_rect(700, 320, 100, 20)
level4.add_rect(700, 240, 100, 20)
level4_goal = game_objects.InteractiveRectangle(760, 200, 40, 40, color=BLUE)
level4.add_object(level4_goal)
def level4_goal_touched(player):
    change_level(level5)
level4_goal.on_touched.connect(level4_goal_touched)
level4_text = TextBox(size=UDim2(), pos=UDim2(Vector2(0.5, 0), Vector2(0, 40)), anchor_point=Vector2(0.5, 0),
                    text_color=(255, 255, 255), font_size=24, text="Can you climb up?")
level4.add_drawable(level4_text)

level5 = Level(50, 520)
level5.add_rect(0, 580, 100, 120)
level5.add_rect(700, 580, 100, 20)
level5_goal = game_objects.InteractiveRectangle(760, 540, 40, 40, color=BLUE)
level5.add_object(level5_goal)
def level5_goal_touched(player):
    change_level(example_level)
level5_goal.on_touched.connect(level5_goal_touched)
level5_text = TextBox(size=UDim2(), pos=UDim2.from_scale(0.5, 0.5), anchor_point=Vector2(0.5, 0.5),
                    text_color=(255, 255, 255), font_size=36, text="Biiiig gap")
level5.add_drawable(level5_text)

end_level = Level(380, 280)
end_level.add_rect(200, 100, 20, 400)
end_level.add_rect(800-220, 100, 20, 400)
end_level.add_rect(220, 100, 800-420, 20)
end_level.add_rect(220, 480, 800-420, 20)
end_level.add_drawable(TextBox(size=UDim2(), pos=UDim2(Vector2(0.5, 0), Vector2(0, 50)),
                        text="Yaaay you won", font_size=36, text_color=(255, 255, 255)))
restart = TextBox(size=UDim2.from_offset(175, 100), pos=UDim2(Vector2(0.333, 1), Vector2(0, -20)),
                anchor_point=Vector2(0.5, 1), text="Restart", font_size=24)
quit_box =TextBox(size=UDim2.from_offset(175, 100), pos=UDim2(Vector2(0.667, 1), Vector2(0, -20)),
                anchor_point=Vector2(0.5, 1), text="Quit", font_size=24)
def on_restart_clicked(inputted):
    change_level(test_level)
def on_quit_clicked(inputted):
    pygame.event.post(pygame.event.Event(pygame.QUIT))
restart.mouse_clicked.connect(on_restart_clicked)
quit_box.mouse_clicked.connect(on_quit_clicked)
end_level.add_drawable(restart)
end_level.add_drawable(quit_box)