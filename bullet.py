import pygame
from pygame.sprite import Sprite

class Bullet(Sprite): # When using sprites, you can group related elements in your game and act on all the grouped elements at once.
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__() # To create a bullet instance, __init__() needs the current instance of AlienInvasion and we call super() to inherit properly from Sprite.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set the correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height) # Have to build a rect from scratch using pygame.Rect() class.
                            # x and y co-ordinates of top-left corner of rect and width and height of rect.
        self.rect.midtop = ai_game.ship.rect.midtop # Set bullet's midtop attribute to match ship's midtop attribute.
                                                    # makes the bullet emerge from top of ship.

        # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
            """Move the bullet up the screen."""
            # Update the decimal position of the bullet.
            self.y -= self.settings.bullet_speed
            # Update the rect position.
            self.rect.y = self.y


    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


