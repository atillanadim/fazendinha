import pygame
import os


class SpriteSheet:
    def __init__(self, filename):
        """Load the sheet."""
        try:
            # Make sure the directory exists
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            self.sheet = pygame.image.load(filename).convert_alpha()
            print(f"Loaded sprite sheet: {filename}")
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            print(e)
            # Create a small colored surface as a fallback
            self.sheet = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.sheet.fill((255, 0, 255))  # Magenta for missing textures

    def image_at(self, rectangle, colorkey=None):
        """Load a specific image from a specific rectangle."""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)

        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def images_at(self, rects, colorkey=None):
        """Load a list of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a strip of images and return them as a list."""
        tups = [(rect[0] + rect[2] * x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid(self, rect, cols, rows, colorkey=None):
        """Load a grid of images and return them as a list."""
        images = []
        for row in range(rows):
            for col in range(cols):
                x = rect[0] + col * rect[2]
                y = rect[1] + row * rect[3]
                images.append(self.image_at((x, y, rect[2], rect[3]), colorkey))
        return images

