import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game): # Give the ai_game parameter so it can access the settings, screen and stats objects
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1) # round() function normally rounds a decimal number to a set number of decimal places given as the second argument.
                                                    # When passing a neg number as 2nd arg, round() will round value to nearest 10, 100, 1000, and so on.
        score_str = "{:,}".format(rounded_score) # A string formatting directive tells Python to insert commas into numbers when converting a numerical value to a string.
        self.score_image = self.font.render(score_str, True, # Then pass this string to render(), which creates the image.
                self.text_color, self.settings.bg_color) # To display score clearly, we pass screen's background color and text color to render().

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20 # Making sure score always lines up with right side of screen and its right edge 20 pixels from right edge of screen.
        self.score_rect.top = 20    # Place top edge 20 pixels down from top of the screen.

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1) # Round the high score to nearest 10
        high_score_str = "{:,}".format(high_score) # Format it with commas.
        self.high_score_image = self.font.render(high_score_str, True, # Generate an image from high score
                self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx # Center high score horizontally
        self.high_score_rect.top = self.score_rect.top # Set its top attribute to match top of the score image.

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_level(self):
        """Turn the level into a rendered image."""

        level_str = str(self.stats.level,)
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right # Sets image right attribute to match score's right attribute
        self.level_rect.top = self.score_rect.bottom + 10 # Sets top attribute 10 pixels beneath the bottom of score image to leave space between score and level.
    
    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group() # Creates an empty group to hold the ship instances
        for ship_number in range(self.stats.ships_left): # Group is filled when loop is run once for every ship the player has left
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width # Ships appear next to each other with a 10-pixel margin on left side of the group of ships
            ship.rect.y = 10 # Set y-coord value 10 pixels down from top of screen os ships appear in upper-left corner of screen
            self.ships.add(ship) # Add each new ship to the group ships.