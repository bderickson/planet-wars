"""
Unit tests for game entities (Planet, Ship, fleet management)
"""
import pytest
import math
from game.entities import (
    Planet, Ship, generate_fleet_id, reset_fleet_counter, 
    generate_planet_name, _fleet_counter
)


class TestFleetIDGeneration:
    """Tests for fleet ID generation"""
    
    def test_generate_fleet_id_returns_string(self):
        """Test that fleet ID is a string"""
        reset_fleet_counter()
        fleet_id = generate_fleet_id()
        assert isinstance(fleet_id, str)
    
    def test_generate_fleet_id_first_is_alpha(self):
        """Test that first fleet is Alpha"""
        reset_fleet_counter()
        fleet_id = generate_fleet_id()
        assert fleet_id == "Alpha"
    
    def test_generate_fleet_id_sequence(self):
        """Test that fleet IDs follow Greek alphabet sequence"""
        reset_fleet_counter()
        expected = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]
        
        for expected_id in expected:
            assert generate_fleet_id() == expected_id
    
    def test_generate_fleet_id_wraps_around(self):
        """Test that fleet IDs wrap around after Omega"""
        reset_fleet_counter()
        
        # Generate 24 IDs (full alphabet)
        for _ in range(24):
            generate_fleet_id()
        
        # 25th should be Alpha again
        assert generate_fleet_id() == "Alpha"
    
    def test_reset_fleet_counter(self):
        """Test that reset_fleet_counter resets to Alpha"""
        # Generate some IDs
        for _ in range(5):
            generate_fleet_id()
        
        reset_fleet_counter()
        assert generate_fleet_id() == "Alpha"


class TestPlanetNameGeneration:
    """Tests for planet name generation"""
    
    def test_generate_planet_name_returns_string(self):
        """Test that planet name is a string"""
        name = generate_planet_name()
        assert isinstance(name, str)
    
    def test_generate_planet_name_not_empty(self):
        """Test that planet name is not empty"""
        name = generate_planet_name()
        assert len(name) > 0
    
    def test_generate_planet_name_variety(self):
        """Test that multiple calls generate different names"""
        names = set()
        for _ in range(50):
            names.add(generate_planet_name())
        
        # Should have some variety (at least 20 unique names in 50 attempts)
        assert len(names) >= 20
    
    def test_generate_planet_name_reasonable_length(self):
        """Test that planet names are reasonable length"""
        for _ in range(20):
            name = generate_planet_name()
            assert len(name) < 50  # Should be under 50 characters


class TestPlanetInit:
    """Tests for Planet initialization"""
    
    def test_planet_init_basic(self):
        """Test basic planet initialization"""
        planet = Planet(100, 200, 30)
        
        assert planet.x == 100
        assert planet.y == 200
        assert planet.radius == 30
        assert planet.owner == "Neutral"
        assert planet.ship_count == 0
    
    def test_planet_init_with_owner(self):
        """Test planet initialization with owner"""
        planet = Planet(100, 200, 30, owner="Player")
        assert planet.owner == "Player"
    
    def test_planet_init_with_ships(self):
        """Test planet initialization with ships"""
        planet = Planet(100, 200, 30, ship_count=50)
        assert planet.ship_count == 50
    
    def test_planet_init_all_parameters(self):
        """Test planet initialization with all parameters"""
        planet = Planet(150, 250, 40, "Enemy", 75)
        
        assert planet.x == 150
        assert planet.y == 250
        assert planet.radius == 40
        assert planet.owner == "Enemy"
        assert planet.ship_count == 75
    
    def test_planet_has_name(self):
        """Test that planet gets a random name"""
        planet = Planet(100, 100, 30)
        assert hasattr(planet, 'name')
        assert len(planet.name) > 0
    
    def test_planet_has_production_rate(self):
        """Test that planet has production rate"""
        planet = Planet(100, 100, 30)
        assert hasattr(planet, 'production_rate')
        assert planet.production_rate >= 1
        assert planet.production_rate <= 4
    
    def test_planet_production_rate_scales_with_size(self):
        """Test that larger planets have higher production"""
        small_planet = Planet(100, 100, 20)  # Min size
        large_planet = Planet(100, 100, 70)  # Max size
        
        assert large_planet.production_rate > small_planet.production_rate
    
    def test_planet_production_rate_is_integer(self):
        """Test that production rate is always an integer"""
        for radius in range(20, 71, 5):
            planet = Planet(100, 100, radius)
            assert isinstance(planet.production_rate, int)


