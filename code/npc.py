import pygame
import os
import random

class NPC:
    def __init__(self, x, y, sprite_name, frame_count, width=32, height=32):
        """
        Inicializa o NPC.
        :param sprite_name: Nome do arquivo de sprite (ex: 'chicken.png' ou 'sheep.png')
        :param frame_count: Número total de frames na spritesheet
        """

        sprite_path = os.path.join("assets", "sprites", sprite_name)
        self.spritesheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames(frame_count, width, height)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimento
        self.speed = 1
        self.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        self.move_timer = 0

    def load_frames(self, frame_count, width, height):
        """Corta os sprites corretamente com base no número de frames."""
        frames = []
        for i in range(frame_count):  # Percorre a quantidade de frames
            frame = self.spritesheet.subsurface((i * width, 0, width, height))
            frames.append(frame)
        return frames

    def update(self):
        """Atualiza a movimentação e animação da galinha/ovelha."""
        self.move_timer += 1
        if self.move_timer > 80:  # Muda de direção a cada 80 frames (~2.6s a 30 FPS)
            self.direction = pygame.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
            self.move_timer = 0

        # Movimentar NPC
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Atualizar animação
        self.index = (self.index + 1) % len(self.frames)
        self.image = self.frames[self.index]
