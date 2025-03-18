import pygame
import os


class Menu:
    def __init__(self, game):
        self.game = game
        self.width = game.WIDTH
        self.height = game.HEIGHT

        # Menu options
        self.options = ["Start Game", "Options", "Exit"]
        self.selected_option = 0

        # Font
        pygame.font.init()
        self.title_font = pygame.font.SysFont("Arial", 64)
        self.option_font = pygame.font.SysFont("Arial", 36)

        # Colors
        self.title_color = (255, 255, 0)
        self.option_color = (255, 255, 255)
        self.selected_color = (255, 0, 0)

        # Background
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill((0, 100, 0))  # Default fallback color

        # Try to load background image
        try:
            self.background_image = pygame.image.load("assets/images/ui/menu_background.png").convert()
            # Scale the image to fit the screen if needed
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            print("Não foi possível carregar a imagem de fundo do menu.")
            self.background_image = None

        # Music
        self.load_music()

    def load_music(self):
        # In a real game, you would load actual music
        print("Loading menu music...")

        # Uncomment these lines when you have the music file
        # pygame.mixer.music.load("assets/music/menu-song.mp3")
        # pygame.mixer.music.play(-1)  # Loop indefinitely

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()

    def select_option(self):
        if self.options[self.selected_option] == "Start Game":
            self.game.in_menu = False
            # pygame.mixer.music.stop()  # Stop menu music
        elif self.options[self.selected_option] == "Options":
            # Options menu would go here
            pass
        elif self.options[self.selected_option] == "Exit":
            self.game.running = False

    def update(self):
        # Menu animations or effects would go here
        pass

    def render(self, screen):
        # Draw background
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.blit(self.background, (0, 0))

        # Draw title
        title_text = self.title_font.render("Pixel Farm", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, self.height // 4))
        screen.blit(title_text, title_rect)

        # Draw options
        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.option_color
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(
                center=(self.width // 2, self.height // 2 + i * 50)
            )
            screen.blit(option_text, option_rect)

