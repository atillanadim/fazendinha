import pygame
import random
import os
from .sprite_sheet import SpriteSheet


class Plant:
    def __init__(self, game, x, y, plant_type):
        self.game = game
        self.x = x
        self.y = y
        self.plant_type = plant_type
        self.width = 32
        self.height = 32

        # Growth stages
        self.growth_stage = 0  # 0: seed, 1: sprout, 2: growing, 3: mature
        self.max_growth_stage = 3
        self.growth_timer = 0
        self.growth_rate = 0.005  # How fast the plant grows

        # Watering
        self.watered = False
        self.water_level = 0
        self.water_drain_rate = 0.001

        # Load sprites
        self.load_sprites()

    def load_sprites(self):
        try:
            # Make sure the directory exists
            os.makedirs("assets/images/items", exist_ok=True)

            # Load item sprite sheet for crops
            item_sheet = SpriteSheet("assets/images/items/PixelFarm_Item.png")

            # Define frame size
            frame_width = 16
            frame_height = 16

            # Create placeholder for growth stage sprites
            self.stage_sprites = [pygame.Surface((self.width, self.height), pygame.SRCALPHA) for _ in range(4)]

            # Extract crop sprites based on plant type
            # The item sheet has different crops at different positions
            if self.plant_type == "wheat":
                # Use the wheat/grain sprite from the item sheet
                crop_sprite = item_sheet.image_at((frame_width * 2, 0, frame_width, frame_height))
                crop_sprite = pygame.transform.scale(crop_sprite, (self.width, self.height))
            elif self.plant_type == "carrot":
                # Use the carrot sprite from the item sheet
                crop_sprite = item_sheet.image_at((frame_width * 3, 0, frame_width, frame_height))
                crop_sprite = pygame.transform.scale(crop_sprite, (self.width, self.height))
            else:
                # Default crop sprite
                crop_sprite = item_sheet.image_at((frame_width * 2, 0, frame_width, frame_height))
                crop_sprite = pygame.transform.scale(crop_sprite, (self.width, self.height))

            # Create growth stage sprites
            # Stage 0: Small dirt mound
            self.stage_sprites[0].fill((139, 69, 19, 100))  # Semi-transparent brown
            pygame.draw.circle(self.stage_sprites[0], (101, 67, 33), (self.width // 2, self.height // 2), 5)

            # Stage 1: Small sprout
            self.stage_sprites[1].fill((0, 0, 0, 0))  # Transparent
            pygame.draw.rect(self.stage_sprites[1], (101, 67, 33), (self.width // 2 - 2, self.height // 2, 4, 8))
            pygame.draw.circle(self.stage_sprites[1], (50, 205, 50), (self.width // 2, self.height // 2 - 2), 3)

            # Stage 2: Growing plant
            self.stage_sprites[2].fill((0, 0, 0, 0))  # Transparent
            pygame.draw.rect(self.stage_sprites[2], (101, 67, 33), (self.width // 2 - 2, self.height // 2, 4, 12))
            pygame.draw.circle(self.stage_sprites[2], (34, 139, 34), (self.width // 2, self.height // 2 - 6), 6)

            # Stage 3: Mature crop (use the crop sprite)
            self.stage_sprites[3] = crop_sprite

            print(f"Loaded sprites for {self.plant_type}")

        except Exception as e:
            print(f"Error loading plant sprites: {e}")
            # Fallback to colored rectangles if images can't be loaded
            if self.plant_type == "wheat":
                colors = [(139, 69, 19), (205, 133, 63), (218, 165, 32), (255, 215, 0)]
            elif self.plant_type == "carrot":
                colors = [(139, 69, 19), (205, 133, 63), (255, 140, 0), (255, 69, 0)]
            elif self.plant_type == "tomato":
                colors = [(139, 69, 19), (34, 139, 34), (50, 205, 50), (255, 0, 0)]
            else:
                colors = [(100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250)]

            for i, surf in enumerate(self.stage_sprites):
                surf.fill(colors[i])

    def water(self):
        self.watered = True
        self.water_level = 1.0

    def update(self):
        # Handle watering effect
        if self.watered:
            self.water_level -= self.water_drain_rate
            if self.water_level <= 0:
                self.watered = False
                self.water_level = 0

        # Handle growth
        if self.growth_stage < self.max_growth_stage:
            growth_multiplier = 2.0 if self.watered else 1.0
            self.growth_timer += self.growth_rate * growth_multiplier

            if self.growth_timer >= 1:
                self.growth_timer = 0
                self.growth_stage += 1

    def render(self, screen):
        # Draw plant at current growth stage
        current_sprite = self.stage_sprites[min(self.growth_stage, len(self.stage_sprites) - 1)]
        screen.blit(current_sprite, (self.x, self.y))

        # Draw water indicator if watered
        if self.watered:
            water_indicator = pygame.Surface((self.width, 5))
            water_indicator.fill((0, 0, 255))
            screen.blit(water_indicator, (self.x, self.y + self.height + 2))


class Tree:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.width = 64
        self.height = 96

        # Growth stages
        self.growth_stage = random.randint(0, 3)  # 0: sapling, 1: young, 2: growing, 3: mature
        self.max_growth_stage = 3
        self.growth_timer = 0
        self.growth_rate = 0.002  # Trees grow slower than plants

        # Tree state
        self.health = 100
        self.cut_progress = 0
        self.cut_threshold = 5  # Number of cuts needed to fell the tree

        # Load sprites
        self.load_sprites()

    def load_sprites(self):
        try:
            # Make sure the directory exists
            os.makedirs("assets/images/trees", exist_ok=True)

            # Load tree sprites
            small_tree = pygame.image.load("assets/images/trees/Oak_Tree_Small.png").convert_alpha()
            large_tree = pygame.image.load("assets/images/trees/Oak_Tree.png").convert_alpha()

            # Create sprites for different growth stages
            self.stage_sprites = [
                pygame.transform.scale(small_tree, (32, 48)),  # Sapling (smallest)
                pygame.transform.scale(small_tree, (48, 64)),  # Young (small)
                pygame.transform.scale(large_tree, (56, 80)),  # Growing (medium)
                pygame.transform.scale(large_tree, (64, 96))  # Mature (full size)
            ]

            print("Tree sprites loaded successfully!")

        except Exception as e:
            print(f"Error loading tree sprites: {e}")
            # Create simple tree sprites as fallback
            self.stage_sprites = [
                pygame.Surface((32, 48), pygame.SRCALPHA),  # Sapling
                pygame.Surface((48, 64), pygame.SRCALPHA),  # Young
                pygame.Surface((56, 80), pygame.SRCALPHA),  # Growing
                pygame.Surface((64, 96), pygame.SRCALPHA)  # Mature
            ]

            # Draw simple tree shapes
            for i, surf in enumerate(self.stage_sprites):
                # Draw trunk
                trunk_width = max(4, int(surf.get_width() * 0.2))
                trunk_height = int(surf.get_height() * 0.6)
                trunk_x = (surf.get_width() - trunk_width) // 2
                trunk_y = surf.get_height() - trunk_height

                pygame.draw.rect(surf, (101, 67, 33), (trunk_x, trunk_y, trunk_width, trunk_height))

                # Draw foliage (bigger for more mature trees)
                foliage_radius = int(surf.get_width() * (0.3 + i * 0.1))
                foliage_x = surf.get_width() // 2
                foliage_y = trunk_y - foliage_radius // 2

                pygame.draw.circle(surf, (34, 139, 34), (foliage_x, foliage_y), foliage_radius)

    def cut(self):
        if self.growth_stage == self.max_growth_stage:  # Only mature trees can be cut
            self.cut_progress += 1
            return self.cut_progress >= self.cut_threshold
        return False

    def update(self):
        # Handle growth
        if self.growth_stage < self.max_growth_stage:
            self.growth_timer += self.growth_rate

            if self.growth_timer >= 1:
                self.growth_timer = 0
                self.growth_stage += 1

    def render(self, screen):
        # Draw tree at current growth stage
        current_sprite = self.stage_sprites[min(self.growth_stage, len(self.stage_sprites) - 1)]

        # Calculate position to center the tree sprite
        sprite_width, sprite_height = current_sprite.get_size()
        pos_x = self.x + (self.width - sprite_width) // 2
        pos_y = self.y + (self.height - sprite_height)

        screen.blit(current_sprite, (pos_x, pos_y))

        # Draw cut progress if being cut
        if self.cut_progress > 0 and self.growth_stage == self.max_growth_stage:
            progress_width = (self.width * self.cut_progress) // self.cut_threshold
            progress_bar = pygame.Surface((progress_width, 5))
            progress_bar.fill((255, 0, 0))
            screen.blit(progress_bar, (self.x, self.y + self.height + 5))


class PlantManager:
    def __init__(self, game):
        self.game = game
        self.plants = []
        self.trees = []

        # We'll spawn trees later, not during initialization
        # This avoids the circular dependency

    def spawn_initial_trees(self):
        # This method should be called after the world is fully initialized
        # Spawn some trees around the map, but not in the farmland area
        world = self.game.world

        for _ in range(10):
            # Try to find a suitable location for a tree
            attempts = 0
            while attempts < 20:  # Limit attempts to avoid infinite loop
                x = random.randint(50, self.game.WIDTH - 100)
                y = random.randint(50, self.game.HEIGHT - 100)

                # Check if this position is on grass (not farmland, water, or stone)
                grid_x = x // world.tile_size
                grid_y = y // world.tile_size

                if (0 <= grid_x < world.grid_width and
                        0 <= grid_y < world.grid_height and
                        world.grid[grid_x][grid_y] == 0):

                    # Check if it's not too close to the house
                    house_center_x = world.house_pos[0] + 64
                    house_center_y = world.house_pos[1] + 64

                    if ((x - house_center_x) ** 2 + (y - house_center_y) ** 2) > 150 ** 2:
                        # Not too close to the house, add the tree
                        self.trees.append(Tree(self.game, x, y))
                        break

                attempts += 1

    def plant_seed(self, x, y, plant_type):
        # Check if there's already a plant or tree at this location
        for plant in self.plants:
            if abs(plant.x - x) < 32 and abs(plant.y - y) < 32:
                return False

        for tree in self.trees:
            if abs(tree.x - x) < 64 and abs(tree.y - y) < 64:
                return False

        # Plant a new seed
        self.plants.append(Plant(self.game, x, y, plant_type))
        return True

    def plant_tree(self, x, y):
        # Check if there's already a plant or tree at this location
        for plant in self.plants:
            if abs(plant.x - x) < 32 and abs(plant.y - y) < 32:
                return False

        for tree in self.trees:
            if abs(tree.x - x) < 64 and abs(tree.y - y) < 64:
                return False

        # Plant a new tree
        self.trees.append(Tree(self.game, x, y))
        self.trees[-1].growth_stage = 0  # Start as a sapling
        return True

    def water_plant(self, x, y):
        # Find the closest plant to water
        for plant in self.plants:
            if abs(plant.x - x) < 32 and abs(plant.y - y) < 32:
                plant.water()
                return True
        return False

    def cut_tree(self, x, y):
        # Find the closest tree to cut
        for i, tree in enumerate(self.trees):
            if abs(tree.x - x) < 64 and abs(tree.y - y) < 64:
                if tree.cut():
                    # Tree has been fully cut, remove it
                    self.trees.pop(i)
                    return True
                return False
        return False

    def update(self):
        for plant in self.plants:
            plant.update()

        for tree in self.trees:
            tree.update()

    def render(self, screen):
        # Sort plants and trees by y-coordinate for proper depth
        all_objects = [(obj, obj.y + obj.height) for obj in self.plants + self.trees]
        sorted_objects = sorted(all_objects, key=lambda item: item[1])

        for obj, _ in sorted_objects:
            obj.render(screen)

