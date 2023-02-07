from .container import Container
import pygame
from pygame.locals import *  # noqa


class PixelDisplay(Container):
    def __init__(self, width, height, x, y):
        image = pygame.Surface([width, height])
        super().__init__(image=image, x=x, y=y)

    def set(self, np_arr):
        pygame.surfarray.blit_array(self.image, np_arr)
