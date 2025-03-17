import pygame
from code.settings import WIDTH, HEIGHT, FPS
from code.npc import NPC

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Farm Demo")
        self.clock = pygame.time.Clock()
        self.running = True

        # Criando NPCs
        self.npcs = [
            NPC(100, 100, "chicken.png", 7),  # Galinha com 6 frames
            NPC(200, 200, "sheep.png", 5)  # Ovelha com 5 frames
        ]

    def run(self):
        pygame.mixer_music.load()
        while self.running:
            self.handle_events()
            self.update()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        for npc in self.npcs:
            npc.update()

if __name__ == "__main__":
    game = Game()
    game.run()
