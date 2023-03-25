import numpy
from .button import Button
from .text import Text


class NumericInput(Button):
    object_count = 1

    def __init__(
        self,
        image_file,
        fontsize,
        value,
        color,
        width,
        use_indicator=False,
        max_character=20,
        *args,
        **kwargs,
    ):
        self.text_display = Text("", fontsize, "TOPLEFT", color)
        self.bar = Text("|", fontsize, "CENTER", color)
        self.negative_sign = Text("-", fontsize, "CENTER", color)
        self.indicator = None
        self.base_x, self.base_y = 0, 0
        self.font_size = fontsize
        self.font_width = fontsize * 0.546  # anonymous pro
        self.max_charactor = max_character
        self.max_width = width
        super().__init__(
            image_file=image_file,
            animation="none",
            align_mode="TOPLEFT",
            width=width,
            height=fontsize + 2,
            *args,
            **kwargs,
        )
        self.text = str(value)
        if numpy.isnan(value):
            self.text = ""
        self.inner_components[
            f"inner_{NumericInput.object_count}_text"
        ] = self.text_display
        self.inner_components[f"inner_{NumericInput.object_count}_bar"] = self.bar
        self.inner_components[f"inner_{NumericInput.object_count}_neg"] = self.negative_sign
        NumericInput.object_count += 1
        self.blink_wait_time = 0
        self.editing = False
        self.cursor_hidden = True
        self.use_indicator = use_indicator
        if use_indicator:
            self.indicator = Text("Unlabeled", fontsize * 2 // 3, "CENTER", (0, 0, 0))
            self.inner_components[
                f"inner_{NumericInput.object_count}_indicator"
            ] = self.indicator
        self.bar.hide()
        self.change_text(self.text)

        def on_click():
            self.editing = True

        self.on_click = on_click
        self.value = value
        self.upper_bound = 1000000
        self.lower_bound = -1000000
        self.negative = value < 0

    def update(
        self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked
    ):
        if screen_clicked:
            self.editing = False
            self.bar.hide()
            self.cursor_hidden = True
        super().update(
            delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked
        )
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
            x, y = self.get_pos()
            abs_value = None
            if keyboard_inputs:
                for c in keyboard_inputs:
                    if c == "-":
                        self.negative = not self.negative
                        self.value = -self.value
                    elif c != "\b":
                        if len(self.text) < self.max_charactor:
                            if self.validate_input(self.text + c):
                                self.text += c
                                self.value = float(self.text)
                                if self.negative:
                                    self.value = - self.value
                    else:
                        if len(self.text.strip()) == 0:
                            if self.negative:
                                self.negative = False
                        else:
                            self.text = self.text[:-1]
                        if len(self.text.strip()) == 0:
                            self.value = float("nan")
                        else:
                            self.value = float(self.text)
                            if self.negative:
                                self.value = - self.value
                self.change_text(self.text)
                if len(self.text.strip()) == 0:
                    if self.indicator is not None:
                        self.indicator.change_text("Unlabeled")
                        self.indicator.show()
                        self.indicator.set_pos(x+self.max_width/2, y+self.font_size*2)
                else:
                    if self.lower_bound > self.value:
                        self.value = self.lower_bound
                        if self.indicator is not None:
                            self.indicator.show()
                            self.indicator.change_text(f"Min:{str(self.value)[:self.max_charactor]}")
                            self.indicator.set_pos(x+self.max_width/2, y+self.font_size*2)
                    elif self.value > self.upper_bound:
                        self.value = self.upper_bound
                        if self.indicator is not None:
                            self.indicator.show()
                            self.indicator.change_text(f"Max:{str(self.value)[:self.max_charactor]}")
                            self.indicator.set_pos(x+self.max_width/2, y+self.font_size*2)
                    else:
                        if self.indicator is not None:
                            self.indicator.hide()
            if self.negative:
                self.negative_sign.show()
            else:
                self.negative_sign.hide()

    def validate_input(self, text):
        try:
            float(text)
            return True
        except:
            return False

    def change_text(self, text):
        self.text_display.change_text(text)
        self.bar.set_pos(
            self.base_x + self.text_display.rect.w + self.font_width / 5, self.base_y
        )

    def change_value(self, value):
        self.value = float(value)
        self.negative = self.value < 0
        if self.negative:
            self.negative_sign.show()
        else:
            self.negative_sign.hide()
        self.text = str(abs(self.value))[:self.max_charactor]
        self.change_text(self.text)
    

    def set_pos(self, x, y=None):
        super().set_pos(x, y)
        self.text_display.set_pos(x + 10 + self.font_width, y)
        self.base_x, self.base_y = x + 10 + self.font_width, y + (self.font_size + 2) // 2
        self.bar.set_pos(
            self.base_x + self.text_display.rect.w + self.font_width / 5, self.base_y
        )
        self.negative_sign.set_pos(
            self.base_x - self.font_width//2, self.base_y - (self.font_size + 2) // 16
        )

    def show(self):
        super().show()
        self.bar.hide()
        if self.negative:
            self.negative_sign.show()
        else:
            self.negative_sign.hide()
        if self.indicator is not None:
            self.indicator.hide()
