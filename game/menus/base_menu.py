"""
Base menu components for consistent theming
"""
import pygame
import random


class MenuItem:
    """Represents a clickable menu item/button"""
    
    def __init__(self, text, x, y, width, height, action):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.hovered = False
        
        # Colors
        self.normal_color = (50, 50, 100)
        self.hover_color = (70, 70, 140)
        self.text_color = (255, 255, 255)
    
    def contains_point(self, x, y):
        """Check if a point is inside this menu item"""
        return self.rect.collidepoint(x, y)
    
    def set_hovered(self, hovered):
        """Set whether this item is currently hovered"""
        self.hovered = hovered
    
    def draw(self, screen, font):
        """Draw the menu item"""
        # Draw button background
        color = self.hover_color if self.hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # Border
        
        # Draw text centered
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)


class BaseMenu:
    """Base class for all menus with consistent theming"""
    
    def __init__(self, screen_width, screen_height, title, title_font_size=80, title_y_position=None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title = title
        
        # Title position (default to 1/3 down the screen, or use custom position)
        self.title_y_position = title_y_position if title_y_position is not None else screen_height // 3
        
        # Fonts
        self.title_font = pygame.font.Font(None, title_font_size)
        self.button_font = pygame.font.Font(None, 40)
        
        # Colors
        self.bg_color = (10, 10, 30)  # Dark space blue
        self.title_color = (255, 255, 255)
        
        # Menu items (to be populated by subclasses)
        self.menu_items = []
        
        # Separate random instance for stars (doesn't affect game RNG)
        self._star_rng = random.Random(42)
        self._stars = None  # Cache star positions
    
    def handle_mouse_motion(self, pos):
        """Handle mouse movement for hover effects"""
        for item in self.menu_items:
            item.set_hovered(item.contains_point(pos[0], pos[1]))
    
    def handle_click(self, pos):
        """
        Handle mouse click on menu
        
        Returns:
            Action string if a button was clicked, None otherwise
        """
        for item in self.menu_items:
            if item.contains_point(pos[0], pos[1]):
                return item.action
        return None
    
    def render(self, screen):
        """Render the menu"""
        # Clear screen
        screen.fill(self.bg_color)
        
        # Draw stars background
        self._draw_stars(screen)
        
        # Draw title
        title_text = self.title_font.render(self.title, True, self.title_color)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.title_y_position))
        screen.blit(title_text, title_rect)
        
        # Draw menu items
        for item in self.menu_items:
            item.draw(screen, self.button_font)
    
    def _draw_stars(self, screen):
        """Draw a simple starfield background"""
        # Generate stars once and cache them
        if self._stars is None:
            self._stars = []
            for _ in range(100):
                x = self._star_rng.randint(0, self.screen_width)
                y = self._star_rng.randint(0, self.screen_height)
                brightness = self._star_rng.randint(100, 255)
                self._stars.append((x, y, brightness))
        
        # Draw cached stars
        for x, y, brightness in self._stars:
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

