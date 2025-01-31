import pygame

class Ship:
    """
    A class to manage the player's ship.

    The ship can move left and right on the screen and is responsible for rendering itself and handling collisions.

    Attributes:
        game (object): The game instance, which provides access to settings and the screen.
        settings (Settings): The settings object that defines the ship's properties.
        screen (Surface): The Pygame screen object where the ship is displayed.
        boundaries (Rect): The screen's boundaries, used to prevent the ship from moving off-screen.
        image (Surface): The Pygame surface representing the ship's visual appearance.
        rect (Rect): The Pygame rect representing the ship's position and size.
        x (float): The horizontal position of the ship, used for smooth movement.
        moving_left (bool): Flag indicating if the ship is moving left.
        moving_right (bool): Flag indicating if the ship is moving right.
    """

    def __init__(self, game) -> None:
        """
        Initializes the ship and sets its starting position.

        Args:
            game (object): The game instance that provides access to settings and the screen.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        
        # Load and scale the ship image
        self.image = pygame.image.load(self.game.settings.ship_file)
        self.image = pygame.transform.scale(self.image, 
            (self.settings.ship_w, self.settings.ship_h))
        self.rect = self.image.get_rect()
        
        # Center the ship on the screen
        self.center_ship()
        
        # The x-coordinate is stored as a float for smooth movement
        self.x = float(self.rect.x)
        self.moving_left = False
        self.moving_right = False

    def update(self):
        """
        Updates the ship's position based on user input.

        The ship moves left or right depending on the state of the movement flags
        and the boundaries of the screen. The position is updated every frame.
        """
        temp_speed = self.game.settings.ship_speed
        
        # Check if the ship is moving right and within screen bounds
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += temp_speed
        
        # Check if the ship is moving left and within screen bounds
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= temp_speed

        # Update the rect with the new position
        self.rect.x = self.x

    def draw(self):
        """
        Draws the ship on the screen.

        This method is called each frame to render the ship at its current position.
        """
        self.screen.blit(self.image, self.rect)

    def ship_hit(self):
        """
        Handles the event when the ship is hit by an alien or bullet.

        This method centers the ship back to its starting position after a collision.
        """
        self.center_ship()

    def center_ship(self):
        """
        Centers the ship at the bottom of the screen.

        This method places the ship at the midpoint of the screen's width and the bottom of the screen.
        """
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)
