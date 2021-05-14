import pygame
from BindableEvent import BindableEvent

BEGAN = "BEGAN"
ENDED = "ENDED"


class InputObject():
    def __init__(self, input_type, key, state):
        self.input_type = input_type
        self.key = key
        self.state = state

class _InputHandler:
    def __init__(self):
        self.input_began = BindableEvent()
        self.input_ended = BindableEvent()
        self.BEGAN = BEGAN
        self.ENDED = ENDED

    def parse_input(self, input_type, key, state):
        if state == BEGAN:
            self.input_began.fire(InputObject(input_type, key, state))
        elif state == ENDED:
            self.input_ended.fire(InputObject(input_type, key, state))


InputHandler = _InputHandler()