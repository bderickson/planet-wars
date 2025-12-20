"""
Scoreboard management - saves and loads high scores
"""
import json
import os
import sys
from datetime import datetime
from game.logger import get_logger

logger = get_logger(__name__)


class Scoreboard:
    """Manages high scores persistence"""
    
    def __init__(self, filename='files/scoreboard.json'):
        self.filename = filename
        self.is_browser = sys.platform == "emscripten"
        logger.debug(f"Scoreboard initializing (browser: {self.is_browser})")
        
        # Ensure files directory exists (desktop only)
        if not self.is_browser:
            os.makedirs("files", exist_ok=True)
        
        self.scores = self.load_scores()
        logger.info(f"Scoreboard loaded: {len(self.scores)} scores")
    
    def load_scores(self):
        """Load scores from JSON file (or localStorage in browser)"""
        try:
            if self.is_browser:
                return self._load_from_localstorage()
            else:
                # Desktop: use file
                if os.path.exists(self.filename):
                    with open(self.filename, 'r') as f:
                        return json.load(f)
        except Exception as e:
            print(f"Could not load scoreboard: {e}")
        return []
    
    def _load_from_localstorage(self):
        """Load from browser localStorage"""
        try:
            import platform
            if hasattr(platform, 'window'):
                storage = platform.window.localStorage
                data_str = storage.getItem('planet_wars_scoreboard')
                if data_str:
                    return json.loads(data_str)
        except Exception as e:
            print(f"localStorage load failed: {e}")
        return []
    
    def save_scores(self):
        """Save scores to JSON file (or localStorage in browser)"""
        try:
            if self.is_browser:
                self._save_to_localstorage()
            else:
                with open(self.filename, 'w') as f:
                    json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Could not save scoreboard: {e}")
    
    def _save_to_localstorage(self):
        """Save to browser localStorage"""
        try:
            import platform
            if hasattr(platform, 'window'):
                storage = platform.window.localStorage
                data_str = json.dumps(self.scores)
                storage.setItem('planet_wars_scoreboard', data_str)
        except Exception as e:
            print(f"localStorage save failed: {e}")
    
    def add_score(self, player_name, score, planets_controlled, ships_produced, 
                  battles_won, battles_lost, victory, is_cheater=False):
        """
        Add a new score entry
        
        Args:
            player_name: Name of the player
            score: Final score
            planets_controlled: Number of planets controlled at end
            ships_produced: Total ships produced
            battles_won: Number of battles won
            battles_lost: Number of battles lost
            victory: True if player won, False if lost
            is_cheater: True if win button was used
        """
        logger.info(f"Adding score: {player_name}={score}, victory={victory}, cheater={is_cheater}")
        entry = {
            'player_name': player_name,
            'score': score if not is_cheater else "CHEATER",
            'planets_controlled': planets_controlled,
            'ships_produced': ships_produced,
            'battles_won': battles_won,
            'battles_lost': battles_lost,
            'victory': victory,
            'is_cheater': is_cheater,
            'timestamp': datetime.now().isoformat()
        }
        
        self.scores.append(entry)
        self.save_scores()
    
    def get_top_scores(self, limit=10):
        """
        Get top scores sorted by score descending
        
        Args:
            limit: Maximum number of scores to return
            
        Returns:
            List of score entries sorted by score
        """
        # Filter out cheaters and non-numeric scores
        valid_scores = [s for s in self.scores if not s.get('is_cheater', False) and isinstance(s.get('score'), (int, float))]
        
        # Sort by score descending
        sorted_scores = sorted(valid_scores, key=lambda x: x['score'], reverse=True)
        
        return sorted_scores[:limit]
    
    def get_all_scores(self, limit=50):
        """
        Get all scores including cheaters, sorted by score
        
        Args:
            limit: Maximum number of scores to return
            
        Returns:
            List of all score entries
        """
        # Separate cheaters and valid scores
        valid_scores = [s for s in self.scores if not s.get('is_cheater', False) and isinstance(s.get('score'), (int, float))]
        cheater_scores = [s for s in self.scores if s.get('is_cheater', False)]
        
        # Sort valid scores by score descending
        sorted_valid = sorted(valid_scores, key=lambda x: x['score'], reverse=True)
        
        # Combine: valid scores first, then cheaters at the end
        all_scores = sorted_valid + cheater_scores
        
        return all_scores[:limit]

