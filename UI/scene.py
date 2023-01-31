import pygame
from pygame.locals import *  # noqa
from .utils import Mouse
from .components.background import Background
from .components.container import Container
from .components.button import Button
from .utils import IMAGE


class Scene:
    def __init__(
        self, screen, width, height, bg_file="white.png"
    ):
        bg = IMAGE(bg_file)
        self.width = width
        self.height = height
        self.background = Background(bg, width, height)
        self.background_music = None
        self.screen = screen
        self.is_pointer = False
        self.layer_number = 6
        self.LAYERS = [{} for i in range(self.layer_number)]
        self.GROUPS = [pygame.sprite.Group() for i in range(self.layer_number)]

    def __getattr__(self, name):
        if name == "BUTTONS":
            return self.LAYERS[1]
        if name == "OTHERS":
            return self.LAYERS[2]
        if name == "TEXTS":
            return self.LAYERS[3]
        else:
            raise Exception("ATTRIBUTE NOT FOUND")

    def display(self, mouse_pos, clicked):
        self.background.draw(self.screen)
        for i in range(self.layer_number):
            self.GROUPS[i].draw(self.screen)
        Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, delta_time, mouse_pos, clicked, pressed):
        btns = list(self.BUTTONS.values()) + list(self.LAYERS[5].values())
        others = list(self.OTHERS.values()) + list(self.LAYERS[4].values())
        self.is_pointer = False
        for button in btns:
            button.hovered = False
        for button in btns:
            button.update(mouse_pos, clicked, pressed)
            if button.hovered and not button.hidden:
                self.is_pointer = True
        for other in others:
            other.update(mouse_pos, clicked, pressed)

    def load_items(self):
        for i in range(self.layer_number):
            self.GROUPS[i].empty()
            self.GROUPS[i].add(list(self.LAYERS[i].values()))

    def add(self, key, value, layer_number = 0):
        if not isinstance(value, Container):
            raise Exception("Not a component")
        if isinstance(value, Button):
            self.BUTTONS[key] = value
        else: 
            self.LAYERS[layer_number][key] = value

    def get(self, key):
        for layer in self.LAYERS:
            item = layer.get(key)
            if item is not None:
                return item
