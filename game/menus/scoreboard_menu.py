"""
Scoreboard menu - displays high scores
"""
import pygame
from game.menus.base_menu import BaseMenu
from game.logger import get_logger

logger = get_logger(__name__)


class ScoreboardMenu(BaseMenu):
    """Scoreboard display menu"""
    
    def __init__(self, screen_width, screen_height, scoreboard):
        # Position title higher on the page (80 pixels from top instead of screen_height // 3)
        super().__init__(screen_width, screen_height, "High Scores", title_font_size=70, title_y_position=80)
        
        logger.debug("ScoreboardMenu initialized")
        
        self.scoreboard = scoreboard
        self.table_font = pygame.font.Font(None, 24)
        self.header_font = pygame.font.Font(None, 28)
        
        # Back button
        button_width = 200
        button_height = 50
        self.back_button_rect = pygame.Rect(
            (screen_width - button_width) // 2,
            screen_height - 80,
            button_width,
            button_height
        )
        self.back_button_hovered = False
        logger.debug(f"Back button rect: {self.back_button_rect}")
    
    def handle_mouse_motion(self, pos):
        """Handle mouse motion for hover effects"""
        was_hovered = self.back_button_hovered
        self.back_button_hovered = self.back_button_rect.collidepoint(pos[0], pos[1])
        
        if self.back_button_hovered and not was_hovered:
            logger.debug(f"Back button hovered at {pos}")
    
    def handle_click(self, pos):
        """
        Handle mouse click
        
        Returns:
            "back" if back button clicked, None otherwise
        """
        logger.debug(f"Scoreboard click at {pos}")
        logger.debug(f"Back button rect: {self.back_button_rect}")
        logger.debug(f"Collidepoint result: {self.back_button_rect.collidepoint(pos[0], pos[1])}")
        
        if self.back_button_rect.collidepoint(pos[0], pos[1]):
            logger.info("Back button clicked - returning to menu")
            return "back"
        return None
    
    def render(self, screen):
        """Render the scoreboard"""
        # Call parent render for background and title
        super().render(screen)
        
        # Get scores
        scores = self.scoreboard.get_all_scores(limit=10)
        
        if not scores:
            # No scores yet
            text = self.button_font.render("No scores yet! Play a game to get started.", True, (200, 200, 200))
            text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            screen.blit(text, text_rect)
        else:
            # Draw table
            self._draw_scores_table(screen, scores)
        
        # Draw back button
        self._draw_back_button(screen)
    
    def _draw_scores_table(self, screen, scores):
        """Draw the scores table"""
        # Table position (starts below the title with good spacing)
        table_start_y = 160
        row_height = 35
        
        # Column positions (x coordinates)
        cols = {
            'rank': 50,
            'name': 120,
            'score': 320,
            'planets': 420,
            'ships': 530,
            'won': 660,
            'lost': 750
        }
        
        # Draw header
        headers = [
            ('rank', "#"),
            ('name', "Player"),
            ('score', "Score"),
            ('planets', "Planets"),
            ('ships', "Ships"),
            ('won', "Won"),
            ('lost', "Lost")
        ]
        
        y = table_start_y
        for col_key, header_text in headers:
            header_surface = self.header_font.render(header_text, True, (150, 200, 255))
            screen.blit(header_surface, (cols[col_key], y))
        
        # Draw separator line
        y += 30
        pygame.draw.line(screen, (100, 100, 150), (40, y), (self.screen_width - 40, y), 2)
        
        # Draw scores
        y += 10
        for idx, score_entry in enumerate(scores, 1):
            # Determine color based on cheater status
            if score_entry.get('is_cheater', False):
                text_color = (255, 100, 100)  # Red for cheaters
            elif not score_entry.get('victory', True):
                text_color = (150, 150, 150)  # Gray for defeats
            else:
                text_color = (255, 255, 255)  # White for victories
            
            # Rank
            rank_text = self.table_font.render(f"{idx}.", True, text_color)
            screen.blit(rank_text, (cols['rank'], y))
            
            # Player name (truncate if too long)
            name = score_entry.get('player_name', 'Unknown')
            if len(name) > 15:
                name = name[:12] + "..."
            name_text = self.table_font.render(name, True, text_color)
            screen.blit(name_text, (cols['name'], y))
            
            # Score
            score = score_entry.get('score', 0)
            score_str = str(score) if not isinstance(score, str) else score
            score_text = self.table_font.render(score_str, True, text_color)
            screen.blit(score_text, (cols['score'], y))
            
            # Planets
            planets = score_entry.get('planets_controlled', 0)
            planets_text = self.table_font.render(str(planets), True, text_color)
            screen.blit(planets_text, (cols['planets'], y))
            
            # Ships
            ships = score_entry.get('ships_produced', 0)
            ships_text = self.table_font.render(str(ships), True, text_color)
            screen.blit(ships_text, (cols['ships'], y))
            
            # Battles Won
            won = score_entry.get('battles_won', 0)
            won_text = self.table_font.render(str(won), True, text_color)
            screen.blit(won_text, (cols['won'], y))
            
            # Battles Lost
            lost = score_entry.get('battles_lost', 0)
            lost_text = self.table_font.render(str(lost), True, text_color)
            screen.blit(lost_text, (cols['lost'], y))
            
            y += row_height
    
    def _draw_back_button(self, screen):
        """Draw the back button"""
        button_color = (70, 70, 140) if self.back_button_hovered else (50, 50, 100)
        
        pygame.draw.rect(screen, button_color, self.back_button_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.back_button_rect, 2)
        
        text = self.button_font.render("Back to Menu", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.back_button_rect.center)
        screen.blit(text, text_rect)

