"""
Simple AI implementation - basic strategy with ability usage
"""
import random
from game.ai.base_ai import BaseAI
from game.logger import get_logger

logger = get_logger(__name__)


class SimpleAI(BaseAI):
    """
    A simple AI that makes basic strategic decisions
    
    Strategy:
    - Periodically evaluates planets to attack
    - Prefers high-production planets over low-production ones
    - Uses abilities strategically on hard difficulty
    - Adjusts aggression based on difficulty
    """
    
    def __init__(self, difficulty="medium"):
        super().__init__(difficulty)
        
        # Decision timing (how often to make decisions)
        self.decision_timer = 0
        self.ability_timer = 0
        
        # Difficulty settings
        if difficulty == "easy":
            self.decision_interval = 3.0  # Slower decisions
            self.aggression = 0.3  # Send 30% of ships
            self.min_ships_to_attack = 20  # Need more ships before attacking
            self.use_abilities = False
        elif difficulty == "medium":
            self.decision_interval = 2.0
            self.aggression = 0.5  # Send 50% of ships
            self.min_ships_to_attack = 10
            self.use_abilities = False
        else:  # hard
            self.decision_interval = 1.0  # Fast decisions
            self.aggression = 0.7  # Send 70% of ships
            self.min_ships_to_attack = 5
            self.use_abilities = True
            self.ability_check_interval = 5.0  # Check abilities every 5 seconds
    
    def make_decision(self, game_state, dt):
        """Make decisions based on simple strategy"""
        # Update decision timer
        self.decision_timer += dt
        self.ability_timer += dt
        
        # Check if we should use abilities (hard mode only)
        if self.use_abilities and self.ability_timer >= self.ability_check_interval:
            self.ability_timer = 0
            self._consider_abilities(game_state)
        
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
            
            # Find best target based on strategic value
            best_target = self._select_best_target(source, targets, game_state)
            
            # Decide whether to attack based on strategic value
            if self._should_attack(source, best_target, game_state):
                ships_to_send = int(source.ship_count * self.aggression)
                if ships_to_send > 0:
                    actions.append({
                        "action": "send_fleet",
                        "source_planet": source,
                        "target_planet": best_target,
                        "ship_count": ships_to_send
                    })
        
        return actions
    
    def _select_best_target(self, source, targets, game_state):
        """
        Select the best target to attack from source planet
        
        On hard difficulty, prioritizes high-production planets.
        Otherwise, prefers closest targets.
        
        Args:
            source: Our planet to attack from
            targets: List of potential target planets
            game_state: Current game state
            
        Returns:
            Best target planet
        """
        if not targets:
            return None
        
        if self.difficulty == "hard":
            # Score each target based on multiple factors
            def score_target(target):
                distance = self.get_distance(source, target)
                production_rate = target.production_rate
                ship_count = target.ship_count
                
                # Higher production is better (up to 2x multiplier)
                production_score = production_rate / 2.0
                
                # Closer is better (normalize distance, max 1000 units = 0 score)
                distance_score = max(0, 1.0 - (distance / 1000.0))
                
                # Weaker defense is better (normalize, 100 ships = 0 score)
                weakness_score = max(0, 1.0 - (ship_count / 100.0))
                
                # Player planets are worth more than neutral
                owner_bonus = 1.5 if target.owner == "Player" else 1.0
                
                # Weighted combination (prioritize production!)
                total_score = (production_score * 3.0 +  # Production is most important
                              distance_score * 1.0 +      # Distance matters
                              weakness_score * 1.5) * owner_bonus
                
                return total_score
            
            return max(targets, key=score_target)
        else:
            # Easy/Medium: Just pick closest
            return min(targets, key=lambda t: self.get_distance(source, t))
    
    def _consider_abilities(self, game_state):
        """
        Consider using abilities strategically (hard mode only)
        
        Args:
            game_state: Current game state
        """
        if not self.use_abilities:
            return
        
        my_planets = self.get_enemy_planets(game_state)
        player_planets = self.get_player_planets(game_state)
        enemy_ships = [s for s in game_state.ships if s.owner == "Enemy"]
        
        # Consider Production Surge
        if game_state.enemy_abilities['production'].is_available():
            # Use if we have multiple high-production planets
            high_prod_planets = [p for p in my_planets if p.production_rate >= 3]
            if len(high_prod_planets) >= 2:
                if game_state.activate_production_surge(owner="Enemy"):
                    logger.info("AI activated Production Surge")
        
        # Consider Shield
        if game_state.enemy_abilities['shield'].is_available():
            # Shield our highest production planet if under threat
            if my_planets:
                # Find our best planet
                best_planet = max(my_planets, key=lambda p: p.production_rate)
                
                # Check if player has ships nearby
                player_ships = [s for s in game_state.ships if s.owner == "Player"]
                threats = [s for s in player_ships if self.get_distance(s, best_planet) < 300]
                
                if threats and best_planet.ship_count < 50:
                    if game_state.activate_shield(best_planet, owner="Enemy"):
                        logger.info(f"AI activated Shield on {best_planet.name}")
        
        # Consider Recall
        if game_state.enemy_abilities['recall'].is_available():
            # Recall if we're losing badly and have many ships in transit
            my_total_ships = sum(p.ship_count for p in my_planets) + len(enemy_ships)
            player_total_ships = sum(p.ship_count for p in player_planets)
            
            # If player has 2x our ships and we have many fleets out, recall
            if player_total_ships > my_total_ships * 2 and len(enemy_ships) >= 3:
                if game_state.activate_recall(owner="Enemy"):
                    logger.info("AI activated Recall (defensive retreat)")
    
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

