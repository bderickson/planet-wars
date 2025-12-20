"""
Game Over screen for victory or defeat
"""
import pygame
import random


class GameOver:
    """Game over screen showing victory or defeat"""
    
    def __init__(self, screen_width, screen_height, victory=True, planets_controlled=0, 
                 ships_produced=0, battles_won=0, battles_lost=0, score=0, is_cheater=False, game_time=0):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.victory = victory
        
        # Game statistics
        self.planets_controlled = planets_controlled
        self.ships_produced = ships_produced
        self.battles_won = battles_won
        self.battles_lost = battles_lost
        self.score = score
        self.is_cheater = is_cheater
        self.game_time = game_time
        
        # Fonts
        self.title_font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 40)
        self.stats_font = pygame.font.Font(None, 32)
        
        # Colors
        self.bg_color = (10, 10, 30)
        self.victory_color = (100, 255, 100)  # Green
        self.defeat_color = (255, 100, 100)   # Red
        
        # Victory phrases - randomly select one
        victory_phrases = [
            "You have unlimited aura",
            "You're so cool",
            "Brian Approved",
            "Absolutely legendary",
            "Galaxy brain plays",
            "Sigma grindset achieved",
            "Touch grass? Nah, touch stars",
            "Main character energy",
            "Built different",
            "No cap, that was fire"
        ]
        self.victory_phrase = random.choice(victory_phrases) if victory else ""
        
        # Button - move down to make room for stats
        self.button_rect = pygame.Rect(
            (screen_width - 300) // 2,
            screen_height - 100,  # Near bottom
            300,
            60
        )
        self.button_hovered = False
        self.button_normal_color = (50, 50, 100)
        self.button_hover_color = (70, 70, 140)
        self.button_text_color = (255, 255, 255)
        
        # Separate random instance for stars (doesn't affect game RNG)
        self._star_rng = random.Random(42)
        self._stars = None  # Cache star positions
    
    def handle_mouse_motion(self, pos):
        """Handle mouse movement for hover effects"""
        self.button_hovered = self.button_rect.collidepoint(pos[0], pos[1])
    
    def handle_click(self, pos):
        """
        Handle mouse click
        
        Returns:
            "menu" if button was clicked, None otherwise
        """
        if self.button_rect.collidepoint(pos[0], pos[1]):
            return "menu"
        return None
    
    def render(self, screen):
        """Render the game over screen"""
        # Clear screen
        screen.fill(self.bg_color)
        
        # Draw stars background
        self._draw_stars(screen)
        
        # Draw victory/defeat message - moved higher
        title_text = "VICTORY!" if self.victory else "DEFEAT"
        title_color = self.victory_color if self.victory else self.defeat_color
        
        title_surface = self.title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 80))  # Fixed position at top
        screen.blit(title_surface, title_rect)
        
        # Draw subtitle
        subtitle_font = pygame.font.Font(None, 30)
        if self.victory:
            subtitle_text = "You have conquered the galaxy!"
        else:
            subtitle_text = "Your empire has fallen..."
        
        subtitle_surface = subtitle_font.render(subtitle_text, True, (255, 255, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(self.screen_width // 2, 130))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw special victory message
        if self.victory:
            aura_font = pygame.font.Font(None, 40)  # Slightly smaller
            aura_surface = aura_font.render(self.victory_phrase, True, (255, 215, 0))  # Gold color
            aura_rect = aura_surface.get_rect(center=(self.screen_width // 2, 170))
            screen.blit(aura_surface, aura_rect)
        
        # Draw game statistics
        self._draw_statistics(screen)
        
        # Draw button
        button_color = self.button_hover_color if self.button_hovered else self.button_normal_color
        pygame.draw.rect(screen, button_color, self.button_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 2)  # Border
        
        button_text = self.button_font.render("Back to Menu", True, self.button_text_color)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        screen.blit(button_text, button_text_rect)
    
    def _draw_statistics(self, screen):
        """Draw game statistics"""
        # Start stats section higher up
        stats_y_start = 220
        line_spacing = 35  # Tighter spacing
        
        # Draw SCORE prominently at the top
        if self.is_cheater:
            score_text = "CHEATER"
            score_color = (255, 50, 50)  # Red
        else:
            score_text = f"Score: {self.score}"
            score_color = (255, 215, 0)  # Gold
        
        score_font = pygame.font.Font(None, 50)  # Slightly smaller
        score_surface = score_font.render(score_text, True, score_color)
        score_rect = score_surface.get_rect(center=(self.screen_width // 2, stats_y_start))
        screen.blit(score_surface, score_rect)
        
        # Show time if victory and not cheater
        current_y = stats_y_start + 45
        if self.victory and not self.is_cheater and self.game_time > 0:
            minutes = int(self.game_time // 60)
            seconds = int(self.game_time % 60)
            time_text = f"Time: {minutes}:{seconds:02d}"
            time_surface = self.stats_font.render(time_text, True, (150, 200, 255))
            time_rect = time_surface.get_rect(center=(self.screen_width // 2, current_y))
            screen.blit(time_surface, time_rect)
            current_y += 35
        
        # Statistics to display
        stats = [
            f"Planets Controlled: {self.planets_controlled}",
            f"Ships Produced: {self.ships_produced}",
            f"Battles Won: {self.battles_won}",
            f"Battles Lost: {self.battles_lost}"
        ]
        
        # Draw header
        header_y = current_y + 10
        header_surface = self.stats_font.render("Game Statistics", True, (200, 200, 255))
        header_rect = header_surface.get_rect(center=(self.screen_width // 2, header_y))
        screen.blit(header_surface, header_rect)
        
        # Draw each stat with tighter spacing
        y_offset = header_y + 35
        for stat_text in stats:
            stat_surface = self.stats_font.render(stat_text, True, (255, 255, 255))
            stat_rect = stat_surface.get_rect(center=(self.screen_width // 2, y_offset))
            screen.blit(stat_surface, stat_rect)
            y_offset += line_spacing
    
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

