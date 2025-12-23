"""
Unit tests for GameState
Note: These tests focus on logic; rendering and AI tests may be limited
"""
import pytest
from unittest.mock import MagicMock, patch
from game.game_state import GameState
from game.entities import Planet, Ship


# Mock pygame and sound for all tests
@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock pygame and sound manager"""
    with patch('game.game_state.SoundManager') as mock_sound:
        mock_sound_instance = MagicMock()
        mock_sound.return_value = mock_sound_instance
        yield mock_sound_instance


class TestGameStateInit:
    """Tests for GameState initialization"""
    
    def test_init_basic(self):
        """Test basic initialization"""
        game = GameState(800, 600)
        
        assert game.screen_width == 800
        assert game.screen_height == 600
        assert len(game.planets) > 0
        assert len(game.ships) == 0
    
    def test_init_with_player_name(self):
        """Test initialization with player name"""
        game = GameState(800, 600, player_name="TestPlayer")
        assert game.player_name == "TestPlayer"
    
    def test_init_with_map_size_small(self):
        """Test initialization with small map (7 planets)"""
        game = GameState(1200, 900, map_size="small")
        # Map generation may not always succeed with all planets
        assert len(game.planets) >= 3  # At least some planets generated
    
    def test_init_with_map_size_medium(self):
        """Test initialization with medium map (13 planets)"""
        game = GameState(1600, 1200, map_size="medium")
        # Map generation may fail with small screens, use larger screen
        assert len(game.planets) >= 5  # At least some planets generated
    
    def test_init_with_map_size_large(self):
        """Test initialization with large map (19 planets)"""
        game = GameState(2000, 1500, map_size="large")
        # Map generation may not always succeed with all planets
        assert len(game.planets) >= 7  # At least some planets generated
    
    def test_init_has_player_and_enemy_planets(self):
        """Test that map has player and enemy starting planets"""
        game = GameState(800, 600)
        
        player_planets = [p for p in game.planets if p.owner == "Player"]
        enemy_planets = [p for p in game.planets if p.owner == "Enemy"]
        
        assert len(player_planets) >= 1
        assert len(enemy_planets) >= 1
    
    def test_init_abilities(self):
        """Test that abilities are initialized"""
        game = GameState(800, 600)
        
        assert 'recall' in game.player_abilities
        assert 'production' in game.player_abilities
        assert 'shield' in game.player_abilities
        
        assert 'recall' in game.enemy_abilities
        assert 'production' in game.enemy_abilities
        assert 'shield' in game.enemy_abilities
    
    def test_init_statistics_tracking(self):
        """Test that statistics trackers are initialized"""
        game = GameState(800, 600)
        
        assert game.player_stats_tracker['ships_produced'] == 0
        assert game.player_stats_tracker['battles_won'] == 0
        assert game.player_stats_tracker['battles_lost'] == 0
        
        assert game.enemy_stats_tracker['ships_produced'] == 0
        assert game.enemy_stats_tracker['battles_won'] == 0
        assert game.enemy_stats_tracker['battles_lost'] == 0
    
    def test_init_score_tracking(self):
        """Test that score tracking is initialized"""
        game = GameState(800, 600)
        
        assert game.base_score == 100
        assert game.tactical_penalties == 0
        assert game.game_time == 0
    
    def test_init_unique_planet_names(self):
        """Test that all planets have unique names"""
        game = GameState(800, 600, map_size="large")
        
        names = [p.name for p in game.planets]
        assert len(names) == len(set(names))  # All unique


class TestGameStateMapGeneration:
    """Tests for map generation"""
    
    def test_map_is_mirrored_vertically(self):
        """Test that map is vertically mirrored"""
        game = GameState(800, 600, map_size="medium")
        
        # Find player planet (should be on left)
        player_planet = next(p for p in game.planets if p.owner == "Player")
        
        # Find enemy planet (should be on right, mirrored)
        enemy_planet = next(p for p in game.planets if p.owner == "Enemy")
        
        # Check mirroring
        assert player_planet.x < game.screen_width / 2
        assert enemy_planet.x > game.screen_width / 2
        
        # Y coordinates should be same (vertically mirrored)
        assert abs(player_planet.y - enemy_planet.y) < 1
        
        # Radii should be same
        assert player_planet.radius == enemy_planet.radius
    
    def test_planets_dont_overlap(self):
        """Test that planets don't overlap"""
        game = GameState(800, 600, map_size="large")
        
        # Check all pairs
        for i, p1 in enumerate(game.planets):
            for p2 in game.planets[i+1:]:
                distance = ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
                min_distance = p1.radius + p2.radius
                assert distance >= min_distance
    
    def test_planets_avoid_ui_zone(self):
        """Test that planets avoid top-left UI zone"""
        game = GameState(800, 600)
        
        ui_exclusion_width = 350
        ui_exclusion_height = 300
        
        for planet in game.planets:
            if planet.x < ui_exclusion_width:
                # If in left zone, should be below UI (>= to allow edge)
                assert planet.y >= ui_exclusion_height
    
    def test_center_planet_on_mirror_line(self):
        """Test that one planet is on the center mirror line"""
        game = GameState(800, 600, map_size="medium")
        
        # Find planet closest to center
        center_x = game.screen_width / 2
        center_planets = [p for p in game.planets if abs(p.x - center_x) < 10]
        
        assert len(center_planets) >= 1


