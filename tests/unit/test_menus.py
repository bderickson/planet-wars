"""
Unit tests for menu classes
"""
import pytest
import pygame
from unittest.mock import Mock, MagicMock, patch
from game.menus.base_menu import MenuItem, BaseMenu
from game.menus.menu import Menu
from game.menus.game_config_menu import GameConfigMenu
from game.menus.scoreboard_menu import ScoreboardMenu
from game.config import Config


@pytest.fixture
def pygame_init():
    """Initialize pygame before tests"""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def screen(pygame_init):
    """Create a test screen"""
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def config(tmp_path):
    """Create a test config"""
    config_file = tmp_path / "config.json"
    return Config(str(config_file))


class TestMenuItem:
    """Test MenuItem class"""
    
    def test_init(self, pygame_init):
        """Test MenuItem initialization"""
        item = MenuItem("Test", 100, 100, 200, 50, "test_action")
        
        assert item.text == "Test"
        assert item.rect.x == 100
        assert item.rect.y == 100
        assert item.rect.width == 200
        assert item.rect.height == 50
        assert item.action == "test_action"
        assert item.hovered == False
    
    def test_contains_point_inside(self, pygame_init):
        """Test contains_point with point inside"""
        item = MenuItem("Test", 100, 100, 200, 50, "test")
        
        assert item.contains_point(150, 125) == True
        assert item.contains_point(100, 100) == True  # Edge
        assert item.contains_point(299, 149) == True  # Edge
    
    def test_contains_point_outside(self, pygame_init):
        """Test contains_point with point outside"""
        item = MenuItem("Test", 100, 100, 200, 50, "test")
        
        assert item.contains_point(50, 50) == False
        assert item.contains_point(350, 200) == False
    
    def test_set_hovered(self, pygame_init):
        """Test set_hovered"""
        item = MenuItem("Test", 100, 100, 200, 50, "test")
        
        item.set_hovered(True)
        assert item.hovered == True
        
        item.set_hovered(False)
        assert item.hovered == False
    
    def test_draw(self, pygame_init, screen):
        """Test drawing menu item"""
        item = MenuItem("Test", 100, 100, 200, 50, "test")
        font = pygame.font.Font(None, 32)
        
        # Should not crash
        item.draw(screen, font)
        
        # Test with hover
        item.set_hovered(True)
        item.draw(screen, font)


class TestBaseMenu:
    """Test BaseMenu class"""
    
    def test_init(self, pygame_init):
        """Test BaseMenu initialization"""
        menu = BaseMenu(800, 600, "Test Menu")
        
        assert menu.screen_width == 800
        assert menu.screen_height == 600
        assert menu.title == "Test Menu"
        assert isinstance(menu.title_font, pygame.font.Font)
        assert isinstance(menu.button_font, pygame.font.Font)
    
    def test_custom_title_position(self, pygame_init):
        """Test custom title position"""
        menu = BaseMenu(800, 600, "Test", title_y_position=100)
        
        assert menu.title_y_position == 100
    
    def test_default_title_position(self, pygame_init):
        """Test default title position"""
        menu = BaseMenu(800, 600, "Test")
        
        assert menu.title_y_position == 600 // 3
    
    def test_render(self, pygame_init, screen):
        """Test rendering base menu"""
        menu = BaseMenu(800, 600, "Test")
        
        # Should not crash
        menu.render(screen)


