import pygame
from pygame.locals import *  # noqa

from ..animation.button.button_animations import (
    CustomButtonAnimation,
    OpacityButtonAnimation,
    ScaleButtonAnimation,
    JumpButtonAnimation,
    RotateButtonAnimation,
    FrameButtonAnimation,
)
from .container import Container
from .text import Text
from ..utils import SOUND
from ..sound import Channel
import time


class Button(Container):
    ANIMATIONS = {
        "opacity": OpacityButtonAnimation,
        "scale": ScaleButtonAnimation,
        "rotate": RotateButtonAnimation,
        "jump": JumpButtonAnimation,
        "frame": FrameButtonAnimation,
        "custom": CustomButtonAnimation,
        "none": lambda *args, **kwargs: None,
    }

    def __init__(
        self,
        animation="opacity",
        transition=0.2,
        parameter={"factor": 0.5},
        on_click=None,
        can_hover=None,
        text=None,
        text_fontsize=24,
        color=(150, 200, 100),
        sound=SOUND("mouse-click.wav", Channel.UI),
        *args,
        **kwargs
    ):
        self.text = text
        self.text_fontsize = text_fontsize
        self.color = color
        self.sound = sound
        # default button

        super().__init__(*args, **kwargs)
        if kwargs.get("image_file") is None and self.text is not None:
            temp = Text.get_font(self.text_fontsize).render(self.text, True, self.color)
            pos = self.get_pos()
            self.set_image(temp).set_pos(pos)
        self.on_click = on_click
        self.can_hover = can_hover
        self.hovered = False
        self.clicked = False
        self.transition = transition
        self.parameter = parameter
        self.animation = self.ANIMATIONS[animation](self, transition, parameter)

    def is_click(self, click_pos):
        return self.rect.collidepoint(click_pos)

    def check_collide(self, mouse_pos):
        if self.check_collide_original_rect:
            return self.original_rect.collidepoint(mouse_pos)
        else:
            return self.rect.collidepoint(mouse_pos)

    def click(self):
        if self.on_click:
            if self.sound:
                self.sound.play()
            self.on_click()
            self.clicked = True
        else:
            raise NotImplementedError("Function: <on_click> not implemented!!")

    def update(self, mouse_pos, clicked, pressed):
        if not super(Button, self).update(mouse_pos, clicked, pressed):
            return
        current_time = time.time()
        can_hover = self.can_hover is None or (
            self.can_hover is not None and self.can_hover()
        )
        if self.check_collide(mouse_pos):
            self.hovered = True
            if clicked and can_hover:
                self.click()
        if self.animation is None:
            return
        if self.can_hover is not None and not self.can_hover():
            self.animation.stop()
            return
        if self.hovered:
            self.animation.play(current_time)
        else:
            self.animation.stop()
        self.animation.update(current_time)
