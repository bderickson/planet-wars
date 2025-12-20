"""
Game entities - planets, ships, etc.
"""
import math
import random


# Fleet ID generator
_fleet_counter = 0
_fleet_names = [
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta",
    "Iota", "Kappa", "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi",
    "Rho", "Sigma", "Tau", "Upsilon", "Phi", "Chi", "Psi", "Omega"
]


def generate_fleet_id():
    """Generate a fleet ID (Alpha, Beta, Gamma, etc.)"""
    global _fleet_counter
    fleet_id = _fleet_names[_fleet_counter % len(_fleet_names)]
    _fleet_counter += 1
    return fleet_id


def reset_fleet_counter():
    """Reset the fleet counter (useful for new games)"""
    global _fleet_counter
    _fleet_counter = 0


def generate_planet_name():
    """Generate an interesting random planet name with song references"""
    
    # Song-inspired names and space themes
    patterns = [
        # Direct song references
        ["Rocket Man", "Space Oddity", "Starman", "Levitating", "Walking on Sunshine",
         "Mr. Blue Sky", "Drops of Jupiter", "Black Hole Sun", "Across the Universe",
         "Lucy in the Sky", "Supermassive", "Satellite", "Cosmic Love", "Gravity"],
        
        # Creative combinations
        ["Bohemian", "Rhapsody", "Thunder", "Paradise", "Wonderwall", "Yesterday",
         "Imagine", "Hallelujah", "Stairway", "Smells Like", "Sweet Child", "Livin' on"],
        
        # Space + adjectives from famous songs
        ["Purple", "Yellow", "Blue", "Green", "Red", "Golden", "Silver", "Electric",
         "Rolling", "Shining", "Burning", "Dancing", "Forever"],
        
        # Cosmic suffixes
        ["Nebula", "Galaxy", "System", "Cluster", "Station", "Outpost", "Prime",
         "World", "Rock", "Sphere", "Haven", "Dream"]
    ]
    
    # Special complete names (song titles/lyrics that work as planet names)
    special_names = [
        "Total Eclipse",
        "Dancing in the Moonlight",
        "Come Together",
        "Hotel California",
        "Sweet Dreams",
        "September",
        "Africa",
        "Wonderland",
        "Neverland",
        "Strawberry Fields",
        "Penny Lane",
        "Abbey Road",
        "Electric Avenue",
        "Purple Rain",
        "Bohemian Paradise",
        "Thriller Bay",
        "Karma Station",
        "Viva la Vista",
        "Rolling Stone",
        "Stairway Prime"
    ]
    
    # Sometimes use a special name
    if random.random() < 0.4:  # 40% chance
        return random.choice(special_names)
    
    # Otherwise create a combination
    choice = random.randint(0, 2)
    
    if choice == 0:
        # Pattern: Song reference + space word
        return f"{random.choice(patterns[1])} {random.choice(patterns[3])}"
    elif choice == 1:
        # Pattern: Adjective + space word
        return f"{random.choice(patterns[2])} {random.choice(patterns[3])}"
    else:
        # Pattern: Just a song reference or space theme
        return random.choice(patterns[0])


class Planet:
    """Represents a planet in the game"""
    
    def __init__(self, x, y, radius, owner="Neutral", ship_count=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.owner = owner  # "Player", "Enemy", or "Neutral"
        self.ship_count = ship_count
        
        # Calculate production rate based on planet size (integer ships per second)
        # Smallest planets (radius 20) = 1 ship/second
        # Largest planets (radius 70) = 4 ships/second
        min_radius = 20
        max_radius = 70
        min_production = 1
        max_production = 4
        
        # Linear interpolation, rounded to nearest integer
        if max_radius > min_radius:
            ratio = (radius - min_radius) / (max_radius - min_radius)
            self.production_rate = round(min_production + ratio * (max_production - min_production))
        else:
            self.production_rate = min_production
        
        self.production_timer = 0
        self.name = generate_planet_name()  # Give each planet a goofy name
    
    def update(self, dt):
        """Update planet state (produce ships if owned)"""
        if self.owner != "Neutral":
            self.production_timer += dt
            # Time needed to produce 1 ship based on production rate
            time_per_ship = 1.0 / self.production_rate
            if self.production_timer >= time_per_ship:
                self.ship_count += 1
                self.production_timer -= time_per_ship
    
    def contains_point(self, x, y):
        """Check if a point is inside the planet"""
        distance = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distance <= self.radius
    
    def get_color(self):
        """Get the color for this planet based on owner"""
        colors = {
            "Player": (100, 150, 255),   # Blue
            "Enemy": (255, 100, 100),     # Red
            "Neutral": (150, 150, 150)    # Gray
        }
        return colors.get(self.owner, (255, 255, 255))


class Ship:
    """Represents a fleet of ships traveling between planets"""
    
    def __init__(self, start_planet, target_planet, owner, fleet_size=1):
        self.x = start_planet.x
        self.y = start_planet.y
        self.target_x = target_planet.x
        self.target_y = target_planet.y
        self.source_planet = start_planet  # Store reference to origin
        self.target_planet = target_planet  # Store reference to target
        self.owner = owner
        self.fleet_size = fleet_size  # Number of ships in this fleet
        self.base_speed = 200  # Base pixels per second
        self.speed = self.base_speed  # Current speed (can be modified by abilities)
        self.arrived = False
        self.fleet_id = generate_fleet_id()  # Unique fleet identifier
        
        # Calculate direction
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 0:
            self.velocity_x = (dx / distance) * self.speed
            self.velocity_y = (dy / distance) * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def update(self, dt):
        """Move the ship towards its target"""
        if self.arrived:
            return
        
        # Move towards target
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Check if we've arrived (within 5 pixels of target)
        distance = math.sqrt((self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2)
        if distance < 5:
            self.arrived = True
    
    def has_arrived(self):
        """Check if the ship has reached its destination"""
        return self.arrived
    
    def get_color(self):
        """Get the color for this ship based on owner"""
        colors = {
            "Player": (100, 150, 255),   # Blue
            "Enemy": (255, 100, 100),     # Red
        }
        return colors.get(self.owner, (255, 255, 255))

