"""
Simple AI implementation - basic strategy
"""
import random
from game.ai.base_ai import BaseAI


class SimpleAI(BaseAI):
    """
    A simple AI that makes basic strategic decisions
    
    Strategy:
    - Periodically evaluates planets to attack
    - Prefers closer targets
    - Adjusts aggression based on difficulty
    """
    
    def __init__(self, difficulty="medium"):
        super().__init__(difficulty)
        
        # Decision timing (how often to make decisions)
        self.decision_timer = 0
        
        # Difficulty settings
        if difficulty == "easy":
            self.decision_interval = 3.0  # Slower decisions
            self.aggression = 0.3  # Send 30% of ships
            self.min_ships_to_attack = 20  # Need more ships before attacking
        elif difficulty == "medium":
            self.decision_interval = 2.0
            self.aggression = 0.5  # Send 50% of ships
            self.min_ships_to_attack = 10
        else:  # hard
            self.decision_interval = 1.0  # Fast decisions
            self.aggression = 0.7  # Send 70% of ships
            self.min_ships_to_attack = 5
    
    def make_decision(self, game_state, dt):
        """Make decisions based on simple strategy"""
        # Update decision timer
        self.decision_timer += dt
        
        # Only make decisions at intervals
        if self.decision_timer < self.decision_interval:
            return []
        
        self.decision_timer = 0
        actions = []
        
        # Get all planets
        my_planets = self.get_enemy_planets(game_state)
        player_planets = self.get_player_planets(game_state)
        neutral_planets = self.get_neutral_planets(game_state)
        
        # For each of our planets, consider attacking
        for source in my_planets:
            # Skip if we don't have enough ships
            if source.ship_count < self.min_ships_to_attack:
                continue
            
            # Find potential targets (player planets and neutral planets)
            targets = player_planets + neutral_planets
            
            if not targets:
                continue
            
            # Find closest target
            closest_target = min(targets, key=lambda t: self.get_distance(source, t))
            
            # Decide whether to attack based on strategic value
            if self._should_attack(source, closest_target, game_state):
                ships_to_send = int(source.ship_count * self.aggression)
                if ships_to_send > 0:
                    actions.append({
                        "action": "send_fleet",
                        "source_planet": source,
                        "target_planet": closest_target,
                        "ship_count": ships_to_send
                    })
        
        return actions
    
    def _should_attack(self, source, target, game_state):
        """
        Decide if we should attack a target
        
        Args:
            source: Our planet to attack from
            target: Target planet to attack
            game_state: Current game state
            
        Returns:
            True if we should attack, False otherwise
        """
        # Calculate ships to send
        ships_to_send = int(source.ship_count * self.aggression)
        
        # Don't attack if we don't have enough ships
        if ships_to_send == 0:
            return False
        
        # Against neutral planets, attack if we have more ships
        if target.owner == "Neutral":
            return ships_to_send > target.ship_count
        
        # Against player planets, be more cautious
        # Only attack if we have significantly more ships
        safety_margin = 1.5 if self.difficulty == "easy" else 1.2
        return ships_to_send > target.ship_count * safety_margin