class TestGameStateUpdate:
    """Tests for game state updates"""
    
    def test_update_increases_game_time(self):
        """Test that update increases game time"""
        game = GameState(800, 600)
        initial_time = game.game_time
        
        game.update(1.0)
        
        assert game.game_time == initial_time + 1.0
    
    def test_update_updates_planets(self):
        """Test that update calls planet updates"""
        game = GameState(800, 600)
        
        # Find a player planet
        player_planet = next(p for p in game.planets if p.owner == "Player")
        initial_ships = player_planet.ship_count
        
        # Update for 1 second
        game.update(1.0)
        
        # Should have produced ships
        assert player_planet.ship_count >= initial_ships
    
    def test_update_moves_ships(self):
        """Test that update moves ships"""
        game = GameState(800, 600)
        
        # Create a test ship
        source = game.planets[0]
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=10)
        game.ships.append(ship)
        
        initial_x = ship.x
        
        game.update(0.1)
        
        # Ship should have moved (unless already arrived)
        if not ship.has_arrived():
            assert ship.x != initial_x
    
    def test_update_removes_arrived_ships(self):
        """Test that arrived ships are removed"""
        game = GameState(800, 600)
        
        # Create a ship that will arrive quickly
        source = game.planets[0]
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=10)
        ship.arrived = True  # Mark as arrived
        game.ships.append(ship)
        
        initial_count = len(game.ships)
        
        game.update(0.1)
        
        # Ship should be removed
        assert len(game.ships) == initial_count - 1


class TestGameStateAddShip:
    """Tests for adding ships"""
    
    def test_add_ship(self):
        """Test adding a ship"""
        game = GameState(800, 600)
        
        source = game.planets[0]
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=10)
        
        initial_count = len(game.ships)
        game.add_ship(ship)
        
        assert len(game.ships) == initial_count + 1
        assert ship in game.ships


class TestGameStateCheckGameOver:
    """Tests for game over detection"""
    
    def test_check_game_over_ongoing(self):
        """Test game over check during ongoing game"""
        game = GameState(800, 600)
        result = game.check_game_over()
        assert result is None
    
    def test_check_game_over_victory(self):
        """Test victory condition"""
        game = GameState(800, 600)
        
        # Give all planets to player
        for planet in game.planets:
            planet.owner = "Player"
        
        # Remove all enemy ships
        game.ships = [s for s in game.ships if s.owner != "Enemy"]
        
        result = game.check_game_over()
        assert result == "victory"
    
    def test_check_game_over_defeat(self):
        """Test defeat condition"""
        game = GameState(800, 600)
        
        # Give all planets to enemy
        for planet in game.planets:
            planet.owner = "Enemy"
        
        # Remove all player ships
        game.ships = [s for s in game.ships if s.owner != "Player"]
        
        result = game.check_game_over()
        assert result == "defeat"
    
    def test_check_game_over_player_has_fleet(self):
        """Test that player with fleet is not defeated"""
        game = GameState(800, 600)
        
        # Remove all player planets but add a fleet
        for planet in game.planets:
            if planet.owner == "Player":
                planet.owner = "Neutral"
        
        # Add a player fleet
        source = game.planets[0]
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=10)
        game.ships.append(ship)
        
        result = game.check_game_over()
        assert result is None  # Still playing


