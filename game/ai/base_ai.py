"""
Base AI class defining the interface for all AI implementations
"""
from abc import ABC, abstractmethod


class BaseAI(ABC):
    """Abstract base class for AI opponents"""
    
    def __init__(self, difficulty="medium"):
        """
        Initialize the AI
        
        Args:
            difficulty: "easy", "medium", or "hard"
        """
        self.difficulty = difficulty
    
    @abstractmethod
    def make_decision(self, game_state, dt):
        """
        Make AI decisions based on current game state
        
        This method is called every frame and should decide whether to take
        any actions (like sending fleets). It should not modify game_state directly,
        but return a list of actions to perform.
        
        Args:
            game_state: The current GameState object (read-only)
            dt: Delta time since last frame in seconds
            
        Returns:
            List of action dictionaries, each with:
            {
                "action": "send_fleet",
                "source_planet": Planet object,
                "target_planet": Planet object,
                "ship_count": int (number of ships to send)
            }
        """
        pass
    
    def get_enemy_planets(self, game_state):
        """Helper: Get all planets owned by the AI (Enemy)"""
        return [p for p in game_state.planets if p.owner == "Enemy"]
    
    def get_player_planets(self, game_state):
        """Helper: Get all planets owned by the player"""
        return [p for p in game_state.planets if p.owner == "Player"]
    
    def get_neutral_planets(self, game_state):
        """Helper: Get all neutral planets"""
        return [p for p in game_state.planets if p.owner == "Neutral"]
    
    def get_distance(self, planet1, planet2):
        """Helper: Calculate distance between two planets"""
        import math
        return math.sqrt((planet1.x - planet2.x) ** 2 + (planet1.y - planet2.y) ** 2)

