import pygame
from pygame.locals import *  # noqa
from .utils import vec, IMAGE


class App:
    def __init__(self, scene_class, width, height):
        pygame.init()
        GAME_RESOLUTION = (width, height)
        screen = pygame.display.set_mode(GAME_RESOLUTION)
        self.scene = scene_class(screen, width, height)
        pygame.display.set_caption("Title")
        # Icon = IMAGE("icon.png") # add your own icon image
        # pygame.display.set_icon(Icon)
        pygame.mouse.set_visible(False)
        self.scene.load_items()

    def display(self, mouse_pos, clicked):
        self.scene.display(mouse_pos, clicked)

    def update(self, delta_time, mouse_pos, clicked, pressed):
        self.scene.update(delta_time, mouse_pos, clicked, pressed)

    def run(self):
        # pygame setup
        clock = pygame.time.Clock()
        clicked = False
        mouse_pos = vec(0, 0)
        pressing = False
        delta_time = 0.016
        running = True
        self.scene.background_music.play()

        # app settings
        while running:
            clicked = False
            mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if pressing:
                        clicked = event.button
                        pressing = False
                        # development purpose
                        if clicked == 1:
                            pass
                            # print(str(mouse_pos) + " is clicked!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pressing = True

            self.update(delta_time, mouse_pos, clicked, pressing)
            self.display(mouse_pos, clicked)
            delta_time = clock.tick(60) / 1000
            pygame.display.flip()

        pygame.quit()