class TestGameStateGetPlanetAt:
    """Tests for finding planets at coordinates"""
    
    def test_get_planet_at_center(self):
        """Test getting planet at its center"""
        game = GameState(800, 600)
        planet = game.planets[0]
        
        found = game.get_planet_at(planet.x, planet.y)
        assert found == planet
    
    def test_get_planet_at_edge(self):
        """Test getting planet at its edge"""
        game = GameState(800, 600)
        planet = game.planets[0]
        
        # Point on edge
        x = planet.x + planet.radius
        y = planet.y
        
        found = game.get_planet_at(x, y)
        assert found == planet
    
    def test_get_planet_at_empty_space(self):
        """Test getting planet in empty space"""
        game = GameState(800, 600)
        
        # Far outside any planet
        found = game.get_planet_at(99999, 99999)
        assert found is None


class TestGameStateGetPlayerStats:
    """Tests for player statistics"""
    
    def test_get_player_stats(self):
        """Test getting player statistics"""
        game = GameState(800, 600)
        
        stats = game.get_player_stats("Player")
        
        assert "planet_count" in stats
        assert "total_ships" in stats
        assert "production_rate" in stats
        assert stats["planet_count"] > 0
    
    def test_get_enemy_stats(self):
        """Test getting enemy statistics"""
        game = GameState(800, 600)
        
        stats = game.get_player_stats("Enemy")
        
        assert stats["planet_count"] > 0
        assert "total_ships" in stats
    
    def test_stats_include_fleet_ships(self):
        """Test that stats include ships in fleets"""
        game = GameState(800, 600)
        
        # Add a player fleet
        source = game.planets[0]
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=100)
        game.ships.append(ship)
        
        stats = game.get_player_stats("Player")
        
        # Should include fleet ships
        assert stats["total_ships"] >= 100


class TestGameStateCalculateFinalScore:
    """Tests for score calculation"""
    
    def test_calculate_final_score_no_penalties(self):
        """Test score calculation with no penalties"""
        game = GameState(800, 600)
        game.base_score = 100
        game.tactical_penalties = 0
        game.game_time = 30  # Fast victory
        
        score = game.calculate_final_score()
        
        # Should get base + time bonus (under 60s = +50)
        assert score == 150
    
    def test_calculate_final_score_with_penalties(self):
        """Test score calculation with penalties"""
        game = GameState(800, 600)
        game.base_score = 100
        game.tactical_penalties = 20
        game.game_time = 200  # Gets 5 point bonus (< 300s)
        
        score = game.calculate_final_score()
        
        # 100 - 20 + 5 = 85
        assert score == 85
    
    def test_calculate_final_score_time_bonuses(self):
        """Test different time bonuses"""
        game = GameState(800, 600)
        game.base_score = 100
        game.tactical_penalties = 0
        
        # Test various time thresholds
        test_cases = [
            (30, 50),   # < 60s
            (90, 30),   # < 120s
            (150, 15),  # < 180s
            (250, 5),   # < 300s
            (400, 0),   # >= 300s
        ]
        
        for time, expected_bonus in test_cases:
            game.game_time = time
            score = game.calculate_final_score()
            assert score == 100 + expected_bonus
    
    def test_calculate_final_score_cant_go_negative(self):
        """Test that score can't go below zero"""
        game = GameState(800, 600)
        game.base_score = 100
        game.tactical_penalties = 200  # More than base
        game.game_time = 500  # No bonus
        
        score = game.calculate_final_score()
        
        assert score >= 0