class TestMenu:
    """Test Menu class (main menu)"""
    
    def test_init(self, pygame_init, config):
        """Test Menu initialization"""
        menu = Menu(800, 600, config)
        
        assert menu.config == config
        assert menu.title == "Planet Wars"
        assert len(menu.menu_items) == 3  # New Game, High Scores, Quit
    
    def test_menu_items(self, pygame_init, config):
        """Test menu items are created"""
        menu = Menu(800, 600, config)
        
        actions = [item.action for item in menu.menu_items]
        assert "new_game" in actions
        assert "scoreboard" in actions  # Changed from high_scores
        assert "quit" in actions
    
    def test_handle_click_new_game(self, pygame_init, config):
        """Test clicking new game"""
        menu = Menu(800, 600, config)
        
        # Find new game button
        new_game = next(item for item in menu.menu_items if item.action == "new_game")
        
        result = menu.handle_click(new_game.rect.center)
        assert result == "new_game"
    
    def test_handle_click_quit(self, pygame_init, config):
        """Test clicking quit"""
        menu = Menu(800, 600, config)
        
        quit_item = next(item for item in menu.menu_items if item.action == "quit")
        result = menu.handle_click(quit_item.rect.center)
        assert result == "quit"
    
    def test_handle_click_outside(self, pygame_init, config):
        """Test clicking outside buttons"""
        menu = Menu(800, 600, config)
        
        result = menu.handle_click((10, 10))
        assert result is None
    
    def test_handle_mouse_motion(self, pygame_init, config):
        """Test mouse motion updates hover state"""
        menu = Menu(800, 600, config)
        
        # Hover over first item
        first_item = menu.menu_items[0]
        menu.handle_mouse_motion(first_item.rect.center)
        
        assert first_item.hovered == True
    
    def test_player_name_input_active(self, pygame_init, config):
        """Test player name input activation"""
        menu = Menu(800, 600, config)
        
        # Click on input box
        menu.handle_text_input(Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center))
        
        assert menu.input_active == True
    
    def test_player_name_input_text(self, pygame_init, config):
        """Test typing in player name auto-saves"""
        menu = Menu(800, 600, config)
        menu.input_active = True
        initial_name = config.player_name
        
        # Type character
        event = Mock(type=pygame.KEYDOWN, key=ord('A'), unicode='A')
        menu.handle_text_input(event)
        
        assert 'A' in menu.input_text
        # Verify it auto-saved
        assert config.player_name == menu.input_text
        assert config.player_name != initial_name
    
    def test_player_name_input_backspace(self, pygame_init, config):
        """Test backspace in player name auto-saves"""
        menu = Menu(800, 600, config)
        menu.input_active = True
        menu.input_text = "ABC"
        config.player_name = "ABC"
        
        event = Mock(type=pygame.KEYDOWN, key=pygame.K_BACKSPACE, unicode='')
        menu.handle_text_input(event)
        
        assert menu.input_text == "AB"
        # Verify it auto-saved
        assert config.player_name == "AB"
    
    def test_render(self, pygame_init, config, screen):
        """Test rendering menu"""
        menu = Menu(800, 600, config)
        
        # Should not crash
        menu.render(screen)
    
    @patch('sys.platform', 'linux')
    def test_desktop_platform_detection(self, pygame_init, config):
        """Test that is_browser is False on desktop"""
        menu = Menu(800, 600, config)
        assert menu.is_browser == False
    
    @patch('sys.platform', 'emscripten')
    def test_browser_platform_detection(self, pygame_init, config):
        """Test that is_browser is True in browser"""
        menu = Menu(800, 600, config)
        assert menu.is_browser == True
    
    @patch('sys.platform', 'emscripten')
    def test_mobile_text_input_prompt(self, pygame_init, config):
        """Test mobile text input via JavaScript prompt"""
        with patch('platform.window', create=True) as mock_window:
            mock_window.prompt.return_value = "MobileUser"
            
            menu = Menu(800, 600, config)
            
            # Simulate clicking input box on mobile
            event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
            menu.handle_text_input(event)
            
            # Verify prompt was called
            mock_window.prompt.assert_called_once()
            assert menu.input_text == "MobileUser"
            assert config.player_name == "MobileUser"
    
    @patch('sys.platform', 'emscripten')
    def test_mobile_text_input_cancel(self, pygame_init, config):
        """Test mobile text input when user cancels"""
        with patch('platform.window', create=True) as mock_window:
            # Setup mock - None means user canceled
            mock_window.prompt.return_value = None
            
            menu = Menu(800, 600, config)
            original_name = menu.input_text
            
            # Simulate clicking input box on mobile
            event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
            menu.handle_text_input(event)
            
            # Name should not change when canceled
            assert menu.input_text == original_name
    
    @patch('sys.platform', 'emscripten')
    def test_mobile_text_input_length_limit(self, pygame_init, config):
        """Test mobile text input respects 20 character limit"""
        with patch('platform.window', create=True) as mock_window:
            # Setup mock with very long name
            mock_window.prompt.return_value = "A" * 50
            
            menu = Menu(800, 600, config)
            
            # Simulate clicking input box on mobile
            event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
            menu.handle_text_input(event)
            
            # Should be truncated to 20 characters
            assert len(menu.input_text) == 20
            assert menu.input_text == "A" * 20
    
    @patch('sys.platform', 'emscripten')
    def test_mobile_text_input_empty_string(self, pygame_init, config):
        """Test mobile text input with empty string"""
        with patch('platform.window', create=True) as mock_window:
            # Setup mock with empty string
            mock_window.prompt.return_value = ""
            
            menu = Menu(800, 600, config)
            
            # Simulate clicking input box on mobile
            event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
            menu.handle_text_input(event)
            
            # Should default to "Player"
            assert menu.input_text == "Player"
            assert config.player_name == "Player"
    
    @patch('sys.platform', 'emscripten')
    def test_mobile_text_input_no_platform_window(self, pygame_init, config):
        """Test mobile text input when platform.window is not available"""
        menu = Menu(800, 600, config)
        original_name = menu.input_text
        
        # Simulate clicking input box on mobile (should not crash)
        event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
        menu.handle_text_input(event)
        
        # Should not crash, name may or may not change
        assert menu.input_text is not None
    
    @patch('sys.platform', 'linux')
    def test_desktop_text_input_activates_field(self, pygame_init, config):
        """Test that clicking input on desktop activates the field"""
        menu = Menu(800, 600, config)
        
        # Simulate clicking input box on desktop
        event = Mock(type=pygame.MOUSEBUTTONDOWN, pos=menu.input_rect.center)
        menu.handle_text_input(event)
        
        # Should activate input field (not open prompt)
        assert menu.input_active == True
    
    def test_github_link_rendered(self, pygame_init, config, screen):
        """Test that GitHub link is rendered on menu"""
        menu = Menu(800, 600, config)
        
        # Render and verify it doesn't crash
        menu.render(screen)
        
        # The link should be part of the rendering
        # (visual inspection needed for actual appearance)


