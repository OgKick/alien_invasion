import math
import pygame
from alien import Alien

class AlienFleet:
    """
    A class to manage the fleet of aliens in the game.

    Attributes:
    game (AlienInvasion): The game instance to access game settings and resources.
    settings (Settings): The game settings to control fleet and alien behavior.
    fleet (pygame.sprite.Group): A group of all aliens in the fleet.
    direction (int): The current direction of movement for the entire alien fleet.
    """
    def __init__(self, game) -> None:
        """
        Initializes the AlienFleet instance.

        Args:
        game (AlienInvasion): The main game object that provides access to settings and resources.
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.direction = 1
        self.create_fleet()

    def create_fleet(self):
        """
        Creates the initial fleet of aliens in a snowflake pattern.

        The snowflake pattern consists of multiple arms, each containing a set number
        of aliens, with aliens spaced out along the arms. Additionally, aliens are placed 
        in the center of the screen.
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        # Calculate the radius for the snowflake pattern
        radius = min(screen_w, screen_h) // 4  # Adjust the radius size to fit your screen
        num_arms = 6  # Number of arms for the snowflake
        num_aliens_per_arm = 5  # Number of aliens per arm

        alien_spacing = alien_w * 1.5  # Add some space between aliens to minimize overlap

        # Create aliens along the arms
        for arm in range(num_arms):
            arm_angle = (360 / num_arms) * arm  # 60-degree separation between arms

            # Create aliens for this arm
            for i in range(num_aliens_per_arm):
                # Distribute aliens along the arm (from center to outer radius)
                alien_distance = (i + 1) * alien_spacing  # Use alien_spacing to space them apart
                x_offset = int(math.cos(math.radians(arm_angle)) * alien_distance)
                y_offset = int(math.sin(math.radians(arm_angle)) * alien_distance)

                # Adjust the alien's position
                current_x = screen_w // 2 + x_offset - alien_w // 2
                current_y = screen_h // 2 + y_offset - alien_h // 2

                # Create alien at the calculated position
                self._create_alien(current_x, current_y)

        # Optionally, you can also add aliens to the center of the snowflake.
        self._create_alien(screen_w // 2, screen_h // 2)  # Center of the snowflake

    def _create_alien(self, current_x, current_y):
        """
        Creates a new alien at a specific position and adds it to the fleet.

        Args:
        current_x (int): The x-coordinate for the new alien.
        current_y (int): The y-coordinate for the new alien.
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def update_fleet(self):
        """
        Updates the position and state of all aliens in the fleet.
        This method also checks for any edge collisions.
        """
        self._check_fleet_edges()
        self.fleet.update()

    def _check_fleet_edges(self):
        """
        Checks if any alien in the fleet has reached the edge of the screen.
        If so, the fleet's direction is changed.
        """
        for alien in self.fleet:
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def draw_fleet(self):
        """
        Draws all the aliens in the fleet to the screen.
        """
        for alien in self.fleet:
            alien.draw()

    def _change_fleet_direction(self):
        """
        Changes the direction of movement for the entire fleet and drops the fleet down.
        This is called when an alien reaches the edge of the screen.
        """
        for alien in self.fleet:
            alien.rect.y += self.settings.fleet_drop_amount
        self.direction *= -1

    def check_fleet_bottom(self):
        """
        Checks if any alien has reached the bottom of the screen.

        Returns:
        bool: True if any alien has reached the bottom, False otherwise.
        """
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
