import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    A class to manage bullets fired by the ship.

    Inherits from the Pygame Sprite class and handles the bullet's creation, movement, and rendering on the screen.

    Attributes:
        game (object): The game instance, providing access to game settings and screen.
        screen (Surface): The Pygame screen object where the bullet is displayed.
        settings (Settings): The settings object that defines the bullet's properties.
        image (Surface): The Pygame surface representing the bullet's visual appearance.
        rect (Rect): The Pygame rect representing the bullet's position and size.
        y (float): The vertical position of the bullet, used for smooth movement.
    """
    
    def __init__(self, game):
        """
        Initializes the bullet, setting its position and loading the appropriate image.

        Args:
            game (object): The game instance that provides access to game settings and the screen.
        """
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings

        # Load and scale the bullet image
        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (
            self.settings.bullet_w, self.settings.bullet_h))
        self.rect = self.image.get_rect()

        # Set initial position of the bullet (at the ship's position)
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)

    def update(self) -> None:
        """
        Updates the position of the bullet as it moves upwards on the screen.
        The bullet moves based on the speed defined in the game settings.

        This method is called during each frame of the game to update the bullet's position.
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self):
        """
        Draws the bullet on the screen at its current position.

        This method is called during each frame to render the bullet.
        """
        self.screen.blit(self.image, self.rect)
