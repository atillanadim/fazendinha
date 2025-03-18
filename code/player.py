import pygame
import os
from .sprite_sheet import SpriteSheet


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 3

        # Movement
        self.moving = False
        self.direction = "down"  # down, up, left, right

        # Animation
        self.frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0

        # Actions
        self.cutting = False
        self.planting = False
        self.watering = False
        self.using_tool = False
        self.current_tool = None  # None, "axe", "hoe", "watering_can"

        # Debug
        self.debug = True

        # Load sprites
        self.load_sprites()

        # Load tool animations
        self.load_tool_animations()

    def _create_colored_rect(self, color):
        # Helper method to create a colored rectangle with a border
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, self.width, self.height))
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.width, self.height), 2)  # Black border
        return surf

    def load_sprites(self):
        try:
            # Make sure the directory exists
            os.makedirs("assets/images/characters", exist_ok=True)

            # Create a fallback sprite first
            fallback_sprite = self._create_colored_rect((255, 0, 0))  # Red for player

            # Try to load farmer sprite sheet
            try:
                farmer_sheet = SpriteSheet("assets/images/characters/PixelFarm_Farmer-Sheet.png")

                # Define frame size
                frame_width = 16
                frame_height = 16

                # Extract frames for each direction and scale them
                down_frames = [pygame.transform.scale(frame, (self.width, self.height))
                               for frame in farmer_sheet.load_strip((0, 0, frame_width, frame_height), 2)]

                up_frames = [pygame.transform.scale(frame, (self.width, self.height))
                             for frame in farmer_sheet.load_strip((frame_width * 2, 0, frame_width, frame_height), 2)]

                left_frames = [pygame.transform.scale(frame, (self.width, self.height))
                               for frame in farmer_sheet.load_strip((frame_width * 4, 0, frame_width, frame_height), 2)]

                right_frames = [pygame.transform.scale(frame, (self.width, self.height))
                                for frame in
                                farmer_sheet.load_strip((frame_width * 6, 0, frame_width, frame_height), 2)]

                # Store animations in dictionary
                self.animations = {
                    "down": down_frames,
                    "up": up_frames,
                    "left": left_frames,
                    "right": right_frames
                }

                print("Farmer sprites loaded successfully!")

            except Exception as e:
                print(f"Error loading farmer sprites: {e}")
                # Use fallback sprites
                self.animations = {
                    "down": [fallback_sprite, fallback_sprite],
                    "up": [fallback_sprite, fallback_sprite],
                    "left": [fallback_sprite, fallback_sprite],
                    "right": [fallback_sprite, fallback_sprite]
                }

        except Exception as e:
            print(f"Critical error in load_sprites: {e}")
            # Last resort fallback
            self.animations = {
                "down": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                "up": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                "left": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                "right": [self._create_colored_rect((255, 0, 0)) for _ in range(2)]
            }

    def load_tool_animations(self):
        try:
            # Make sure the directory exists
            os.makedirs("assets/images/tools", exist_ok=True)

            # Create fallback tool sprites
            axe_sprite = self._create_colored_rect((255, 0, 0))  # Red for axe
            hoe_sprite = self._create_colored_rect((0, 255, 0))  # Green for hoe
            watering_can_sprite = self._create_colored_rect((0, 0, 255))  # Blue for watering can

            # Try to load tool animation sprite sheet
            try:
                tool_sheet = SpriteSheet("assets/images/tools/PixelFarm_Tool Animation-Sheet.png")

                # Define frame size for tools
                frame_width = 16
                frame_height = 16

                # Create a dictionary to store tool animations
                self.tool_animations = {
                    "axe": {
                        "right": [pygame.transform.scale(tool_sheet.image_at((0, 0, frame_width, frame_height)),
                                                         (self.width, self.height)),
                                  pygame.transform.scale(
                                      tool_sheet.image_at((frame_width, 0, frame_width, frame_height)),
                                      (self.width, self.height))],
                        "up": [
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 2, 0, frame_width, frame_height)),
                                                   (self.width, self.height)),
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 3, 0, frame_width, frame_height)),
                                                   (self.width, self.height))],
                        "left": [
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 4, 0, frame_width, frame_height)),
                                                   (self.width, self.height)),
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 5, 0, frame_width, frame_height)),
                                                   (self.width, self.height))],
                        "down": [
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 6, 0, frame_width, frame_height)),
                                                   (self.width, self.height)),
                            pygame.transform.scale(tool_sheet.image_at((frame_width * 7, 0, frame_width, frame_height)),
                                                   (self.width, self.height))]
                    },
                    "hoe": {
                        "right": [
                            pygame.transform.scale(tool_sheet.image_at((0, frame_height, frame_width, frame_height)),
                                                   (self.width, self.height)),
                            pygame.transform.scale(
                                tool_sheet.image_at((frame_width, frame_height, frame_width, frame_height)),
                                (self.width, self.height))],
                        "up": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 2, frame_height, frame_width, frame_height)),
                            (self.width, self.height)),
                               pygame.transform.scale(
                                   tool_sheet.image_at((frame_width * 3, frame_height, frame_width, frame_height)),
                                   (self.width, self.height))],
                        "left": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 4, frame_height, frame_width, frame_height)),
                            (self.width, self.height)),
                                 pygame.transform.scale(
                                     tool_sheet.image_at((frame_width * 5, frame_height, frame_width, frame_height)),
                                     (self.width, self.height))],
                        "down": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 6, frame_height, frame_width, frame_height)),
                            (self.width, self.height)),
                                 pygame.transform.scale(
                                     tool_sheet.image_at((frame_width * 7, frame_height, frame_width, frame_height)),
                                     (self.width, self.height))]
                    },
                    "watering_can": {
                        "right": [pygame.transform.scale(
                            tool_sheet.image_at((0, frame_height * 2, frame_width, frame_height)),
                            (self.width, self.height)),
                                  pygame.transform.scale(
                                      tool_sheet.image_at((frame_width, frame_height * 2, frame_width, frame_height)),
                                      (self.width, self.height))],
                        "up": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 2, frame_height * 2, frame_width, frame_height)),
                            (self.width, self.height)),
                               pygame.transform.scale(
                                   tool_sheet.image_at((frame_width * 3, frame_height * 2, frame_width, frame_height)),
                                   (self.width, self.height))],
                        "left": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 4, frame_height * 2, frame_width, frame_height)),
                            (self.width, self.height)),
                                 pygame.transform.scale(tool_sheet.image_at(
                                     (frame_width * 5, frame_height * 2, frame_width, frame_height)),
                                                        (self.width, self.height))],
                        "down": [pygame.transform.scale(
                            tool_sheet.image_at((frame_width * 6, frame_height * 2, frame_width, frame_height)),
                            (self.width, self.height)),
                                 pygame.transform.scale(tool_sheet.image_at(
                                     (frame_width * 7, frame_height * 2, frame_width, frame_height)),
                                                        (self.width, self.height))]
                    }
                }

                print("Tool animations loaded successfully!")

            except Exception as e:
                print(f"Error loading tool animations: {e}")
                # Use fallback tool sprites
                self.tool_animations = {
                    "axe": {
                        "down": [axe_sprite, axe_sprite],
                        "up": [axe_sprite, axe_sprite],
                        "left": [axe_sprite, axe_sprite],
                        "right": [axe_sprite, axe_sprite]
                    },
                    "hoe": {
                        "down": [hoe_sprite, hoe_sprite],
                        "up": [hoe_sprite, hoe_sprite],
                        "left": [hoe_sprite, hoe_sprite],
                        "right": [hoe_sprite, hoe_sprite]
                    },
                    "watering_can": {
                        "down": [watering_can_sprite, watering_can_sprite],
                        "up": [watering_can_sprite, watering_can_sprite],
                        "left": [watering_can_sprite, watering_can_sprite],
                        "right": [watering_can_sprite, watering_can_sprite]
                    }
                }

        except Exception as e:
            print(f"Critical error in load_tool_animations: {e}")
            # Last resort fallback
            self.tool_animations = {
                "axe": {
                    "down": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                    "up": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                    "left": [self._create_colored_rect((255, 0, 0)) for _ in range(2)],
                    "right": [self._create_colored_rect((255, 0, 0)) for _ in range(2)]
                },
                "hoe": {
                    "down": [self._create_colored_rect((0, 255, 0)) for _ in range(2)],
                    "up": [self._create_colored_rect((0, 255, 0)) for _ in range(2)],
                    "left": [self._create_colored_rect((0, 255, 0)) for _ in range(2)],
                    "right": [self._create_colored_rect((0, 255, 0)) for _ in range(2)]
                },
                "watering_can": {
                    "down": [self._create_colored_rect((0, 0, 255)) for _ in range(2)],
                    "up": [self._create_colored_rect((0, 0, 255)) for _ in range(2)],
                    "left": [self._create_colored_rect((0, 0, 255)) for _ in range(2)],
                    "right": [self._create_colored_rect((0, 0, 255)) for _ in range(2)]
                }
            }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.current_tool = "axe"
                print("Selected axe")
            elif event.key == pygame.K_2:
                self.current_tool = "hoe"
                print("Selected hoe")
            elif event.key == pygame.K_3:
                self.current_tool = "watering_can"
                print("Selected watering can")

            if event.key == pygame.K_SPACE:
                self.using_tool = True

                # Perform action based on current tool
                if self.current_tool == "axe":
                    self.cutting = True
                    # Try to cut a tree
                    world = self.game.world
                    tile_x = (self.x + self.width // 2) // world.tile_size
                    tile_y = (self.y + self.height // 2) // world.tile_size

                    # Get the position in front of the player based on direction
                    if self.direction == "up":
                        tile_y -= 1
                    elif self.direction == "down":
                        tile_y += 1
                    elif self.direction == "left":
                        tile_x -= 1
                    elif self.direction == "right":
                        tile_x += 1

                    # Try to cut a tree at this position
                    tree_x = tile_x * world.tile_size
                    tree_y = tile_y * world.tile_size
                    world.plant_manager.cut_tree(tree_x, tree_y)

                elif self.current_tool == "hoe":
                    self.planting = True
                    # Try to plant on farmland
                    world = self.game.world
                    tile_x = (self.x + self.width // 2) // world.tile_size
                    tile_y = (self.y + self.height // 2) // world.tile_size

                    # Get the position in front of the player based on direction
                    if self.direction == "up":
                        tile_y -= 1
                    elif self.direction == "down":
                        tile_y += 1
                    elif self.direction == "left":
                        tile_x -= 1
                    elif self.direction == "right":
                        tile_x += 1

                    if 0 <= tile_x < world.grid_width and 0 <= tile_y < world.grid_height:
                        # Check if the tile is farmland
                        if world.grid[tile_x][tile_y] == 1:  # Farmland
                            # Try to plant a seed
                            plant_x = tile_x * world.tile_size
                            plant_y = tile_y * world.tile_size
                            world.plant_manager.plant_seed(plant_x, plant_y, "wheat")

                elif self.current_tool == "watering_can":
                    self.watering = True
                    # Try to water a plant
                    world = self.game.world
                    tile_x = (self.x + self.width // 2) // world.tile_size
                    tile_y = (self.y + self.height // 2) // world.tile_size

                    # Get the position in front of the player based on direction
                    if self.direction == "up":
                        tile_y -= 1
                    elif self.direction == "down":
                        tile_y += 1
                    elif self.direction == "left":
                        tile_x -= 1
                    elif self.direction == "right":
                        tile_x += 1

                    # Try to water a plant at this position
                    plant_x = tile_x * world.tile_size
                    plant_y = tile_y * world.tile_size
                    world.plant_manager.water_plant(plant_x, plant_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.using_tool = False
                self.cutting = False
                self.planting = False
                self.watering = False

    def update(self):
        # Handle movement
        keys = pygame.key.get_pressed()

        # Reset movement flag
        self.moving = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = "left"
            self.moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
            self.direction = "right"
            self.moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
            self.direction = "up"
            self.moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
            self.direction = "down"
            self.moving = True

        # Keep player on screen
        self.x = max(0, min(self.game.WIDTH - self.width, self.x))
        self.y = max(0, min(self.game.HEIGHT - self.height, self.y))

        # Update animation
        if self.moving or self.using_tool:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                if self.using_tool:
                    # Tool animations might have different frame counts
                    if self.current_tool and self.direction in self.tool_animations.get(self.current_tool, {}):
                        tool_frames = self.tool_animations[self.current_tool][self.direction]
                        self.frame = (self.frame + 1) % len(tool_frames)
                else:
                    # Regular movement animation
                    self.frame = (self.frame + 1) % len(self.animations[self.direction])

    def render(self, screen):
        # Determine which animation to use
        if self.using_tool and self.current_tool:
            # Use tool animation if available
            if self.direction in self.tool_animations.get(self.current_tool, {}):
                tool_frames = self.tool_animations[self.current_tool][self.direction]
                frame_index = min(self.frame, len(tool_frames) - 1)
                current_frame = tool_frames[frame_index]
                screen.blit(current_frame, (self.x, self.y))

                # Debug outline
                if self.debug:
                    pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)
                return

        # Use regular movement animation
        animation_key = self.direction
        frame_index = min(self.frame, len(self.animations[animation_key]) - 1)
        current_frame = self.animations[animation_key][frame_index]

        # Draw player
        screen.blit(current_frame, (self.x, self.y))

        # Debug outline
        if self.debug:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 1)

