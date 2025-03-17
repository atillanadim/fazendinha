class TileMap:
    def __init__(self):
        self.tiles = []

    def draw(self, screen):
        for tile in self.tiles:
            pygame.draw.rect(screen, BROWN, tile)
