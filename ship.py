import pygame
from pygame.sprite import Sprite

class Ship(Sprite): # Import Sprite
    """A class to manage the ship."""

    def __init__(self, ai_game): # Paremeters: self reference and self reference to current instance of AlienInvasion class.
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen # Assign screen to attribute of ship, so we can access it easily in all methods in this class.
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() # Access screen's rect attribute using get_rect() and allows us to place ship in correct location on the screen.

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect() # When image is loaded, we call get_rect() to access the ship's surface rect attribute so we can later use it to place the ship.

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right: # self.rect.right returns x-coordinate of right edge of ship's rect.
            self.x += self.settings.ship_speed                             # If this value is < value returned by self.screen_rect.right, ship hasn't reached right edge of screen.
        if self.moving_left and self.rect.left > 0: # If value of left side of rect is > 0 the ship hasn't reached left edge of screen. # Ensures ship is within these bounds before adjusting value of x.
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x # controls position of ship


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)