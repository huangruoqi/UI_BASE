from .container import Container
import pygame
from pygame.locals import *  # noqa


class PixelDisplay(Container):
    def __init__(self, width, height, x, y):
        super().__init__(x=x, y=y)
        image = pygame.Surface([width, height])
        pos = self.get_pos()
        self.set_image(image).set_pos(pos)

    def set(self, np_arr):
        pygame.surfarray.blit_array(self.image, np_arr)
