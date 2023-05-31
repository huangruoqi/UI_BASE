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
        self.curr_scene_index = 0
        self.prev_scene_index = 0
        pygame.display.set_caption(title)
        # Icon = IMAGE("icon.png") # add your own icon image
        # pygame.display.set_icon(Icon)
        # pygame.mouse.set_visible(False)

    def display(self, mouse_pos, clicked):
        self.scene.display(mouse_pos, clicked)

    def update(
        self,
        delta_time,
        mouse_pos,
        keyboard_inputs,
        clicked,
        mouse_pressed,
        keyboard_pressed
    ):
        self.scene.update(delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressed, keyboard_pressed)

    def change_scene(self, scene_index, func=lambda s: 0):
        self.prev_scene_index = self.curr_scene_index
        self.curr_scene_index = scene_index
        self.next_scene = self.scenes[scene_index]
        self.next_scene_callback = func

    def run(self):
        # pygame setup
        clock = pygame.time.Clock()
        clicked = False
        mouse_pos = vec(0, 0)
        mouse_pressing = False
        keyboard_pressed = {}
        delta_time = 0.016
        running = True
        keyboard_inputs = []
        pygame.key.set_repeat(250, 50)

        while running:
            clicked = False
            mouse_pos.x, mouse_pos.y = pygame.mouse.get_pos()
            keyboard_inputs.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if mouse_pressing:
                        clicked = event.button
                        mouse_pressing = False
                        # development purpose
                        if clicked == 1:
                            pass
                            # print(str(mouse_pos) + " is clicked!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pressing = True
                if event.type == pygame.TEXTINPUT:
                    keyboard_inputs.append(event.text)
                if event.type == pygame.KEYDOWN:
                    if event.unicode == "\b":
                        keyboard_inputs.append("\b")
                    keyboard_pressed[event.unicode] = True
                if event.type == pygame.KEYUP:
                    keyboard_pressed[event.unicode] = False

            self.update(delta_time, mouse_pos, keyboard_inputs, clicked, mouse_pressing, keyboard_pressed)
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
