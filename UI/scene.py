import pygame
from pygame.locals import *  # noqa

# from .utils import Mouse
from .components.background import Background
from .components.container import Container
from .components.button import Button
from .utils import IMAGE


class Scene:
    def __init__(self, app, screen, width, height, bg_file=None, *args, **kwargs):
        self.app = app
        self.width = width
        self.height = height
        if bg_file is None:
            self.background = Background("white.png", True, width, height)
        else:
            self.background = Background(bg_file, False, width, height)
        self.background_music = None
        self.screen = screen
        self.is_pointer = False
        self.layer_number = 6
        self.LAYERS = [{} for i in range(self.layer_number)]
        self.GROUPS = [pygame.sprite.Group() for i in range(self.layer_number)]
        self.keys_to_remove = []
        self.items_to_add = []
        self.started = False

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
        # Mouse.draw(self.screen, mouse_pos, self.is_pointer)

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed):
        self.started = True
        btns = self.BUTTONS.values()
        self.is_pointer = False
        screen_clicked = clicked
        for button in btns:
            button.hovered = False
            button.clicked = False
        for layer in self.LAYERS:
            for item in layer.values():
                item.update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked)
                if isinstance(item, Button):
                    if item.clicked:
                        clicked = False
        for button in btns:
            if button.hovered and not button.hidden:
                self.is_pointer = True
        for layer in self.LAYERS:
            for key in self.keys_to_remove:
                if layer.get(key) is not None:
                    del layer[key]
        self.keys_to_remove.clear()
        for layer in self.LAYERS:
            for k, v, l in self.items_to_add:
                self.LAYERS[l][k] = v
                self.GROUPS[l].add(v)
                for k, v in v.inner_components.items():
                    self.add(k, v, layer_number=l+2)
        self.items_to_add.clear()

    def add(self, key, value, layer_number=0):
        if not isinstance(value, Container):
            raise Exception("Not a component")
        if layer_number==0 and isinstance(value, Button):
            layer_number = 1
        if not self.started:
            self.LAYERS[layer_number][key] = value
            self.GROUPS[layer_number].add(value)
            for k, v in value.inner_components.items():
                self.add(k, v, layer_number=layer_number+2)
        else:
            self.items_to_add.append((key, value, layer_number))
        return value

    def remove(self, key):
        self.keys_to_remove.append(key)
        for layer in self.LAYERS:
            item = layer.get(key)
            if item is not None:
                item.kill()
                for k in item.inner_components:
                    self.remove(k)
                return
        


    def get(self, key):
        for layer in self.LAYERS:
            item = layer.get(key)
            if item is not None:
                return item


    def close(self):
        pass
