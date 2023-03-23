from .button import Button
from .text import Text


class Input(Button):
    object_count = 1
    def __init__(self, image_file, text, fontsize, color, width, max_character=20, *args, **kwargs):
        self.text_display = Text('', fontsize, 'TOPLEFT', color)
        self.bar = Text('|', fontsize, 'CENTER', color)
        self.base_x, self.base_y = 0, 0
        self.font_size = fontsize
        self.font_width = fontsize * 0.546 # anonymous pro
        self.max_charactor = max_character
        super().__init__(
            image_file=image_file,
            animation='none',
            align_mode='TOPLEFT',
            width=width,
            height=fontsize+2,
            *args, **kwargs
        )
        self.text = text
        self.inner_components[f'inner_{Input.object_count}_text'] = self.text_display
        self.inner_components[f'inner_{Input.object_count}_bar'] = self.bar
        Input.object_count += 1
        self.blink_wait_time = 0
        self.editing = False
        self.cursor_hidden = True
        self.bar.hide()
        self.change_text(self.text)
        def on_click():
            self.editing = True
        self.on_click = on_click

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
        if screen_clicked:
            self.editing = False
            self.bar.hide()
            self.cursor_hidden = True
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked)
        self.blink_wait_time += delta_time
        if self.editing:
            # default blink time is 530ms
            if self.blink_wait_time > 0.530:
                if self.cursor_hidden:
                    self.bar.show()
                else:
                    self.bar.hide()
                self.cursor_hidden = not self.cursor_hidden
                self.blink_wait_time = 0
            if keyboard_inputs:
                for c in keyboard_inputs:
                    if c != '\b':
                        if len(self.text) < self.max_charactor:
                            self.text += c
                    else:
                        self.text = self.text[:-1]
                self.change_text(self.text)

    def change_text(self, text):
        self.text_display.change_text(text)
        self.bar.set_pos(self.base_x+self.text_display.rect.w + self.font_width/5, self.base_y)

    def set_pos(self, x, y=None):
        super().set_pos(x, y)
        self.text_display.set_pos(x+10, y)
        self.base_x, self.base_y = x+10, y+(self.font_size+2)//2
        self.bar.set_pos(self.base_x, self.base_y)