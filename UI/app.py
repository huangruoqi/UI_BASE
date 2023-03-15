import pygame
from pygame.locals import *  # noqa
from .utils import vec, IMAGE


class App:
    def __init__(self, scene_classes, width, height, title="Title", *args, **kwargs):
        pygame.init()
        GAME_RESOLUTION = (width, height)
        screen = pygame.display.set_mode(GAME_RESOLUTION)
        self.scenes = [
            i(self, screen, width, height, *args, **kwargs) for i in scene_classes
        ]
        self.scene = self.scenes[0]
        self.next_scene = None
        self.next_scene_callback = None
        pygame.display.set_caption(title)
        # Icon = IMAGE("icon.png") # add your own icon image
        # pygame.display.set_icon(Icon)
        # pygame.mouse.set_visible(False)

    def display(self, mouse_pos, clicked):
        self.scene.display(mouse_pos, clicked)

    def update(self, delta_time, mouse_pos, clicked, pressed):
        self.scene.update(delta_time, mouse_pos, clicked, pressed)

    def change_scene(self, scene_index, func=lambda s: 0):
        self.next_scene = self.scenes[scene_index]
        self.next_scene_callback = func

    def run(self):
        # pygame setup
        clock = pygame.time.Clock()
        clicked = False
        mouse_pos = vec(0, 0)
        pressing = False
        delta_time = 0.016
        running = True

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
            if self.next_scene is not None:
                self.scene = self.next_scene
                self.next_scene_callback(self.scene)
                self.next_scene = None
                self.next_scene_callback = None
            self.display(mouse_pos, clicked)
            delta_time = clock.tick(30) / 1000
            pygame.display.flip()

        pygame.quit()
        for s in self.scenes:
            s.close()
