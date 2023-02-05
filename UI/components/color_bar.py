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
        self.color_buffer = numpy.array([self.colors('black') for i in range(100)])
        self.n = height

    def set_color(self, i, color):
        self.color_buffer[i] = self.colors[color]
        np_arr = numpy.array([self.color_buffer for i in range(self.n)])
        self.set(np_arr)

