"""
Main menu system
"""
import pygame
from game.menus.base_menu import BaseMenu, MenuItem
from game.logger import get_logger

logger = get_logger(__name__)


class Menu(BaseMenu):
    """Main menu for the game"""
    
    def __init__(self, screen_width, screen_height, config):
        super().__init__(screen_width, screen_height, "Planet Wars", title_font_size=80)
        
        self.config = config
        
        # Font for input label and text
        self.input_font = pygame.font.Font(None, 36)
        
        # Text input for player name
        self.input_rect = pygame.Rect(
            (screen_width - 300) // 2,
            screen_height // 2 - 20,
            300,
            50
        )
        self.input_active = False
        self.input_text = config.player_name
        
        # Create menu items (positioned lower to make room for input)
        button_width = 300
        button_height = 60
        button_x = (screen_width - button_width) // 2
        button_spacing = 80
        start_y = screen_height // 2 + 80  # Match the gap above input
        
        self.menu_items = [
            MenuItem("New Game", button_x, start_y, button_width, button_height, "new_game"),
            MenuItem("Scoreboard", button_x, start_y + button_spacing, button_width, button_height, "scoreboard"),
            MenuItem("Quit", button_x, start_y + button_spacing * 2, button_width, button_height, "quit")
        ]
    
    def handle_text_input(self, event):
        """Handle text input for player name"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked on input box
            was_active = self.input_active
            self.input_active = self.input_rect.collidepoint(event.pos)
            if self.input_active and not was_active:
                logger.debug("Player name input activated")
        
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                logger.debug(f"Player name text: {self.input_text}")
            elif event.key == pygame.K_RETURN:
                self.input_active = False
                old_name = self.config.player_name
                self.config.player_name = self.input_text if self.input_text else "Player"
                logger.info(f"Player name changed: '{old_name}' -> '{self.config.player_name}'")
                self.config.save()
            elif len(self.input_text) < 20:  # Limit length
                self.input_text += event.unicode
                logger.debug(f"Player name text: {self.input_text}")
    
    def render(self, screen):
        """Render the menu with player name input"""
        # Call parent render for background and title
        super().render(screen)
        
        # Draw player name label
        label_text = self.input_font.render("Your Name:", True, (255, 255, 255))
        label_rect = label_text.get_rect(center=(self.screen_width // 2, self.input_rect.y - 35))
        screen.blit(label_text, label_rect)
        
        # Draw input box
        input_color = (70, 70, 140) if self.input_active else (50, 50, 100)
        pygame.draw.rect(screen, input_color, self.input_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.input_rect, 2)
        
        # Draw input text
        input_surface = self.input_font.render(self.input_text, True, (255, 255, 255))
        screen.blit(input_surface, (self.input_rect.x + 10, self.input_rect.y + 12))
        
        # Draw cursor if active
        if self.input_active and pygame.time.get_ticks() % 1000 < 500:  # Blinking cursor
            cursor_x = self.input_rect.x + 10 + input_surface.get_width() + 2
            cursor_y = self.input_rect.y + 10
            pygame.draw.line(screen, (255, 255, 255), 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + 30), 2)



