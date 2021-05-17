import pygame
import pygame.font
from vector2 import Vector2
from vector2 import ZERO as ZERO_VECTOR
from instance import Instance
from bindable_event import BindableEvent
from input_handler import InputHandler, InputObject

DEFAULT_FONT = pygame.font.SysFont("Arial", 12)


class UDim2:
    def __init__(self, scale=ZERO_VECTOR, offset=ZERO_VECTOR):
        self.scale = scale
        self.offset = offset
    
    def __repr__(self):
        return f"<UDim2 ({self.scale.x}, {self.scale.y}, {self.offset.x}, {self.offset.y})"
    def __str__(self):
        return f"({self.scale.x}, {self.scale.y}, {self.offset.x}, {self.offset.y})"
    
    @staticmethod
    def from_offset(x, y):
        return UDim2(offset=Vector2(x,y))
    
    @staticmethod
    def from_scale(x, y):
        return UDim2(scale=Vector2(x,y))
    
    @staticmethod
    def new(sx=0, sy=0, ox=0, oy=0):
        return UDim2(Vector2(sx, sy), Vector2(ox, oy))

class GuiObject(Instance, class_name="GuiObject"):
    def __init__(self, parent=None, size=UDim2.from_offset(100, 100), pos=UDim2.new(), anchor_point = ZERO_VECTOR, visible=True):
        super().__init__(parent)
        self.size = size
        self.pos = pos
        self.anchor_point = anchor_point
        self.visible = visible

        self.__focused = False
        self.mouse_entered = BindableEvent()
        self.mouse_clicked = BindableEvent()

        def mouse_clicked(inputted: InputObject):
            if not self.visible:
                return
            if inputted.input_type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                if self.get_pyrect().collidepoint(x, y):
                    self.mouse_clicked.fire(inputted.key)
        self.__connections = []
        self.__connections.append(InputHandler.input_began.connect(mouse_clicked))
    
    def update(self, elapsedTime):
        pass
    
    def get_pyrect(self) -> pygame.Rect:
        left, top = self.absolute_pos.unpack()
        width, height = self.absolute_size.unpack()
        return pygame.Rect(left, top, width, height)

    @property
    def absolute_size(self) -> Vector2:
        (x, y) = self.parent.absolute_size.unpack() if self.parent else pygame.display.get_surface().get_size()
        return self.size.offset + self.size.scale * Vector2.new(x, y)
    
    @property
    def absolute_pos(self) -> Vector2:
        (x, y) = self.parent.absolute_size.unpack() if self.parent else pygame.display.get_surface().get_size()
        return self.pos.offset + self.pos.scale * Vector2.new(x, y) - self.absolute_size * self.anchor_point

class Frame(GuiObject, class_name="Frame"):
    def __init__(self, parent=None, size=UDim2.from_offset(100, 100), pos=UDim2.new(), anchor_point = ZERO_VECTOR, visible=True, color=(255, 255, 255)):
        super().__init__(parent, size, pos, anchor_point, visible)
        self.color = color
    
    def draw(self):
        if self.visible:
            pygame.draw.rect(pygame.display.get_surface(), self.color, self.get_pyrect())
            return True

class TextBox(Frame, class_name="TextBox"):
    def __init__(self, parent=None, size=UDim2.from_offset(100, 100), pos=UDim2.new(),
                anchor_point = ZERO_VECTOR, visible=True, color=(255, 255, 255),
                text="TextBox", text_color=(0,0,0), font="Arial", font_size=12):
        super().__init__(parent, size, pos, anchor_point, visible, color)
        self.text: str = text
        self.text_color = text_color
        if font == "Arial" and font_size == 12:
            self.font = DEFAULT_FONT
        else:
            self.font: pygame.font.Font = pygame.font.SysFont(font, font_size)
    
    def draw(self):
        if super().draw():
            text = self.font.render(self.text, True, self.text_color)
            rect = text.get_rect()
            pos = self.absolute_pos + self.absolute_size / 2 - Vector2(rect.width/2, rect.height/2)
            pygame.display.get_surface().blit(text, pos.unpack())


if __name__ == "__main__":
    display = pygame.display.set_mode((300, 400))
    print(pygame.display.get_surface().get_size())
    gui = GuiObject()
    gui.name = "Hello"
    gui.size = UDim2.from_scale(0.5, 0.5)
    gui2 = GuiObject(gui)
    gui2.size = UDim2.from_scale(0.5, 0.5)
    print(gui.__repr__())
    print(gui.absolute_size)
    print(gui2.size)
    print(gui2.absolute_size)