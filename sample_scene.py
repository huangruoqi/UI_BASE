from UI.scene import Scene
from UI.components.button import Button
from UI.components.text import Text
from UI.sound import Channel
from UI.utils import IMAGE, SOUND


class SampleScene(Scene):
    def __init__(self, screen, *args, **kwargs):
        super(SampleScene, self).__init__(screen, *args, **kwargs)
        self.background_music = SOUND("castle.wav", Channel.BACKGROUND)
        self.add("abc", Button(
            text="abc",
            text_fontsize=100,
            x=100,
            y=100,
            on_click=lambda:0,
        ))
        self.add("text", Text(
            "something",
            x=200,
            y=300
        ))
