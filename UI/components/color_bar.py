from .pixel_display import PixelDisplay
import numpy


class ColorBar(PixelDisplay):
    # names are not correct, edited from chatgpt result
    colors = {
        "dark_red": (139, 128, 0),
        "maroon": (128, 0, 0),
        "dark_orange": (255, 140, 0),
        "olive": (60, 32, 0),
        "dark_green": (0, 100, 0),
        "navy_blue": (0, 20, 150),
        "indigo": (75, 0, 130),
        "dark_violet": (148, 0, 211),
        "grey": (47, 79, 79),
        "sienna": (160, 40, 75),
        "saddle_brown": (139, 69, 19),
        "midnight_blue": (40, 25, 112),
        "black": (0, 0, 0)
    }

    def __init__(self, width, height, x, y, color="black", on_click=None):
        if width % 100 != 0:
            raise Exception("<width> for ColorBar must be multiples of 100")
        super(ColorBar, self).__init__(width, height, x, y)
        self.color_buffer = numpy.array(
            [self.colors[color] for i in range(100)], dtype="u1"
        )
        self.m = width
        self.n = height
        self.k = self.m // 100
        self.on_click = on_click
        self.process()

    def set_color(self, i, color):
        if all([self.color_buffer[i][j] == self.colors[color][j] for j in range(3)]):
            return
        self.color_buffer[i] = self.colors[color]
        self.process()

    def set_arr(self, np_arr):
        self.color_buffer = np_arr
        self.process()

    def process(self):
        np_arr = numpy.zeros((self.m, self.n, 3), dtype="u1")
        for i in range(self.k):
            for j in range(self.n):
                np_arr[i : self.m : self.k, j] = self.color_buffer
        self.set(np_arr)

    def is_click(self, click_pos):
        return self.rect.collidepoint(click_pos)

    def check_collide(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
        if not super(ColorBar, self).update(delta_time, mouse_pos, keyboard_inputs, clicked, pressed, screen_clicked):
            return
        if self.check_collide(mouse_pos):
            if clicked and self.on_click:
                self.on_click((mouse_pos.x - self.get_pos().x + self.m / 2) / self.m)