class TestGameConfigMenu:
    """Test GameConfigMenu class"""
    
    def test_init(self, pygame_init):
        """Test GameConfigMenu initialization"""
        menu = GameConfigMenu(800, 600)
        
        assert menu.title == "Game Configuration"
        assert menu.selected_size == "medium"  # Changed from selected_map_size
        assert menu.selected_ai == "medium"    # Changed from selected_difficulty
        assert menu.selected_sound == "default"  # Changed from selected_sound_pack
    
    def test_map_size_selection(self, pygame_init):
        """Test selecting map size"""
        menu = GameConfigMenu(800, 600)
        
        # Find small button (action is just "small", not "map_small")
        small_item = next(item for item in menu.size_buttons if item.action == "small")
        menu.handle_click(small_item.rect.center)
        
        assert menu.selected_size == "small"
    
    def test_difficulty_selection(self, pygame_init):
        """Test selecting difficulty"""
        menu = GameConfigMenu(800, 600)
        
        hard_item = next(item for item in menu.ai_buttons if item.action == "hard")
        menu.handle_click(hard_item.rect.center)
        
        assert menu.selected_ai == "hard"
    
    def test_sound_pack_selection(self, pygame_init):
        """Test selecting sound pack"""
        menu = GameConfigMenu(800, 600)
        
        classical_item = next(item for item in menu.sound_buttons if item.action == "classical")
        menu.handle_click(classical_item.rect.center)
        
        assert menu.selected_sound == "classical"
    
    def test_start_game(self, pygame_init):
        """Test starting game"""
        menu = GameConfigMenu(800, 600)
        menu.selected_size = "large"
        menu.selected_ai = "hard"
        menu.selected_sound = "silly"
        
        start_item = next(item for item in menu.menu_items if item.action == "start")
        result = menu.handle_click(start_item.rect.center)
        
        assert result == {
            "action": "start",
            "map_size": "large",
            "difficulty": "hard",
            "sound_pack": "silly"
        }
    
    def test_render(self, pygame_init, screen):
        """Test rendering config menu"""
        menu = GameConfigMenu(800, 600)
        
        # Should not crash
        menu.render(screen)


