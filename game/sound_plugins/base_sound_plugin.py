"""
Base class for sound plugins
"""
from abc import ABC, abstractmethod


class BaseSoundPlugin(ABC):
    """Abstract base class for sound plugins"""
    
    def __init__(self):
        """Initialize the sound plugin"""
        pass
    
    @abstractmethod
    def attack_succeeded(self):
        """
        Play sound when an attack successfully conquers a planet
        This is the conquest/victory sound
        """
        pass
    
    @abstractmethod
    def attack_failed(self):
        """
        Play sound when an attack fails to conquer a planet
        This is the explosion/defeat sound when ships don't conquer
        """
        pass
    
    @abstractmethod
    def fleet_launched(self):
        """
        Play sound when a fleet is launched from a planet
        This is the swoosh/launch sound
        """
        pass
    
    @abstractmethod
    def game_victory(self):
        """
        Play sound when the player wins the game
        Optional - can be None if no special victory sound
        """
        pass
    
    @abstractmethod
    def game_defeat(self):
        """
        Play sound when the player loses the game
        Optional - can be None if no special defeat sound
        """
        pass
    
    def cleanup(self):
        """
        Optional cleanup method called when plugin is destroyed
        """
        pass

