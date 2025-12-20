"""
Game configuration menu - map size and AI difficulty
"""
import pygame
from game.menus.base_menu import BaseMenu, MenuItem
from game.logger import get_logger

logger = get_logger(__name__)


class GameConfigMenu(BaseMenu):
    """Game configuration menu for size and AI settings"""
    
    def __init__(self, screen_width, screen_height):
        super().__init__(screen_width, screen_height, "Game Configuration", title_font_size=60)
        
        logger.debug("GameConfigMenu initialized")
        
        # Selected options
        self.selected_size = "medium"
        self.selected_ai = "medium"
        self.selected_sound = "default"
        
        # Create selection buttons
        button_width = 200
        button_height = 50
        spacing = 70
        
        # Position sections below the title with more space
        section_start_y = screen_height // 2 + 20
        
        # Map Size section (left)
        size_x = screen_width // 4 - button_width // 2
        
        self.size_buttons = [
            MenuItem("Small", size_x, section_start_y, button_width, button_height, "small"),
            MenuItem("Medium", size_x, section_start_y + spacing, button_width, button_height, "medium"),
            MenuItem("Large", size_x, section_start_y + spacing * 2, button_width, button_height, "large")
        ]
        
        # AI Difficulty section (center)
        ai_x = screen_width // 2 - button_width // 2
        
        self.ai_buttons = [
            MenuItem("Easy", ai_x, section_start_y, button_width, button_height, "easy"),
            MenuItem("Medium", ai_x, section_start_y + spacing, button_width, button_height, "medium"),
            MenuItem("Hard", ai_x, section_start_y + spacing * 2, button_width, button_height, "hard")
        ]
        
        # Sound Pack section (right)
        sound_x = 3 * screen_width // 4 - button_width // 2
        
        self.sound_buttons = [
            MenuItem("Default", sound_x, section_start_y, button_width, button_height, "default"),
            MenuItem("Classical", sound_x, section_start_y + spacing, button_width, button_height, "classical"),
            MenuItem("Silly", sound_x, section_start_y + spacing * 2, button_width, button_height, "silly")
        ]
        
        # Start Game button (bottom center)
        start_button_width = 300
        start_button_height = 60
        start_x = (screen_width - start_button_width) // 2
        start_y = section_start_y + spacing * 3 + 40
        
        self.start_button = MenuItem("Start Game", start_x, start_y, start_button_width, 
                                    start_button_height, "start")
        
        # Combine all buttons for easy iteration
        self.menu_items = self.size_buttons + self.ai_buttons + self.sound_buttons + [self.start_button]
        
        logger.debug(f"Start button rect: {self.start_button.rect}")
    
    def handle_click(self, pos):
        """
        Handle mouse click on menu
        
        Returns:
            Configuration dict if Start Game clicked, None otherwise
        """
        logger.debug(f"Config menu click at {pos}")
        
        # Check size buttons
        for button in self.size_buttons:
            if button.contains_point(pos[0], pos[1]):
                logger.info(f"Map size selected: {button.action}")
                self.selected_size = button.action
                return None
        
        # Check AI buttons
        for button in self.ai_buttons:
            if button.contains_point(pos[0], pos[1]):
                logger.info(f"AI difficulty selected: {button.action}")
                self.selected_ai = button.action
                return None
        
        # Check sound buttons
        for button in self.sound_buttons:
            if button.contains_point(pos[0], pos[1]):
                logger.info(f"Sound pack selected: {button.action}")
                self.selected_sound = button.action
                return None
        
        # Check start button
        logger.debug(f"Checking start button: pos={pos}, rect={self.start_button.rect}")
        logger.debug(f"Contains point result: {self.start_button.contains_point(pos[0], pos[1])}")
        
        if self.start_button.contains_point(pos[0], pos[1]):
            config = {
                "action": "start",
                "map_size": self.selected_size,
                "difficulty": self.selected_ai,
                "sound_pack": self.selected_sound
            }
            logger.info(f"Start game clicked with config: {config}")
            return config
        
        logger.debug("No button clicked")
        return None
    
    def render(self, screen):
        """Render the configuration menu"""
        # Call parent render for background and title
        super().render(screen)
        
        # Calculate label position (above buttons, with more space from title)
        label_y = self.screen_height // 2 - 40
        
        # Draw section labels
        label_font = pygame.font.Font(None, 36)
        
        # Map Size label (left)
        size_label = label_font.render("Map Size", True, (255, 255, 255))
        size_rect = size_label.get_rect(center=(self.screen_width // 4, label_y))
        screen.blit(size_label, size_rect)
        
        # AI Difficulty label (center)
        ai_label = label_font.render("AI Difficulty", True, (255, 255, 255))
        ai_rect = ai_label.get_rect(center=(self.screen_width // 2, label_y))
        screen.blit(ai_label, ai_rect)
        
        # Sound Pack label (right)
        sound_label = label_font.render("Sound Pack", True, (255, 255, 255))
        sound_rect = sound_label.get_rect(center=(3 * self.screen_width // 4, label_y))
        screen.blit(sound_label, sound_rect)
        
        # Draw all buttons with selection highlighting
        for button in self.size_buttons:
            is_selected = (button.action == self.selected_size)
            self._draw_button_with_selection(screen, button, is_selected)
        
        for button in self.ai_buttons:
            is_selected = (button.action == self.selected_ai)
            self._draw_button_with_selection(screen, button, is_selected)
        
        for button in self.sound_buttons:
            is_selected = (button.action == self.selected_sound)
            self._draw_button_with_selection(screen, button, is_selected)
        
        # Draw start button normally
        self.start_button.draw(screen, self.button_font)
    
    def _draw_button_with_selection(self, screen, button, is_selected):
        """Draw a button with selection highlighting"""
        import pygame
        
        # Determine color based on hover and selection
        if is_selected:
            color = (90, 140, 200)  # Bright blue for selected
        elif button.hovered:
            color = (70, 70, 140)   # Standard hover
        else:
            color = (50, 50, 100)   # Standard normal
        
        # Draw button
        pygame.draw.rect(screen, color, button.rect)
        
        # Thicker border if selected
        border_width = 3 if is_selected else 2
        pygame.draw.rect(screen, (255, 255, 255), button.rect, border_width)
        
        # Draw text
        text_surface = self.button_font.render(button.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=button.rect.center)
        screen.blit(text_surface, text_rect)

