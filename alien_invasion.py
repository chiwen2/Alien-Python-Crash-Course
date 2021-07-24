import sys # Use tools in sys module to exit game when player quits.
from time import sleep

import pygame # Contains functionality needed to make the game.

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # Function that initializes the background settings that Pygame needs to work properly

        self.settings = Settings() 
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)) # Defines dimensions of game window: 1200 pixels wide / 800 pixels high.
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics.
        #   and create a scoreboard
        self.stats = GameStats(self) # Make the instance after creating the game window but before defining other game elements: such as the ship.
        self.sb = Scoreboard(self) # Make an instance of Scoreboard

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group() # Stores all live bullets so we can manage bullets that have already been fired
                                             # Will use this group to draw bullets to the screen on each pass through the main loop and to update each bullet's position.

        self.aliens = pygame.sprite.Group() # Create a group to hold the fleet of aliens.
        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")

        # Make difficulty level buttons.
        self._make_difficulty_buttons()

    def _make_difficulty_buttons(self):
        """Make buttons that allow player to select difficulty level."""
        self.easy_button = Button(self, "Easy")
        self.medium_button = Button(self, "Medium")
        self.difficult_button = Button(self, "Difficult")

        # Position buttons so they don't all overlap.
        self.easy_button.rect.top = (
            self.play_button.rect.top + 1.5*self.play_button.rect.height)
        self.easy_button._update_msg_position()

        self.medium_button.rect.top = (
            self.easy_button.rect.top + 1.5*self.easy_button.rect.height)
        self.medium_button._update_msg_position()

        self.difficult_button.rect.top = (
            self.medium_button.rect.top + 1.5*self.medium_button.rect.height)
        self.difficult_button._update_msg_position()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()     


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get(): # Event: action that the user performs while playing the game.
            if event.type == pygame.QUIT: # When player clicks game window's close button a pygame.QUIT event detected and call sys.exit() to exit the game.
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos() # Returns a tuple containing mouse cursor's x- and y- coordinates when mouse button is clicked.
                self._check_play_button(mouse_pos) # Send these values to the method _check_play_button
                self._check_difficulty_buttons(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos) # Flag button_clicked stores true/false value
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score() # Call this after resetting the game stats when starting a new game
            self.sb.prep_level() # Ensures level image updates properly at start of a new game when player clicks Play button.
            self.sb.prep_ships() # Show player how many ships they have to start with
            self._start_game() # Game restarts only if Play is clicked AND game is not currently active.

    def _check_difficulty_buttons(self, mouse_pos):
        """Set the appropriate difficulty level."""
        easy_button_clicked = self.easy_button.rect.collidepoint(mouse_pos)
        medium_button_clicked = self.medium_button.rect.collidepoint(
                mouse_pos)
        diff_button_clicked = self.difficult_button.rect.collidepoint(
                mouse_pos)
        if easy_button_clicked:
            self.settings.difficulty_level = 'easy'
        elif medium_button_clicked:
            self.settings.difficulty_level = 'medium'
        elif diff_button_clicked:
            self.settings.difficulty_level = 'difficult'

    def _start_game(self):
        """Start a new game."""
        # Reset the game settings.
        self.settings.initialize_dynamic_settings()

        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of any remaining aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        
        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

       
                
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p and not self.stats.game_active:
            self._start_game()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update() # When calling update() on a group, the group automatically calls update() for each sprite in the group.
                                 # The line calls bullet.update() for each bullet we place in the group bullets.

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): # Can't remove items from a list/group within a for loop, so have to loop over a copy of the group.
            if bullet.rect.bottom <= 0: # Check each bullet to see whether it has disappeared off top of the screen.
                 self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self): # Any bullet that collides with an alien becomes a key in collisions dic
        """Respond to bullet=alien collisions."""
        # Remove any bullets and aliens that have collided
        collisions = pygame.sprite.groupcollide(        # Compares positions of all bullets and aliens - identifying any that overlap
                self.bullets, self.aliens, True, True)  # The two True arguments tell Pygame to delete the bullets and aliens that have collided

        if collisions: # When bullet hits an alien, Pygame returns a collisions dictionary.
            for aliens in collisions.values(): # Value associated with each bullet is a list of aliens it hits.
                self.stats.score += self.settings.alien_points * len(aliens) # multiply value of each alien by number of aliens in each list and add this amount to the score.
            self.sb.prep_score() # Then call prep_score() to create new image for the updated score.
            self.sb.check_high_score() # Checking high score each time an alien is hit after updating the score after all aliens have been hit

        if not self.aliens: # Check whether the aliens group is empty.
            # Destroy existing bullets and create new fleet.
            self.bullets.empty() # Removes all remaining sprites from a group
            self._create_fleet()
            self.settings.increase_speed() # Increased difficulty when all aliens shot down.

            # Increase level.
            self.stats.level += 1 # When a fleet is destroyed increment this
            self.sb.prep_level() # Call this to make sure new level displays correctly.

        
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens): # Takes 2 args: sprite and a group.
            self._ship_hit()                                       # Loops through the group aliens and returns first alien it finds collided with ship.
                                                                   # If no collisons occur, the function returns None and if block won't execute.
        
        # Look for aliens hitting bottom of the screen after updating positions of all aliens and after looking for collisions.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships() # Call prep_ships after decreasing value of ships_left, so correct number of ships displays each time a ship is destroyed
            self.aliens.empty()
        # Get rid of any remaining aliens and bullets.
            self.bullets.empty()
        # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
        # Pause.     
            sleep(0.5)
           # self.settings.initialize_dynamic_settings()
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        


    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if ship got hit.
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self) # Need to know alien's width and height to place aliens, so we create one here before any calculations.
                            # This alien won't be part of the fleet, so don't add it to the group aliens.
        alien_width, alien_height = alien.rect.size # Use the attribute size, which contains a tuple with the width and height of a rect object.
        available_space_x = self.settings.screen_width - (2 * alien_width) # Calculating horizontal space avaialble for aliens
        number_aliens_x = available_space_x // (2 * alien_width) # Calcualting number of aliens that can fit in that space

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height) - (3 * alien_height) - ship_height
            # Subtract alien height from top, two alien heights from bottom and ship height from bottom
        number_rows = available_space_y // (2 * alien_height) # To find number of rows, we divide available space by two times height of an alien.

        # Create the full fleet of aliens.
        for row_number in range(number_rows): # Counts from 0 to number of rows we want
            for alien_number in range(number_aliens_x): # Creates the aliens in one row.
               self._create_alien(alien_number, row_number)

            
    def _create_alien(self, alien_number, row_number): # Requires number of aliens that's currently being created and row number
        """Create an alien and place it in the row."""
        alien = Alien(self) # Create new alien
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + (2 * alien_width) * alien_number # Each alien pushed to right one alien width from left margin.
                                                                 # Multiply alien width by 2 to account for space one alien takes up, incl empty space to right
                                                                 # Next, multiply this amount by alien's position in the row.
        alien.rect.y = alien.rect.height + (2 * alien.rect.height) * row_number # Change alien's y-coorindate value when it's not in the first row
                                                                                # by starting with one alien's height to create empty space at top of screen.
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges(): # If true is returned, we know an alien is at the edge and whole fleet needs to change direction.
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed # Drop each alien using fleet_drop_speed from settings.
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score() # Call show_score() just before we draw the Play button.

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.difficult_button.draw_button()


        pygame.display.flip() # When we move game elements around, pygame.display.flip() continually updates display to show new positions of game elements and hides old ones -> smooth movement


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

