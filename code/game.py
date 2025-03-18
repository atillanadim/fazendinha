import pygame
import sys
import os
from .menu import Menu
from .world import World
from .player import Player


class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()

        # Game settings
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pixel Farm")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Create necessary directories
        self.create_directories()

        # Save tree images
        self.save_tree_images()

        # Game states
        self.running = True
        self.in_menu = True

        # Initialize game components
        self.menu = Menu(self)
        self.world = World(self)

        # Initialize player in the center of the screen, but not on top of the house
        self.player = Player(self, self.WIDTH // 2, self.HEIGHT // 2 + 100)

        # Now that world is fully initialized, spawn trees
        self.world.plant_manager.spawn_initial_trees()

        # Load game assets
        self.load_assets()

    def create_directories(self):
        """Create necessary directories for assets"""
        directories = [
            "assets/images/tiles",
            "assets/images/buildings",
            "assets/images/characters",
            "assets/images/animals",
            "assets/images/items",
            "assets/images/tools",
            "assets/images/trees",
            "assets/images/ui",
            "assets/music",
            "assets/sounds"
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")

    def save_tree_images(self):
        """Save tree images from URLs to files"""
        try:
            # Only save if the files don't exist
            if not os.path.exists("assets/images/trees/Oak_Tree.png"):
                # This is a placeholder for downloading images
                # In a real implementation, you would use requests or urllib
                # to download the images from the URLs
                print("Would download tree images here")

                # For now, we'll create placeholder images
                oak_tree = pygame.Surface((64, 96), pygame.SRCALPHA)
                pygame.draw.rect(oak_tree, (101, 67, 33), (24, 48, 16, 48))  # Trunk
                pygame.draw.circle(oak_tree, (34, 139, 34), (32, 32), 24)  # Foliage

                oak_tree_small = pygame.Surface((32, 48), pygame.SRCALPHA)
                pygame.draw.rect(oak_tree_small, (101, 67, 33), (12, 24, 8, 24))  # Trunk
                pygame.draw.circle(oak_tree_small, (34, 139, 34), (16, 16), 12)  # Foliage

                # Save the images
                pygame.image.save(oak_tree, "assets/images/trees/Oak_Tree.png")
                pygame.image.save(oak_tree_small, "assets/images/trees/Oak_Tree_Small.png")

                print("Created placeholder tree images")
        except Exception as e:
            print(f"Error saving tree images: {e}")

    def load_assets(self):
        # This method would load all necessary game assets
        # For demonstration, we'll just print a message
        print("Loading game assets...")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Handle menu events if in menu
            if self.in_menu:
                self.menu.handle_event(event)
            else:
                # Handle game events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.in_menu = True

                # Pass events to player
                self.player.handle_event(event)

    def update(self):
        if self.in_menu:
            self.menu.update()
        else:
            self.world.update()
            self.player.update()
            # Update all game entities here

    def render(self):
        self.screen.fill((0, 0, 0))  # Clear screen

        if self.in_menu:
            self.menu.render(self.screen)
        else:
            self.world.render(self.screen)
            self.player.render(self.screen)
            # Render UI elements

        pygame.display.flip()

    def run(self):
        print("Starting game...")
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

