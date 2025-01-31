import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    Represents a single alien in the fleet. Inherits from the Pygame Sprite class.

    Attributes:
        fleet (Fleet): The fleet that this alien is a part of.
        game (Game): The game instance where the alien exists.
        settings (Settings): The settings for the game, including alien size and speed.
        screen (Surface): The screen where the alien will be drawn.
        boundaries (Rect): The boundaries of the screen to check the alien's position.
        image (Surface): The image of the alien.
        rect (Rect): The rectangular area of the alien image.
        x (float): The x-coordinate of the alien, used for movement calculations.
    """

    def __init__(self, fleet, x, y):
        """
        Initializes an Alien object.

        Args:
            fleet (Fleet): The fleet that this alien belongs to.
            x (int): The x-coordinate of the alien.
            y (int): The y-coordinate of the alien.
        """
        super().__init__()
        self.fleet = fleet
        self.game = fleet.game
        self.settings = fleet.game.settings
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w, self.settings.alien_h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)

    def update(self):
        """
        Updates the position of the alien based on the fleet's direction and speed.

        Moves the alien horizontally on the screen by adjusting its x-coordinate.
        The movement is based on the fleet's current direction and the fleet speed.
        """
        tmp_speed = self.settings.fleet_speed
        self.x += tmp_speed * self.fleet.direction
        self.rect.x = self.x

    def check_edges(self):
        """
        Checks if the alien has reached the edge of the screen.

        Returns:
            bool: True if the alien has reached the left or right edge of the screen, False otherwise.
        """
        return (self.rect.left <= self.boundaries.left 
                or self.rect.right >= self.boundaries.right)

    def draw(self):
        """
        Draws the alien on the screen.

        Uses the Pygame `blit` method to render the alien image at its current position.
        """
        self.screen.blit(self.image, self.rect)