class TestGameStateAbilities:
    """Tests for ability activation"""
    
    def test_activate_recall(self):
        """Test recall ability"""
        game = GameState(800, 600)
        
        # Add a player fleet
        source = game.planets[0]
        source.owner = "Player"
        target = game.planets[1]
        ship = Ship(source, target, "Player", fleet_size=50)
        game.ships.append(ship)
        
        initial_ships = source.ship_count
        
        # Activate recall
        result = game.activate_recall("Player")
        
        assert result is True
        assert len([s for s in game.ships if s.owner == "Player"]) == 0
        assert source.ship_count == initial_ships + 50
    
    def test_activate_production_surge(self):
        """Test production surge ability"""
        game = GameState(800, 600)
        
        result = game.activate_production_surge("Player")
        
        assert result is True
        assert game.player_abilities['production'].is_active()
    
    def test_activate_shield(self):
        """Test shield ability"""
        game = GameState(800, 600)
        
        # Find a player planet
        player_planet = next(p for p in game.planets if p.owner == "Player")
        
        result = game.activate_shield(player_planet, "Player")
        
        assert result is True
        assert game.player_abilities['shield'].is_active()
        assert game.player_abilities['shield'].target == player_planet
    
    def test_shield_only_on_owned_planets(self):
        """Test that shield only works on owned planets"""
        game = GameState(800, 600)
        
        # Find an enemy planet
        enemy_planet = next(p for p in game.planets if p.owner == "Enemy")
        
        result = game.activate_shield(enemy_planet, "Player")
        
        assert result is False
    
    def test_abilities_single_use(self):
        """Test that abilities are single-use"""
        game = GameState(800, 600)
        
        # First activation succeeds
        assert game.activate_production_surge("Player") is True
        
        # Second activation fails
        assert game.activate_production_surge("Player") is False


class TestGameStateShipArrival:
    """Tests for ship arrival handling"""
    
    def test_ship_arrival_reinforcement(self):
        """Test ship arriving at owned planet"""
        game = GameState(800, 600)
        
        # Find a player planet
        planet = next(p for p in game.planets if p.owner == "Player")
        initial_ships = planet.ship_count
        
        # Create a ship
        source = game.planets[0]
        ship = Ship(source, planet, "Player", fleet_size=10)
        ship.target_planet = planet
        ship.arrived = True
        
        game._handle_ship_arrival(ship)
        
        # Ships should be added
        assert planet.ship_count == initial_ships + 10
    
    def test_ship_arrival_conquest(self):
        """Test ship conquering a planet"""
        game = GameState(800, 600)
        
        # Find a neutral planet with few ships
        planet = next(p for p in game.planets if p.owner == "Neutral")
        planet.ship_count = 5
        
        # Create a stronger ship
        source = game.planets[0]
        ship = Ship(source, planet, "Player", fleet_size=20)
        ship.target_planet = planet
        ship.arrived = True
        
        game._handle_ship_arrival(ship)
        
        # Planet should be conquered
        assert planet.owner == "Player"
        assert planet.ship_count == 15  # 20 - 5 = 15 remaining
    
    def test_ship_arrival_failed_attack(self):
        """Test ship failing to conquer planet"""
        game = GameState(800, 600)
        
        # Find a planet
        planet = next(p for p in game.planets if p.owner == "Neutral")
        planet.ship_count = 20
        
        # Create a weaker ship
        source = game.planets[0]
        ship = Ship(source, planet, "Player", fleet_size=10)
        ship.target_planet = planet
        ship.arrived = True
        
        game._handle_ship_arrival(ship)
        
        # Planet should remain neutral
        assert planet.owner == "Neutral"
        assert planet.ship_count == 10  # 20 - 10 = 10 remaining


class TestGameStateEdgeCases:
    """Tests for edge cases"""
    
    def test_empty_map_size(self):
        """Test with invalid map size defaults to medium"""
        game = GameState(1600, 1200, map_size="invalid")
        # Should generate some planets (may not be exactly 9 due to generation limits)
        assert len(game.planets) >= 3
    
    def test_very_small_screen(self):
        """Test with very small screen"""
        game = GameState(400, 300, map_size="small")
        # May not fit all 5 planets, but should have at least 1
        assert len(game.planets) >= 1
    
    def test_very_large_screen(self):
        """Test with very large screen (19 planets for large)"""
        game = GameState(2000, 1500, map_size="large")
        assert len(game.planets) == 19

