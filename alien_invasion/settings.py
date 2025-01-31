class Settings:
    """
    A class to store all settings for the 'Alien Invasion' game.

    This class contains all configurable settings related to screen size, game assets (like images and sounds),
    ship properties, bullet settings, alien settings, and button/font properties. It also includes methods for
    initializing dynamic settings and adjusting difficulty.

    Attributes:
        screen_w (int): The width of the game screen.
        screen_h (int): The height of the game screen.
        title (str): The title of the game.
        FPS (int): Frames per second for the game.
        bg_file (str): The file path to the background image (from opengameart.com).
        background_sound (str): The file path to the background music (from opengameart.com).
        icon (str): The file path to the game icon (from opengameart.com).
        difficulty_scale (float): The factor by which game difficulty increases over time.
        scores_file (str): The file path to the scores file (in JSON format).
        life_image (str): The file path to the image used for displaying remaining lives (from opengameart.com).
        
        # Ship settings
        ship_file (str): The file path to the ship image (from opengameart.com).
        ship_w (int): The width of the ship.
        ship_h (int): The height of the ship.

        # Bullet settings
        bullet_file (str): The file path to the bullet image (from opengameart.com).
        laser_sound (str): The file path to the laser sound effect (from opengameart.com).
        impact_sound (str): The file path to the impact sound effect (from opengameart.com).

        # Alien settings
        alien_file (str): The file path to the alien image (from opengameart.com).

        # Fleet settings
        fleet_drop_amount (int): The amount the alien fleet drops each time.

        # Button settings
        button_w (int): The width of the buttons.
        button_h (int): The height of the buttons.
        button_color (tuple): The RGB color for the buttons.

        # Font settings
        text_color (tuple): The RGB color for text in the HUD.
        button_font_size (int): The font size for button text.
        HUD_font_size (int): The font size for the HUD.
        font_file (str): The file path to the main game font.
        title_font (str): The file path to the title screen font.
        dialog_font (str): The file path to the dialog font.

    Methods:
        init_dynamic_settings() -> None:
            Initializes the dynamic settings that adjust based on the game state.

        increase_difficulty() -> None:
            Increases the difficulty of the game by adjusting various speed and point settings.
    """

    def __init__(self) -> None:
        """
        Initializes the game settings.

        Sets up both static and dynamic settings, including screen dimensions, game assets, ship, bullet, 
        alien properties, and button/font settings.

        Path references for images, sounds, and fonts are provided, all of which are sourced from
        opengameart.com.

        Attributes initialized:
            screen_w (int): Screen width (1200).
            screen_h (int): Screen height (800).
            title (str): Game title ('Alien Invasion').
            FPS (int): Frames per second (60).
            bg_file (str): Path to the background image from opengameart.com.
            background_sound (str): Path to background music from opengameart.com.
            icon (str): Game icon path from opengameart.com.
            difficulty_scale (float): Difficulty scaling factor (1.4).
            scores_file (str): Path to scores file.
            life_image (str): Path to life image from opengameart.com.
            ship_file (str): Path to ship image from opengameart.com.
            ship_w (int): Ship width (40).
            ship_h (int): Ship height (60).
            bullet_file (str): Bullet image path from opengameart.com.
            laser_sound (str): Laser sound effect path from opengameart.com.
            impact_sound (str): Impact sound effect path from opengameart.com.
            alien_file (str): Alien image path from opengameart.com.
            fleet_drop_amount (int): Amount the alien fleet drops (10).
            button_w (int): Button width (200).
            button_h (int): Button height (50).
            button_color (tuple): Button color (0,135,50).
            text_color (tuple): Text color (255,255,255).
            button_font_size (int): Button font size (35).
            HUD_font_size (int): HUD font size (20).
            font_file (str): Path to main font.
            title_font (str): Title screen font.
            dialog_font (str): Dialog font.
        """
        
        # Screen settings
        self.screen_w = 1200
        self.screen_h = 800
        self.title = 'Alien Invasion'
        self.FPS = 60
        self.bg_file = 'Assets\images\Starset.png'  
        self.background_sound = 'Assets\sound\ObservingTheStar.ogg'  
        self.icon = 'Assets\images\shuttle.png'  
        self.difficulty_scale = 1.4
        self.scores_file = r'Assets\file\scores.json'
        self.life_image = "Assets\images\heart.png"  

        # Ship settings
        self.ship_file = 'Assets\images\shuttle.png'  
        self.ship_w = 40
        self.ship_h = 60

        # Bullet settings
        self.bullet_file = 'Assets\images\laserBlast.png'  
        self.laser_sound = "Assets\sound\laser.mp3"  
        self.impact_sound = "Assets\sound\impactSound.mp3"  

        # Alien settings
        self.alien_file = r"Assets\images\tomatohead1cut.png"  

        # Fleet settings
        self.fleet_drop_amount = 10

        # Button settings
        self.button_w = 200
        self.button_h = 50
        self.button_color = (0, 135, 50)

        # Font settings
        self.text_color = (255, 255, 255)
        self.button_font_size = 35
        self.HUD_font_size = 20
        self.font_file = r"Assets\fonts\Silkscreen-Bold.ttf"
        self.init_dynamic_settings()
        self.title_font = r"Assets\fonts\Press_Start_2P\PressStart2P-Regular.ttf"
        self.dialog_font = r"Assets\fonts\VT323\VT323-Regular.ttf"

    def init_dynamic_settings(self):
        """
        Initializes dynamic game settings that can change during gameplay.

        These settings include the speed of the ship, bullet, and alien fleet, as well as the number of 
        bullets that can be fired and the points for each alien. These values are the starting values for the game.

        Attributes initialized:
            ship_speed (float): Speed of the ship (4).
            ship_limit (int): Number of ships the player can have (3).
            bullet_speed (float): Speed of the bullets (7).
            bullet_w (int): Bullet width (25).
            bullet_h (int): Bullet height (45).
            bullet_amount (int): Number of bullets the player can fire (5).
            alien_w (int): Alien width (40).
            alien_h (int): Alien height (40).
            fleet_speed (float): Speed of the alien fleet (1).
            alien_points (int): Points earned for destroying an alien (10).
        """
        self.ship_speed = 4
        self.ship_limit = 3

        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 45
        self.bullet_amount = 5

        self.alien_w = 40
        self.alien_h = 40
        self.fleet_speed = 1
        self.alien_points = 10

    def increase_difficulty(self):
        """
        Increases the difficulty of the game.

        This method adjusts the speed of the ship, bullets, and alien fleet, and increases the points earned 
        for each alien. The difficulty is scaled by a factor defined in `difficulty_scale`.

        Attributes updated:
            ship_speed (float): New speed of the ship after scaling.
            bullet_speed (float): New speed of the bullets after scaling.
            fleet_speed (float): New speed of the alien fleet after scaling.
            alien_points (int): New points for destroying an alien after scaling.
        """
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale
        self.alien_points = int(self.alien_points * self.difficulty_scale)