class TestPlanetUpdate:
    """Tests for Planet update logic"""
    
    def test_neutral_planet_no_production(self):
        """Test that neutral planets don't produce ships"""
        planet = Planet(100, 100, 30, "Neutral", 10)
        initial_count = planet.ship_count
        
        planet.update(1.0)
        assert planet.ship_count == initial_count
    
    def test_player_planet_produces_ships(self):
        """Test that player-owned planets produce ships"""
        planet = Planet(100, 100, 30, "Player", 0)
        planet.production_rate = 1  # 1 ship per second
        
        planet.update(1.0)  # 1 second
        assert planet.ship_count == 1
    
    def test_enemy_planet_produces_ships(self):
        """Test that enemy-owned planets produce ships"""
        planet = Planet(100, 100, 30, "Enemy", 0)
        planet.production_rate = 2  # 2 ships per second
        
        planet.update(1.0)  # 1 second
        # Should produce at least 1 ship (may be 1 or 2 depending on timer precision)
        assert planet.ship_count >= 1
    
    def test_production_over_multiple_updates(self):
        """Test production over multiple update calls"""
        planet = Planet(100, 100, 30, "Player", 0)
        planet.production_rate = 1
        
        for _ in range(5):
            planet.update(1.0)
        
        assert planet.ship_count == 5
    
    def test_production_with_fractional_time(self):
        """Test production with fractional time steps"""
        planet = Planet(100, 100, 30, "Player", 0)
        planet.production_rate = 2  # 2 ships per second
        
        planet.update(0.5)  # Half second
        assert planet.ship_count == 1  # Should produce 1 ship
    
    def test_production_accumulates_timer(self):
        """Test that production timer accumulates correctly"""
        planet = Planet(100, 100, 30, "Player", 0)
        planet.production_rate = 1  # 1 ship per second
        
        # 0.3 seconds - not enough for a ship
        planet.update(0.3)
        assert planet.ship_count == 0
        
        # 0.8 more seconds - total 1.1, should produce 1 ship
        planet.update(0.8)
        assert planet.ship_count == 1


class TestPlanetContainsPoint:
    """Tests for Planet collision detection"""
    
    def test_contains_point_center(self):
        """Test that planet contains its center point"""
        planet = Planet(100, 100, 30)
        assert planet.contains_point(100, 100) is True
    
    def test_contains_point_inside(self):
        """Test point inside planet"""
        planet = Planet(100, 100, 30)
        assert planet.contains_point(110, 110) is True
    
    def test_contains_point_outside(self):
        """Test point outside planet"""
        planet = Planet(100, 100, 30)
        assert planet.contains_point(200, 200) is False
    
    def test_contains_point_on_edge(self):
        """Test point on planet edge"""
        planet = Planet(100, 100, 30)
        # Point exactly on the edge (30 pixels away)
        assert planet.contains_point(130, 100) is True
    
    def test_contains_point_just_outside(self):
        """Test point just outside planet"""
        planet = Planet(100, 100, 30)
        # Point just beyond the edge
        assert planet.contains_point(131, 100) is False


class TestPlanetGetColor:
    """Tests for Planet color assignment"""
    
    def test_get_color_player(self):
        """Test player planet color"""
        planet = Planet(100, 100, 30, "Player")
        color = planet.get_color()
        assert color == (100, 150, 255)  # Blue
    
    def test_get_color_enemy(self):
        """Test enemy planet color"""
        planet = Planet(100, 100, 30, "Enemy")
        color = planet.get_color()
        assert color == (255, 100, 100)  # Red
    
    def test_get_color_neutral(self):
        """Test neutral planet color"""
        planet = Planet(100, 100, 30, "Neutral")
        color = planet.get_color()
        assert color == (150, 150, 150)  # Gray


