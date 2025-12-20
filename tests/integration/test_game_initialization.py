"""
Integration tests for full game initialization flow.

These tests verify that all components can be properly initialized together,
catching issues that unit tests might miss due to testing components in isolation.
"""

import pygame
import pytest
from game.game_state import GameState
from game.renderer import Renderer
from game.input_handler import InputHandler


@pytest.fixture
def pygame_setup():
    """Initialize pygame for tests"""
    pygame.init()
    pygame.display.set_mode((1, 1))  # Minimal display for testing
    yield
    pygame.quit()


class TestGameInitialization:
    """Test the full game initialization flow"""
    
    def test_game_state_renderer_input_handler_integration(self, pygame_setup):
        """Test that GameState, Renderer, and InputHandler can be initialized together"""
        screen_width = 1200
        screen_height = 800
        
        # Create screen
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # Initialize GameState (like main.py does)
        game_state = GameState(
            screen_width,
            screen_height,
            player_name="TestPlayer",
            map_size="medium",
            ai_difficulty="medium",
            sound_pack="default"
        )
        
        # Initialize Renderer (like main.py does)
        renderer = Renderer(screen)
        
        # Initialize InputHandler (like main.py does)
        input_handler = InputHandler(game_state)
        
        # Verify basic properties
        assert game_state is not None
        assert renderer is not None
        assert input_handler is not None
        assert len(game_state.planets) > 0
        assert game_state.player_name == "TestPlayer"
    
    def test_renderer_has_required_methods(self, pygame_setup):
        """Test that Renderer has all the methods expected by main.py"""
        screen = pygame.display.set_mode((1200, 800))
        renderer = Renderer(screen)
        
        # These methods are called by main.py
        assert hasattr(renderer, 'render')
        assert hasattr(renderer, 'handle_mouse_motion')
        assert hasattr(renderer, 'is_quit_button_clicked')
        assert hasattr(renderer, 'is_win_button_clicked')
        assert hasattr(renderer, 'get_ability_clicked')
    
    def test_input_handler_has_required_methods(self, pygame_setup):
        """Test that InputHandler has all the methods expected by main.py"""
        screen_width = 1200
        screen_height = 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        game_state = GameState(
            screen_width,
            screen_height,
            player_name="TestPlayer",
            map_size="small",
            ai_difficulty="easy",
            sound_pack="default"
        )
        
        input_handler = InputHandler(game_state)
        
        # These methods are called by main.py
        assert hasattr(input_handler, 'handle_event')
    
    def test_game_state_with_all_map_sizes(self, pygame_setup):
        """Test that all map sizes can be initialized"""
        screen_width = 1200
        screen_height = 800
        
        for map_size in ['small', 'medium', 'large']:
            game_state = GameState(
                screen_width,
                screen_height,
                player_name="TestPlayer",
                map_size=map_size,
                ai_difficulty="medium",
                sound_pack="default"
            )
            
            assert game_state is not None
            assert len(game_state.planets) > 0
    
    def test_game_state_with_all_ai_difficulties(self, pygame_setup):
        """Test that all AI difficulties can be initialized"""
        screen_width = 1200
        screen_height = 800
        
        for ai_difficulty in ['easy', 'medium', 'hard']:
            game_state = GameState(
                screen_width,
                screen_height,
                player_name="TestPlayer",
                map_size="medium",
                ai_difficulty=ai_difficulty,
                sound_pack="default"
            )
            
            assert game_state is not None
            assert game_state.ai is not None
    
    def test_game_state_with_all_sound_packs(self, pygame_setup):
        """Test that all sound packs can be initialized"""
        screen_width = 1200
        screen_height = 800
        
        for sound_pack in ['default', 'classical', 'silly']:
            game_state = GameState(
                screen_width,
                screen_height,
                player_name="TestPlayer",
                map_size="medium",
                ai_difficulty="medium",
                sound_pack=sound_pack
            )
            
            assert game_state is not None
            assert game_state.sound_manager is not None
    
    def test_full_game_loop_iteration(self, pygame_setup):
        """Test that we can run one iteration of the game loop"""
        screen_width = 1200
        screen_height = 800
        screen = pygame.display.set_mode((screen_width, screen_height))
        
        # Initialize all components
        game_state = GameState(
            screen_width,
            screen_height,
            player_name="TestPlayer",
            map_size="small",
            ai_difficulty="easy",
            sound_pack="default"
        )
        renderer = Renderer(screen)
        input_handler = InputHandler(game_state)
        
        # Simulate one game loop iteration
        dt = 0.016  # ~60 FPS
        
        # Update game state
        game_state.update(dt)
        
        # Render (this should not crash)
        renderer.render(game_state)
        
        # Handle a mouse motion event (this should not crash)
        mouse_event = pygame.event.Event(pygame.MOUSEMOTION, {'pos': (100, 100)})
        input_handler.handle_event(mouse_event, renderer)
        
        # Handle a mouse click event (this should not crash)
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (100, 100), 'button': 1})
        input_handler.handle_event(click_event, renderer)
        
        # Handle a mouse up event (this should not crash)
        up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {'pos': (100, 100), 'button': 1})
        input_handler.handle_event(up_event, renderer)
        
        # If we get here without crashes, the test passes
        assert True
    
    def test_all_abilities_can_be_activated(self, pygame_setup):
        """Test that all abilities can be activated through GameState"""
        screen_width = 1200
        screen_height = 800
        
        game_state = GameState(
            screen_width,
            screen_height,
            player_name="TestPlayer",
            map_size="small",
            ai_difficulty="easy",
            sound_pack="default"
        )
        
        # Verify abilities exist
        assert 'recall' in game_state.player_abilities
        assert 'production' in game_state.player_abilities
        assert 'shield' in game_state.player_abilities
        
        # Test recall ability
        recall_ability = game_state.player_abilities['recall']
        assert recall_ability.is_available()
        game_state.activate_recall()
        assert not recall_ability.is_available()  # Should be unavailable after use
        
        # Test production surge ability
        production_ability = game_state.player_abilities['production']
        assert production_ability.is_available()
        game_state.activate_production_surge()
        assert production_ability.is_active()  # Should be active
        assert not production_ability.is_available()  # Should be unavailable
        
        # Test shield ability (needs a planet)
        player_planet = next((p for p in game_state.planets if p.owner == "Player"), None)
        assert player_planet is not None, "Should have at least one player planet"
        
        shield_ability = game_state.player_abilities['shield']
        assert shield_ability.is_available()
        game_state.activate_shield(player_planet)  # Pass the planet object, not ID
        assert shield_ability.is_active()  # Should be active
        assert not shield_ability.is_available()  # Should be unavailable
        assert shield_ability.target == player_planet  # Target should be the planet object

