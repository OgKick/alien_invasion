from pathlib import Path
import json

class GameStats:
    """
    A class to track and manage the game statistics, including score, high score, and level.

    Attributes:
        game (object): The game instance.
        settings (Settings): The settings object that contains the game configurations.
        max_score (int): The highest score reached in the current game session.
        hi_score (int): The highest score across all sessions, saved to a file.
        ships_left (int): The number of ships remaining for the player.
        score (int): The current score of the player.
        level (int): The current level of the game.
    """

    def __init__(self, game) -> None:
        """
        Initializes the game statistics, including loading saved high score and initializing other stats.

        Args:
            game (object): The game instance to access settings and other game data.
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        # Initialize saved scores
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """
        Initializes the saved scores by reading from a file. If no file exists, a new one is created with a hi_score of 0.
        """
        self.path = Path(self.settings.scores_file)
        if self.path.exists():
            contents = self.path.read_text()
            scores: dict = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()

    def reset_stats(self):
        """
        Resets the game statistics, including the number of ships left, score, and level.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """
        Updates the game statistics based on the current collisions.

        Args:
            collisions (dict): A dictionary containing collision data to calculate the score.
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_max_score(self):
        """
        Updates the maximum score achieved in the current game session if the current score is higher.
        """
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_hi_score(self):
        """
        Updates the high score if the current score exceeds the previously recorded high score, and saves it to a file.
        """
        if self.score > self.hi_score:
            self.hi_score = self.score
            self.save_scores()

    def _update_score(self, collisions):
        """
        Updates the score based on the current collisions with aliens.

        Args:
            collisions (dict): A dictionary of collisions to calculate the score, where each alien group
                                contributes points to the score based on the number of aliens in that group.
        """
        for alien_group in collisions.values():
            self.score += len(alien_group) * self.settings.alien_points

    def update_level(self):
        """
        Increases the level of the game.
        """
        self.level += 1

    def save_scores(self):
        """
        Saves the current high score to a file in JSON format.
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        self.path.write_text(contents)