class TestShipInit:
    """Tests for Ship initialization"""
    
    def test_ship_init_basic(self):
        """Test basic ship initialization"""
        source = Planet(100, 100, 30, "Player", 50)
        target = Planet(300, 300, 30, "Enemy", 50)
        
        ship = Ship(source, target, "Player", fleet_size=25)
        
        assert ship.x == 100
        assert ship.y == 100
        assert ship.target_x == 300
        assert ship.target_y == 300
        assert ship.owner == "Player"
        assert ship.fleet_size == 25
        assert ship.arrived is False
    
    def test_ship_has_fleet_id(self):
        """Test that ship gets a fleet ID"""
        reset_fleet_counter()
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player")
        assert hasattr(ship, 'fleet_id')
        assert ship.fleet_id == "Alpha"
    
    def test_ship_stores_source_planet(self):
        """Test that ship stores reference to source planet"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player")
        assert ship.source_planet == source
    
    def test_ship_stores_target_planet(self):
        """Test that ship stores reference to target planet"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player")
        assert ship.target_planet == target
    
    def test_ship_calculates_velocity(self):
        """Test that ship calculates velocity towards target"""
        source = Planet(100, 100, 30)
        target = Planet(300, 100, 30)  # Directly to the right
        
        ship = Ship(source, target, "Player")
        
        assert ship.velocity_x > 0  # Moving right
        assert abs(ship.velocity_y) < 0.01  # Not moving vertically
    
    def test_ship_velocity_magnitude(self):
        """Test that ship velocity matches speed"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player")
        
        velocity_magnitude = math.sqrt(ship.velocity_x**2 + ship.velocity_y**2)
        assert abs(velocity_magnitude - ship.speed) < 0.01


class TestShipUpdate:
    """Tests for Ship movement"""
    
    def test_ship_update_moves_ship(self):
        """Test that update moves ship"""
        source = Planet(100, 100, 30)
        target = Planet(300, 100, 30)
        
        ship = Ship(source, target, "Player")
        initial_x = ship.x
        
        ship.update(1.0)
        
        assert ship.x != initial_x
        assert ship.x > initial_x  # Moving towards target (right)
    
    def test_ship_arrives_at_target(self):
        """Test that ship arrives at target after sufficient time"""
        source = Planet(100, 100, 30)
        target = Planet(300, 100, 30)
        
        ship = Ship(source, target, "Player")
        
        # Update in small increments to allow proper arrival detection
        # Distance = 200, speed = 200, takes ~1 second
        for _ in range(100):  # 100 updates of 0.1s each = 10 seconds
            if not ship.has_arrived():
                ship.update(0.1)
        
        assert ship.has_arrived() is True
    
    def test_ship_no_movement_after_arrival(self):
        """Test that ship doesn't move after arriving"""
        source = Planet(100, 100, 30)
        target = Planet(200, 100, 30)
        
        ship = Ship(source, target, "Player")
        
        # Arrive at target using small updates
        for _ in range(50):
            if not ship.has_arrived():
                ship.update(0.1)
        assert ship.has_arrived() is True
        
        # Store position
        x_after_arrival = ship.x
        y_after_arrival = ship.y
        
        # Update again
        ship.update(1.0)
        
        # Position shouldn't change
        assert ship.x == x_after_arrival
        assert ship.y == y_after_arrival
    
    def test_ship_multiple_updates(self):
        """Test ship movement over multiple updates"""
        source = Planet(0, 0, 30)
        target = Planet(200, 0, 30)
        
        ship = Ship(source, target, "Player")
        
        # Simulate frame-by-frame updates (60 FPS)
        dt = 1.0 / 60.0
        for _ in range(60):  # 1 second of updates
            if not ship.has_arrived():
                ship.update(dt)
        
        # Should be close to or at target after 1 second
        assert ship.x > 150  # Moved significantly


class TestShipGetColor:
    """Tests for Ship color assignment"""
    
    def test_get_color_player(self):
        """Test player ship color"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        ship = Ship(source, target, "Player")
        
        color = ship.get_color()
        assert color == (100, 150, 255)  # Blue
    
    def test_get_color_enemy(self):
        """Test enemy ship color"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        ship = Ship(source, target, "Enemy")
        
        color = ship.get_color()
        assert color == (255, 100, 100)  # Red


class TestEntityEdgeCases:
    """Tests for edge cases"""
    
    def test_planet_zero_radius(self):
        """Test planet with zero radius"""
        planet = Planet(100, 100, 0)
        # Should still work, just with minimal size
        assert planet.radius == 0
    
    def test_ship_same_source_and_target(self):
        """Test ship where source and target are same location"""
        source = Planet(100, 100, 30)
        target = Planet(100, 100, 30)
        
        ship = Ship(source, target, "Player")
        
        # Velocity should be zero
        assert ship.velocity_x == 0
        assert ship.velocity_y == 0
    
    def test_ship_zero_fleet_size(self):
        """Test ship with zero fleet size"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player", fleet_size=0)
        assert ship.fleet_size == 0
    
    def test_negative_coordinates(self):
        """Test entities with negative coordinates"""
        planet = Planet(-100, -200, 30)
        assert planet.x == -100
        assert planet.y == -200
    
    def test_very_large_fleet(self):
        """Test ship with very large fleet size"""
        source = Planet(100, 100, 30)
        target = Planet(300, 300, 30)
        
        ship = Ship(source, target, "Player", fleet_size=999999)
        assert ship.fleet_size == 999999

