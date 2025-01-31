import pygame.font

class HUD:
    """
    The HUD (Heads-Up Display) class is responsible for rendering all on-screen text
    and images that display the player's current game statistics, such as score, 
    high score, maximum score, level, and remaining lives.

    Attributes:
        game (Game): The game instance, which contains settings and game statistics.
        settings (Settings): The settings object containing game configurations.
        screen (pygame.Surface): The screen where the HUD is drawn.
        screen_rect (pygame.Rect): The rectangle representing the screen area.
        game_stats (GameStats): The game statistics object holding the player's score, level, etc.
        font (pygame.font.Font): The font used for rendering text in the HUD.
        padding (int): The padding between HUD elements.
        score_image (pygame.Surface): The rendered image for the current score.
        score_rect (pygame.Rect): The rectangle for positioning the score image.
        hi_score_image (pygame.Surface): The rendered image for the high score.
        hi_score_rect (pygame.Rect): The rectangle for positioning the high score image.
        max_score_image (pygame.Surface): The rendered image for the max score.
        max_score_rect (pygame.Rect): The rectangle for positioning the max score image.
        level_image (pygame.Surface): The rendered image for the current level.
        level_rect (pygame.Rect): The rectangle for positioning the level image.
        life_image (pygame.Surface): The image of a single life icon.
        life_rect (pygame.Rect): The rectangle for positioning each life icon.
    """
    
    def __init__(self, game) -> None:
        """
        Initializes the HUD instance by setting up game settings, fonts, and
        preparing all elements that will be displayed on the screen.

        Args:
            game (Game): The game instance to access game settings, statistics, and screen.
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.dialog_font, self.settings.HUD_font_size)
        self.padding = 20
        self.update_scores()
        self.setup_life_image()
        self._update_level()

    def update_scores(self):
        """
        Updates all score-related information on the HUD, including the high score,
        max score, and the current score.
        """
        self._update_hi_score()
        self._update_max_score()
        self._update_score()

    def _update_score(self):
        """
        Updates and renders the current score to display on the HUD.

        This method creates an image of the current score and positions it on the screen
        based on the screen's dimensions and padding.
        """
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True, self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def _update_hi_score(self):
        """
        Updates and renders the high score to display on the HUD.

        This method creates an image of the high score and centers it at the top of the screen.
        """
        hi_score_str = f'Hi-score: {self.game_stats.hi_score: ,.0f}'
        self.hi_score_image = self.font.render(hi_score_str, True, self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.centerx = self.screen_rect.centerx
        self.hi_score_rect.top = self.padding

    def _update_max_score(self):
        """
        Updates and renders the maximum score to display on the HUD.

        This method creates an image of the maximum score and positions it near the top-right
        corner of the screen.
        """
        max_score_str = f'Max-Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True, self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.screen_rect.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_level(self):
        """
        Updates and renders the current level to display on the HUD.

        This method creates an image of the current level and positions it below the life icons.
        """
        level_str = f'Level: {self.game_stats.level: ,.0f}'
        self.level_image = self.font.render(level_str, True, self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + self.padding
        self.level_rect.top = self.life_rect.bottom + self.padding

    def setup_life_image(self):
        """
        Loads and scales the image that represents a single life icon for the player.

        This image will be used to display the number of remaining lives on the HUD.
        """
        self.life_image = pygame.image.load(self.game.settings.life_image)
        self.life_image = pygame.transform.scale(self.life_image, (40, 40))
        self.life_rect = self.life_image.get_rect()

    def draw(self):
        """
        Draws the HUD elements on the screen, including the high score, max score, 
        current score, level, and remaining lives.

        This method is called each frame to update the display of game statistics.
        """
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()

    def _draw_lives(self):
        """
        Draws the player's remaining lives on the screen as a series of life icons.

        The life icons are positioned horizontally with padding between them, and 
        are drawn based on the number of ships left.
        """
        current_x = self.padding
        current_y = self.padding
        for life in range(self.game_stats.ships_left):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding
