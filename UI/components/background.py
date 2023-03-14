from .container import Container


class Background(Container):
    def __init__(self, image_file, image_relative, width, height):
        super().__init__(
            image_file=image_file,
            image_relative=image_relative,
            width=width,
            height=height,
        )

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect(center=screen.get_rect().center))

    def update(self):
        pass
