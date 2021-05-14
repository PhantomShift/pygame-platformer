import GameObjects
import Geometry
from pygame import Color, error
from Vector2 import Vector2
from BindableEvent import BindableEvent
from GameObjects import Player

CURRENT_LEVEL = None
on_level_changed = BindableEvent.new()
class LevelObject:
    def __init__(self, player: Player, objects: dict):
        self.player = player
        self.objects = objects

class Level:
    def __init__(self, start_x, start_y):
        self.start_x = start_x
        self.start_y = start_y
        self.objects = {}
    
    def load(self) -> LevelObject:
        return LevelObject(Player(self.objects, self.start_x, self.start_y), self.objects)

    def add_object(self, obj):
        self.objects[obj] = True

def change_level(new_level: Level):
    print("Hey level should be changed?")
    global CURRENT_LEVEL
    CURRENT_LEVEL = new_level
    on_level_changed.fire(CURRENT_LEVEL.load())

def reset_level():
    global CURRENT_LEVEL
    if not CURRENT_LEVEL:
        raise error("CURRENT_LEVEL not initialized when attempted to reset level")
    change_level(CURRENT_LEVEL)

example_level = Level(50, 50)
def construct_platform(x, y, w, h):
    example_level.add_object(Geometry.Rectangle(x, y, w, h))
construct_platform(0, 200, 200, 20)
construct_platform(100, 220, 200, 20)
construct_platform(600, 220, 200, 20)
construct_platform(640, 300, 200, 20)
construct_platform(640, 240, 20, 80)
construct_platform(400, 50, 20, 200)

goal = GameObjects.InteractiveRectangle(760, 260, 40, 40, color=(50, 50, 240))
def goal_touched(player):
    print(test_level)
    change_level(test_level)
goal.on_touched.connect(goal_touched)
example_level.add_object(goal)

test_level = Level(50, 520)
base = Geometry.Rectangle(0, 580, 800, 120)
goal2 = GameObjects.InteractiveRectangle(760, 540, 40, 40, color=(50, 50, 240))
def goal_touched2(player):
    change_level(example_level)
test_level.add_object(base)
test_level.add_object(goal2)
goal2.on_touched.connect(goal_touched2)