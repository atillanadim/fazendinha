import pygame
import random
import os
from .animals import AnimalManager
from .plants import PlantManager


class World:
    def __init__(self, game):
        self.game = game
        self.width = game.WIDTH
        self.height = game.HEIGHT

        # Tile size
        self.tile_size = 32

        # Create tile grid
        self.grid_width = self.width // self.tile_size
        self.grid_height = self.height // self.tile_size
        self.grid = [[0 for _ in range(self.grid_height)] for _ in range(self.grid_width)]

        # Initialize tile types
        # 0: grass, 1: farmland, 2: water, 3: stone, 4: path, 5: beach, 6: cliff
        self.generate_world()

        # Load tile sprites
        self.load_tiles()

        # Load background
        self.load_background()

        # House position
        self.house_pos = (self.width // 2 - 64, self.height // 4 - 64)

        # Initialize managers
        self.animal_manager = AnimalManager(game)
        self.plant_manager = PlantManager(game)

    def generate_world(self):
        # Fill the world with grass
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                # Default to grass
                self.grid[x][y] = 0

        # Create a farmland area in front of where the house will be
        farm_center_x = self.grid_width // 2
        farm_center_y = self.grid_height // 2 + 3
        farm_width = 8
        farm_height = 6

        for x in range(farm_center_x - farm_width // 2, farm_center_x + farm_width // 2):
            for y in range(farm_center_y - farm_height // 2, farm_center_y + farm_height // 2):
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    self.grid[x][y] = 1  # Farmland

        # Add some water spots (small pond)
        pond_x = farm_center_x + farm_width
        pond_y = farm_center_y
        pond_size = 3

        for x in range(pond_x - pond_size, pond_x + pond_size):
            for y in range(pond_y - pond_size, pond_y + pond_size):
                if 0 <= x < self.grid_width and 0 <= y < self.grid_height:
                    # Make a circular-ish pond
                    if (x - pond_x) ** 2 + (y - pond_y) ** 2 < pond_size ** 2:
                        self.grid[x][y] = 2  # Water

        # Add some paths around the farm
        # Horizontal path in front of the house
        path_y = farm_center_y - farm_height // 2 - 1
        for x in range(farm_center_x - 4, farm_center_x + 4):
            if 0 <= x < self.grid_width and 0 <= path_y < self.grid_height:
                self.grid[x][path_y] = 4  # Path

        # Add some beach tiles around the water
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if self.grid[x][y] == 2:  # If it's water
                    # Check adjacent tiles
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if (0 <= nx < self.grid_width and
                                    0 <= ny < self.grid_height and
                                    self.grid[nx][ny] == 0):  # If it's grass
                                # Convert to beach
                                self.grid[nx][ny] = 5  # Beach

        # Add some cliff tiles at the edges of the map
        for x in range(self.grid_width):
            for y in range(5):  # Top edge
                if random.random() < 0.7:
                    self.grid[x][y] = 6  # Cliff

            for y in range(self.grid_height - 5, self.grid_height):  # Bottom edge
                if random.random() < 0.7:
                    self.grid[x][y] = 6  # Cliff

        for y in range(self.grid_height):
            for x in range(5):  # Left edge
                if random.random() < 0.7:
                    self.grid[x][y] = 6  # Cliff

            for x in range(self.grid_width - 5, self.grid_width):  # Right edge
                if random.random() < 0.7:
                    self.grid[x][y] = 6  # Cliff

        # Add some stone patches
        for _ in range(5):
            stone_x = random.randint(0, self.grid_width - 1)
            stone_y = random.randint(0, self.grid_height - 1)

            # Don't place stones on farmland, water, or paths
            if self.grid[stone_x][stone_y] == 0:
                self.grid[stone_x][stone_y] = 3  # Stone

    def load_tiles(self):
        print("Loading tile sprites")

        # Make sure the directory exists
        os.makedirs("assets/images/tiles", exist_ok=True)

        # Load actual tile sprites
        try:
            # Load grass tile
            grass_tile = pygame.image.load("assets/images/tiles/Grass_Middle.png").convert_alpha()
            grass_tile = pygame.transform.scale(grass_tile, (self.tile_size, self.tile_size))

            # Load farmland tile
            farmland_tile = pygame.image.load("assets/images/tiles/FarmLand_Tile.png").convert_alpha()
            farmland_tile = pygame.transform.scale(farmland_tile, (self.tile_size, self.tile_size))

            # Load water tile
            water_tile = pygame.image.load("assets/images/tiles/Water_Middle.png").convert_alpha()
            water_tile = pygame.transform.scale(water_tile, (self.tile_size, self.tile_size))

            # Load path tile
            path_tile = pygame.image.load("assets/images/tiles/Path_Middle.png").convert_alpha()
            path_tile = pygame.transform.scale(path_tile, (self.tile_size, self.tile_size))

            # Load beach tile
            beach_tile = pygame.image.load("assets/images/tiles/Beach_Tile.png").convert_alpha()
            beach_tile = pygame.transform.scale(beach_tile, (self.tile_size, self.tile_size))

            # Load cliff tile
            cliff_tile = pygame.image.load("assets/images/tiles/Cliff_Tile.png").convert_alpha()
            cliff_tile = pygame.transform.scale(cliff_tile, (self.tile_size, self.tile_size))

            # Load house
            self.house_image = pygame.image.load("assets/images/buildings/House.png").convert_alpha()
            # Scale house if needed (adjust size as appropriate)
            house_width = 128  # Adjust based on your house image
            house_height = 128  # Adjust based on your house image
            self.house_image = pygame.transform.scale(self.house_image, (house_width, house_height))

            # Create placeholder for stone
            stone_tile = pygame.Surface((self.tile_size, self.tile_size))
            stone_tile.fill((169, 169, 169))  # Gray for stone

            # Store tiles in list
            self.tile_sprites = [
                grass_tile,  # 0: Grass
                farmland_tile,  # 1: Farmland
                water_tile,  # 2: Water
                stone_tile,  # 3: Stone
                path_tile,  # 4: Path
                beach_tile,  # 5: Beach
                cliff_tile  # 6: Cliff
            ]

            print("Tiles carregados com sucesso!")

        except pygame.error as e:
            print(f"Erro ao carregar tiles: {e}")
            # Fallback to colored rectangles if images can't be loaded
            self.tile_sprites = [
                pygame.Surface((self.tile_size, self.tile_size)),  # Grass
                pygame.Surface((self.tile_size, self.tile_size)),  # Farmland
                pygame.Surface((self.tile_size, self.tile_size)),  # Water
                pygame.Surface((self.tile_size, self.tile_size)),  # Stone
                pygame.Surface((self.tile_size, self.tile_size)),  # Path
                pygame.Surface((self.tile_size, self.tile_size)),  # Beach
                pygame.Surface((self.tile_size, self.tile_size))  # Cliff
            ]

            # Color the placeholders for each tile type
            self.tile_sprites[0].fill((34, 139, 34))  # Grass (forest green)
            self.tile_sprites[1].fill((139, 69, 19))  # Farmland (saddle brown)
            self.tile_sprites[2].fill((30, 144, 255))  # Water (dodger blue)
            self.tile_sprites[3].fill((169, 169, 169))  # Stone (dark gray)
            self.tile_sprites[4].fill((210, 180, 140))  # Path (tan)
            self.tile_sprites[5].fill((238, 214, 175))  # Beach (wheat)
            self.tile_sprites[6].fill((105, 105, 105))  # Cliff (dim gray)

            # Create a placeholder for the house
            self.house_image = pygame.Surface((128, 128))
            self.house_image.fill((165, 42, 42))  # Brown for house

    def load_background(self):
        print("Creating background from grass tiles")

        try:
            # Try to load the background image if it exists
            self.background_image = pygame.image.load("assets/images/tiles/world_background.png").convert()
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Background image not found, creating from grass tiles: {e}")

            # Create a background using the grass tile
            if hasattr(self, 'tile_sprites') and len(self.tile_sprites) > 0:
                # Use the grass tile (index 0) to create a background
                grass_tile = self.tile_sprites[0]

                # Create a surface for the background
                self.background_image = pygame.Surface((self.width, self.height))

                # Tile the grass across the background
                for x in range(0, self.width, self.tile_size):
                    for y in range(0, self.height, self.tile_size):
                        self.background_image.blit(grass_tile, (x, y))
            else:
                # Fallback to a colored background if tiles aren't loaded
                self.background_image = pygame.Surface((self.width, self.height))
                self.background_image.fill((34, 139, 34))  # Forest green

    def get_tile_at(self, x, y):
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size

        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            return self.grid[grid_x][grid_y]
        return 0  # Default to grass

    def set_tile_at(self, x, y, tile_type):
        grid_x = x // self.tile_size
        grid_y = y // self.tile_size

        if 0 <= grid_x < self.grid_width and 0 <= grid_y < self.grid_height:
            self.grid[grid_x][grid_y] = tile_type

    def update(self):
        # Update animal and plant managers
        self.animal_manager.update()
        self.plant_manager.update()

    def render(self, screen):
        # Render background
        screen.blit(self.background_image, (0, 0))

        # Render tiles that are different from grass (since grass is already in background)
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                tile_type = self.grid[x][y]
                if tile_type != 0:  # Skip grass tiles (0) as they're in the background
                    screen.blit(self.tile_sprites[tile_type],
                                (x * self.tile_size, y * self.tile_size))

        # Render house (draw after tiles but before plants and animals for proper layering)
        screen.blit(self.house_image, self.house_pos)

        # Render plants and trees
        self.plant_manager.render(screen)

        # Render animals
        self.animal_manager.render(screen)

