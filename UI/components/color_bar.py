from .pixel_display import PixelDisplay
import numpy

class ColorBar(PixelDisplay):
    colors = {
        'black' : (0, 0, 0),
        'red'   : (255, 100, 100),
        'green' : (100, 255, 100),
        'blue'  : (100, 255, 255),
        'orange': (255, 255, 100),
        'purple': (255, 100, 255),
        'tint'  : (100, 255, 255),
        'white' : (255, 255, 255),
    }

    def __init__(self, width, height, x, y):
        if width % 100 != 0:
            raise Exception("<width> for ColorBar must be multiples of 100")
        super(ColorBar, self).__init__(width, height, x, y)
        self.color_buffer = numpy.array([self.colors['black'] for i in range(100)], dtype='u8')
        self.m = width
        self.n = height
        self.k = self.m // 100

    def set_color(self, i, color):
        self.color_buffer[i] = self.colors[color]
        self.process()

    def process(self):
        np_arr = numpy.zeros((self.m, self.n, 3), dtype='u8')
        for i in range(self.k):
            for j in range(self.n):
                np_arr[i:self.m:self.k, j] = self.color_buffer
        self.set(np_arr)
