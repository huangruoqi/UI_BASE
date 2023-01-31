from UI.components.text import Text
from ...mixin import Mixin
import pygame
from pygame.locals import *  # noqa


class ScaleMixin(Mixin):
    def effect(self, current_time=0.5):
        x_grow = self.w * self.scale - self.w
        y_grow = self.h * self.scale - self.h

        if self.scale < 1:
            self.button.check_collide_original_rect = True

        temp = pygame.transform.smoothscale(
            self.button.original_image,
            (
                int(self.w + x_grow * self.progress(current_time)),
                int(self.h + y_grow * self.progress(current_time)),
            ),
        )
        pos = self.button.get_pos()
        self.button.set_temp_image(temp).set_pos(pos)
        pass

    def reset(self):
        self.button.image = self.button.original_image
        self.button.rect = self.button.original_rect
