"""
Sound effects system for Planet Wars
Uses pluggable sound system
"""
import pygame
from game.sound_plugins import create_sound_plugin
from game.logger import get_logger

logger = get_logger(__name__)


class SoundManager:
    """Manages all game sound effects using plugins"""
    
    def __init__(self, plugin_name="default"):
        """
        Initialize sound manager with a specific plugin
        
        Args:
            plugin_name: "default", "classical", or "silly"
        """
        logger.info(f"Initializing SoundManager: plugin={plugin_name}")
        
        # Initialize pygame mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            logger.debug("Pygame mixer initialized")
        
        # Load the sound plugin
        self.plugin = create_sound_plugin(plugin_name)
        self.plugin_name = plugin_name
        logger.debug(f"Sound plugin loaded: {type(self.plugin).__name__}")
    
    def play_attack_succeeded(self):
        """Play sound when an attack successfully conquers a planet"""
        self.plugin.attack_succeeded()
    
    def play_attack_failed(self):
        """Play sound when an attack fails to conquer a planet"""
        self.plugin.attack_failed()
    
    def play_fleet_launched(self):
        """Play sound when a fleet is launched"""
        self.plugin.fleet_launched()
    
    def play_game_victory(self):
        """Play sound when player wins the game"""
        self.plugin.game_victory()
    
    def play_game_defeat(self):
        """Play sound when player loses the game"""
        self.plugin.game_defeat()
    
    def change_plugin(self, plugin_name):
        """
        Switch to a different sound plugin
        
        Args:
            plugin_name: "default", "classical", or "silly"
        """
        # Cleanup old plugin
        if hasattr(self.plugin, 'cleanup'):
            self.plugin.cleanup()
        
        # Load new plugin
        self.plugin = create_sound_plugin(plugin_name)
        self.plugin_name = plugin_name
    
    def stop_all(self):
        """Stop all currently playing sounds"""
        pygame.mixer.stop()
