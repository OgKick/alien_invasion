import pygame.font

class Button:
    """
    A Button class that represents a clickable button in the game.

    Attributes:
        game (Game): The game instance where the button will be displayed.
        screen (Surface): The screen where the button will be drawn.
        screen_rect (Rect): The rectangle representing the screen's boundaries.
        settings (Settings): The settings containing various configurations for the button.
        font (Font): The font used to render the button's message.
        rect (Rect): The rectangle that defines the button's position and size.
        msg_image (Surface): The image of the button's message.
        msg_image_rect (Rect): The rectangle representing the position of the message.
    """

    def __init__(self, game, msg):
        """
        Initializes the button with the specified message.

        Args:
            game (Game): The game instance where the button will be displayed.
            msg (str): The message to be displayed on the button.
        """
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.font = pygame.font.Font(self.settings.title_font, self.settings.button_font_size)
        self.rect = pygame.Rect(0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Prepares the message to be rendered on the button.

        Args:
            msg (str): The message to be displayed on the button.

        This method creates a surface with the rendered text, sets the text's position 
        at the center of the button, and prepares the button's message to be drawn.
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw(self):
        """
        Draws the button on the screen.

        Fills the button's rectangle with the button's background color and draws the 
        message text at the center of the button.
        """
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    
    def check_clicked(self, mouse_pos):
        """
        Checks if the button was clicked based on the mouse position.

        Args:
            mouse_pos (tuple): A tuple representing the mouse position (x, y).

        Returns:
            bool: True if the mouse position is within the button's rectangle, 
                  indicating that the button was clicked; False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)
