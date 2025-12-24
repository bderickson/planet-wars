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
        self.is_mobile = self._detect_mobile()
        
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
    
    def _detect_mobile(self):
        """Detect if running on a mobile browser"""
        if not self.is_browser:
            return False
        
        try:
            import platform
            if hasattr(platform, 'window') and platform.window:
                # Check if it's a touch device using JavaScript
                # This will be true for mobile/tablet browsers
                js_code = """
                (function() {
                    return ('ontouchstart' in window) || 
                           (navigator.maxTouchPoints > 0) || 
                           (navigator.msMaxTouchPoints > 0);
                })()
                """
                is_touch = platform.window.eval(js_code)
                logger.info(f"Mobile detection: is_touch={is_touch}")
                return bool(is_touch)
        except Exception as e:
            logger.warning(f"Mobile detection failed: {e}")
        
        # Default to False (desktop browser)
        return False
    
    def handle_text_input(self, event):
        """Handle text input for player name"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked on input box
            if self.input_rect.collidepoint(event.pos):
                logger.debug(f"Text input box clicked (browser: {self.is_browser}, mobile: {self.is_mobile})")
                # On mobile browser, use JavaScript prompt for text input
                # On desktop browser, use regular keyboard input
                if self.is_mobile:
                    logger.info("Opening mobile text input prompt")
                    self._mobile_text_input()
                else:
                    was_active = self.input_active
                    self.input_active = True
                    if not was_active:
                        logger.debug("Player name input activated")
        
        # Desktop and desktop browser keyboard input
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
            # Import platform module (only available in Pygbag)
            import platform
            
            logger.debug(f"Platform module loaded, checking for window attribute")
            
            # Check if window object exists
            if not hasattr(platform, 'window'):
                logger.warning("platform.window not available, cannot open mobile prompt")
                return
            
            if not platform.window:
                logger.warning("platform.window is None, cannot open mobile prompt")
                return
            
            # Use JavaScript prompt on mobile
            logger.info(f"Opening mobile text input prompt with current name: '{self.input_text}'")
            new_name = platform.window.prompt("Enter your name:", self.input_text)
            
            logger.debug(f"Prompt returned: {repr(new_name)}")
            
            if new_name is not None:  # User didn't cancel
                # Limit length and handle empty string
                if not new_name:
                    new_name = "Player"
                else:
                    new_name = new_name[:20]
                
                self.input_text = new_name
                self.config.player_name = new_name
                self.config.save()
                logger.info(f"Player name updated via mobile prompt: '{new_name}'")
            else:
                logger.debug("User canceled mobile prompt")
                
        except ImportError as e:
            logger.error(f"Failed to import platform module: {e}")
        except AttributeError as e:
            logger.error(f"platform.window.prompt not available: {e}")
        except Exception as e:
            logger.error(f"Mobile text input failed: {e}", exc_info=True)

    
    def render(self, screen):
        """Render the menu with player name input"""
        # Call parent render for background and title
        super().render(screen)
        
        # Draw player name label
        label_text = self.input_font.render("Your Name:", True, (255, 255, 255))
        label_rect = label_text.get_rect(center=(self.screen_width // 2, self.input_rect.y - 35))
        screen.blit(label_text, label_rect)
        
        # Draw input box
        # On mobile browser, make it look like a button
        if self.is_mobile:
            # Draw as a button-like box
            input_color = (60, 60, 120)
            pygame.draw.rect(screen, input_color, self.input_rect)
            pygame.draw.rect(screen, (100, 100, 200), self.input_rect, 3)
            
            # Draw current name
            input_surface = self.input_font.render(self.input_text, True, (255, 255, 255))
            screen.blit(input_surface, (self.input_rect.x + 10, self.input_rect.y + 12))
            
            # Draw tap hint in bottom right of box
            hint_font = pygame.font.Font(None, 20)
            hint_text = hint_font.render("(tap to edit)", True, (150, 150, 150))
            hint_rect = hint_text.get_rect(right=self.input_rect.right - 5, centery=self.input_rect.centery)
            screen.blit(hint_text, hint_rect)
        else:
            # Desktop (both native and browser): Draw as editable text field
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



