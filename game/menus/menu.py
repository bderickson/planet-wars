"""
Main menu system
"""
import sys
import pygame
from game.menus.base_menu import BaseMenu, MenuItem
from game.logger import get_logger

logger = get_logger(__name__)


class Menu(BaseMenu):
    """Main menu for the game"""
    
    def __init__(self, screen_width, screen_height, config):
        super().__init__(screen_width, screen_height, "Planet Wars", title_font_size=80)
        
        self.config = config
        self.is_browser = sys.platform == "emscripten"
        
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
            if self.input_rect.collidepoint(event.pos):
                # On mobile browser, use JavaScript prompt for text input
                if self.is_browser:
                    self._mobile_text_input()
                else:
                    was_active = self.input_active
                    self.input_active = True
                    if not was_active:
                        logger.debug("Player name input activated")
        
        # Desktop keyboard input
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                # Auto-save after backspace
                self.config.player_name = self.input_text if self.input_text else "Player"
                self.config.save()
                logger.debug(f"Player name auto-saved: {self.config.player_name}")
            elif event.key == pygame.K_RETURN:
                # Enter key just deactivates the input field
                self.input_active = False
                logger.debug("Player name input deactivated (Enter pressed)")
            elif len(self.input_text) < 20:  # Limit length
                self.input_text += event.unicode
                # Auto-save after each character
                self.config.player_name = self.input_text if self.input_text else "Player"
                self.config.save()
                logger.debug(f"Player name auto-saved: {self.config.player_name}")
    
    def _mobile_text_input(self):
        """Use JavaScript prompt for mobile text input"""
        try:
            import platform
            if hasattr(platform, 'window') and platform.window:
                # Use JavaScript prompt on mobile
                logger.debug("Opening mobile text input prompt")
                new_name = platform.window.prompt("Enter your name:", self.input_text)
                if new_name is not None:  # User didn't cancel
                    # Limit length
                    new_name = new_name[:20] if new_name else "Player"
                    self.input_text = new_name
                    self.config.player_name = new_name
                    self.config.save()
                    logger.info(f"Player name updated via mobile prompt: {new_name}")
        except Exception as e:
            logger.warning(f"Mobile text input failed: {e}")

    
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
        
        # Draw GitHub link at bottom
        link_font = pygame.font.Font(None, 24)
        link_text = link_font.render("Source code available at github.com/bderickson/planet-wars", True, (150, 150, 150))
        link_rect = link_text.get_rect(center=(self.screen_width // 2, self.screen_height - 30))
        screen.blit(link_text, link_rect)



