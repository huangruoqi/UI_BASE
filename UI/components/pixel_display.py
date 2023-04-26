from .container import Container
import pygame
import numpy
from pygame.locals import *  # noqa


class PixelDisplay(Container):
    def __init__(self, width, height, x, y):
        super().__init__(x=x, y=y)
        image = pygame.Surface([width, height])
        pos = self.get_pos()
        self.rot90 = 0
        self.set_image(image).set_pos(pos)

    def set(self, np_arr):
        m = numpy.rot90(np_arr, k=self.rot90, axes=(0, 1))
        pygame.surfarray.blit_array(self.image, m)
