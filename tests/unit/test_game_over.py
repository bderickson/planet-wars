"""
Unit tests for the GameOver screen
Note: These tests focus on logic and state; rendering tests are excluded
due to pygame display requirements.
"""
import pytest
from unittest.mock import MagicMock, patch
from game.game_over import GameOver


# Mock pygame to avoid display requirements
@pytest.fixture(autouse=True)
def mock_pygame():
    """Mock pygame for all tests in this module"""
    with patch('game.game_over.pygame') as mock_pg:
        # Mock font
        mock_font = MagicMock()
        mock_pg.font.Font.return_value = mock_font
        
        # Mock Rect
        mock_rect = MagicMock()
        mock_rect.collidepoint.return_value = False
        mock_pg.Rect.return_value = mock_rect
        
        yield mock_pg


class TestGameOverInit:
    """Tests for GameOver initialization"""
    
    def test_init_victory(self):
        """Test initialization for victory"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True
        )
        
        assert game_over.victory is True
        assert game_over.screen_width == 800
        assert game_over.screen_height == 600
    
    def test_init_defeat(self):
        """Test initialization for defeat"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=False
        )
        
        assert game_over.victory is False
    
    def test_init_with_statistics(self):
        """Test initialization with game statistics"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True,
            planets_controlled=5,
            ships_produced=150,
            battles_won=10,
            battles_lost=3
        )
        
        assert game_over.planets_controlled == 5
        assert game_over.ships_produced == 150
        assert game_over.battles_won == 10
        assert game_over.battles_lost == 3
    
    def test_init_with_score(self):
        """Test initialization with score"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True,
            score=125
        )
        
        assert game_over.score == 125
    
    def test_init_cheater_flag(self):
        """Test initialization with cheater flag"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True,
            score=100,
            is_cheater=True
        )
        
        assert game_over.is_cheater is True
    
    def test_init_game_time(self):
        """Test initialization with game time"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True,
            game_time=125.5
        )
        
        assert game_over.game_time == 125.5
    
    def test_init_victory_has_phrase(self):
        """Test that victory screen gets a victory phrase"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True
        )
        
        assert hasattr(game_over, 'victory_phrase')
        assert len(game_over.victory_phrase) > 0
    
    def test_init_defeat_no_phrase(self):
        """Test that defeat screen has empty phrase"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=False
        )
        
        assert game_over.victory_phrase == ""
    
    def test_init_victory_phrase_varies(self):
        """Test that victory phrase varies between instances"""
        phrases = set()
        for _ in range(20):
            game_over = GameOver(
                screen_width=800,
                screen_height=600,
                victory=True
            )
            phrases.add(game_over.victory_phrase)
        
        # Should have some variety (at least 3 different phrases)
        assert len(phrases) >= 3
    
    def test_init_creates_button(self):
        """Test that initialization creates button rect"""
        game_over = GameOver(
            screen_width=800,
            screen_height=600,
            victory=True
        )
        
        assert hasattr(game_over, 'button_rect')
        assert game_over.button_hovered is False


class TestGameOverHandleMouseMotion:
    """Tests for mouse motion handling"""
    
    def test_handle_mouse_motion_over_button(self):
        """Test mouse motion over button"""
        game_over = GameOver(800, 600, victory=True)
        
        # Mock button collision
        game_over.button_rect.collidepoint.return_value = True
        
        game_over.handle_mouse_motion((250, 500))
        
        assert game_over.button_hovered is True
    
    def test_handle_mouse_motion_not_over_button(self):
        """Test mouse motion not over button"""
        game_over = GameOver(800, 600, victory=True)
        
        # Mock no collision
        game_over.button_rect.collidepoint.return_value = False
        
        game_over.handle_mouse_motion((100, 100))
        
        assert game_over.button_hovered is False
    
    def test_handle_mouse_motion_multiple_times(self):
        """Test multiple mouse motions"""
        game_over = GameOver(800, 600, victory=True)
        
        # Hover
        game_over.button_rect.collidepoint.return_value = True
        game_over.handle_mouse_motion((250, 500))
        assert game_over.button_hovered is True
        
        # Move away
        game_over.button_rect.collidepoint.return_value = False
        game_over.handle_mouse_motion((100, 100))
        assert game_over.button_hovered is False


class TestGameOverHandleClick:
    """Tests for mouse click handling"""
    
    def test_handle_click_on_button(self):
        """Test clicking on button returns menu"""
        game_over = GameOver(800, 600, victory=True)
        
        # Mock button collision
        game_over.button_rect.collidepoint.return_value = True
        
        result = game_over.handle_click((250, 500))
        
        assert result == "menu"
    
    def test_handle_click_not_on_button(self):
        """Test clicking outside button returns None"""
        game_over = GameOver(800, 600, victory=True)
        
        # Mock no collision
        game_over.button_rect.collidepoint.return_value = False
        
        result = game_over.handle_click((100, 100))
        
        assert result is None
    
    def test_handle_click_coordinates(self):
        """Test that click coordinates are passed correctly"""
        game_over = GameOver(800, 600, victory=True)
        
        click_pos = (123, 456)
        game_over.handle_click(click_pos)
        
        # Verify collidepoint was called with correct coordinates
        game_over.button_rect.collidepoint.assert_called_with(123, 456)


