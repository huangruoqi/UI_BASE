import pygame
from pygame.locals import *  # noqa

from .button import Button


class Slider(Button):
    def __init__(
        self,
        drag_width,
        on_change,
        width=30,
        height=30,
        interval=[0, 31],
        color=(0, 0, 0),
        on_click=lambda: 0,
        *args,
        **kwargs
    ):
        super().__init__(on_click=on_click, opacity=0.8, *args, **kwargs)
        image = pygame.Surface([width, height])
        image.fill(color)
        self.origin = self.get_pos()
        self.set_image(image)
        self.dragged = False
        self.half_width = drag_width // 2
        self.set_pos(self.origin.x - self.half_width, self.origin.y)
        self.on_change = on_change
        self.offset = 0
        self.interval = interval
        self.sound = None

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked)
        if self.dragged:
            self.dragged = pressed
            val = (
                (self.get_pos().x - self.origin.x) + self.half_width
            ) / self.half_width / 2 * (
                self.interval[1] - self.interval[0]
            ) + self.interval[
                0
            ]
            if clicked:
                self.on_change(val)
        else:
            self.dragged = pressed and self.check_collide(mouse_pos)
            self.offset = mouse_pos - self.get_pos()

        if self.dragged:
            self.set_slider_pos(mouse_pos.x - self.offset.x)

    def set_slider_pos(self, pos):
        x_pos = min(
            max(self.origin.x - self.half_width, pos), self.origin.x + self.half_width
        )
        self.set_pos(x_pos, self.origin.y)

    def set_progress(self, progress):
        pos = self.half_width * 2 * progress + self.origin.x - self.half_width
        self.set_slider_pos(pos)
