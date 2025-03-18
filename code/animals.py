import pygame
import random
import os
from .sprite_sheet import SpriteSheet


class Animal:
    def __init__(self, game, x, y, animal_type, is_baby=False):
        self.game = game
        self.x = x
        self.y = y
        self.animal_type = animal_type
        self.is_baby = is_baby

        # Set size based on whether it's a baby or adult
        if is_baby:
            self.width = 24
            self.height = 24
        else:
            self.width = 32
            self.height = 32

        # Movement
        self.speed = 1 if not is_baby else 0.7
        self.direction = random.choice(["down", "up", "left", "right"])
        self.moving = False
        self.move_timer = 0
        self.move_cooldown = random.uniform(1.0, 3.0)  # Time between movements
        self.move_duration = random.uniform(0.5, 2.0)  # How long to move

        # Animation
        self.frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

        # Growth (for baby animals)
        self.age = 0
        self.growth_rate = 0.001  # How fast the animal grows

        # Debug
        self.debug = True

        # Load sprites
        self.load_sprites()

    def _create_colored_rect(self, color):
        # Helper method to create a colored rectangle with a border
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, (0, 0, self.width, self.height))
        pygame.draw.rect(surf, (0, 0, 0), (0, 0, self.width, self.height), 2)  # Black border
        return surf

    def _get_animal_color(self):
        # Helper method to get color based on animal type
        if self.animal_type == "chicken":
            return (255, 255, 150) if not self.is_baby else (255, 255, 0)
        elif self.animal_type == "cow":
            return (200, 200, 200) if not self.is_baby else (255, 200, 200)
        elif self.animal_type == "sheep":
            return (240, 240, 240) if not self.is_baby else (255, 240, 240)
        return (255, 255, 255)  # Default white

    def load_sprites(self):
        try:
            # Make sure the directory exists
            os.makedirs("assets/images/animals", exist_ok=True)

            # Create fallback sprite first
            fallback_sprite = self._create_colored_rect(self._get_animal_color())

            # Try to load the appropriate sprite sheet
            try:
                # Determine which sprite sheet to load based on animal type and age
                if self.animal_type == "chicken":
                    if self.is_baby:
                        sheet_path = "assets/images/animals/PixelFarm_BabyChicken-Sheet.png"
                        frame_count = 7  # Number of frames in the baby chicken sheet
                    else:
                        sheet_path = "assets/images/animals/PixelFarm_Chicken-Sheet.png"
                        frame_count = 7  # Number of frames in the chicken sheet
                elif self.animal_type == "cow":
                    if self.is_baby:
                        sheet_path = "assets/images/animals/PixelFarm_BabyCow-Sheet.png"
                        frame_count = 6  # Number of frames in the baby cow sheet
                    else:
                        sheet_path = "assets/images/animals/PixelFarm_Cow-Sheet.png"
                        frame_count = 6  # Number of frames in the cow sheet
                elif self.animal_type == "sheep":
                    if self.is_baby:
                        sheet_path = "assets/images/animals/PixelFarm_BabySheep-Sheet.png"
                        frame_count = 6  # Number of frames in the baby sheep sheet
                    else:
                        sheet_path = "assets/images/animals/PixelFarm_Sheep-Sheet.png"
                        frame_count = 6  # Number of frames in the sheep sheet
                else:
                    raise ValueError(f"Unknown animal type: {self.animal_type}")

                # Load the sprite sheet
                sheet = SpriteSheet(sheet_path)

                # Define frame size (16x16 pixels for the original sprites)
                frame_width = 16
                frame_height = 16

                # Load all frames from the sheet
                frames = sheet.load_strip((0, 0, frame_width, frame_height), frame_count)

                # Scale frames to the appropriate size
                scaled_frames = [pygame.transform.scale(frame, (self.width, self.height)) for frame in frames]

                # Organize frames into animations
                self.animations = {
                    "down": scaled_frames[:2],
                    "up": scaled_frames[2:4] if len(scaled_frames) > 3 else scaled_frames[:2],
                    "left": scaled_frames[4:6] if len(scaled_frames) > 5 else scaled_frames[:2],
                    "right": scaled_frames[4:6] if len(scaled_frames) > 5 else scaled_frames[:2],
                    "idle": [scaled_frames[0]]  # Use first frame for idle
                }

                print(f"Loaded sprites for {self.animal_type} (baby: {self.is_baby})")

            except Exception as e:
                print(f"Error loading animal sprites: {e}")
                # Use fallback sprites
                self.animations = {
                    "down": [fallback_sprite, fallback_sprite],
                    "up": [fallback_sprite, fallback_sprite],
                    "left": [fallback_sprite, fallback_sprite],
                    "right": [fallback_sprite, fallback_sprite],
                    "idle": [fallback_sprite]
                }

        except Exception as e:
            print(f"Critical error in animal load_sprites: {e}")
            # Last resort fallback
            color = self._get_animal_color()
            self.animations = {
                "down": [self._create_colored_rect(color) for _ in range(2)],
                "up": [self._create_colored_rect(color) for _ in range(2)],
                "left": [self._create_colored_rect(color) for _ in range(2)],
                "right": [self._create_colored_rect(color) for _ in range(2)],
                "idle": [self._create_colored_rect(color)]
            }

    def update(self):
        # Handle growth for baby animals
        if self.is_baby:
            self.age += self.growth_rate
            if self.age >= 1.0:
                self.is_baby = False
                self.width = 32
                self.height = 32
                self.speed = 1
                self.load_sprites()  # Reload sprites with adult size

        # Handle movement
        self.move_timer += 1 / 60  # Assuming 60 FPS

        if self.moving:
            if self.move_timer >= self.move_duration:
                self.moving = False
                self.move_timer = 0
                self.move_cooldown = random.uniform(1.0, 3.0)
            else:
                # Move in the current direction
                if self.direction == "left":
                    self.x -= self.speed
                elif self.direction == "right":
                    self.x += self.speed
                elif self.direction == "up":
                    self.y -= self.speed
                elif self.direction == "down":
                    self.y += self.speed

                # Keep animal on screen
                self.x = max(0, min(self.game.WIDTH - self.width, self.x))
                self.y = max(0, min(self.game.HEIGHT - self.height, self.y))
        else:
            if self.move_timer >= self.move_cooldown:
                self.moving = True
                self.move_timer = 0
                self.move_duration = random.uniform(0.5, 2.0)
                self.direction = random.choice(["down", "up", "left", "right"])

        # Update animation
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            animation_key = self.direction if self.moving else "idle"
            self.frame = (self.frame + 1) % len(self.animations[animation_key])

    def render(self, screen):
        # Determine which animation to use
        animation_key = self.direction if self.moving else "idle"

        # Get current frame
        frame_index = min(self.frame, len(self.animations[animation_key]) - 1)
        current_frame = self.animations[animation_key][frame_index]

        # Draw animal
        screen.blit(current_frame, (self.x, self.y))

        # Debug outline
        if self.debug:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height), 1)


class AnimalManager:
    def __init__(self, game):
        self.game = game
        self.animals = []

        # Spawn some initial animals
        self.spawn_initial_animals()

    def spawn_initial_animals(self):
        # Spawn some chickens
        for _ in range(3):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "chicken", is_baby=False))

        # Spawn some baby chickens
        for _ in range(2):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "chicken", is_baby=True))

        # Spawn some cows
        for _ in range(2):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "cow", is_baby=False))

        # Spawn some baby cows
        for _ in range(1):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "cow", is_baby=True))

        # Spawn some sheep
        for _ in range(2):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "sheep", is_baby=False))

        # Spawn some baby sheep
        for _ in range(1):
            x = random.randint(100, self.game.WIDTH - 100)
            y = random.randint(100, self.game.HEIGHT - 100)
            self.animals.append(Animal(self.game, x, y, "sheep", is_baby=True))

    def update(self):
        for animal in self.animals:
            animal.update()

    def render(self, screen):
        # Sort animals by y-coordinate for proper depth
        sorted_animals = sorted(self.animals, key=lambda animal: animal.y)

        for animal in sorted_animals:
            animal.render(screen)

