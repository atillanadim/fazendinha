import pygame
import os

class Player:
    def __init__(self, x, y):
        # Caminho do spritesheet
        sprite_path = os.path.join("assets", "sprites", "chicken.png")
        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames(32, 32)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.direction = pygame.Vector2(0, 0)

    def load_frames(self, width, height):
        """Corta os sprites do spritesheet e retorna uma lista de frames."""
        frames = []
        for row in range(3):  # Assume que há 3 linhas no sprite
            for col in range(3):  # Assume que há 3 colunas
                frame = self.spritesheet.subsurface((col * width, row * height, width, height))
                frames.append(frame)
        return frames

    def update(self):
        """Apenas atualiza o índice do frame, sem desenhar na tela."""
        self.index = (self.index + 1) % len(self.frames)
        self.image = self.frames[self.index]
