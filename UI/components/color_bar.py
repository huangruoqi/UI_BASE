from .pixel_display import PixelDisplay
import numpy


class ColorBar(PixelDisplay):
    colors = {
        "red": (255, 100, 100),
        "green": (100, 255, 100),
        "blue": (100, 100, 255),
        "orange": (255, 255, 100),
        "purple": (255, 100, 255),
        "tint": (100, 255, 255),
        "white": (255, 255, 255),
        "grey": (150, 150, 150),
        "red1": (255, 100, 100),
        "green1": (100, 255, 100),
        "blue1": (100, 100, 255),
        "orange1": (255, 255, 100),
        "purple1": (255, 100, 255),
        "tint1": (100, 255, 255),
        "white1": (255, 255, 255),
        "grey1": (150, 150, 150),
        "black": (0, 0, 0),
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

    def update(self, mouse_pos, clicked, pressed):
        if not super(ColorBar, self).update(mouse_pos, clicked, pressed):
            return
        if self.check_collide(mouse_pos):
            if clicked and self.on_click:
                self.on_click((mouse_pos.x - self.get_pos().x + self.m / 2) / self.m)
