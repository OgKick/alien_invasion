import sys
import pygame
#import vlc
#import time
from time import sleep
from settings import Settings
from ship import Ship
from alien_fleet import AlienFleet
from game_stats import GameStats
from bullet import Bullet
from button import Button
from hud import HUD

class AlienInvasion:
    """
    This class manages the core game functionality for the Alien Invasion game. It handles the initialization, 
    game loop, user input, and the overall flow of the game, including starting, restarting, and ending the game. 
    
    The game includes a spaceship controlled by the player, a fleet of alien enemies, and bullets fired by the spaceship. 
    It also manages the game state (active, game over) and updates various game elements (ship, aliens, bullets, etc.) 
    on each frame. Additionally, it controls the display, sound, and HUD (heads-up display) elements, such as the score 
    and level.

    Attributes:
        screen (pygame.Surface): The screen surface where the game is drawn.
        screen_rect (pygame.Rect): The rectangle representing the screen dimensions.
        settings (Settings): The configuration settings for the game.
        game_stats (GameStats): The game's statistics, such as score and remaining ships.
        HUD (HUD): The heads-up display for showing the player's score, level, and other stats.
        ship (Ship): The player's spaceship.
        bullets (pygame.sprite.Group): A group containing all the player's bullets.
        aliens (AlienFleet): The group containing all the alien enemies.
        play_button (Button): The button to start the game when it's over.
        running (bool): A flag indicating whether the game is running.
        game_active (bool): A flag indicating whether the game is currently active.
        game_over (bool): A flag indicating whether the game is over.
        clock (pygame.time.Clock): The clock used to control the game's frame rate.
        bg (pygame.Surface): The background image displayed during the game.
        laser_sound (pygame.mixer.Sound): The sound played when the spaceship fires a bullet.
        impact_sound (pygame.mixer.Sound): The sound played when a bullet hits an alien.
    """

    def __init__(self) -> None:
        """
    Initializes the game by setting up the core components required for the Alien Invasion game.
    
    This includes initializing Pygame, setting up game settings, loading resources, and initializing
    game objects such as the player ship, alien fleet, bullets, HUD, and sounds. It also creates the
    main screen, sets the game icon, and sets the title for the window. The method further prepares
    the game to run by configuring the background image, setting up sound effects and background 
    music, and initializing the clock for frame rate control. The 'Play' button is also created, and
    the initial game state is set to active.
    
    Attributes:
        screen (pygame.Surface): The main screen for displaying the game.
        HUD (HUD): The heads-up display for showing scores, level, and other game information.
        ship (Ship): The player's spaceship.
        bullets (pygame.sprite.Group): Group of bullets fired by the player's ship.
        aliens (AlienFleet): The group of aliens in the game.
        icon (pygame.Surface): Icon image for the game window.
        clock (pygame.time.Clock): Clock object to control the frame rate.
        bg (pygame.Surface): Background image for the game window.
        laser_sound (pygame.mixer.Sound): Sound effect for firing lasers.
        impact_sound (pygame.mixer.Sound): Sound effect for bullet-alien collisions.
        play_button (Button): Button to start the game when pressed.
        running (bool): Flag indicating if the game is running.
        game_active (bool): Flag indicating if the game is currently active.
        game_over (bool): Flag indicating if the game has ended.
    """
        pygame.init()
        self.settings = Settings()
        self.game_stats = GameStats(self)

        # Create the screen with the configured size
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h)
        )
    
        self.HUD = HUD(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = AlienFleet(self)

        # Spaceship icon
        self.icon = pygame.image.load(self.settings.icon)
        pygame.display.set_icon(self.icon)

        # Set up the caption for the game
        pygame.display.set_caption(self.settings.title)
        
        self.running = True
        self.game_active = True
        self.game_over = False
        self.clock = pygame.time.Clock()
        
        # Load background image and scale it to the screen size
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, 
            (self.settings.screen_w, self.settings.screen_h)
        )

        # Sound setup
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.2)

        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.8)

        # Load background music
        pygame.mixer.music.load(self.settings.background_sound)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        
        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self):
        """
    Runs the main game loop, managing the flow of the game from user input to updates 
    and screen rendering.

    The method continuously checks for user inputs, updates the game state (such as 
    movement of the player ship, bullet firing, and alien behavior), and renders the 
    updated game screen. It also controls the frame rate based on the FPS setting. 
    The loop runs until the game is no longer active or the game window is closed.

    Game flow:
        1. Handles user input via events (mouse, keyboard, etc.).
        2. Updates game elements like the player's ship, bullets, and aliens if the game is active.
        3. Updates the display with the latest game graphics.
        4. Regulates the frame rate using the clock.

    Attributes:
        running (bool): Flag indicating if the game is still running.
        game_active (bool): Flag indicating whether the game is active (not paused or over).
        clock (pygame.time.Clock): Clock object used to control the frame rate.
        settings (Settings): Game settings, including FPS and other configuration options.
    """
        # Game loop
        while self.running:
            # Inputs - events (mouse, keyboard, controllers)
            self._check_events()

            # Update the game state (create enemies, destroy enemies, collision)
            if self.game_active:
                self.ship.update()
                self._update_bullets()            
                self._update_aliens()

            # Display graphics
            self._update_screen()
            self.clock.tick(self.settings.FPS) 

    def _update_aliens(self):
        """
    Updates the alien fleet's position and checks for collisions with the player ship 
    or the bottom of the screen.

    The method:
        1. Updates the movement and behavior of all aliens in the fleet.
        2. Checks if any alien collides with the player ship, triggering a game status check.
        3. Checks if the alien fleet has reached the bottom of the screen, triggering a game status check.

    If a collision occurs or the fleet reaches the bottom, the game's status is updated to reflect 
    a potential game over condition.

    Attributes:
        ship (Ship): The player's ship that may collide with aliens.
        aliens (AlienFleet): The group of alien sprites and their associated behavior.
    """
        self.aliens.update_fleet()
        if pygame.sprite.spritecollideany(self.ship, self.aliens.fleet):
            self._check_game_status()

        if self.aliens.check_fleet_bottom():
            self._check_game_status()

    def _check_game_status(self):
        """
    Checks the current game status and updates it based on the number of remaining ships.

    If the player has more than one ship left:
        1. Reduces the number of remaining ships by one.
        2. Triggers the ship hit logic, updating the ship's state.
        3. Resets the level for the player to continue.

    If the player has no ships left:
        1. Ends the game by setting the game state to inactive and marking it as a game over.
        2. Plays a game over video or animation.

    Attributes:
        game_stats (GameStats): The game's statistics, including the number of ships left.
        ship (Ship): The player's ship, which will be updated upon collision.
        game_active (bool): Indicates whether the game is currently active.
        game_over (bool): Marks the game as over.
    """
        if self.game_stats.ships_left > 1:
            self.game_stats.ships_left -= 1
            self.ship.ship_hit()
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
            self.game_over = True
            self._play_game_over_video() 

    def _reset_level(self):
        """
    Resets the current level by clearing all bullets and aliens, then re-creating the alien fleet.

    This method is called when the player loses a ship, and it prepares the game for the next round or level
    by resetting key elements like bullets and the alien fleet.

    It performs the following actions:
        1. Clears the list of bullets to remove any leftover projectiles.
        2. Empties the alien fleet to remove all currently existing aliens.
        3. Recreates the alien fleet at its starting position.

    Attributes:
        bullets (pygame.sprite.Group): A group that holds all the bullet sprites in the game.
        aliens (AlienFleet): The alien fleet, responsible for managing and updating the aliens in the game.
    """
        self.bullets.empty()
        self.aliens.fleet.empty()
        self.aliens.create_fleet()

    def restart_game(self):
        """
    Restarts the game by resetting the settings, stats, level, and other game elements for a fresh start.

    This method is typically called when the player chooses to restart the game after it has ended. It resets 
    the game's dynamic settings, updates the HUD with the latest scores, and prepares the game for a new round.

    The following actions are performed:
        1. Resets dynamic settings to their initial values (e.g., difficulty settings).
        2. Resets the game statistics, including the score, remaining ships, and level.
        3. Updates the HUD to reflect the current scores and level.
        4. Clears the previous level and recreates the alien fleet.
        5. Centers the player's ship on the screen and prepares it for the next round.
        6. Resets game status to active and hides the mouse cursor.

    Attributes:
        settings (Settings): The configuration object that holds the game's dynamic settings.
        game_stats (GameStats): The object that manages and tracks the player's statistics during the game.
        HUD (HUD): The object that updates and displays the heads-up display (HUD) with current game information.
        ship (Ship): The player's spaceship, which is repositioned to the center of the screen.
        game_active (bool): A flag that indicates whether the game is currently active or paused.
        game_over (bool): A flag that indicates whether the game has ended.
    """
        # Set up dynamic settings
        self.settings.init_dynamic_settings()
    
        # Reset game stats
        self.game_stats.reset_stats()
           
        # HUD update scores
        self.HUD.update_scores()

        # Reset level
        self._reset_level()
        self.HUD._update_level()
        self.game_stats.update_level()

        # Ship get centered
        self.ship.center_ship()
        self.game_active = True
        self.game_over = False
        pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """
    Updates the position of all bullets and handles their removal when they go off-screen.

    This method is responsible for updating the movement of all active bullets, checking if they have 
    moved off the top of the screen, and removing them if they are no longer visible. It also checks 
    for collisions between bullets and aliens.

    Actions performed:
        1. Updates the position of each bullet in the `bullets` sprite group.
        2. Removes bullets that have moved off the top of the screen.
        3. Checks for any collisions between bullets and aliens, triggering the necessary response.

    Attributes:
        bullets (pygame.sprite.Group): A group containing all active bullets currently on the screen.
        screen (pygame.Surface): The screen surface used to check if bullets have gone off-screen.
    """
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= self.screen.get_rect().top:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()
           
    def _check_bullet_alien_collision(self):
        """
    Checks for collisions between bullets and aliens, handles the consequences of those collisions, 
    and updates game state accordingly.

    This method detects when a bullet collides with an alien, removes both the bullet and the alien, 
    plays the impact sound effect, updates the game statistics and score, and checks if the alien fleet 
    has been completely destroyed. If all aliens are eliminated, the level is reset.

    Actions performed:
        1. Detects collisions between bullets and aliens using `pygame.sprite.groupcollide`.
        2. If collisions are detected, plays an impact sound effect (if not too many channels are active),
           fades out the sound, and updates the game statistics and score.
        3. If no aliens are left, the level is reset and the HUD is updated.

    Attributes:
        bullets (pygame.sprite.Group): The group of all active bullets currently on the screen.
        aliens (AlienFleet): The fleet of aliens to check for collisions.
        impact_sound (pygame.mixer.Sound): The sound effect played upon collision between bullets and aliens.
        game_stats (GameStats): Object that tracks the game's statistics and updates based on collisions.
        HUD (HUD): The heads-up display that updates the score and level information.
    """
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens.fleet, True, True)
        if collisions and self.impact_sound.get_num_channels() <= 4:
            self.impact_sound.play()
            self.impact_sound.fadeout(1500)
            self.game_stats.update(collisions)     
            self.HUD.update_scores()

        if not self.aliens.fleet:
            self._reset_level()
            self.HUD._update_level()

    def _update_screen(self):
        """
    Updates and redraws the game screen with the latest visual elements.

    This method is responsible for refreshing the display each frame. It first draws the background image 
    to cover the entire screen, then iterates over and draws all active bullets, the spaceship, the alien fleet, 
    and the heads-up display (HUD). After all elements are drawn, the updated screen is displayed to the player.

    Actions performed:
        1. Draws the background image to the screen.
        2. Draws all active bullets currently in the game.
        3. Draws the player's spaceship.
        4. Draws the alien fleet.
        5. Updates and draws the heads-up display (HUD) showing the score, level, etc.

    Attributes:
        screen (pygame.Surface): The surface representing the game window where all elements are drawn.
        bg (pygame.Surface): The background image to be drawn on the screen.
        bullets (pygame.sprite.Group): The group containing all active bullets in the game.
        ship (Ship): The player's spaceship object.
        aliens (AlienFleet): The fleet of alien sprites.
        HUD (HUD): The heads-up display object that manages score and game status.
    """
        self.screen.blit(self.bg, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.ship.draw()
        self.aliens.draw_fleet()
        self.HUD.draw()

        if not self.game_active and self.game_over:
            self._draw_game_over()  
            pygame.mouse.set_visible(True)

        elif not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """
    Handles and processes all input events from the user, such as keyboard, mouse, or quit events.

    This method listens for all events in the event queue and responds accordingly:
        - If the user closes the game window (QUIT event), the game ends by setting `running` to False 
          and quitting the pygame session.
        - If a key is pressed (KEYDOWN event), it calls the appropriate method to handle the key press.
        - If a key is released (KEYUP event), it calls the appropriate method to handle the key release.
        - If the user clicks the mouse (MOUSEBUTTONDOWN event), it checks if a button was clicked 
          and calls the respective button click handler.

    Actions performed:
        1. Processes the quit event to terminate the game.
        2. Processes key press and release events for movement and actions.
        3. Processes mouse click events to interact with on-screen buttons.

    Attributes:
        running (bool): A flag indicating whether the game is running or should quit.
        pygame (module): The Pygame library used for event handling and game functionality.
    """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        """
    Checks if the play button is clicked by the user and triggers the game restart if clicked.

    This method checks the current mouse position and determines whether the user has clicked 
    on the play button. If the play button is clicked, it calls the `restart_game` method to
    reset the game state and start a new game session.

    Actions performed:
        1. Retrieves the mouse position.
        2. Checks if the play button is clicked using the `check_clicked` method.
        3. If the play button is clicked, it restarts the game by calling `restart_game`.

    Attributes:
        play_button (Button): The button used to start or restart the game.
        pygame (module): The Pygame library used for mouse input and event handling.
    """
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()

    def _check_keyup_events(self, event):
        """
    Handles the key release events for controlling the ship's movement.

    This method checks if the user releases a key corresponding to ship movement
    controls (right or left) and updates the ship's movement flags accordingly.

    Actions performed:
        1. Checks if the released key is the right arrow key (pygame.K_RIGHT).
        2. Sets the `moving_right` attribute of the ship to `False` to stop movement in the right direction.
        3. Checks if the released key is the left arrow key (pygame.K_LEFT).
        4. Sets the `moving_left` attribute of the ship to `False` to stop movement in the left direction.

    Parameters:
        event (pygame.event): The event object containing information about the key release event.

    Attributes:
        ship (Ship): The player's ship object whose movement is controlled by key events.
    """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_keydown_events(self, event):
        """
    Handles the key press events for controlling the ship and exiting the game.

    This method checks if the user presses a key and updates the game state or 
    controls accordingly. It includes movement controls for the ship, firing 
    bullets, and quitting the game.

    Actions performed:
        1. If the right arrow key (pygame.K_RIGHT) is pressed, sets the `moving_right` attribute
           of the ship to `True`, causing it to move right.
        2. If the left arrow key (pygame.K_LEFT) is pressed, sets the `moving_left` attribute
           of the ship to `True`, causing it to move left.
        3. If the 'Q' key (pygame.K_q) is pressed, sets `running` to `False`, saves the game 
           scores, quits the game, and exits the program.
        4. If the spacebar (pygame.K_SPACE) is pressed, calls the `_fire_bullet()` method to fire
           a bullet from the ship.

    Parameters:
        event (pygame.event): The event object containing information about the key press event.

    Attributes:
        ship (Ship): The player's ship object controlled by key press events.
        game_stats (GameStats): The object that tracks the game statistics and scores.
    """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
    
    def _fire_bullet(self):
        """
    Fires a bullet from the player's ship if the maximum bullet limit has not been reached.

    This method checks if the number of bullets currently on screen is less than or equal
    to the configured maximum bullet amount. If the condition is met, a new bullet is created
    and added to the bullet group, and the laser sound effect is played.

    The bullet is created as an instance of the `Bullet` class and is added to the `bullets` group,
    allowing it to be updated and drawn during the game loop.

    Actions performed:
        1. If the current number of bullets is less than or equal to the maximum allowed by the settings,
           a new bullet is instantiated and added to the `bullets` sprite group.
        2. The laser sound effect is played upon firing the bullet.

    Attributes:
        bullets (pygame.sprite.Group): A group that holds all the active bullets in the game.
        laser_sound (pygame.mixer.Sound): The sound effect that is played when a bullet is fired.
        settings (Settings): The configuration object that holds game settings such as the maximum bullet amount.

    Returns:
        None
    """
        if len(self.bullets) <= self.settings.bullet_amount:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)            
            self.laser_sound.play()

    #def _draw_game_over(self):
        """
     Displays the final game over screen, including playing a video and showing the mouse cursor.
     
     This method is intended to be used when the game ends. It triggers the game over video to
     play and ensures that the mouse cursor is made visible again after the game has concluded.
     
     Actions performed:
         1. Calls the `_play_game_over_video` method to display the game over video.
         2. Makes the mouse cursor visible after the game over screen is displayed.
     
     Attributes:
         None
     
     Returns:
         None
     """
        # Play the final game over video when the game is over
        #self._play_game_over_video()
        #pygame.mouse.set_visible(True)

    #def _play_game_over_video(self):
        """
     Plays the game over video file when the game ends.
     
     This method initializes a video player (using VLC), loads the game over video, and plays it
     until it finishes. After the video ends, the player stops.
     
     Actions performed:
         1. Loads and plays the game over video using VLC MediaPlayer.
         2. Waits for the video to finish playing before stopping the player.
     
     Attributes:
         video_path (str): The path to the game over video file.
         player (vlc.MediaPlayer): The media player used to play the video.
     
     Returns:
         None
     """
        # Path to your video file (ensure proper path)
        #video_path = r"Assets\sound\game-over.mp4"  

        # Initialize VLC player
        #player = vlc.MediaPlayer(video_path)

        # Play the video
        #player.play()

        # Wait until the video finishes
        #while player.is_playing():
            #time.sleep(0.1) 

        #player.stop()


if __name__ == '__main__':
    game = AlienInvasion()
    game.run_game()
