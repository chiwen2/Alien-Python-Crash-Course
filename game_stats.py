class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats() # Calling this method so stats are set properly when the GameStats instance is first created.
        
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit # Resetting some stats each time a player starts a new game
        self.score = 0 # Resetting score each time a new game starts
        self.level = 1
