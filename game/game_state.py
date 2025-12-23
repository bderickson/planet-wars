"""
Game state management - tracks all game entities and logic
"""
import random
import math
from game.entities import Planet, Ship, reset_fleet_counter
from game.ai import create_ai
from game.abilities import RecallAbility, ProductionSurgeAbility, ShieldGeneratorAbility
from game.sound import SoundManager
from game.logger import get_logger

logger = get_logger(__name__)


class GameState:
    """Manages the current state of the game"""
    
    def __init__(self, screen_width, screen_height, map_size="medium", player_name="Player", ai_difficulty="medium", sound_pack="default"):
        logger.info(f"Initializing GameState: map={map_size}, ai={ai_difficulty}, sound={sound_pack}")
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.player_name = player_name
        self.ai_difficulty = ai_difficulty
        self.planets = []
        self.ships = []
        self.selected_planet = None
        
        # Special abilities - player gets all three, enemy gets all three
        self.player_abilities = {
            'recall': RecallAbility(),
            'production': ProductionSurgeAbility(),
            'shield': ShieldGeneratorAbility()
        }
        self.enemy_abilities = {
            'recall': RecallAbility(),
            'production': ProductionSurgeAbility(),
            'shield': ShieldGeneratorAbility()
        }
        logger.debug("Abilities initialized")
        
        # Game statistics tracking
        self.player_stats_tracker = {
            'ships_produced': 0,
            'battles_won': 0,
            'battles_lost': 0
        }
        self.enemy_stats_tracker = {
            'ships_produced': 0,
            'battles_won': 0,
            'battles_lost': 0
        }
        
        # Score tracking
        self.base_score = 100  # Starting tactical score
        self.tactical_penalties = 0  # Track penalties separately
        self.game_time = 0  # Track total game time in seconds
        
        # Sound manager with selected plugin
        self.sound_manager = SoundManager(sound_pack)
        
        # Create AI opponent
        self.ai = create_ai(ai_difficulty)
        
        # Reset fleet counter for new game
        reset_fleet_counter()
        
        # Create planets based on map size
        self._generate_map(map_size)
    
    def _generate_map(self, map_size):
        """
        Generate a vertically mirrored map based on size
        
        Args:
            map_size: "small" (7 planets), "medium" (13 planets), or "large" (19 planets)
        """
        logger.info(f"Generating map: size={map_size}")
        
        # Determine number of planets
        planet_counts = {
            "small": 7,
            "medium": 13,
            "large": 19
        }
        total_planets = planet_counts.get(map_size, 13)
        logger.debug(f"Target planet count: {total_planets}")
        
        # Generate unique planet names upfront
        used_names = set()
        
        def get_unique_planet_name():
            """Generate a unique planet name"""
            from game.entities import generate_planet_name
            attempts = 0
            while attempts < 100:  # Prevent infinite loop
                name = generate_planet_name()
                if name not in used_names:
                    used_names.add(name)
                    return name
                attempts += 1
            # Fallback: add a number suffix if we somehow run out
            base_name = generate_planet_name()
            counter = 1
            while f"{base_name} {counter}" in used_names:
                counter += 1
            name = f"{base_name} {counter}"
            used_names.add(name)
            return name
        
        # Calculate how many to place on each side (excluding center planet)
        planets_per_side = (total_planets - 1) // 2
        
        # Planet constraints
        min_radius = 20
        max_radius = 70
        min_distance = 180  # Minimum distance between planet centers (increased for name spacing)
        margin = 80  # Keep planets away from edges
        
        # UI exclusion zone (top-left corner where game UI is displayed)
        # Includes player stats, instructions, and fleet list
        # Also mirrored to top-right for ability buttons (which extend to y~260)
        ui_exclusion_width = 350
        ui_exclusion_height = 320  # Increased to prevent overlap with mirrored right-side buttons
        
        # Generate planets on the left side
        left_planets = []
        attempts = 0
        max_attempts = 1000
        
        while len(left_planets) < planets_per_side and attempts < max_attempts:
            attempts += 1
            
            # Random position on left half
            x = random.randint(margin, self.screen_width // 2 - margin)
            y = random.randint(margin, self.screen_height - margin)
            radius = random.randint(min_radius, max_radius)
            
            # Check if position is in the UI exclusion zone (top-left)
            if x < ui_exclusion_width and y < ui_exclusion_height:
                continue
            
            # Check if this position is valid (doesn't overlap with existing planets)
            valid = True
            for existing in left_planets:
                distance = math.sqrt((x - existing[0]) ** 2 + (y - existing[1]) ** 2)
                if distance < (radius + existing[2] + min_distance):
                    valid = False
                    break
            
            if valid:
                left_planets.append((x, y, radius))
        
        # Create the actual planet objects
        # First planet on left = Player, its mirror = Enemy
        for i, (x, y, radius) in enumerate(left_planets):
            if i == 0:
                # Player's starting planet (left side)
                owner = "Player"
                ship_count = 50
            else:
                # Neutral planets
                owner = "Neutral"
                ship_count = random.randint(15, 30)
            
            planet = Planet(x, y, radius, owner, ship_count)
            planet.name = get_unique_planet_name()  # Override with unique name
            self.planets.append(planet)
        
        # Mirror planets to the right side
        for i, (x, y, radius) in enumerate(left_planets):
            mirror_x = self.screen_width - x
            
            if i == 0:
                # Enemy's starting planet (mirrored from player)
                owner = "Enemy"
                ship_count = 50
            else:
                # Neutral planets
                owner = "Neutral"
                ship_count = random.randint(15, 30)
            
            planet = Planet(mirror_x, y, radius, owner, ship_count)
            planet.name = get_unique_planet_name()  # Override with unique name
            self.planets.append(planet)
        
        # Place center planet on the vertical mirror line
        center_x = self.screen_width // 2
        center_y = random.randint(margin, self.screen_height - margin)
        center_radius = random.randint(min_radius, max_radius)
        
        center_planet = Planet(center_x, center_y, center_radius, "Neutral", 
                              random.randint(20, 35))
        center_planet.name = get_unique_planet_name()  # Override with unique name
        self.planets.append(center_planet)
    
    def update(self, dt):
        """
        Update all game entities
        
        Args:
            dt: Delta time in seconds since last frame
        """
        # Track game time
        self.game_time += dt
        
        # Update all abilities
        for ability in self.player_abilities.values():
            ability.update(dt)
        for ability in self.enemy_abilities.values():
            ability.update(dt)
        
        # Update AI (make decisions)
        ai_actions = self.ai.make_decision(self, dt)
        
        # Execute AI actions
        for action in ai_actions:
            if action["action"] == "send_fleet":
                self._send_fleet(
                    action["source_planet"],
                    action["target_planet"],
                    action["ship_count"]
                )
        
        # Update all ships
        for ship in self.ships[:]:  # Use slice to allow removal during iteration
            ship.update(dt)
            
            # Remove ships that have reached their destination
            if ship.has_arrived():
                self.ships.remove(ship)
                self._handle_ship_arrival(ship)
        
        # Apply production surge if active
        production_multiplier_player = 2.0 if self.player_abilities['production'].is_active() else 1.0
        production_multiplier_enemy = 2.0 if self.enemy_abilities['production'].is_active() else 1.0
        
        # Update all planets and track ship production
        for planet in self.planets:
            # Track ships before update
            ships_before = planet.ship_count
            
            # Apply production multiplier based on owner
            if planet.owner == "Player":
                original_rate = planet.production_rate
                planet.production_rate = int(original_rate * production_multiplier_player)
                planet.update(dt)
                planet.production_rate = original_rate  # Reset for next frame
                # Track ships produced
                ships_produced = planet.ship_count - ships_before
                self.player_stats_tracker['ships_produced'] += ships_produced
            elif planet.owner == "Enemy":
                original_rate = planet.production_rate
                planet.production_rate = int(original_rate * production_multiplier_enemy)
                planet.update(dt)
                planet.production_rate = original_rate  # Reset for next frame
                # Track ships produced
                ships_produced = planet.ship_count - ships_before
                self.enemy_stats_tracker['ships_produced'] += ships_produced
            else:
                planet.update(dt)
    
    def add_ship(self, ship):
        """Add a ship to the game"""
        self.ships.append(ship)
    
    def _send_fleet(self, source_planet, target_planet, ship_count):
        """
        Send a fleet from source to target
        
        Args:
            source_planet: Planet to send ships from
            target_planet: Planet to send ships to
            ship_count: Number of ships to send
        """
        logger.debug(f"Sending fleet: {ship_count} ships from {source_planet.name} to {target_planet.name}")
        
        # Validate
        if source_planet.ship_count < ship_count:
            ship_count = source_planet.ship_count
            logger.debug(f"Adjusted ship count to available: {ship_count}")
        
        if ship_count <= 0:
            logger.warning(f"No ships to send from {source_planet.name}")
            return
        
        # Deduct ships from source
        source_planet.ship_count -= ship_count
        
        # Create fleet
        ship = Ship(source_planet, target_planet, source_planet.owner, fleet_size=ship_count)
        self.add_ship(ship)
        
        # Play launch sound
        self.sound_manager.play_fleet_launched()
    
    def check_game_over(self):
        """
        Check if the game is over (victory or defeat)
        
        Returns:
            "victory" if player wins
            "defeat" if player loses
            None if game is still ongoing
        """
        player_planets = [p for p in self.planets if p.owner == "Player"]
        player_ships = [s for s in self.ships if s.owner == "Player"]
        
        enemy_planets = [p for p in self.planets if p.owner == "Enemy"]
        enemy_ships = [s for s in self.ships if s.owner == "Enemy"]
        
        # Check for victory: Enemy has no planets and no fleets
        if len(enemy_planets) == 0 and len(enemy_ships) == 0:
            logger.info("VICTORY: Enemy has no planets or ships")
            return "victory"
        
        # Check for defeat: Player has no planets and no fleets
        if len(player_planets) == 0 and len(player_ships) == 0:
            logger.info("DEFEAT: Player has no planets or ships")
            return "defeat"
        
        return None
    
    def get_planet_at(self, x, y):
        """
        Find a planet at the given coordinates
        
        Returns:
            Planet if found, None otherwise
        """
        for planet in self.planets:
            if planet.contains_point(x, y):
                return planet
        return None
    
    def get_player_stats(self, owner):
        """
        Get statistics for a player
        
        Args:
            owner: "Player" or "Enemy"
            
        Returns:
            Dictionary with planet_count, total_ships, production_rate
        """
        # Count planets owned
        owned_planets = [p for p in self.planets if p.owner == owner]
        planet_count = len(owned_planets)
        
        # Total ships on planets
        total_ships = sum(p.ship_count for p in owned_planets)
        
        # Total ships in fleets
        fleet_ships = sum(s.fleet_size for s in self.ships if s.owner == owner)
        total_ships += fleet_ships
        
        # Production rate (ships per second from all owned planets)
        base_production_rate = sum(p.production_rate for p in owned_planets)
        
        # Apply production surge multiplier if active
        if owner == "Player" and self.player_abilities['production'].is_active():
            production_rate = int(base_production_rate * 2.0)
        elif owner == "Enemy" and self.enemy_abilities['production'].is_active():
            production_rate = int(base_production_rate * 2.0)
        else:
            production_rate = base_production_rate
        
        return {
            "planet_count": planet_count,
            "total_ships": total_ships,
            "production_rate": production_rate
        }
    
    def calculate_final_score(self):
        """
        Calculate final score based on tactical performance and time
        
        Score formula:
        - Base: 100 points
        - Tactical penalties: -5 for lost battles, -10 for lost planets
        - Time bonus: Up to +50 points for fast victories
          - Under 60s: +50 bonus (perfect speedrun!)
          - Under 120s: +30 bonus (fast)
          - Under 180s: +15 bonus (decent)
          - Under 300s: +5 bonus (okay)
          - 300s+: No time bonus
        
        Returns:
            Final score (0-150 range)
        """
        # Start with base score minus tactical penalties
        tactical_score = max(0, self.base_score - self.tactical_penalties)
        
        # Calculate time bonus
        if self.game_time < 60:
            time_bonus = 50  # Blazing fast!
        elif self.game_time < 120:
            time_bonus = 30  # Very fast
        elif self.game_time < 180:
            time_bonus = 15  # Fast
        elif self.game_time < 300:
            time_bonus = 5   # Moderate
        else:
            time_bonus = 0   # Slow
        
        final_score = tactical_score + time_bonus
        return final_score
    
    def _handle_ship_arrival(self, ship):
        """
        Handle what happens when a ship fleet arrives at a planet
        
        Args:
            ship: The Ship that has arrived
        """
        planet = ship.target_planet
        original_owner = planet.owner
        
        if planet.owner == ship.owner:
            # Reinforcement: Same owner, add ships to planet
            planet.ship_count += ship.fleet_size
        else:
            # Combat: Different owner (enemy or neutral)
            # Apply shield defense if active
            attacking_force = ship.fleet_size
            
            # Check if defender has shield active
            if planet.owner == "Player" and self.player_abilities['shield'].is_active():
                if self.player_abilities['shield'].target == planet:
                    # Shield reduces attacking force by 50%
                    attacking_force = int(attacking_force * 0.5)
            elif planet.owner == "Enemy" and self.enemy_abilities['shield'].is_active():
                if self.enemy_abilities['shield'].target == planet:
                    # Shield reduces attacking force by 50%
                    attacking_force = int(attacking_force * 0.5)
            
            planet.ship_count -= attacking_force
            
            # Check if attacker wins
            if planet.ship_count < 0:
                # Attacker takes over the planet
                planet.owner = ship.owner
                planet.ship_count = abs(planet.ship_count)  # Remaining ships occupy planet
                
                # Track battle won
                if ship.owner == "Player":
                    self.player_stats_tracker['battles_won'] += 1
                else:
                    self.enemy_stats_tracker['battles_won'] += 1
                
                # Track battle lost for defender
                if original_owner == "Player":
                    self.player_stats_tracker['battles_lost'] += 1
                    # Score penalty for losing a planet
                    self.tactical_penalties += 10
                elif original_owner == "Enemy":
                    self.enemy_stats_tracker['battles_lost'] += 1
                
                # Play conquest sound
                self.sound_manager.play_attack_succeeded()
            elif planet.ship_count == 0:
                # Exact match - attacker takes over with 0 ships
                planet.owner = ship.owner
                planet.ship_count = 0
                
                # Track battle won
                if ship.owner == "Player":
                    self.player_stats_tracker['battles_won'] += 1
                else:
                    self.enemy_stats_tracker['battles_won'] += 1
                
                # Track battle lost for defender
                if original_owner == "Player":
                    self.player_stats_tracker['battles_lost'] += 1
                    # Score penalty for losing a planet
                    self.tactical_penalties += 10
                elif original_owner == "Enemy":
                    self.enemy_stats_tracker['battles_lost'] += 1
                
                # Play conquest sound
                self.sound_manager.play_attack_succeeded()
            else:
                # Defender wins - ships destroyed
                # Track battle lost for attacker
                if ship.owner == "Player":
                    self.player_stats_tracker['battles_lost'] += 1
                    # Score penalty for losing a battle
                    self.tactical_penalties += 5
                else:
                    self.enemy_stats_tracker['battles_lost'] += 1
                
                # Track battle won for defender
                if planet.owner == "Player":
                    self.player_stats_tracker['battles_won'] += 1
                elif planet.owner == "Enemy":
                    self.enemy_stats_tracker['battles_won'] += 1
                
                # Play explosion sound
                self.sound_manager.play_attack_failed()
    
    def activate_recall(self, owner="Player"):
        """Recall all fleets back to their origin planets"""
        ability = self.player_abilities['recall'] if owner == "Player" else self.enemy_abilities['recall']
        
        if ability.activate():
            # Return all ships to their origin planets
            for ship in self.ships[:]:
                if ship.owner == owner:
                    # Add ships back to origin planet
                    origin_planet = ship.source_planet
                    if origin_planet and origin_planet in self.planets:
                        origin_planet.ship_count += ship.fleet_size
                    # Remove ship from game
                    self.ships.remove(ship)
            return True
        return False
    
    def activate_production_surge(self, owner="Player"):
        """Activate production surge for the specified owner"""
        ability = self.player_abilities['production'] if owner == "Player" else self.enemy_abilities['production']
        return ability.activate()
    
    def activate_shield(self, planet, owner="Player"):
        """Activate shield on a specific planet"""
        ability = self.player_abilities['shield'] if owner == "Player" else self.enemy_abilities['shield']
        
        # Only activate on owned planets
        if planet and planet.owner == owner:
            return ability.activate(target=planet)
        return False

