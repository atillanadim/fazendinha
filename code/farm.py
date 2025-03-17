import pygame
from settings import *

class Farm:
    def __init__(self):
        self.crops = []  # Lista de plantações

    def plant(self, x, y):
        self.crops.append({"pos": (x, y), "grown": False})

    def harvest(self):
        self.crops = [crop for crop in self.crops if not crop["grown"]]

    def draw(self, screen):
        for crop in self.crops:
            color = BROWN if not crop["grown"] else GREEN
            pygame.draw.rect(screen, color, (*crop["pos"], 20, 20))