class TestScoreboardMenu:
    """Test ScoreboardMenu class"""
    
    def test_init(self, pygame_init):
        """Test ScoreboardMenu initialization"""
        from game.scoreboard import Scoreboard
        
        scoreboard = Scoreboard()
        scoreboard.scores = [
            {"player_name": "Alice", "score": 100, "planets": 5},
            {"player_name": "Bob", "score": 80, "planets": 3}
        ]
        
        menu = ScoreboardMenu(800, 600, scoreboard)
        
        assert menu.title == "High Scores"
        assert menu.scoreboard == scoreboard
    
    def test_empty_scoreboard(self, pygame_init, tmp_path):
        """Test with empty scoreboard"""
        from game.scoreboard import Scoreboard
        
        # Create a scoreboard with a custom path to avoid loading existing scores
        scoreboard_file = tmp_path / "empty_scoreboard.json"
        scoreboard = Scoreboard(str(scoreboard_file))
        menu = ScoreboardMenu(800, 600, scoreboard)
        
        assert len(menu.scoreboard.scores) == 0
    
    def test_back_button(self, pygame_init, tmp_path):
        """Test back button"""
        from game.scoreboard import Scoreboard
        
        scoreboard_file = tmp_path / "test_scoreboard.json"
        scoreboard = Scoreboard(str(scoreboard_file))
        menu = ScoreboardMenu(800, 600, scoreboard)
        
        # Click on back button using the back_button_rect
        result = menu.handle_click(menu.back_button_rect.center)
        
        assert result == "back"
    
    def test_render(self, pygame_init, screen):
        """Test rendering scoreboard"""
        from game.scoreboard import Scoreboard
        
        scoreboard = Scoreboard()
        scoreboard.scores = [{"player_name": "Test", "score": 100, "planets": 5}]
        menu = ScoreboardMenu(800, 600, scoreboard)
        
        # Should not crash
        menu.render(screen)
    
    def test_render_many_scores(self, pygame_init, screen):
        """Test rendering with many scores"""
        from game.scoreboard import Scoreboard
        
        scoreboard = Scoreboard()
        scoreboard.scores = [
            {"player_name": f"Player{i}", "score": 100-i, "planets": 5}
            for i in range(20)
        ]
        
        menu = ScoreboardMenu(800, 600, scoreboard)
        menu.render(screen)


class TestMenuIntegration:
    """Test menu interactions"""
    
    def test_menu_to_config_flow(self, pygame_init, config, screen):
        """Test navigating from main menu to config"""
        main_menu = Menu(800, 600, config)
        
        # Click new game
        new_game_item = next(item for item in main_menu.menu_items if item.action == "new_game")
        result = main_menu.handle_click(new_game_item.rect.center)
        
        assert result == "new_game"
        
        # Create config menu
        config_menu = GameConfigMenu(800, 600)
        config_menu.render(screen)
    
    def test_menu_to_scoreboard_flow(self, pygame_init, config, screen):
        """Test navigating from main menu to scoreboard"""
        from game.scoreboard import Scoreboard
        
        main_menu = Menu(800, 600, config)
        
        # Click scoreboard (changed from high_scores)
        scores_item = next(item for item in main_menu.menu_items if item.action == "scoreboard")
        result = main_menu.handle_click(scores_item.rect.center)
        
        assert result == "scoreboard"
        
        # Create scoreboard menu
        scoreboard = Scoreboard()
        scoreboard_menu = ScoreboardMenu(800, 600, scoreboard)
        scoreboard_menu.render(screen)


@pytest.fixture(autouse=True)
def cleanup():
    """Clean up after each test"""
    yield
    # Cleanup happens automatically