class TestGameOverStatistics:
    """Tests for statistics handling"""
    
    def test_default_statistics(self):
        """Test default statistics are zero"""
        game_over = GameOver(800, 600, victory=True)
        
        assert game_over.planets_controlled == 0
        assert game_over.ships_produced == 0
        assert game_over.battles_won == 0
        assert game_over.battles_lost == 0
    
    def test_custom_statistics(self):
        """Test custom statistics are stored"""
        game_over = GameOver(
            800, 600,
            victory=True,
            planets_controlled=7,
            ships_produced=250,
            battles_won=15,
            battles_lost=5
        )
        
        assert game_over.planets_controlled == 7
        assert game_over.ships_produced == 250
        assert game_over.battles_won == 15
        assert game_over.battles_lost == 5
    
    def test_statistics_independent_of_victory(self):
        """Test that statistics work for both victory and defeat"""
        victory_screen = GameOver(
            800, 600,
            victory=True,
            planets_controlled=10,
            battles_won=20
        )
        
        defeat_screen = GameOver(
            800, 600,
            victory=False,
            planets_controlled=2,
            battles_lost=15
        )
        
        assert victory_screen.planets_controlled == 10
        assert defeat_screen.planets_controlled == 2


class TestGameOverScore:
    """Tests for score handling"""
    
    def test_default_score(self):
        """Test default score is zero"""
        game_over = GameOver(800, 600, victory=True)
        assert game_over.score == 0
    
    def test_custom_score(self):
        """Test custom score is stored"""
        game_over = GameOver(800, 600, victory=True, score=150)
        assert game_over.score == 150
    
    def test_zero_score(self):
        """Test zero score for defeat"""
        game_over = GameOver(800, 600, victory=False, score=0)
        assert game_over.score == 0
    
    def test_cheater_flag(self):
        """Test cheater flag overrides score display"""
        game_over = GameOver(
            800, 600,
            victory=True,
            score=100,
            is_cheater=True
        )
        
        assert game_over.is_cheater is True
        # Score value still stored, but display should show "CHEATER"


class TestGameOverColors:
    """Tests for color assignments"""
    
    def test_has_victory_color(self):
        """Test that GameOver defines victory color"""
        game_over = GameOver(800, 600, victory=True)
        assert hasattr(game_over, 'victory_color')
        assert len(game_over.victory_color) == 3  # RGB tuple
    
    def test_has_defeat_color(self):
        """Test that GameOver defines defeat color"""
        game_over = GameOver(800, 600, victory=False)
        assert hasattr(game_over, 'defeat_color')
        assert len(game_over.defeat_color) == 3  # RGB tuple
    
    def test_colors_are_different(self):
        """Test that victory and defeat colors are different"""
        game_over = GameOver(800, 600, victory=True)
        assert game_over.victory_color != game_over.defeat_color


class TestGameOverStarfield:
    """Tests for starfield background"""
    
    def test_stars_cached(self):
        """Test that stars are cached after first generation"""
        game_over = GameOver(800, 600, victory=True)
        
        # Initially None
        assert game_over._stars is None
        
        # After render would be called, stars would be generated and cached
        # (We can't test render directly without pygame display)
    
    def test_star_rng_separate(self):
        """Test that star RNG is separate instance"""
        game_over = GameOver(800, 600, victory=True)
        
        assert hasattr(game_over, '_star_rng')
        # Should not affect global random


class TestGameOverEdgeCases:
    """Tests for edge cases"""
    
    def test_very_small_screen(self):
        """Test with very small screen dimensions"""
        game_over = GameOver(100, 100, victory=True)
        
        assert game_over.screen_width == 100
        assert game_over.screen_height == 100
    
    def test_very_large_screen(self):
        """Test with very large screen dimensions"""
        game_over = GameOver(4000, 3000, victory=True)
        
        assert game_over.screen_width == 4000
        assert game_over.screen_height == 3000
    
    def test_negative_statistics(self):
        """Test with negative statistics (shouldn't happen but test it)"""
        game_over = GameOver(
            800, 600,
            victory=True,
            planets_controlled=-1,
            ships_produced=-10
        )
        
        # Should still store the values
        assert game_over.planets_controlled == -1
        assert game_over.ships_produced == -10
    
    def test_very_large_statistics(self):
        """Test with very large statistics"""
        game_over = GameOver(
            800, 600,
            victory=True,
            planets_controlled=999,
            ships_produced=999999,
            battles_won=999,
            battles_lost=999
        )
        
        assert game_over.ships_produced == 999999
    
    def test_very_large_score(self):
        """Test with very large score"""
        game_over = GameOver(800, 600, victory=True, score=999999)
        assert game_over.score == 999999
    
    def test_long_game_time(self):
        """Test with very long game time"""
        game_over = GameOver(800, 600, victory=True, game_time=3600)
        assert game_over.game_time == 3600
    
    def test_fractional_game_time(self):
        """Test with fractional game time"""
        game_over = GameOver(800, 600, victory=True, game_time=123.456)
        assert game_over.game_time == 123.456


class TestGameOverVictoryPhrases:
    """Tests for victory phrase system"""
    
    def test_victory_phrase_from_known_list(self):
        """Test that victory phrase is from known list"""
        known_phrases = [
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
        
        game_over = GameOver(800, 600, victory=True)
        assert game_over.victory_phrase in known_phrases
    
    def test_defeat_has_no_victory_phrase(self):
        """Test that defeat doesn't show victory phrase"""
        game_over = GameOver(800, 600, victory=False)
        assert game_over.victory_phrase == ""

