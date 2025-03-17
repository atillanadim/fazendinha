import pygame
from settings import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.background = pygame.image.load("assets/background.png")

        # Criando botões
        self.start_text = self.font.render("Iniciar Jogo", True, WHITE)
        self.quit_text = self.font.render("Sair", True, WHITE)

        self.start_rect = self.start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.start_text, self.start_rect)
        self.screen.blit(self.quit_text, self.quit_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_rect.collidepoint(event.pos):
                        running = False  # Sai do menu e inicia o jogo
                    if self.quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()
