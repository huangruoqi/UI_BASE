from .button import Button
from .text import Text


class Input(Button):
    def __init__(self, image_file, text, fontsize, color, width, *args, **kwargs):
        super().__init__(
            image_file=image_file,
            animation='none',
            align_mode='TOPLEFT',
            width=width,
            height=fontsize+2,
            *args, **kwargs
        )
        x, y = self.get_pos()
        self.text_display = Text('', fontsize, 'TOPLEFT', color, x=x+10, y=y)
        self.base_x, self.base_y = x+10, y+(fontsize+2)//2
        self.bar = Text('|', fontsize, 'CENTER', color, x=self.base_x, y=self.base_y)
        self.inner_components.append(self.text_display)
        self.inner_components.append(self.bar)
        self.text = text
        self.font_width = fontsize * 0.546 # anonymous pro
        self.blink_wait_time = 0
        self.editting = False
        self.cursor_hidden = True
        self.bar.hide()
        self.change_text(self.text)
        def on_click():
            self.editting = True

        self.on_click = on_click

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
        if screen_clicked:
            self.editting = False
            self.bar.hide()
            self.cursor_hidden = True
        super().update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked)
        self.blink_wait_time += delta_time
        if self.editting:
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
                        self.text += c
                    else:
                        self.text = self.text[:-1]
                self.change_text(self.text)

    def change_text(self, text):
        self.text_display.change_text(text)
        self.bar.set_pos(self.base_x+self.text_display.rect.w + self.font_width/5, self.base_y)
