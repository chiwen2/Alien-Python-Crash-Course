import pygame.font # Lets pygame render text to the screen.

class Button:

    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48) # Font attribute for rendering text
                                                  # None arg = default font, 48 = size

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,   # Turns the text stored in msg into an image
                self.button_color) # Boolean also used to turn antialiasing on/off                                    
        self.msg_image_rect = self.msg_image.get_rect() # Creating a rect from the image 
        self.msg_image_rect.center = self.rect.center # And setting its center attribute to match that of the button.

    def _update_msg_position(self):
        """If the button has been moved, the text needs to be moved as well."""
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect) # Draw rectangular portion of button
        self.screen.blit(self.msg_image, self.msg_image_rect) # Draw text image to screen, passing it an image and the rect object associated with image

